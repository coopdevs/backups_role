backups-role
=========

Backups strategies for Coopdevs projects.

Requirements
------------

This role uses [Restic](https://restic.net).

Role Variables
--------------
```
# Restic version
backups_role_restic_version: '0.9.3'

# Location of the scripts
backups_role_script_path: '/opt/backups'

# Location of the files generated by cron jobs
backups_role_last_backup_path: '/var/backup/last'

# Lists of paths to backup
backups_role_config_paths: ['/etc', '/root', '/usr/local/etc']
backups_role_assets_paths: []

# System user and group. Who will run scripts, restic and cron jobs
#+  and will own directories and files
backups_role_user:
backups_role_group:

# Postgresql user to run the pg_dump
backups_role_postgresql_user: "postgres"

# Restic repository name used only in case
#+ we need to address different restic repos
backups_role_restic_repo_name:

# Restic repository password
backups_role_restic_password:

# Remote bucket URL in restic format
# Example for backblaze:  "b2:bucketname:path/to/repo"
# Example for local repo: "/var/backups/repo"
backups_role_bucket_url:

# Backblaze credentials
backups_role_b2_account_id:
backups_role_b2_account_key:
```


Dependencies
------------

* [paulfantom.restic](https://galaxy.ansible.com/paulfantom/restic)

Example Playbook
----------------

    - hosts: servers
      roles:
         - role: coopdevs.backups-role

License
-------

GPLv3
