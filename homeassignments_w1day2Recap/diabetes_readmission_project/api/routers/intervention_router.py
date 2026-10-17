from fastapi import APIRouter, HTTPException

from api.models.intervention import InterventionUpdate
from api.services import service

# Served under /interventions.
router = APIRouter(prefix="/interventions", tags=["interventions"])


@router.patch("/{encounter_id}")
def update_intervention(encounter_id: int, body: InterventionUpdate):
    # exclude_unset keeps only the fields the client actually sent, so
    # PATCH changes just those and leaves the rest untouched.
    fields = body.model_dump(exclude_unset=True)

    try:
        intervention = service.update_intervention(encounter_id, fields)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # No intervention row for this encounter -> 404 (we only update, never create).
    if intervention is None:
        raise HTTPException(
            status_code=404,
            detail=f"No intervention found for encounter {encounter_id}",
        )
    return intervention
