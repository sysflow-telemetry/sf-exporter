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

## [Unreleased]

## [0.6.0] - 2023-11-28

### Changed

- Bumped UBI version to 9.3-1361.1699548029

## [0.5.1] - 2023-06-07

### Changed

- Bump UBI to 8.8-854

## [0.5.0] - 2022-10-17

### Changed

- Bump UBI to 8.6-943.1665521450

## [0.4.4] - 2022-08-01

### Changed

- Bump UBI to 8.6-855

## [0.4.3] - 2022-06-21

### Changed

- Bumped SysFlow version to 0.4.3

## [0.4.2] - 2022-06-13

### Changed

- Bumped SysFlow version to 0.4.2

## [0.4.1] - 2022-05-26

### Changed

- Bumped UBI version to 8.6-754

## [0.4.0] - 2022-02-18

### Added

- Added ability to export from multiple directories to multiple S3 buckets
- Added the --mode flag, which changes exporter copying behavior

### Changed

- Bumped minio version to 7.1.3
- Bumped UBI version to 8.5-226

### Fixed

## [0.3.1] - 2021-09-29

### Changed

- Update(ubi): Bumped UBI version to 8.4-211.

## [0.3.0] - 2021-09-20

### Added

- Export objects to path following \<clusterID\>/\<nodeID\>/\<nodeIP\>/Y/m/d/\<fileName\>.
- Github workflows for CI.
- Docker image push to GHCR and Dockerhub.

### Removed

- Moved away from Dockerhub CI.
- Removed rsyslog export type (implemented in SysFlow processor).

### Changed

- Bumped base docker image to 8.4-203.1622660121.
- Bumped version of urllib3 to 1.26.5.
- Bumped version of minio client to 7.0.3.
- Updated documentation.

## [0.2.2] - 2020-12-07

### Changed

- Sets fixed versions of Pandas and numpy.
- Updated to use latest SysFlow APIs.


## [0.2.1] - 2020-12-02

### Changed

- Updated to use latest SysFlow APIs.


## [0.2.0] - 2020-12-01

### Changed

- Updated to use latest SysFlow APIs.

## [0.1.0] - 2020-10-30

### Changed

- syslog export type depricated; use `sf-processor` instead.

## [0.1.0-rc4] - 2020-08-10

### Added

- Added labels to exporter image.
- Added license to exporter image.

### Changed

- Added support for new Avro schema.
- Tracking latest Python APIs.
- Improves rsyslog handling.
- Increased `sf-exporter` version to the latest release candidate 0.1-rc4.


## [0.1-rc3] - 2020-03-17

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

## [0.1-rc2] - 2019-11-08

### Changed

- Increased `sf-exporter` version to the latest release candidate 0.1-rc2.

## [0.1-rc1] - 2019-10-31

### Added

- First release candidate.

[Unreleased]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.6.0...HEAD
[0.6.0]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.5.1...0.6.0
[0.5.1]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.4.4...0.5.0
[0.4.4]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.4.3...0.4.4
[0.4.3]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.4.2...0.4.3
[0.4.2]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.3.1...0.4.0
[0.3.1]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.2.2...0.3.0
[0.2.2]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.1.0-rc4...0.1.0
[0.1.0-rc4]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.1-rc3...0.1.0-rc4
[0.1-rc3]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.1-rc2...0.1-rc3
[0.1-rc2]: https://github.com/sysflow-telemetry/sf-exporter/compare/0.1-rc1...0.1-rc2
[0.1-rc1]: https://github.com/sysflow-telemetry/sf-exporter/releases/tag/0.1-rc1
