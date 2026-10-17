from fastapi import FastAPI

from api.routers.care_queue_router import router as care_queue_router
from api.routers.encounter_router import router as encounter_router
from api.routers.intervention_router import router as intervention_router
from api.routers.operations_router import router as operations_router

# Entry point of the API. Run from the project root (not from inside api/)
# so the "api.*" imports resolve:
#   uvicorn api.main:app --reload
app = FastAPI(title="Diabetes Readmission API")

# Register the encounter routes (GET /encounters, GET /encounters/{id}) on the app.
app.include_router(encounter_router)

# Register GET /care-queue (MEDIUM/HIGH risk encounters only).
app.include_router(care_queue_router)

# Register PATCH /interventions/{encounter_id} (update an intervention).
app.include_router(intervention_router)

# Register GET /operations/summary (headline counts for reporting).
app.include_router(operations_router)
