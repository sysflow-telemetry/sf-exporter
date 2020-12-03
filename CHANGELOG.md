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

## [[UNRELEASED](https://github.com/sysflow-telemetry/sf-exporter/compare/0.2.1...HEAD)]

## [[0.2.1](https://github.com/sysflow-telemetry/sf-exporter/compare/0.2.0...0.2.1)] - 2020-12-02

### Changed

- Updated to use latest SysFlow APIs.


## [[0.2.0](https://github.com/sysflow-telemetry/sf-exporter/compare/0.1.0...0.2.0)] - 2020-12-01

### Changed

- Updated to use latest SysFlow APIs.

## [[0.1.0](https://github.com/sysflow-telemetry/sf-exporter/compare/0.1-rc4...0.1.0)] - 2020-10-30

### Changed

- syslog export type depricated; use `sf-processor` instead.

## [[0.1.0-rc4](https://github.com/sysflow-telemetry/sf-exporter/compare/0.1-rc3...0.1.0-rc4)] - 2020-08-10

### Added

- Added labels to exporter image.
- Added license to exporter image.

### Changed

- Added support for new Avro schema.
- Tracking latest Python APIs.
- Improves rsyslog handling.
- Increased `sf-exporter` version to the latest release candidate 0.1-rc4.


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
