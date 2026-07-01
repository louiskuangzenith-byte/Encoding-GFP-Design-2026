from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


TEAM_NAME = "Encoding生序队"
EXPECTED_HEADER = ["Team_Name", "Seq_ID", "Sequence"]
STANDARD_AMINO_ACIDS = set("ARNDCQEGHILKMFPSTWYV")


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            return [], []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return header, list(csv.DictReader(handle))


def validate(path: Path) -> list[str]:
    header, rows = read_rows(path)
    errors: list[str] = []

    if header != EXPECTED_HEADER:
        errors.append(f"Header must be exactly: {','.join(EXPECTED_HEADER)}")
    if len(rows) != 6:
        errors.append(f"Expected 6 sequence rows, found {len(rows)}")
    if [row.get("Seq_ID", "") for row in rows] != [str(i) for i in range(1, 7)]:
        errors.append("Seq_ID values must be 1,2,3,4,5,6")

    sequences: list[str] = []
    for row_number, row in enumerate(rows, start=2):
        team_name = row.get("Team_Name", "")
        sequence = row.get("Sequence", "")
        sequences.append(sequence)

        if team_name != TEAM_NAME:
            errors.append(f"Row {row_number}: Team_Name must be {TEAM_NAME}")
        if sequence.strip() != sequence or any(char.isspace() for char in sequence):
            errors.append(f"Row {row_number}: Sequence contains whitespace")
        if not 220 <= len(sequence) <= 250:
            errors.append(f"Row {row_number}: Sequence length must be between 220 and 250 aa")
        if len(sequence) != 238:
            errors.append(f"Row {row_number}: Expected length 238 aa for this file")
        if not sequence.startswith("M"):
            errors.append(f"Row {row_number}: Sequence must start with M")
        if set(sequence) - STANDARD_AMINO_ACIDS:
            errors.append(f"Row {row_number}: Sequence contains non-standard amino-acid letters")
        if re.fullmatch(r"[ARNDCQEGHILKMFPSTWYV]+", sequence or "") is None:
            errors.append(f"Row {row_number}: Sequence must use uppercase one-letter amino-acid codes")

    if len(sequences) != len(set(sequences)):
        errors.append("Sequences must not contain internal duplicates")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a submission-format amino-acid sequence CSV.")
    parser.add_argument("csv_path", type=Path, help="Path to a CSV file with Team_Name, Seq_ID, Sequence columns.")
    args = parser.parse_args()

    errors = validate(args.csv_path)
    if errors:
        print("Validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
