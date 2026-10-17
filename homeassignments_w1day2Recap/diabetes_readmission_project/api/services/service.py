from api.repository import repository


def get_all_encounters() -> list[dict]:
    # Service layer sits between the API and the repository: it calls the
    # repository for raw data so the API never touches database code
    # directly. Any business rules (filtering, formatting) go here.
    return repository.get_all_encounters()


def get_care_queue() -> list[dict]:
    # The care queue is the set of MEDIUM/HIGH risk encounters; the filter
    # itself lives in the repository query.
    return repository.get_care_queue()


# Risk levels that belong in the care queue. LOW is deliberately excluded:
# those patients don't need follow-up.
CARE_QUEUE_LEVELS = {"MEDIUM", "HIGH"}


def get_care_queue_by_risk_level(risk_level: str) -> list[dict]:
    # Normalize so "high", "High" and "HIGH" all work (the DB stores uppercase).
    level = risk_level.upper()

    # Business rule: only MEDIUM/HIGH are allowed. The router turns this
    # ValueError into an HTTP error, keeping HTTP concerns out of here.
    if level not in CARE_QUEUE_LEVELS:
        raise ValueError(
            f"Invalid risk level '{risk_level}'. Allowed: MEDIUM, HIGH"
        )
    return repository.get_care_queue_by_risk_level(level)


def update_intervention(encounter_id: int, fields: dict) -> dict | None:
    # `fields` holds only what the client sent (partial update).
    # Business rules: there must be something to update, and status can't
    # be cleared because the column is NOT NULL. The router turns the
    # ValueError into an HTTP error.
    if not fields:
        raise ValueError("Provide at least one of: status, assigned_to, notes")
    if "status" in fields and fields["status"] is None:
        raise ValueError("status cannot be null")

    # Returns None when the encounter has no intervention row (-> 404).
    return repository.update_intervention(encounter_id, fields)


def get_operations_summary() -> dict:
    # Plain dict so it serializes cleanly to JSON; any extra reporting
    # logic (percentages, trends) would be added here later.
    return dict(repository.get_operations_summary())


def get_encounter_by_id(encounter_id: int) -> dict | None:
    # Returns None when the encounter doesn't exist; the router decides
    # how to report that over HTTP (404), keeping HTTP concerns out of here.
    return repository.get_encounter_by_id(encounter_id)
