from prometheus_client import Gauge

FILESYSTEM_USAGE = Gauge("rne_filesystem_usage", "Filesystem usage", ["name"])
SOFT_QUOTA = Gauge("rne_filesystem_soft_quota", "Filesystem soft quota", ["name"])
HARD_QUOTA = Gauge("rne_filesystem_hard_quota", "Filesystem hard quota", ["name"])
FILES_USED = Gauge("rne_filesystem_files_used", "Number of files used", ["name"])
BILLED_USAGE = Gauge("rne_filesystem_billed_usage", "Billed usage", ["name"])
FREE_SNAPSHOTS = Gauge("rne_filesystem_free_snapshots", "Number of free snapshots", ["name"])
CUSTOM_SNAPSHOTS = Gauge("rne_filesystem_custom_snapshots", "Number of custom snapshots", ["name"])
