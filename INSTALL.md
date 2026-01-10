# Installation Guide

## Method 1: HACS Installation (Recommended)

### Prerequisites
- Home Assistant installed and running
- HACS (Home Assistant Community Store) installed

### Steps

1. **Add Custom Repository to HACS**
   - Open Home Assistant
   - Go to HACS → Integrations
   - Click the three dots (⋮) in the top right
   - Select "Custom repositories"
   - Add this repository URL: `https://github.com/orielgoel/amazon-watcher`
   - Category: Integration
   - Click "Add"

2. **Install the Integration**
   - Find "Amazon Israel Shipping Watcher" in HACS
   - Click "Download"
   - Restart Home Assistant

3. **Configure the Integration**
   - Go to Settings → Devices & Services
   - Click "+ ADD INTEGRATION"
   - Search for "Amazon Israel Shipping Watcher"
   - Click on it to start configuration

4. **Add Your Amazon URLs**
   - Enter your Amazon product URLs, one per line
   - Example:
     ```
     https://www.amazon.com/dp/B08N5WRWNW
     https://www.amazon.com/dp/B07XJ8C8F5
     ```
   - Set scan interval (default: 60 minutes)
   - Click "Submit"

5. **Verify Installation**
   - Go to Settings → Devices & Services
   - You should see "Amazon Israel Shipping Watcher"
   - Click on it to view your sensors

## Method 2: Manual Installation

### Prerequisites
- Access to your Home Assistant configuration directory
- SSH or file access to Home Assistant

### Steps

1. **Download the Integration**
   ```bash
   cd /config  # or your Home Assistant config directory
   mkdir -p custom_components
   cd custom_components
   git clone https://github.com/orielgoel/amazon-watcher.git
   mv amazon-watcher/custom_components/amazon_watcher .
   rm -rf amazon-watcher
   ```

   Or manually:
   - Download the repository as ZIP
   - Extract it
   - Copy the `custom_components/amazon_watcher` folder to your Home Assistant's `custom_components` directory

2. **Verify Directory Structure**
   ```
   /config/
   └── custom_components/
       └── amazon_watcher/
           ├── __init__.py
           ├── manifest.json
           ├── config_flow.py
           ├── sensor.py
           ├── const.py
           ├── amazon_parser.py
           ├── strings.json
           └── translations/
               └── en.json
   ```

3. **Restart Home Assistant**
   - Go to Settings → System → Restart
   - Wait for Home Assistant to restart

4. **Add Integration**
   - Follow steps 3-5 from HACS installation above

## Verification

After installation, verify everything is working:

1. **Check Logs**
   - Go to Settings → System → Logs
   - Look for any errors related to `amazon_watcher`
   - You should see messages like: "Setting up amazon_watcher"

2. **Check Sensors**
   - Go to Developer Tools → States
   - Filter for `sensor.amazon_product_`
   - You should see sensors for each URL you added

3. **Check Sensor Attributes**
   - Click on a sensor
   - Verify attributes are populated:
     - product_title
     - price
     - shipping_status
     - url
     - last_updated

## Troubleshooting

### Integration Not Showing Up

- **Clear browser cache** and refresh Home Assistant
- **Check logs** for any Python errors
- **Verify directory structure** matches exactly
- **Restart Home Assistant** again

### Sensors Show "Unknown"

- **Wait a few minutes** for first update (respects scan interval)
- **Check internet connectivity** from Home Assistant
- **Verify URLs** are valid Amazon product pages
- **Check logs** for specific errors

### Sensors Not Updating

- **Check scan interval** - default is 60 minutes
- **Force update**: Developer Tools → Services → `homeassistant.update_entity`
  - Entity: `sensor.amazon_product_1` (or your sensor)
- **Check rate limiting** - Amazon may be blocking requests if interval is too short

### Configuration Flow Errors

- **"Invalid URLs"**: Make sure URLs are from Amazon domains (.com, .co.uk, etc.)
- **"Already configured"**: This set of URLs is already set up
  - Remove the old integration first or use different URLs

## Updating

### Via HACS
1. Go to HACS → Integrations
2. Find "Amazon Israel Shipping Watcher"
3. Click "Update" if available
4. Restart Home Assistant

### Manual Update
1. Delete the old `custom_components/amazon_watcher` folder
2. Follow manual installation steps again
3. Restart Home Assistant
4. Reconfigure if needed (usually not required)

## Uninstallation

1. **Remove Integration**
   - Go to Settings → Devices & Services
   - Find "Amazon Israel Shipping Watcher"
   - Click the three dots (⋮)
   - Click "Delete"

2. **Remove Files** (optional)
   - Delete `custom_components/amazon_watcher` folder
   - Restart Home Assistant

3. **Remove from HACS** (if installed via HACS)
   - Go to HACS → Integrations
   - Find "Amazon Israel Shipping Watcher"
   - Click the three dots (⋮)
   - Click "Remove"

## Support

For issues during installation:
- Check the [README.md](README.md) for more information
- Review [Troubleshooting](#troubleshooting) section above
- Open an issue on GitHub with:
  - Your Home Assistant version
  - Installation method used
  - Relevant log entries
  - Steps you've already tried

## Next Steps

After successful installation:
- Read [info.md](info.md) for usage examples
- Check [examples/configuration.yaml](examples/configuration.yaml) for automation ideas
- Set up notifications for shipping changes
- Create dashboard cards to display product information
