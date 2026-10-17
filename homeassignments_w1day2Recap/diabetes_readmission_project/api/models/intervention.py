from typing import Literal

from pydantic import BaseModel


class InterventionUpdate(BaseModel):
    # Request body for PATCH /interventions/{encounter_id}. Every field is
    # optional because PATCH is a partial update: only the fields the
    # client actually sends get changed.

    # Must match the CHECK constraint on care_interventions.status, so a bad
    # value is rejected with a 422 before it ever reaches the database.
    status: Literal[
        "PENDING_REVIEW",
        "ASSIGNED",
        "CONTACTED",
        "FOLLOW_UP_SCHEDULED",
        "CLOSED",
    ] | None = None
    assigned_to: str | None = None
    notes: str | None = None
