from time import sleep
from typing import Optional, TypedDict
from dotenv import load_dotenv

import click
from fabric import Connection
from prometheus_client import start_http_server

from rsync_net_exporter.prom import (
  BILLED_USAGE,
  CUSTOM_SNAPSHOTS,
  FILES_USED,
  FILESYSTEM_USAGE,
  FREE_SNAPSHOTS,
  HARD_QUOTA,
  SOFT_QUOTA,
)

load_dotenv()


class FileSystemMetric(TypedDict):
  name: str
  usage: float
  soft_quota: float
  hard_quota: float
  files: int
  billed_usage: float
  free_snaps: float
  custom_snaps: Optional[float]

def get_quota(user: Optional[str], endpoint: str) -> list[FileSystemMetric]:
  result = Connection(host=endpoint, user=user).run('quota')

  lines = result.stdout.strip().split('\n')

  metrics: list[FileSystemMetric] = []

  for line in lines:
    line = line.strip()
    if not line or line.startswith('Disk Quotas') or line.startswith('Filesystem') or line.startswith('*'):
      continue

    parts = line.split()

    if len(parts) >= 7:
      metric: FileSystemMetric = {
        'name': parts[0],
        'usage': float(parts[1]),
        'soft_quota': float(parts[2]),
        'hard_quota': float(parts[3]),
        'files': int(parts[4]),
        'billed_usage': float(parts[5]),
        'free_snaps': float(parts[6]),
        'custom_snaps': float(parts[7]) if len(parts) > 7 else None
      }
      metrics.append(metric)

  return metrics


@click.command()
@click.option("--endpoint", prompt="your rsync.net endpoint", envvar="RNE_ENDPOINT")
@click.option("--user", prompt="your rsync.net username", default="", envvar="RNE_USER")
@click.option("--port", default=8000, envvar="RNE_EXPORTER_PORT")
@click.option("--interval", default=300, envvar="RNE_SCRAPE_INTERVAL")
def exporter(endpoint: str, user: Optional[str], interval: int, port: int):
  if user == "":
    user = None

  start_http_server(port)

  while True:
    metrics = get_quota(user, endpoint)
    for metric in metrics:
      FILESYSTEM_USAGE.labels(name=metric['name']).set(metric['usage'])
      SOFT_QUOTA.labels(name=metric['name']).set(metric['soft_quota'])
      HARD_QUOTA.labels(name=metric['name']).set(metric['hard_quota'])
      FILES_USED.labels(name=metric['name']).set(metric['files'])
      BILLED_USAGE.labels(name=metric['name']).set(metric['billed_usage'])
      FREE_SNAPSHOTS.labels(name=metric['name']).set(metric['free_snaps'])
      if metric['custom_snaps'] is not None:
        CUSTOM_SNAPSHOTS.labels(name=metric['name']).set(metric['custom_snaps'])
    sleep(interval)

if __name__ == "__main__":
  exporter()
