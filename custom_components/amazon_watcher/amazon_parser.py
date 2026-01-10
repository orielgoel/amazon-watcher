"""Amazon product parser for shipping information."""
from __future__ import annotations

import logging
import re
from typing import Any

import aiohttp
from bs4 import BeautifulSoup

from .const import USER_AGENT

_LOGGER = logging.getLogger(__name__)


class AmazonParser:
    """Parser for Amazon product pages."""

    def __init__(self, session: aiohttp.ClientSession):
        """Initialize the parser."""
        self.session = session

    async def fetch_product_info(self, url: str) -> dict[str, Any]:
        """Fetch product information from Amazon URL."""
        try:
            headers = {
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }

            async with self.session.get(url, headers=headers, timeout=30) as response:
                if response.status != 200:
                    _LOGGER.error(
                        "Failed to fetch URL %s: HTTP %s", url, response.status
                    )
                    return self._create_error_response(url)

                html = await response.text()
                return self._parse_html(html, url)

        except aiohttp.ClientError as err:
            _LOGGER.error("Network error fetching %s: %s", url, err)
            return self._create_error_response(url)
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching %s: %s", url, err)
            return self._create_error_response(url)

    def _parse_html(self, html: str, url: str) -> dict[str, Any]:
        """Parse HTML content to extract product information."""
        soup = BeautifulSoup(html, "html.parser")

        product_title = self._extract_title(soup)
        price = self._extract_price(soup)
        shipping_info = self._extract_shipping_info(soup)

        # Determine if free shipping to Israel is available
        has_free_shipping = self._check_israel_free_shipping(shipping_info, html)

        return {
            "product_title": product_title,
            "price": price,
            "shipping_status": shipping_info,
            "has_free_shipping": has_free_shipping,
            "url": url,
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract product title from page."""
        # Try multiple possible title selectors
        selectors = [
            "#productTitle",
            "#title",
            "span#productTitle",
            "h1.product-title",
            "h1#title",
        ]

        for selector in selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text(strip=True)

        return "Unknown Product"

    def _extract_price(self, soup: BeautifulSoup) -> str:
        """Extract product price from page."""
        # Try multiple possible price selectors
        selectors = [
            ".a-price .a-offscreen",
            "#priceblock_ourprice",
            "#priceblock_dealprice",
            ".a-price-whole",
            "span.a-price",
        ]

        for selector in selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                return price_elem.get_text(strip=True)

        return "N/A"

    def _extract_shipping_info(self, soup: BeautifulSoup) -> str:
        """Extract shipping information from page."""
        # Look for shipping information in various locations
        shipping_selectors = [
            "#mir-layout-DELIVERY_BLOCK",
            "#delivery-message",
            "#deliveryMessageMirId",
            ".delivery-message",
            "[data-feature-name='deliveryMessage']",
            "#shipping-message",
        ]

        for selector in shipping_selectors:
            shipping_elem = soup.select_one(selector)
            if shipping_elem:
                text = shipping_elem.get_text(strip=True)
                if text:
                    return text

        return "No shipping information found"

    def _check_israel_free_shipping(self, shipping_info: str, html: str) -> bool:
        """Check if product has free shipping to Israel."""
        # Convert to lowercase for case-insensitive matching
        shipping_lower = shipping_info.lower()
        
        # If shipping info says "No shipping information found", return False (or Unknown)
        if "no shipping information found" in shipping_lower:
            return False

        # Keywords indicating free shipping
        free_keywords = [
            "free shipping",
            "free delivery",
            "free international shipping",
            "ships free",
            "qualified for free shipping",
        ]

        # Check if any free shipping keyword is present IN THE SHIPPING INFO ONLY
        # We do NOT check the full HTML anymore to avoid false positives from footers/ads
        has_free = any(keyword in shipping_lower for keyword in free_keywords)

        if not has_free:
            return False

        # Now check if it mentions Israel or international shipping
        # OR if we are confident because the shipping info block itself was extracted correctly
        israel_keywords = ["israel", "international"]

        # Check if shipping info mentions Israel/international
        israel_mentioned = any(
            keyword in shipping_lower for keyword in israel_keywords
        )
        
        # Also check if "Deliver to Israel" is in the page header to confirm context,
        # but only if we found "Free Shipping" in the specific delivery block.
        # This helps confirm we are viewing the page as an Israeli user.
        location_confirmed = "israel" in html.lower()

        if israel_mentioned:
            return True
            
        # If we found "Free Shipping" in the delivery block, and the page mentions Israel anywhere
        # (likely in the "Deliver to" location), it's highly likely to be free shipping to Israel.
        if has_free and location_confirmed:
            return True

        return False

    def _create_error_response(self, url: str) -> dict[str, Any]:
        """Create an error response."""
        return {
            "product_title": "Error fetching product",
            "price": "N/A",
            "shipping_status": "Unable to fetch shipping information",
            "has_free_shipping": None,
            "url": url,
        }
