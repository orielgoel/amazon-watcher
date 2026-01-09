# Amazon Israel Shipping Watcher

Monitor Amazon products for free shipping to Israel directly from Home Assistant!

## Features

✅ **Multi-Product Monitoring**: Track unlimited Amazon product URLs  
✅ **Automatic Updates**: Configurable scan intervals (5 minutes to 24 hours)  
✅ **Smart Detection**: Intelligently detects free shipping offers to Israel  
✅ **Rich Attributes**: Access product title, price, and shipping details  
✅ **Automation Ready**: Use sensor states in automations and scripts  
✅ **HACS Compatible**: Easy installation and updates through HACS

## Quick Start

1. **Install via HACS** or manually copy to `custom_components/amazon_watcher`
2. **Restart Home Assistant**
3. **Add Integration**: Settings → Devices & Services → Add Integration → Search "Amazon"
4. **Configure**: Paste your Amazon product URLs (one per line)
5. **Done!** Sensors will appear immediately

## Example URLs

```
https://www.amazon.com/dp/B08N5WRWNW
https://www.amazon.com/dp/B07XJ8C8F5
https://www.amazon.co.uk/dp/B09G9FPHY6
```

## Sensor States

- **Yes**: Free shipping to Israel is available ✅
- **No**: No free shipping to Israel ❌
- **Unknown**: Unable to determine shipping status ❓

## Automation Example

Get notified when free shipping becomes available:

```yaml
automation:
  - alias: "Amazon Free Shipping Alert"
    trigger:
      - platform: state
        entity_id: sensor.amazon_product_1
        to: "Yes"
    action:
      - service: notify.mobile_app
        data:
          title: "🎉 Free Shipping Available!"
          message: >
            {{ state_attr('sensor.amazon_product_1', 'product_title') }} 
            now ships free to Israel!
            Price: {{ state_attr('sensor.amazon_product_1', 'price') }}
          data:
            url: "{{ state_attr('sensor.amazon_product_1', 'url') }}"
```

## Dashboard Card

```yaml
type: entities
title: Amazon Products
entities:
  - entity: sensor.amazon_product_1
    secondary_info: last-updated
  - entity: sensor.amazon_product_2
    secondary_info: last-updated
```

## How It Works

The integration periodically visits each Amazon product page and analyzes:
- Product availability
- Current pricing
- Shipping options to Israel
- Free shipping eligibility

It looks for keywords like "free shipping", "free delivery", and checks if they apply to Israel or international shipping.

## Privacy & Performance

- **No Data Collection**: All processing happens locally in Home Assistant
- **Rate Limited**: Respects Amazon's servers with configurable intervals
- **Lightweight**: Minimal resource usage
- **No API Keys**: Works without any Amazon API credentials

## Troubleshooting

### Sensor shows "Unknown"
- Amazon's page structure may have changed
- Network connectivity issues
- Amazon may be blocking automated requests (try increasing scan interval)

### Sensor not updating
- Check Home Assistant logs for errors
- Verify URLs are valid Amazon product pages
- Ensure network access to Amazon domains

## Support

For issues and feature requests, please visit the GitHub repository.

## Legal Notice

This integration is for personal use only. It respects Amazon's robots.txt and implements reasonable rate limiting. Users are responsible for complying with Amazon's Terms of Service.
