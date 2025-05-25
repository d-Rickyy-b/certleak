# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]
### Added
### Changed
### Fixed

## [0.1.1] - 2025-05-25

### Changed

- Add more logging when stopping the app

### Fixed

- Fix for on_error and on_close callbacks in WebSocketClient
- Remove wrong call to idle() in example.py

## [0.1.0] - 2024-12-20

### Added

- Dockerfile for easy deployment
- New AuthorityKeyIDAnalyzer for matching certificates based on CA

### Fixed

- Use right module for DNStwister
- Properly handle empty updates

### Changed

- Switch to pyproject.toml for configuration
- Improve code based on ruff linting suggestions

## [0.0.1] - 2021-05-13

Initial release

[unreleased]: https://github.com/d-Rickyy-b/certleak/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/d-Rickyy-b/certleak/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/d-Rickyy-b/certleak/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/d-Rickyy-b/certleak/tree/v0.0.1
