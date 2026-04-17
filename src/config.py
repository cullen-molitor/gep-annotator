from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "sites.csv"
WATCHER_KML_PATH = DATA_DIR / "watcher.kml"
TARGET_KML_PATH = DATA_DIR / "target.kml"

BUFFER_SIZE_DEGREES = 0.002
LOOKAT_RANGE_METERS = 1500.0
REFRESH_INTERVAL_SECONDS = 2
TARGET_DATE = "2020-06-15"
