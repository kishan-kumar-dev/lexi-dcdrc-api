from fastapi import APIRouter
from app.services.jagriti_client import get_states

router = APIRouter()

@router.get("/states")
async def states():
    return get_states()
