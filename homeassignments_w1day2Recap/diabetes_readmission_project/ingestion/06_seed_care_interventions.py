from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# This script lives in ingestion/, so the project root is one level up.
# Resolving from __file__ makes the path work from any working directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD from the project-root .env
# into the process environment, same as the other ingestion scripts.
load_dotenv(PROJECT_ROOT / ".env")

# One-time seed: create one care_interventions row for every MEDIUM/HIGH
# risk encounter (the care queue). Only encounter_id is supplied - the
# table fills in the rest itself:
#   intervention_id -> auto-increment, status -> 'PENDING_REVIEW',
#   assigned_to/notes -> NULL, created_at/updated_at -> NOW().
# ORDER BY risk_score DESC gives the highest-risk encounters the lowest ids.
# ON CONFLICT (encounter_id) DO NOTHING makes the script safe to re-run:
# encounters that already have an intervention are skipped, not duplicated.
SEED_SQL = """
    INSERT INTO care_interventions (encounter_id)
    SELECT encounter_id
    FROM patient_encounters
    WHERE risk_level IN ('MEDIUM', 'HIGH')
    ORDER BY risk_score DESC, encounter_id
    ON CONFLICT (encounter_id) DO NOTHING;
"""

COUNT_SQL = "SELECT COUNT(*) FROM care_interventions;"

# How many encounters qualify for the care queue, used to report how many
# were skipped because they already had an intervention.
ELIGIBLE_SQL = """
    SELECT COUNT(*) FROM patient_encounters
    WHERE risk_level IN ('MEDIUM', 'HIGH');
"""

BREAKDOWN_SQL = """
    SELECT pe.risk_level, COUNT(*)
    FROM care_interventions ci
    JOIN patient_encounters pe ON pe.encounter_id = ci.encounter_id
    GROUP BY pe.risk_level
    ORDER BY pe.risk_level;
"""


if __name__ == "__main__":
    conn = psycopg2.connect()
    try:
        # "with conn" wraps everything in one transaction: it commits on
        # success and rolls back if anything fails, so the seed is all-or-nothing.
        with conn, conn.cursor() as cur:
            cur.execute(ELIGIBLE_SQL)
            eligible = cur.fetchone()[0]

            cur.execute(COUNT_SQL)
            before = cur.fetchone()[0]

            cur.execute(SEED_SQL)
            inserted = cur.rowcount

            cur.execute(COUNT_SQL)
            after = cur.fetchone()[0]

            cur.execute(BREAKDOWN_SQL)
            breakdown = cur.fetchall()

        print(f"care_interventions rows before: {before}")
        print(f"Eligible (MEDIUM/HIGH) encounters: {eligible}")
        print(f"Inserted: {inserted}, skipped (already present): "
              f"{eligible - inserted}")
        print(f"care_interventions rows after:  {after}")
        for level, count in breakdown:
            print(f"  {level}: {count}")
    finally:
        conn.close()
