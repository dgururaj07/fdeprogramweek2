from fastapi import APIRouter

from api.services import service

# Served under /operations.
router = APIRouter(prefix="/operations", tags=["operations"])


@router.get("/summary")
def get_operations_summary():
    # Answers: how many encounters, how many HIGH, how many MEDIUM, and
    # how many interventions are still pending review.
    return service.get_operations_summary()
