# Diabetes Readmission Project

Loads hospital encounter data from the diabetic readmission CSV into PostgreSQL, scores each encounter for readmission risk, and exposes a FastAPI service for a care team to review high-risk patients and track follow-up.

**Flow:** CSV -> clean + risk score -> PostgreSQL -> Care Queue API -> human action (PATCH) -> PostgreSQL update

## Project structure

```
diabetes_readmission_project/
├── data/diabetic_data.csv         # source data (101,766 rows)
├── schema/
│   ├── patient_encounters.sql     # encounters table
│   └── care_interventions.sql     # follow-up tracking table
├── ingestion/                     # scripts that load the data (run in order)
├── api/
│   ├── main.py                    # FastAPI app entry point
│   ├── routers/                   # HTTP layer (one router per area)
│   ├── services/service.py        # business rules
│   ├── repository/repository.py   # all SQL / database access
│   └── models/intervention.py     # request body model for PATCH
├── .env.example                   # template for database settings
└── .gitignore
```

The API is layered: **router -> service -> repository**. Routers only handle HTTP, services hold rules, and only the repository talks to the database.

## Setup

1. **Install dependencies** (Python 3.10+):
   ```
   pip install fastapi uvicorn psycopg2-binary python-dotenv
   ```
2. **Configure the database.** Copy `.env.example` to `.env` and fill in your values. `.env` is gitignored, so never put real credentials in `.env.example`.
   ```
   PGHOST=localhost
   PGPORT=5432
   PGDATABASE=your_database
   PGUSER=your_user
   PGPASSWORD=your_password
   ```
3. **Create the tables** by running both files in `schema/` against your database (`patient_encounters.sql` first, because `care_interventions` references it).
4. **Grant access** to the app user. As a superuser, give it `SELECT, INSERT` on `patient_encounters`, and `SELECT, INSERT, UPDATE` on `care_interventions` plus `USAGE` on the sequence `care_interventions_intervention_id_seq`.

## Ingestion

Scripts in `ingestion/` can be run from any directory, for example `python ingestion/05_import_all_rows.py`. They read `.env` and the CSV relative to the project root.

| Script | What it does |
|---|---|
| `01_readonefromsql.py` | Reads the first CSV row (9 columns of interest) and prints each value with its type. Everything comes back as `str`. |
| `02_clean_row.py` | `clean_row()` casts the numeric columns to `int` (bad values fall back to `0`); `age` and `readmitted` stay strings. |
| `03_calculate_risk.py` | `calculate_risk()` returns `(risk_score, risk_level)` for a cleaned row. |
| `04_insert_first_row.py` | Cleans, scores and inserts only the first row. A good connection test. |
| `05_import_all_rows.py` | **Main load.** Imports all 101,766 rows in batches of 1,000. Safe to re-run (`ON CONFLICT DO NOTHING`). |
| `06_seed_care_interventions.py` | **One-time seed.** Creates a `PENDING_REVIEW` intervention for every MEDIUM/HIGH encounter (8,538 rows). Safe to re-run. |

Run `05` before `06`.

### Columns loaded

`encounter_id`, `patient_nbr`, `age`, `time_in_hospital`, `number_inpatient`, `number_emergency`, `number_outpatient`, `num_medications`, `readmitted`, plus the calculated `risk_score` and `risk_level`.

### Risk scoring

| Condition | Points |
|---|---|
| `number_inpatient >= 3` | +3 |
| `number_emergency >= 2` | +2 |
| `number_outpatient >= 3` | +1 |
| `time_in_hospital >= 7` | +1 |
| `num_medications >= 20` | +1 |

| Score | Risk level |
|---|---|
| 0-2 | LOW |
| 3-4 | MEDIUM |
| 5+ | HIGH |

Result on the full dataset: LOW 93,228, MEDIUM 6,180, HIGH 2,358.

## Running the API

Run from the **project root** (not from inside `api/`), so the `api.*` imports resolve:

```
uvicorn api.main:app --reload
```

Interactive docs (Swagger) are at `http://127.0.0.1:8000/docs`.

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/encounters` | All encounters (about 28 MB of JSON, so expect it to be slow) |
| GET | `/encounters/{encounter_id}` | One encounter. 404 if not found, 422 if the id isn't an integer |
| GET | `/care-queue` | MEDIUM and HIGH risk encounters, highest risk score first |
| GET | `/care-queue/{risk_level}` | One level only: `medium` or `high` (case-insensitive). `low` or anything else returns 422 |
| PATCH | `/interventions/{encounter_id}` | Partially update an intervention. 404 if the encounter has no intervention |
| GET | `/operations/summary` | Headline counts: total encounters, HIGH, MEDIUM, pending reviews |

### PATCH /interventions/{encounter_id}

All fields are optional, and only the fields you send are changed. `updated_at` is refreshed on every update.

```json
{
  "status": "CONTACTED",
  "assigned_to": "Care Team A",
  "notes": "Follow-up initiated"
}
```

`status` must be one of `PENDING_REVIEW`, `ASSIGNED`, `CONTACTED`, `FOLLOW_UP_SCHEDULED`, `CLOSED`. Sending an empty body or `"status": null` returns 422. Send `"notes": null` to clear the notes.

### GET /operations/summary

```json
{"total_encounters": 101766, "high_risk": 2358, "medium_risk": 6180, "pending_reviews": 8538}
```

`pending_reviews` counts interventions whose status is still `PENDING_REVIEW`, so it drops as items are worked through the PATCH endpoint.

## Database tables

**`patient_encounters`**: one row per encounter. `encounter_id` is the primary key; `risk_level` is constrained to `LOW`, `MEDIUM` or `HIGH`; `created_at` defaults to now.

**`care_interventions`**: one row per encounter (`encounter_id` is `UNIQUE` and a foreign key to `patient_encounters`, with `ON DELETE CASCADE`). `intervention_id` auto-increments, and `status` defaults to `PENDING_REVIEW` and is restricted to the five values above.

## Notes

- `GET /encounters` returns every row at once. Add paging before using it with a real client.
- The `.venv` folder lives one level above this project, in `fde-week2-recap/`.
- There is no `POST /interventions` yet: intervention rows are created only by the seed script (`06`).
