"""Sensor platform for Amazon Israel Shipping Watcher."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import Throttle

from .const import (
    DOMAIN,
    CONF_URLS,
    CONF_PRODUCTS,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    ATTR_PRODUCT_TITLE,
    ATTR_PRICE,
    ATTR_SHIPPING_STATUS,
    ATTR_URL,
    ATTR_LAST_UPDATED,
    STATE_FREE_SHIPPING,
    STATE_NO_FREE_SHIPPING,
    STATE_UNKNOWN,
)
from .amazon_parser import AmazonParser

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Amazon Watcher sensors from a config entry."""
    # Try to get products from new format, fall back to old format for backward compatibility
    if CONF_PRODUCTS in config_entry.data:
        products = config_entry.data[CONF_PRODUCTS]
    else:
        # Backward compatibility: parse old format
        urls = config_entry.data[CONF_URLS].strip().split("\n")
        urls = [url.strip() for url in urls if url.strip()]
        products = [{"url": url} for url in urls]
    
    scan_interval = config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    session = async_get_clientsession(hass)
    parser = AmazonParser(session)

    sensors = []
    for idx, product in enumerate(products, start=1):
        url = product["url"]
        # Use custom name if provided, otherwise use default
        custom_name = product.get("name")
        if custom_name:
            name = custom_name
        else:
            name = f"Amazon Product {idx}"
        
        sensors.append(
            AmazonShippingSensor(
                parser=parser,
                url=url,
                name=name,
                unique_id=f"{config_entry.entry_id}_{idx}",
                scan_interval=scan_interval,
            )
        )

    async_add_entities(sensors, True)


class AmazonShippingSensor(SensorEntity):
    """Representation of an Amazon Shipping Sensor."""

    _attr_icon = "mdi:package-variant-closed"
    
    # Explicitly disable numeric features to prevent type errors
    _attr_device_class = None
    _attr_state_class = None
    _attr_native_unit_of_measurement = None

    def __init__(
        self,
        parser: AmazonParser,
        url: str,
        name: str,
        unique_id: str,
        scan_interval: int,
    ) -> None:
        """Initialize the sensor."""
        self._parser = parser
        self._url = url
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._scan_interval = timedelta(minutes=scan_interval)
        
        self._attr_native_value = STATE_UNKNOWN
        self._product_title = None
        self._price = None
        self._shipping_status = None
        self._last_updated = None

        # Create throttled update method
        self._throttled_update = Throttle(self._scan_interval)(self._async_update_data)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            ATTR_PRODUCT_TITLE: self._product_title,
            ATTR_PRICE: self._price,
            ATTR_SHIPPING_STATUS: self._shipping_status,
            ATTR_URL: self._url,
            ATTR_LAST_UPDATED: self._last_updated,
        }

    async def async_update(self) -> None:
        """Update the sensor."""
        await self._throttled_update()

    async def _async_update_data(self) -> None:
        """Fetch new state data for the sensor."""
        _LOGGER.debug("Updating Amazon shipping sensor for %s", self._url)

        try:
            product_info = await self._parser.fetch_product_info(self._url)

            self._product_title = product_info.get("product_title")
            self._price = product_info.get("price")
            self._shipping_status = product_info.get("shipping_status")
            
            has_free_shipping = product_info.get("has_free_shipping")
            
            if has_free_shipping is None:
                self._attr_native_value = STATE_UNKNOWN
            elif has_free_shipping:
                self._attr_native_value = STATE_FREE_SHIPPING
                self._attr_icon = "mdi:truck-delivery"
            else:
                self._attr_native_value = STATE_NO_FREE_SHIPPING
                self._attr_icon = "mdi:truck-remove"

            from datetime import datetime
            self._last_updated = datetime.now().isoformat()

            _LOGGER.debug(
                "Updated %s: %s - Free shipping: %s",
                self._attr_name,
                self._product_title,
                self._attr_native_value,
            )

        except Exception as err:
            _LOGGER.error("Error updating sensor %s: %s", self._attr_name, err)
            self._attr_native_value = STATE_UNKNOWN
            self._attr_icon = "mdi:alert-circle"
