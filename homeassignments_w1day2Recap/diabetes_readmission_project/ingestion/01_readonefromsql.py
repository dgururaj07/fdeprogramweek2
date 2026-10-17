import csv
from pathlib import Path

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

# This script lives in ingestion/, so the project root is one level up.
# Resolving from __file__ makes the path work from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "diabetic_data.csv"

# DictReader consumes the header row automatically, so next() gives the
# first data row.
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    first_row = next(reader)

# Keep only the columns of interest from the raw row.
row = {col: first_row[col] for col in COLUMNS}

# csv.DictReader returns every value as a string - print the type to make
# that explicit (no numeric parsing happens here).
for col, value in row.items():
    print(f"{col}: {value} ({type(value).__name__})")
