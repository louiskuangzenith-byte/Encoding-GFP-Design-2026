# Encoding GFP Design 2026

This repository contains the public code package for the 2026 SynBio Challenges GFP design submission by Team Encoding生序队.

## Repository contents

* `scripts/validate_submission.py`: validates the amino-acid sequence CSV format.
* `scripts/make_final_submission.py`: prepares a CSV file in the required submission format.
* `data/final_candidates.csv`: final candidate sequence file in the required three-column format.
* `requirements.txt`: minimal Python dependencies.

## Submission format

The sequence file follows the required format:

```text
Team_Name,Seq_ID,Sequence
```

The validation script checks:

* sequence count;
* required header;
* valid sequence length;
* starting methionine;
* standard amino-acid alphabet;
* duplicate sequences.

## Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Validate the candidate CSV:

```bash
python scripts/validate_submission.py data/final_candidates.csv
```

## Data note

This repository only contains lightweight public files needed for sequence-format preparation and validation. Official challenge resources should be obtained from the SynBio Challenges data package.

## Team

Encoding生序队
