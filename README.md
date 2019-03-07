backups-role
=========

Backups strategies for Coopdevs projects.

Requirements
------------

This role uses [Restic](https://restic.net).

Role Variables
--------------
```yaml
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
backups_role_restic_repo_name: {{ ansible.hostname }}

#########################################
### Warning! Sensible variables below ###
#########################################

# Restic repository password
backups_role_restic_password:

# Remote bucket URL in restic format
# Example for backblaze:  "b2:bucketname:path/to/repo"
# Example for local repo: "/var/backups/repo"
backups_role_bucket_url:

# Backblaze "application" or bucket credentials
backups_role_b2_app_key_id:
backups_role_b2_app_key:
```


Dependencies
------------

* [paulfantom.restic](https://galaxy.ansible.com/paulfantom/restic)

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
    - role: coopdevs.backups-role
```

Sensible variables
------------------
Please protect at least the variables below the "sensible variables" above. To do so, use [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) to encrypt with a passphrase the config file with these vars.


Backblaze
---------
Backblaze provides two kind of keys: account or master, and application. There's only one account key and has power over all the buckets. We can have many app keys, that can have rw access to any, one or more buckets.

We should not use account key or reuse application keys. Even if restic passwords are different and buckets are different, one server could be able to delete backups of others, or even create more buckets and feed the bill.

Therefore, we use app keys instead of account key. As per, `ansible-restic`, it just gives the credentials to restic, regardless of the type of key. This is why we can set `ansible-restic`'s `b2_account_key` with `backup-role`'s `backups_role_b2_app_key`.

What restic calls "Account key" appears at B2 web as "Master application key".


Restic
------

Restic will create a "repository" during the Ansible provisioning. This looks like a directory inside the BackBlaze bucket being the path inside the bucket the last part of `backups_role_bucket_url`, split by `:`. If you want to place it at the root, try something like `b2:mybucket:/`. More on this at [restic docs](https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#backblaze-b2). From the outside, you will see:  
`config  data  index  keys  locks  snapshots`

And if you decrypt it, for instance, when [mounting it](https://restic.readthedocs.io/en/latest/050_restore.html#restore-using-mount):  
`hosts  ids  snapshots  tags`

However, you may probably want to restore just a particular snapshot from the repo. To do it, use [`restic restore`](https://restic.readthedocs.io/en/latest/050_restore.html#restoring-from-a-snapshot). You will need to provide it with the snapshot id you want to resotore and the target dir to unload it. You can explore snapshots doing [`restic snapshots`](https://restic.readthedocs.io/en/latest/045_working_with_repos.html#listing-all-snapshots). A particular case is to restore the last snapshot, where you can use `latest` as snapshot id.

To restore just a file from the last snapshot instead of the whole repo, you can use the `dump` subcommand: `restic dump latest myfile > /home/user/myfile`

Remember that all restic commands need to know where to communicate to and which credentials with. So you can either pass them as parameters, or export them as environment variables. For this case, we need:

```sh
export RESTIC_REPOSITORY="b2:mybucketname:/"
export RESTIC_PASSWORD="long sentence with at least 7 words"
export B2_ACCOUNT_ID="our app key id"
export B2_ACCOUNT_KEY="our app key that is very long and has numbers and uppercase letters"
```


License
-------

GPLv3