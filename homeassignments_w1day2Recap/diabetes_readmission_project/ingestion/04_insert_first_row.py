import csv
import importlib.util
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# This script lives in ingestion/, so the project root is one level up.
# Resolving from __file__ makes the paths work from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD from the .env file at the
# project root (if present) into the process environment. Falls back to
# whatever's already set in the shell if no .env file exists.
load_dotenv(PROJECT_ROOT / ".env")

CSV_PATH = PROJECT_ROOT / "data" / "diabetic_data.csv"


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

INSERT_SQL = """
    INSERT INTO patient_encounters (
        encounter_id, patient_nbr, age, time_in_hospital,
        number_inpatient, number_emergency, number_outpatient,
        num_medications, readmitted, risk_score, risk_level
    )
    VALUES (
        %(encounter_id)s, %(patient_nbr)s, %(age)s, %(time_in_hospital)s,
        %(number_inpatient)s, %(number_emergency)s, %(number_outpatient)s,
        %(num_medications)s, %(readmitted)s, %(risk_score)s, %(risk_level)s
    )
    ON CONFLICT (encounter_id) DO NOTHING;
"""


if __name__ == "__main__":
    # DictReader consumes the header row automatically, so next() gives the
    # first data row.
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        raw_row = next(reader)

    # Clean/type-cast the row, then compute risk_score and risk_level -
    # neither column exists in the source CSV, they're derived values.
    cleaned = clean_row_module.clean_row(raw_row)
    risk_score, risk_level = calculate_risk_module.calculate_risk(cleaned)
    cleaned["risk_score"] = risk_score
    cleaned["risk_level"] = risk_level

    # Connection params come from standard libpq env vars
    # (PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD) - psycopg2 picks
    # these up automatically when connect() is called with no arguments.
    conn = psycopg2.connect()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(INSERT_SQL, cleaned)
        print(f"Inserted encounter_id={cleaned['encounter_id']} "
              f"(risk_score={risk_score}, risk_level={risk_level})")
    finally:
        conn.close()
