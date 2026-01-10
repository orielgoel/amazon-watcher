# Contributing to Amazon Israel Shipping Watcher

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Home Assistant version
   - Integration version
   - Relevant logs (with sensitive info redacted)

### Suggesting Features

1. Check if the feature has already been requested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Any implementation ideas

### Code Contributions

1. **Fork the repository**
2. **Create a branch** for your feature/fix: `git checkout -b feature/amazing-feature`
3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   - Test with Home Assistant
   - Verify all sensors work correctly
   - Check logs for errors
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## Development Setup

### Prerequisites

- Home Assistant development environment
- Python 3.11 or later
- Git

### Local Development

1. Clone your fork:
```bash
git clone https://github.com/orielgoel/amazon-watcher.git
cd amazon-watcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy to Home Assistant custom_components:
```bash
ln -s $(pwd)/custom_components/amazon_watcher ~/.homeassistant/custom_components/amazon_watcher
```

4. Restart Home Assistant and test

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

## Testing

Before submitting a PR:

1. Test with multiple Amazon URLs
2. Test error scenarios (invalid URLs, network issues)
3. Check Home Assistant logs for warnings/errors
4. Verify sensors update correctly
5. Test configuration flow

## Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Write clear commit messages
- Update CHANGELOG.md
- Update documentation if needed
- Ensure no new linter errors
- Respond to review feedback

## Questions?

Feel free to open an issue for any questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
