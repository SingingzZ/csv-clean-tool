import argparse
import csv
import os


def read_csv_rows(filepath):
    encodings = ["utf-8", "gbk", "latin-1"]
    for encoding in encodings:
        try:
            with open(filepath, "r", newline="", encoding=encoding) as f:
                reader = csv.reader(f)
                return list(reader), encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("utf-8", b"", 0, 1, "Unable to decode file with utf-8, gbk, or latin-1")


def is_empty_row(row):
    return all(field.strip() == "" for field in row)


def main():
    parser = argparse.ArgumentParser(description="CSV file cleaning tool")
    parser.add_argument("filepath", help="Path to the CSV file")
    args = parser.parse_args()

    filepath = args.filepath
    filename = os.path.basename(filepath)

    if not os.path.exists(filepath):
        print(f"Error: File not found - {filepath}")
        return

    try:
        rows, used_encoding = read_csv_rows(filepath)
    except UnicodeDecodeError as e:
        print(f"Error: Unable to decode file - {e}")
        return

    total_rows = len(rows)
    total_cols = len(rows[0]) if total_rows > 0 else 0

    cleaned_rows = []
    seen = set()
    for row in rows:
        if is_empty_row(row):
            continue
        row_tuple = tuple(row)
        if row_tuple in seen:
            continue
        seen.add(row_tuple)
        cleaned_rows.append(row)

    before_count = total_rows
    after_count = len(cleaned_rows)
    deleted_count = before_count - after_count

    with open("cleaned.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(cleaned_rows)

    print(f"File: {filename}", flush=True)
    print(f"Total rows: {total_rows}", flush=True)
    print(f"Total columns: {total_cols}", flush=True)
    print(f"清洗前: {before_count}行, 清洗后: {after_count}行, 删除了 {deleted_count}行", flush=True)


if __name__ == "__main__":
    main()
