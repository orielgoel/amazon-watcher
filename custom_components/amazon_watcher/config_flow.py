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
    CONF_PRODUCT_URL,
    CONF_PRODUCT_NAME,
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


def validate_product_url(url: str) -> None:
    """Validate a single product URL."""
    if not url or not url.strip():
        raise InvalidURLs("URL cannot be empty")
    if not validate_amazon_url(url.strip()):
        raise InvalidURLs(f"Invalid Amazon URL: {url}")


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Amazon Israel Shipping Watcher."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.products: list[dict[str, Any]] = []
        self.scan_interval: int = DEFAULT_SCAN_INTERVAL

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step - scan interval."""
        if user_input is not None:
            self.scan_interval = user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            return await self.async_step_product()

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): int,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
        )

    async def async_step_product(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle adding a product."""
        errors: dict[str, str] = {}

        if user_input is not None:
            url = user_input.get(CONF_PRODUCT_URL, "").strip()
            custom_name = user_input.get(CONF_PRODUCT_NAME, "").strip() or None
            add_another = user_input.get("add_another", False)

            # If URL is provided, validate and add it
            if url:
                try:
                    validate_product_url(url)
                except InvalidURLs as err:
                    errors["base"] = "invalid_url"
                    _LOGGER.error("Invalid URL: %s", err)
                else:
                    # Add product to list
                    product = {"url": url}
                    if custom_name:
                        product["name"] = custom_name
                    self.products.append(product)

            # If no errors and user wants to add another, show form again
            if not errors and add_another:
                return await self.async_step_product()
            
            # If no errors and user doesn't want to add another, finish
            if not errors:
                if not self.products:
                    errors["base"] = "no_products"
                else:
                    return await self._async_create_entry()
            
            # If user doesn't want to add another and we have products, allow finishing
            if not add_another and self.products and errors:
                # User wants to finish but current input has error
                # Allow them to finish with existing products
                return await self._async_create_entry()

        # Show form
        data_schema = vol.Schema(
            {
                vol.Required(CONF_PRODUCT_URL): str,
                vol.Optional(CONF_PRODUCT_NAME): str,
                vol.Optional("add_another", default=False): bool,
            }
        )

        return self.async_show_form(
            step_id="product",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "product_count": str(len(self.products)),
            },
        )

    async def _async_create_entry(self) -> FlowResult:
        """Create the config entry."""
        # Create unique ID based on URLs
        urls = [product["url"] for product in self.products]
        await self.async_set_unique_id("_".join(sorted(urls))[:100])
        self._abort_if_unique_id_configured()

        # Build URLs string for backward compatibility
        urls_string = "\n".join([p["url"] for p in self.products])

        # Store products in the config entry data
        entry_data = {
            CONF_PRODUCTS: self.products,
            CONF_SCAN_INTERVAL: self.scan_interval,
            # Keep CONF_URLS for backward compatibility
            CONF_URLS: urls_string,
        }

        title = f"Amazon Watcher ({len(self.products)} product{'s' if len(self.products) != 1 else ''})"
        return self.async_create_entry(title=title, data=entry_data)


class InvalidURLs(HomeAssistantError):
    """Error to indicate invalid URLs."""
