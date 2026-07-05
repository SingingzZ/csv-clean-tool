import argparse
import csv
import os


def read_csv_rows(filepath):
    """尝试多种编码读取CSV文件，返回行列表和实际使用的编码"""
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
    """检查行是否所有字段均为空白"""
    return all(field.strip() == "" for field in row)


def is_header_row(row, row_index):
    """自动检测是否为表头行（第一行且 age 列非整数、全行无数字）"""
    if row_index != 0:
        return False
    if len(row) < 3:
        return False
    age_field = row[1].strip()
    try:
        int(age_field)
        return False
    except ValueError:
        for field in row:
            if field.strip() == "":
                continue
            if any(c.isdigit() for c in field):
                return False
        return True


def validate_columns(rows):
    """验证所有非空行的列数是否一致"""
    if not rows:
        return
    expected_len = None
    for idx, row in enumerate(rows, start=1):
        if is_empty_row(row):
            continue
        if expected_len is None:
            expected_len = len(row)
        elif len(row) != expected_len:
            raise ValueError(
                f"CSV format error: column count mismatch at row {idx}. "
                f"Expected {expected_len}, got {len(row)}."
            )


def main():
    parser = argparse.ArgumentParser(description="CSV file cleaning tool")
    parser.add_argument("--input", default="test.csv", help="Input CSV file path")
    parser.add_argument("--output", default="cleaned.csv", help="Output CSV file path")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    filename = os.path.basename(input_path)

    if not os.path.exists(input_path):
        print(f"Error: Input file not found - {input_path}")
        return

    try:
        rows, used_encoding = read_csv_rows(input_path)
    except UnicodeDecodeError as e:
        print(f"Error: Failed to decode file. Tried utf-8, gbk, latin-1. Detail: {e}")
        return

    total_rows = len(rows)
    total_cols = len(rows[0]) if total_rows > 0 else 0

    try:
        validate_columns(rows)
    except ValueError as e:
        print(f"Error: {e}")
        return

    cleaned_rows = []
    seen = set()
    age_invalid_count = 0
    city_empty_count = 0

    for idx, row in enumerate(rows):
        if is_empty_row(row):
            continue

        row_tuple = tuple(row)
        if row_tuple in seen:
            continue
        seen.add(row_tuple)

        if is_header_row(row, idx):
            cleaned_rows.append(row)
            continue

        if len(row) < 3:
            print(f"Warning: Row skipped due to insufficient columns: {row}")
            continue

        age_field = row[1].strip()
        city_field = row[2].strip()

        try:
            int(age_field)
        except ValueError:
            print(f"Warning: Invalid age value '{age_field}' in row, skipped. Row: {row}")
            age_invalid_count += 1
            continue

        if city_field == "":
            print(f"Warning: Empty city in row, skipped. Row: {row}")
            city_empty_count += 1
            continue

        cleaned_rows.append(row)

    before_count = total_rows
    after_count = len(cleaned_rows)
    deleted_count = before_count - after_count

    try:
        with open(output_path, "w", newline="", encoding=used_encoding) as f:
            writer = csv.writer(f)
            writer.writerows(cleaned_rows)
    except IOError as e:
        print(f"Error: Failed to write output file - {e}")
        return

    print(f"File: {filename}", flush=True)
    print(f"Total rows: {total_rows}", flush=True)
    print(f"Total columns: {total_cols}", flush=True)
    print(f"清洗前: {before_count}行", flush=True)
    print(f"清洗后: {after_count}行", flush=True)
    print(
        f"删除了 {deleted_count}行（其中 {age_invalid_count}行因年龄无效，{city_empty_count}行因城市为空）",
        flush=True,
    )
    print(f"输出文件: {output_path}", flush=True)


if __name__ == "__main__":
    main()
