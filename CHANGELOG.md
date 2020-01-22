# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.2.6] - 2020-01-23
### Changed
- Fix: when using default backups-prepare script, manage the case when no assets_paths are defined.
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
