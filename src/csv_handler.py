import csv
import os
import tempfile
from pathlib import Path

EXPECTED_COLUMNS = ["lat", "lon", "label", "confidence"]


def load_csv(path: Path) -> list[dict]:
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                f"Expected columns {EXPECTED_COLUMNS}, got {reader.fieldnames}"
            )
        return list(reader)


def save_csv(path: Path, rows: list[dict]) -> None:
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".csv")
    try:
        with os.fdopen(fd, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(tmp_path, path)
    except BaseException:
        os.unlink(tmp_path)
        raise


def next_unlabeled_index(rows: list[dict]) -> int | None:
    for i, row in enumerate(rows):
        if not row.get("label"):
            return i
    return None


def update_row(rows: list[dict], index: int, label: str, confidence: int) -> None:
    rows[index]["label"] = label
    rows[index]["confidence"] = str(confidence)
