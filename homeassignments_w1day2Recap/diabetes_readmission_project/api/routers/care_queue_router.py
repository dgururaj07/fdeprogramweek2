from fastapi import APIRouter, HTTPException

from api.services import service

# Served under /care-queue.
router = APIRouter(prefix="/care-queue", tags=["care-queue"])


@router.get("")
def get_care_queue():
    # Returns only MEDIUM and HIGH risk encounters, highest risk first.
    # Like the other routers, this delegates to the service layer.
    return service.get_care_queue()


@router.get("/{risk_level}")
def get_care_queue_by_risk_level(risk_level: str):
    # Only medium / high are valid (case-insensitive); low is excluded.
    try:
        return service.get_care_queue_by_risk_level(risk_level)
    except ValueError as e:
        # 422 = the request was well-formed but the value isn't acceptable.
        raise HTTPException(status_code=422, detail=str(e))
