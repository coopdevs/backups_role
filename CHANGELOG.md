# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

- Fix coopdevs.restic-role version [See]

## [v1.2.10] - 2023-08-16
### Fixed
- Replace paulfantom restic role because of no maintenace
  See [#45](https://github.com/coopdevs/backups_role/pull/45)

## [v1.2.9] - 2022-08-04
### Fixed
- Escape dollar character in docker compose
  See [#44](https://github.com/coopdevs/backups_role/pull/44)


## [v1.2.8] - 2022-08-03
### Fixed
- Backup user can manage docker containers
  See [#43](https://github.com/coopdevs/backups_role/pull/43)

## [v1.2.7] - 2022-08-03
### Fixed
- Activated restic exporter and exposed with Prometheus format
  See [#42](https://github.com/coopdevs/backups_role/pull/42)
- Ensure the backups user has USAGE privilage on the database's schema. We assume it to be`public` #41.


## [v1.2.6] - 2020-01-23
### Fixed
- When using default backups-prepare script, manage the case when no assets_paths are defined.
  See [#38](https://github.com/coopdevs/backups_role/pull/38)

## [v1.2.5] - 2020-01-20
### Changed
- Print promtail-friendly logs to be compatible with monitoring-role. See [#37](https://github.com/coopdevs/backups_role/pull/37)

## [v1.2.4] - 2019-12-03

### Fixed

- Do not backup non-existing `config.tar.gz` with the restic command [#36](https://github.com/coopdevs/backups_role/pull/36)

## [v1.2.3] - 2019-12-03

### Removed

- `backups_role_config_paths` as we don't see the point on backing up anything
    other than a single path with assets. We always have a provisioning repo
    that is able to setup a new server with its config [#34](https://github.com/coopdevs/backups_role/pull/34/files)
