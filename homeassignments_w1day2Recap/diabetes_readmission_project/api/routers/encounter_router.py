from fastapi import APIRouter, HTTPException

from api.services import service

# All routes in this file are served under /encounters.
router = APIRouter(prefix="/encounters", tags=["encounters"])


@router.get("")
def get_all_encounters():
    # The router only handles HTTP; it delegates to the service layer,
    # which in turn calls the repository. FastAPI converts the Decimal and
    # datetime values in each row to JSON automatically.
    return service.get_all_encounters()


@router.get("/{encounter_id}")
def get_encounter(encounter_id: int):
    # FastAPI validates that encounter_id is an integer (422 otherwise).
    encounter = service.get_encounter_by_id(encounter_id)

    # No matching row -> 404 instead of returning null with a 200.
    if encounter is None:
        raise HTTPException(
            status_code=404, detail=f"Encounter {encounter_id} not found"
        )
    return encounter
