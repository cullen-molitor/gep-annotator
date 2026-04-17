import argparse
import sys

from config import CSV_PATH
from csv_handler import load_csv, next_unlabeled_index, save_csv, update_row
from gep_launcher import launch_gep, open_target_kml
from kml_generator import generate_target_kml, write_target_kml


def get_user_input() -> tuple[str, int] | None:
    try:
        raw = input("  Label (P/N) + Confidence (1-5), e.g. 'P3': ").strip().upper()
    except EOFError:
        return None

    if len(raw) < 2:
        print("  Invalid. Expected format: P3 or N2")
        return None

    label = raw[0]
    if label not in ("P", "N"):
        print("  Invalid label. Use P or N.")
        return None

    try:
        confidence = int(raw[1])
    except ValueError:
        print("  Invalid confidence. Use 1-5.")
        return None

    if confidence < 1 or confidence > 5:
        print("  Confidence must be 1-5.")
        return None

    return (label, confidence)


def count_labeled(rows: list[dict]) -> int:
    return sum(1 for r in rows if r.get("label"))


def main() -> None:
    parser = argparse.ArgumentParser(description="ASM Annotator v2")
    parser.add_argument("csv", nargs="?", default=str(CSV_PATH), help="Path to CSV file")
    args = parser.parse_args()

    csv_path = args.csv if args.csv == str(CSV_PATH) else args.csv
    from pathlib import Path

    csv_path = Path(csv_path)

    rows = load_csv(csv_path)
    total = len(rows)
    labeled = count_labeled(rows)
    print(f"Loaded {total} points ({labeled} labeled, {total - labeled} remaining)\n")

    idx = next_unlabeled_index(rows)
    if idx is None:
        print("All points are already labeled.")
        return

    # Launch GEP, then open first target
    launch_gep()

    try:
        while True:
            idx = next_unlabeled_index(rows)
            if idx is None:
                print("\nAll points labeled. Done!")
                break

            row = rows[idx]
            labeled = count_labeled(rows)
            print(f"Point {labeled + 1}/{total}: ({row['lat']}, {row['lon']})")

            # Write target KML and open it in GEP
            kml = generate_target_kml(str(idx), float(row["lat"]), float(row["lon"]))
            write_target_kml(kml)
            open_target_kml()

            # Collect input (retry on invalid)
            while True:
                result = get_user_input()
                if result is not None:
                    break

            label, confidence = result
            update_row(rows, idx, label, confidence)
            save_csv(csv_path, rows)
            print(f"  -> {label}{confidence}\n")

    except KeyboardInterrupt:
        labeled = count_labeled(rows)
        print(f"\n\nInterrupted. Progress: {labeled}/{total} points labeled.")
        sys.exit(0)


if __name__ == "__main__":
    main()
