from fastapi import APIRouter, Query, HTTPException
from app.services.jagriti_client import search_cases

router = APIRouter()

@router.get("/")
async def cases(
    kind: str = Query(..., description="Search kind: by-case-number/by-complainant/..."),
    state: str = Query(..., description="State name"),
    commission: str = Query(..., description="Commission name"),
    value: str = Query(..., description="Search value")
):
    results = search_cases(kind, state, commission, value)
    if not results:
        raise HTTPException(404, detail="No matching cases found")
    return results
