# Amazon Israel Shipping Watcher - Project Overview

## 🎯 Project Purpose

A Home Assistant Custom Integration (HACS compatible) that monitors Amazon product URLs and automatically checks if products offer free shipping to Israel.

## 📁 Project Structure

```
amazon-watcher/
├── custom_components/          # Main integration code
│   └── amazon_watcher/
│       ├── __init__.py         # Integration setup and lifecycle
│       ├── manifest.json       # Integration metadata
│       ├── const.py           # Constants and configuration
│       ├── config_flow.py     # UI configuration flow
│       ├── sensor.py          # Sensor platform implementation
│       ├── amazon_parser.py   # Amazon page parsing logic
│       ├── strings.json       # UI strings
│       └── translations/
│           └── en.json        # English translations
│
├── examples/
│   └── configuration.yaml     # Example automations & configs
│
├── .github/
│   └── workflows/
│       └── validate.yml       # GitHub Actions for validation
│
├── hacs.json                  # HACS integration manifest
├── README.md                  # Main documentation
├── INSTALL.md                 # Installation guide
├── info.md                    # Detailed feature documentation
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
├── requirements.txt           # Python dependencies
└── .gitignore                # Git ignore rules
```

## 🔧 Technical Components

### Core Files

1. **`__init__.py`**
   - Integration entry point
   - Sets up sensor platform
   - Handles lifecycle (setup, unload, reload)

2. **`manifest.json`**
   - Integration metadata
   - Dependencies: beautifulsoup4, aiohttp
   - Version: 1.0.0

3. **`const.py`**
   - Domain: `amazon_watcher`
   - Configuration keys
   - Sensor states and attributes
   - Default values

4. **`config_flow.py`**
   - Configuration UI flow
   - URL validation
   - Scan interval configuration
   - Error handling

5. **`sensor.py`**
   - Sensor entity implementation
   - Update throttling
   - State management
   - Attribute handling

6. **`amazon_parser.py`**
   - HTML parsing with BeautifulSoup
   - Product information extraction
   - Shipping status detection
   - Israel-specific free shipping logic

## 🎨 Features

### User Features
- ✅ Monitor multiple Amazon product URLs
- ✅ Automatic free shipping detection for Israel
- ✅ Configurable scan intervals (5-1440 minutes)
- ✅ Rich sensor attributes (title, price, shipping status)
- ✅ Visual state indicators (icons change based on status)
- ✅ Easy UI-based configuration
- ✅ HACS compatible

### Technical Features
- ✅ Async/await for non-blocking operations
- ✅ Rate limiting and throttling
- ✅ Robust error handling
- ✅ Multiple selector fallbacks for parsing
- ✅ Support for multiple Amazon domains
- ✅ Automatic state updates
- ✅ Integration lifecycle management
- ✅ Proper Home Assistant conventions

## 🔄 Data Flow

```
User Configuration (UI)
    ↓
Config Flow Validation
    ↓
Sensor Creation
    ↓
Periodic Updates (Throttled)
    ↓
Amazon Parser
    ↓
HTTP Request → HTML Response
    ↓
BeautifulSoup Parsing
    ↓
Extract: Title, Price, Shipping
    ↓
Detect Israel Free Shipping
    ↓
Update Sensor State & Attributes
    ↓
Home Assistant State Machine
    ↓
Dashboard / Automations
```

## 📊 Sensor Information

### Sensor Entity
- **Entity ID**: `sensor.amazon_product_[1-N]`
- **Device Class**: None (custom sensor)
- **Icon**: Dynamic based on state
  - `mdi:package-variant-closed` (default)
  - `mdi:truck-delivery` (free shipping)
  - `mdi:truck-remove` (no free shipping)
  - `mdi:alert-circle` (error)

### Sensor States
- `Yes` - Free shipping to Israel available
- `No` - No free shipping to Israel
- `Unknown` - Unable to determine

### Sensor Attributes
```yaml
product_title: "Product Name"
price: "$99.99"
shipping_status: "Free shipping to Israel"
url: "https://amazon.com/..."
last_updated: "2026-01-10T12:00:00"
```

## 🔐 Security & Privacy

- **No API Keys Required**: Works without Amazon API credentials
- **No Data Collection**: All processing is local
- **Privacy Friendly**: Only fetches public product pages
- **Rate Limited**: Respects server resources
- **No Persistent Storage**: Only stores configuration

## 🚀 Performance

- **Update Frequency**: Configurable (default: 60 minutes)
- **Throttling**: Built-in to prevent excessive requests
- **Async Operations**: Non-blocking HTTP requests
- **Lightweight**: Minimal resource usage
- **Timeout**: 30 seconds per request
- **Memory**: Minimal footprint

## 🧪 Testing Checklist

- [ ] Installation via HACS
- [ ] Manual installation
- [ ] Configuration flow validation
- [ ] Multiple URL handling
- [ ] Invalid URL error handling
- [ ] Network error handling
- [ ] Sensor state updates
- [ ] Attribute population
- [ ] Icon changes
- [ ] Scan interval configuration
- [ ] Integration reload
- [ ] Integration unload
- [ ] Home Assistant restart
- [ ] Multiple Amazon domains

## 📝 Future Enhancements

### Planned Features
- Price tracking and history
- Price drop alerts
- Availability notifications
- Support for more Amazon domains
- Custom notification templates
- Historical data storage
- Dashboard card component
- Batch URL import
- Category-based monitoring

### Potential Improvements
- GraphQL API support (if available)
- Better parsing algorithms
- Machine learning for shipping detection
- Multi-country support
- CSV import/export
- Mobile app integration

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Development setup
- Testing procedures
- Pull request process

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 📚 Documentation

- **README.md**: Overview and quick start
- **INSTALL.md**: Detailed installation instructions
- **info.md**: Features and usage examples
- **CHANGELOG.md**: Version history
- **examples/configuration.yaml**: Automation examples

## 🐛 Known Limitations

1. **Amazon Structure Changes**: May require updates if Amazon changes page structure
2. **Rate Limiting**: Amazon may block requests if scan interval is too short
3. **No Historical Data**: Current state only (no history storage)
4. **Parsing Reliability**: Depends on consistent HTML structure
5. **International Shipping**: Detection relies on keywords (may need refinement)

## 🔗 Dependencies

### Required
- `homeassistant >= 2023.1.0`
- `beautifulsoup4 == 4.12.2`
- `aiohttp == 3.9.1`

### Included with Home Assistant
- `voluptuous` (validation)
- `python >= 3.11`

## 📞 Support

For help and support:
1. Check documentation files
2. Review example configurations
3. Check Home Assistant logs
4. Open GitHub issue with details

## 🎓 Learning Resources

This integration demonstrates:
- Home Assistant integration development
- Config flow implementation
- Sensor entity creation
- Web scraping with BeautifulSoup
- Async Python programming
- HACS integration structure
- Error handling patterns
- State management

Perfect for learning Home Assistant custom integration development!
