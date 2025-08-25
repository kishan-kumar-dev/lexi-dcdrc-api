from fastapi import FastAPI, HTTPException, Path
from typing import List
from app.models import State, Commission, CaseResult
from app.services import jagriti_client as service

app = FastAPI(title="Lexi DCDRC API", version="1.0")

# ------------------------------
# States & Commissions
# ------------------------------
@app.get("/states", response_model=List[State])
def get_states():
    return service.get_states()

@app.get("/commissions/{state_id}", response_model=List[Commission])
def get_commissions(state_id: str = Path(..., description="State ID")):
    return service.get_commissions(state_id)

# ------------------------------
# Cases
# ------------------------------
@app.post("/cases/{kind}", response_model=List[CaseResult])
def search_cases(
    kind: str = Path(..., description="Search kind"),
    payload: dict = {}
):
    state = payload.get("state")
    commission = payload.get("commission")
    value = payload.get("search_value")

    if not state or not commission or not value:
        raise HTTPException(status_code=400, detail="state, commission, and search_value are required")
    
    return service.search_cases(kind, state, commission, value)
