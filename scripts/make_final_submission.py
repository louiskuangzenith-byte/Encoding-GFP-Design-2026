from __future__ import annotations

import argparse
import csv
from pathlib import Path


TEAM_NAME = "Encoding生序队"
EXPECTED_COLUMNS = ["Team_Name", "Seq_ID", "Sequence"]


def read_sequences(input_path: Path) -> list[str]:
    with input_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if "Sequence" not in (reader.fieldnames or []):
            raise ValueError("Input CSV must contain a Sequence column.")
        return [row["Sequence"].strip() for row in reader]


def write_submission(sequences: list[str], output_path: Path) -> None:
    if len(sequences) != 6:
        raise ValueError(f"Expected 6 sequences, found {len(sequences)}.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPECTED_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for seq_id, sequence in enumerate(sequences, start=1):
            writer.writerow(
                {
                    "Team_Name": TEAM_NAME,
                    "Seq_ID": seq_id,
                    "Sequence": sequence,
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a three-column sequence submission CSV.")
    parser.add_argument("input_csv", type=Path, help="Input CSV containing a Sequence column.")
    parser.add_argument("output_csv", type=Path, help="Output CSV path.")
    args = parser.parse_args()

    sequences = read_sequences(args.input_csv)
    write_submission(sequences, args.output_csv)
    print(args.output_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
