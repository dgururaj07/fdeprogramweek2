from contextlib import contextmanager
from pathlib import Path

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# .env lives at the project root, three levels above this file
# (api/repository/repository.py -> api/repository -> api -> project root).
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")


def get_connection():
    # PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD come from the .env file
    # loaded above (or the shell environment if no .env is present).
    return psycopg2.connect()


@contextmanager
def get_cursor():
    # Yields a dict-cursor (rows come back as dicts, not tuples) wrapped in
    # a transaction: commits on success, rolls back if an exception
    # happens inside the "with" block. CRUD functions should use this
    # instead of opening their own connections.
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                yield cur
    finally:
        conn.close()


def get_all_encounters() -> list[dict]:
    # Returns every row in patient_encounters as a list of dicts, ordered
    # by encounter_id so the result is stable between calls.
    with get_cursor() as cur:
        cur.execute("SELECT * FROM patient_encounters ORDER BY encounter_id;")
        return cur.fetchall()


def get_care_queue() -> list[dict]:
    # Encounters that need follow-up: only MEDIUM and HIGH risk, highest
    # risk first (encounter_id breaks ties so the order is stable).
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT * FROM patient_encounters
            WHERE risk_level IN ('MEDIUM', 'HIGH')
            ORDER BY risk_score DESC, encounter_id;
            """
        )
        return cur.fetchall()


def get_care_queue_by_risk_level(risk_level: str) -> list[dict]:
    # Encounters for a single risk level, highest risk score first. The
    # level is a bound parameter (%s), never formatted into the SQL string.
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT * FROM patient_encounters
            WHERE risk_level = %s
            ORDER BY risk_score DESC, encounter_id;
            """,
            (risk_level,),
        )
        return cur.fetchall()


def update_intervention(encounter_id: int, fields: dict) -> dict | None:
    # Partial update of the intervention for one encounter. Only the keys in
    # `fields` are written; updated_at is refreshed on every update.
    # Returns the updated row, or None if no intervention exists for that
    # encounter. Column names are whitelisted (never taken from the client)
    # and values are bound parameters, so this is safe from SQL injection.
    allowed = {"status", "assigned_to", "notes"}
    columns = [c for c in fields if c in allowed]

    set_clause = sql.SQL(", ").join(
        sql.SQL("{} = %s").format(sql.Identifier(c)) for c in columns
    )
    query = sql.SQL(
        "UPDATE care_interventions SET {}, updated_at = NOW() "
        "WHERE encounter_id = %s RETURNING *;"
    ).format(set_clause)

    with get_cursor() as cur:
        cur.execute(query, [fields[c] for c in columns] + [encounter_id])
        return cur.fetchone()


def get_operations_summary() -> dict:
    # All four headline numbers in a single round trip. COUNT(*) FILTER
    # counts only the rows matching each condition, and pending_reviews is
    # a subquery on care_interventions (interventions still awaiting review).
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                COUNT(*)                                       AS total_encounters,
                COUNT(*) FILTER (WHERE risk_level = 'HIGH')    AS high_risk,
                COUNT(*) FILTER (WHERE risk_level = 'MEDIUM')  AS medium_risk,
                (SELECT COUNT(*) FROM care_interventions
                  WHERE status = 'PENDING_REVIEW')             AS pending_reviews
            FROM patient_encounters;
            """
        )
        return cur.fetchone()


def get_encounter_by_id(encounter_id: int) -> dict | None:
    # Returns one encounter as a dict, or None if no row has that id.
    # The id is passed as a bound parameter (%s), never string-formatted
    # into the SQL, which prevents SQL injection.
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM patient_encounters WHERE encounter_id = %s;",
            (encounter_id,),
        )
        return cur.fetchone()
