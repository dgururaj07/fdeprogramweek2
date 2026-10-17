import csv
from pathlib import Path
from typing import Any

# This script lives in ingestion/, so the project root is one level up.
# Resolving from __file__ makes the path work from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "diabetic_data.csv"

# Only the columns we're interested in - not loading the full 50-column CSV.
COLUMNS = [
    "encounter_id",
    "patient_nbr",
    "age",
    "time_in_hospital",
    "number_inpatient",
    "number_emergency",
    "number_outpatient",
    "num_medications",
    "readmitted",
]


def to_int(value: Any, default: int = 0) -> int:
    # CSV values are always strings; fall back to `default` for missing or
    # non-numeric values (e.g. a stray "?" placeholder) instead of raising.
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def clean_row(row: dict) -> dict:
    # Cast the numeric columns to int to match the Postgres schema types;
    # age and readmitted stay as strings since they're categorical.
    return {
        "encounter_id": to_int(row.get("encounter_id")),
        "patient_nbr": to_int(row.get("patient_nbr")),
        "age": row.get("age", ""),
        "time_in_hospital": to_int(row.get("time_in_hospital")),
        "number_inpatient": to_int(row.get("number_inpatient")),
        "number_emergency": to_int(row.get("number_emergency")),
        "number_outpatient": to_int(row.get("number_outpatient")),
        "num_medications": to_int(row.get("num_medications")),
        "readmitted": row.get("readmitted", ""),
    }


if __name__ == "__main__":
    # DictReader consumes the header row automatically, so next() gives the
    # first data row.
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_row = next(reader)

    cleaned = clean_row(raw_row)

    for col, value in cleaned.items():
        print(f"{col}: {value} ({type(value).__name__})")
