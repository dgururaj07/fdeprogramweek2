import csv
import importlib.util
from pathlib import Path

# 02_clean_row.py starts with a digit, so it can't be imported with a normal
# "import" statement - load it directly from its file path instead.
_spec = importlib.util.spec_from_file_location(
    "clean_row_module", Path(__file__).parent / "02_clean_row.py"
)
clean_row_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(clean_row_module)

# This script lives in ingestion/, so the project root is one level up.
# Resolving from __file__ makes the path work from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "diabetic_data.csv"


def calculate_risk(row: dict) -> tuple[int, str]:
    # Prototype scoring rule (Checkpoint 4): each condition below adds
    # points; the total maps to a LOW/MEDIUM/HIGH risk level.
    score = 0

    if row["number_inpatient"] >= 3:
        score += 3
    if row["number_emergency"] >= 2:
        score += 2
    if row["number_outpatient"] >= 3:
        score += 1
    if row["time_in_hospital"] >= 7:
        score += 1
    if row["num_medications"] >= 20:
        score += 1

    # Score -> risk band: 0-2 LOW, 3-4 MEDIUM, 5+ HIGH
    if score <= 2:
        level = "LOW"
    elif score <= 4:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return score, level


if __name__ == "__main__":
    # Read only the first data row from the CSV (header row is consumed by
    # DictReader automatically).
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_row = next(reader)

    # Cast the columns of interest to their proper types before scoring.
    cleaned = clean_row_module.clean_row(raw_row)
    risk_score, risk_level = calculate_risk(cleaned)

    cleaned["risk_score"] = risk_score
    cleaned["risk_level"] = risk_level

    for col, value in cleaned.items():
        print(f"{col}: {value} ({type(value).__name__})")
