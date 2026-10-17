import csv
import importlib.util
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

# This script lives in ingestion/, so the project root is one level up.
# Resolving from __file__ makes the paths work from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD from the project-root .env
# into the process environment, same as 04_insert_first_row.py.
load_dotenv(PROJECT_ROOT / ".env")

CSV_PATH = PROJECT_ROOT / "data" / "diabetic_data.csv"
BATCH_SIZE = 1000


def load_sibling_module(filename: str):
    # Filenames like 02_clean_row.py / 03_calculate_risk.py start with a
    # digit, so they can't be imported with a normal "import" statement -
    # load them directly from their file path instead.
    spec = importlib.util.spec_from_file_location(
        filename.removesuffix(".py"), Path(__file__).parent / filename
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


clean_row_module = load_sibling_module("02_clean_row.py")
calculate_risk_module = load_sibling_module("03_calculate_risk.py")

# Column order must match the %s placeholders below.
COLUMNS = (
    "encounter_id", "patient_nbr", "age", "time_in_hospital",
    "number_inpatient", "number_emergency", "number_outpatient",
    "num_medications", "readmitted", "risk_score", "risk_level",
)

INSERT_SQL = f"""
    INSERT INTO patient_encounters ({", ".join(COLUMNS)})
    VALUES %s
    ON CONFLICT (encounter_id) DO NOTHING;
"""


def row_to_values(row: dict) -> tuple:
    # Clean/type-cast the row, then compute risk_score and risk_level -
    # neither column exists in the source CSV, they're derived values.
    cleaned = clean_row_module.clean_row(row)
    risk_score, risk_level = calculate_risk_module.calculate_risk(cleaned)
    cleaned["risk_score"] = risk_score
    cleaned["risk_level"] = risk_level
    return tuple(cleaned[col] for col in COLUMNS)


if __name__ == "__main__":
    conn = psycopg2.connect()
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            total_inserted = 0
            batch = []

            with conn, conn.cursor() as cur:
                for raw_row in reader:
                    batch.append(row_to_values(raw_row))

                    # Flush once the batch is full, instead of inserting
                    # one row at a time - much faster for 100k+ rows.
                    if len(batch) >= BATCH_SIZE:
                        execute_values(cur, INSERT_SQL, batch)
                        total_inserted += len(batch)
                        batch.clear()
                        print(f"Inserted {total_inserted} rows so far...")

                # Flush any remaining rows smaller than one full batch.
                if batch:
                    execute_values(cur, INSERT_SQL, batch)
                    total_inserted += len(batch)

            print(f"Done. Processed {total_inserted} rows "
                  f"(duplicates skipped via ON CONFLICT DO NOTHING).")
    finally:
        conn.close()
