#!/usr/bin/python3

# To run restic
import subprocess
# To decode restic output
import json
# To generate prometheus file
#from prometheus_client import Info, Gauge, write_to_textfile, CollectorRegistry, start_http_server
# to get env vars
import os
# to parse time
import re
#from datetime import datetime
#import time

"""
Snapshots

command: restic snapshots --json

output:
    """
json1 = """
[
  {
    "time": "2019-10-20T03:45:31.594690521+02:00",
    "parent": "c05d5a8427d0a90d858398071966f46df13d99a1479793ba4be27593819e6d5e",
    "tree": "fe6dda4485c4c1f38d4aea92b9df641e17d0bc438cd107c9684fca685c030610",
    "paths": [
      "/opt/backup/.tmp/pg_dump_opencell.sql",
      "/opt/backup/.tmp/pg_dump_keycloak.sql",
      "/home/opencell/input-files/opencell-version.txt"
    ],
    "hostname": "stagingopencell.coopdevs.org",
    "id": "9c860da944bb4bf2dfc19882603e7923f427c36ba01d06f8c3f54ee10836a59b",
    "short_id": "9c860da9"
  },
  {
    "time": "2019-10-20T03:45:31.594690521+02:00",
    "parent": "c05d5a8427d0a90d858398071966f46df13d99a1479793ba4be27593819e6d5e",
    "tree": "fe6dda4485c4c1f38d4aea92b9df641e17d0bc438cd107c9684fca685c030610",
    "paths": [
      "/opt/backup/.tmp/pg_dump_opencell.sql",
      "/opt/backup/.tmp/pg_dump_keycloak.sql",
      "/home/opencell/input-files/opencell-version.txt"
    ],
    "hostname": "stagingopencell.coopdevs.org",
    "id": "9c860da944bb4bf2dfc19882603e7923f427c36ba01d06f8c3f54ee10836a59b",
    "short_id": "9c860da9"
  }
]
"""

"""
Snapshots

command: restic stats --mode restore-size 9c860da9 --json

output:
    """
json2 = """
{
  "total_size": 1389273071,
  "total_file_count": 9
}

"""


"""
command: restic stats --mode raw-data --json

output:
    """
json3 = """
{
  "total_size":6110624501,
  "total_file_count":0,
  "total_blob_count":20909
}

"""

# Run restic calls and save output


def run_cmd(args):
    argv = args.split(" ")
    out = subprocess.run(argv, capture_output=True)
    out = out.stdout.decode("utf-8")
    return json.loads(out)


def str_to_isoformat(s):
    regex = re.compile("([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]{8}\.[0-9]{6})[0-9]*([+-][0-9]{2}:[0-9]{2})")
    return regex.sub("\g<1>\g<2>", s)


class PrometheusEntry(object):
    def __init__(self, name, _type, description, labels, value, timestamp):
        self.name = name
        self.type = _type
        self.description = description
        self.labels = labels
        self.value = value
        self.timestamp = timestamp

    def to_str(self):
        raise NotImplementedError("Use GaugeEntry, InfoEntry or implement your subclass instead")


class GaugeEntry(PrometheusEntry):
    def __init__(self, name, description, labels, value, timestamp):
        super().__init__(name, "gauge", description, labels, value, timestamp)

    def to_str(self):

        # Metric name
        line = self.name

        # Labels (optional)
        if (isinstance(self.labels, dict) and self.labels):
            line = line + "{"
            for k, v in self.labels.items():
                line = line + k + '="' + v + '", '
            line = line + "}"

        # Value
        line = line + " " + str(self.value)

        # Timestamp (optional)
        if (self.timestamp):
            line = line + " " + self.timestamp.toisoformat()

        result = '# HELP {} {}\n'.format(self.name, self.description)
        result = result + '# TYPE {} {}\n'.format(self.name, self.type)
        result = result + line

        return result


class InfoEntry(GaugeEntry):
    def __init__(self, name, description, labels):
        super().__init__(name, description, labels, 1.0, None)


def main():
    restic_helper = os.getenv("RESTIC_WRAPPER_PATH")
    restic_helper = "/home/raneq/somconnexio/opencell/opencell-provisioning/backup-restore/restic-stagingopencell_coopdevs_org"

    #restic_list = run_cmd(restic_helper + ' snapshots --json')
    restic_list = json.loads(json1)
    restic_latest_info = restic_list[-1]

    #restic_latest_size = run_cmd(restic_helper + ' stats --mode restore-size {} --json'.format(restic_latest_info['short_id']))
    restic_latest_size = json.loads(json2)

    #restic_overview = run_cmd(restic_helper + ' stats --mode raw-data --json')
    restic_overview = json.loads(json3)

    # Use the data to generate prometheus-compatible file
    # from prometheus_client import CollectorRegistry, Gauge, write_to_textfile

#   registry = CollectorRegistry()
#   g = Gauge('raid_status', '1 if raid array is okay', registry=registry)
#   g.set(1)
#   write_to_textfile('/configured/textfile/path/raid.prom', registry)

    #

    # Info for last backup
    #prom_reg = CollectorRegistry()

    """
    prom_latest_info = Info('backups_latest', 'Details about latest snapshot', registry=prom_reg)
    prom_latest_info.info({
        'short_id': str(restic_latest_info['short_id']),
        'paths_saved': str(restic_latest_info['paths']),
        'restore_size': str(restic_latest_size['total_size']),
        })
    """
    #dt_s = str_to_isoformat(restic_latest_info['time'])
    #dt = datetime.fromisoformat(dt_s)
    #td = datetime.now() - dt
    #prom_latest_elapsed = Gauge('backups_latest_elapse', 'Elapsed seconds since last snapshot was taken', registry=prom_reg)
    #prom_latest_elapsed.set(td.total_seconds())

    #prom_latest_gauge = Gauge('backups_latest_size', 'Restore size of latest snapshot', registry=prom_reg)
    #prom_latest_gauge.set(restic_latest_size['total_size'])

    #write_to_textfile('example.prom', prom_reg)
#    start_http_server(8030, registry=prom_reg)
 #   time.sleep(10)
    prom_latest_info = InfoEntry(
        'backups_latest',
        'Details about latest snapshot',
        {
            'short_id': str(restic_latest_info['short_id']),
            'paths_saved': str(restic_latest_info['paths']),
            'restore_size': str(restic_latest_size['total_size']),
        }
    )
    fd = open("proves.pom","w")
    print(prom_latest_info.to_str(), file=fd)

"""
    "time": "2019-10-20T03:45:31.594690521+02:00",
    "paths": [
      "/opt/backup/.tmp/pg_dump_opencell.sql",
      "/opt/backup/.tmp/pg_dump_keycloak.sql",
      "/home/opencell/input-files/opencell-version.txt"
    ],
    "hostname": "stagingopencell.coopdevs.org",
    "short_id": "9c860da9"

"""


if __name__ == "__main__":
    main()
