# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-10

### Added
- Initial release of Amazon Israel Shipping Watcher
- Support for monitoring multiple Amazon product URLs
- Automatic detection of free shipping to Israel
- Configurable scan intervals (5 minutes to 24 hours)
- Config flow for easy setup through Home Assistant UI
- Sensor entities with rich attributes (product title, price, shipping status)
- Support for multiple Amazon domains (.com, .co.uk, .de, .fr, .it, .es, .ca, .co.jp)
- HACS integration support
- Comprehensive documentation and examples

### Features
- Smart HTML parsing with BeautifulSoup
- Multiple selector fallbacks for robust data extraction
- Rate limiting and throttling
- Error handling and recovery
- Dynamic icon updates based on shipping status
- Last updated timestamp tracking
- Proper Home Assistant integration lifecycle management

## [Unreleased]

### Planned
- Support for price tracking and alerts
- Historical shipping status tracking
- Support for more Amazon domains
- Customizable notification templates
- Dashboard card component
- Integration with Home Assistant shopping list
