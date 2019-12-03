# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed

- `backups_role_config_paths` as we don't see the point on backing up anything
    other than a single path with assets. We always have a provisioning repo
    that is able to setup a new server with its config.
