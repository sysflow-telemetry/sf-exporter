# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

> **Types of changes:**
>
> -   **Added**: for new features.
> -   **Changed**: for changes in existing functionality.
> -   **Deprecated**: for soon-to-be removed features.
> -   **Removed**: for now removed features.
> -   **Fixed**: for any bug fixes.
> -   **Security**: in case of vulnerabilities.

## [[UNRELEASED](https://github.com/sysflow-telemetry/sf-exporter/compare/0.1-rc3...HEAD)]

## [[0.1-rc3](https://github.com/sysflow-telemetry/sf-exporter/compare/0.1-rc2...0.1-rc3)] - 2020-03-17

### Added

- Added TCP transport to rsyslog export.

### Changed

- Changed sysprint's base image to ubi8/ubi.
- Changed JSON schema (v0.1-rc3) [breaking change].
- Fixed issue in fields command option parsing.
- Increased `sf-exporter` version to the latest release candidate 0.1-rc3.
- Changed S3 client (minio) to version 5.0.6.

### Fixed

- Fixed issue in fields command option parsing.

## [[0.1-rc2](https://github.com/sysflow-telemetry/sf-exporter/compare/0.1-rc1...0.1-rc2)] - 2019-11-08

### Changed

- Increased `sf-exporter` version to the latest release candidate 0.1-rc2.

## [0.1-rc1] - 2019-10-31

### Added

- First release candidate.
