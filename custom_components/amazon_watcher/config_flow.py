"""Config flow for Amazon Israel Shipping Watcher integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_URLS,
    CONF_PRODUCTS,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


def validate_amazon_url(url: str) -> bool:
    """Validate if the URL is an Amazon URL."""
    amazon_domains = [
        "amazon.com",
        "amazon.co.uk",
        "amazon.de",
        "amazon.fr",
        "amazon.it",
        "amazon.es",
        "amazon.ca",
        "amazon.co.jp",
    ]
    return any(domain in url.lower() for domain in amazon_domains)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    urls_input = data[CONF_URLS].strip().split("\n")
    urls_input = [line.strip() for line in urls_input if line.strip()]

    if not urls_input:
        raise InvalidURLs("No URLs provided")

    products = []
    invalid_urls = []
    
    for line in urls_input:
        # Support format: "URL|Custom Name" or just "URL"
        if "|" in line:
            parts = line.split("|", 1)
            url = parts[0].strip()
            custom_name = parts[1].strip() if len(parts) > 1 else None
        else:
            url = line.strip()
            custom_name = None
        
        if not validate_amazon_url(url):
            invalid_urls.append(url)
        else:
            product = {"url": url}
            if custom_name:
                product["name"] = custom_name
            products.append(product)

    if invalid_urls:
        raise InvalidURLs(f"Invalid Amazon URLs: {', '.join(invalid_urls)}")

    return {
        "title": f"Amazon Watcher ({len(products)} products)",
        "products": products
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Amazon Israel Shipping Watcher."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except InvalidURLs as err:
                _LOGGER.error("Invalid URLs: %s", err)
                errors["base"] = "invalid_urls"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Create unique ID based on URLs
                urls = [product["url"] for product in info["products"]]
                await self.async_set_unique_id("_".join(sorted(urls))[:100])
                self._abort_if_unique_id_configured()

                # Store products in the config entry data
                entry_data = {
                    CONF_PRODUCTS: info["products"],
                    CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    # Keep CONF_URLS for backward compatibility
                    CONF_URLS: user_input[CONF_URLS],
                }

                return self.async_create_entry(title=info["title"], data=entry_data)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_URLS): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): int,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "urls_example": "https://www.amazon.com/dp/B08N5WRWNW\nhttps://www.amazon.com/dp/B07XJ8C8F5|My Custom Product Name"
            },
        )


class InvalidURLs(HomeAssistantError):
    """Error to indicate invalid URLs."""
