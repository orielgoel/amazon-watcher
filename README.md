# Amazon Israel Shipping Watcher

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A Home Assistant custom integration that monitors Amazon product URLs and checks if they offer free shipping to Israel.

## Features

- Monitor multiple Amazon product URLs
- Automatic checking for free shipping to Israel
- Configurable update intervals
- Individual sensors for each product
- Attributes showing product details and shipping status

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/amazon_watcher` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Configuration** -> **Integrations**
2. Click the **+ ADD INTEGRATION** button
3. Search for "Amazon Israel Shipping Watcher"
4. Enter your Amazon product URLs (one per line)
5. Configure the scan interval (default: 1 hour)

## Usage

Once configured, the integration will create sensors for each Amazon URL you provided. Each sensor will show:

- **State**: Whether free shipping to Israel is available (`Yes`, `No`, or `Unknown`)
- **Attributes**:
  - Product Title
  - Current Price
  - Shipping Status
  - Last Updated
  - Product URL

## Example Automation

```yaml
automation:
  - alias: "Notify when free shipping available"
    trigger:
      - platform: state
        entity_id: sensor.amazon_product_1
        to: "Yes"
    action:
      - service: notify.mobile_app
        data:
          title: "Free Shipping Available!"
          message: "{{ state_attr('sensor.amazon_product_1', 'product_title') }} now has free shipping to Israel!"
```

## Notes

- The integration respects Amazon's robots.txt and implements reasonable rate limiting
- Updates are throttled to avoid overwhelming Amazon's servers
- Shipping information accuracy depends on Amazon's website structure
- Some Amazon domains may require different parsing logic

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/orielgoel/amazon-watcher).

## License

MIT License - See LICENSE file for details
