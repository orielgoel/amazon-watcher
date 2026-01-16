"""Constants for the Amazon Israel Shipping Watcher integration."""

DOMAIN = "amazon_watcher"
CONF_URLS = "urls"
CONF_PRODUCTS = "products"  # List of dicts with 'url' and optional 'name'
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 60  # minutes

# Sensor attributes
ATTR_PRODUCT_TITLE = "product_title"
ATTR_PRICE = "price"
ATTR_SHIPPING_STATUS = "shipping_status"
ATTR_URL = "url"
ATTR_LAST_UPDATED = "last_updated"

# States
STATE_FREE_SHIPPING = "Yes"
STATE_NO_FREE_SHIPPING = "No"
STATE_UNKNOWN = "Unknown"

# User agent for requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
