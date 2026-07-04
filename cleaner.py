import argparse
import csv
import os


def main():
    parser = argparse.ArgumentParser(description="CSV file cleaning tool")
    parser.add_argument("filepath", help="Path to the CSV file")
    args = parser.parse_args()

    filepath = args.filepath
    filename = os.path.basename(filepath)

    if not os.path.exists(filepath):
        print(f"Error: File not found - {filepath}")
        return

    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    total_rows = len(rows)
    total_cols = len(rows[0]) if total_rows > 0 else 0

    print(f"File: {filename}", flush=True)
    print(f"Total rows: {total_rows}", flush=True)
    print(f"Total columns: {total_cols}", flush=True)


if __name__ == "__main__":
    main()
