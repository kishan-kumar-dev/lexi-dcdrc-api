# main.py — Simple one-file FastAPI app for Lexi take-home
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime as dt

app = FastAPI(title="Lexi DCDRC Search API — Simple One-File")

# ----------------- Mock data so it runs instantly -----------------
STATES = [
    {"id": "KA", "name": "KARNATAKA"},
    {"id": "MH", "name": "MAHARASHTRA"},
]

COMMISSIONS = [
    {"id": "KA_BLR_001", "name": "Bangalore 1st & Rural Additional", "state_id": "KA"},
    {"id": "KA_BLR_002", "name": "Bangalore Urban", "state_id": "KA"},
]

CASES = [
    {
        "case_number": "987/2024",
        "case_stage": "Orders",
        "filing_date": "2024-11-18",
        "complainant": "Jane Roe",
        "complainant_advocate": "Adv. Sharma",
        "respondent": "Acme Pvt Ltd",
        "respondent_advocate": "Adv. Patel",
        "document_link": "https://e-jagriti.gov.in/mock/case987",
    },
    {
        "case_number": "123/2025",
        "case_stage": "Hearing",
        "filing_date": "2025-02-01",
        "complainant": "John Doe",
        "complainant_advocate": "Adv. Reddy",
        "respondent": "XYZ Ltd.",
        "respondent_advocate": "Adv. Mehta",
        "document_link": "https://e-jagriti.gov.in/mock/case123",
    },
]

# ----------------- Models -----------------
class State(BaseModel):
    id: str
    name: str

class Commission(BaseModel):
    id: str
    name: str
    state_id: str

class CaseResult(BaseModel):
    case_number: str
    case_stage: Optional[str] = None
    filing_date: Optional[str] = None  # YYYY-MM-DD
    complainant: Optional[str] = None
    complainant_advocate: Optional[str] = None
    respondent: Optional[str] = None
    respondent_advocate: Optional[str] = None
    document_link: Optional[str] = None

class SearchRequest(BaseModel):
    state: str = Field(..., description="State name text, e.g., 'KARNATAKA'")
    commission: str = Field(..., description="Commission name text, e.g., 'Bangalore 1st & Rural Additional'")
    value: str = Field(..., description="Search value string, e.g., 'Reddy'")

# ----------------- Helpers -----------------
def resolve_state_id(state_text: str) -> str:
    for s in STATES:
        if s["name"].lower() == state_text.lower():
            return s["id"]
    raise HTTPException(status_code=400, detail="Unknown state")

def resolve_commission_id(state_id: str, commission_text: str) -> str:
    for c in COMMISSIONS:
        if c["state_id"] == state_id and c["name"].lower() == commission_text.lower():
            return c["id"]
    raise HTTPException(status_code=400, detail="Unknown commission for state")

def _is_daily_order(case: dict) -> bool:
    # Demo rule: treat stages starting with "Orders" as Daily Orders
    return (case.get("case_stage") or "").lower().startswith("orders")

def _sort_by_filing_date_desc(items: List[dict]) -> List[dict]:
    def to_date(s):
        try:
            return dt.datetime.strptime(s or "1900-01-01", "%Y-%m-%d")
        except Exception:
            return dt.datetime(1900, 1, 1)
    return sorted(items, key=lambda x: to_date(x.get("filing_date")), reverse=True)

def search_cases(kind: str, req: SearchRequest) -> List[CaseResult]:
    # Validate state/commission (shows how mapping works)
    state_id = resolve_state_id(req.state)
    _ = resolve_commission_id(state_id, req.commission)

    v = req.value.lower()
    def match(c: dict) -> bool:
        if kind == "by-case-number":
            return v in c.get("case_number", "").lower()
        if kind == "by-complainant":
            return v in (c.get("complainant") or "").lower()
        if kind == "by-respondent":
            return v in (c.get("respondent") or "").lower()
        if kind == "by-complainant-advocate":
            return v in (c.get("complainant_advocate") or "").lower()
        if kind == "by-respondent-advocate":
            return v in (c.get("respondent_advocate") or "").lower()
        if kind == "by-industry-type":
            return False  # not in mock
        if kind == "by-judge":
            return False  # not in mock
        return False

    results = [c for c in CASES if match(c)]
    daily_only = [c for c in results if _is_daily_order(c)]
    results = daily_only or results          # prefer daily orders
    results = _sort_by_filing_date_desc(results)  # default date: filing_date (desc)
    return [CaseResult(**r) for r in results]

# ----------------- Endpoints -----------------
from typing import List as _List  # avoid shadowing

@app.get("/states", response_model=_List[State])
async def states():
    return [State(**s) for s in STATES]

@app.get("/commissions/{state_id}", response_model=_List[Commission])
async def commissions(state_id: str):
    return [Commission(**c) for c in COMMISSIONS if c["state_id"] == state_id]

@app.post("/cases/by-case-number", response_model=_List[CaseResult])
async def by_case_number(req: SearchRequest):
    return search_cases("by-case-number", req)

@app.post("/cases/by-complainant", response_model=_List[CaseResult])
async def by_complainant(req: SearchRequest):
    return search_cases("by-complainant", req)

@app.post("/cases/by-respondent", response_model=_List[CaseResult])
async def by_respondent(req: SearchRequest):
    return search_cases("by-respondent", req)

@app.post("/cases/by-complainant-advocate", response_model=_List[CaseResult])
async def by_complainant_adv(req: SearchRequest):
    return search_cases("by-complainant-advocate", req)

@app.post("/cases/by-respondent-advocate", response_model=_List[CaseResult])
async def by_respondent_adv(req: SearchRequest):
    return search_cases("by-respondent-advocate", req)

@app.post("/cases/by-industry-type", response_model=_List[CaseResult])
async def by_industry(req: SearchRequest):
    return search_cases("by-industry-type", req)

@app.post("/cases/by-judge", response_model=_List[CaseResult])
async def by_judge(req: SearchRequest):
    return search_cases("by-judge", req)
