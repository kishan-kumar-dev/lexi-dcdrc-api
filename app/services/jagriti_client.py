import requests
from typing import List
from fastapi import HTTPException
from app.models import State, Commission, CaseResult

BASE_URL = "https://lexi-dcdrc-api.onrender.com"

# ------------------------------
# Mock Data (Fallback)
# ------------------------------
MOCK_STATES = [
    State(id="KA", name="KARNATAKA"),
    State(id="MH", name="MAHARASHTRA")
]

MOCK_COMMISSIONS = [
    Commission(id="KA_BLR_001", name="Bangalore 1st & Rural Additional", state_id="KA"),
    Commission(id="KA_BLR_002", name="Bangalore Urban", state_id="KA")
]

MOCK_CASES = [
    CaseResult(
        case_number="123/2025",
        case_stage="Hearing",
        filing_date="2025-02-01",
        complainant="John Doe",
        complainant_advocate="Adv. Reddy",
        respondent="XYZ Ltd.",
        respondent_advocate="Adv. Mehta",
        document_link="https://e-jagriti.gov.in/mock/case123"
    ),
    CaseResult(
        case_number="987/2024",
        case_stage="Orders",
        filing_date="2024-11-18",
        complainant="Jane Roe",
        complainant_advocate="Adv. Sharma",
        respondent="Acme Pvt Ltd",
        respondent_advocate="Adv. Patel",
        document_link="https://e-jagriti.gov.in/mock/case987"
    )
]

# ------------------------------
# API Fetch with Fallback
# ------------------------------
def get_states() -> List[State]:
    try:
        resp = requests.get(f"{BASE_URL}/states", timeout=5)
        resp.raise_for_status()
        return [State(**s) for s in resp.json()]
    except Exception:
        return MOCK_STATES

def get_commissions(state_id: str) -> List[Commission]:
    try:
        resp = requests.get(f"{BASE_URL}/commissions/{state_id}", timeout=5)
        resp.raise_for_status()
        return [Commission(**c) for c in resp.json()]
    except Exception:
        return [c for c in MOCK_COMMISSIONS if c.state_id == state_id]

def search_cases(kind: str, state: str, commission: str, value: str) -> List[CaseResult]:
    if kind not in [
        "by-case-number",
        "by-complainant",
        "by-respondent",
        "by-complainant-advocate",
        "by-respondent-advocate",
        "by-industry-type",
        "by-judge"
    ]:
        raise HTTPException(status_code=400, detail="Invalid search kind")

    payload = {
        "state": state,
        "commission": commission,
        "search_value": value
    }

    try:
        resp = requests.post(f"{BASE_URL}/cases/{kind}", json=payload, timeout=5)
        resp.raise_for_status()
        return [CaseResult(**c) for c in resp.json()]
    except Exception:
        # Fallback to mock search
        v = value.lower()
        results = []
        for c in MOCK_CASES:
            if kind == "by-case-number" and v in c.case_number.lower():
                results.append(c)
            elif kind == "by-complainant" and c.complainant and v in c.complainant.lower():
                results.append(c)
            elif kind == "by-respondent" and c.respondent and v in c.respondent.lower():
                results.append(c)
            elif kind == "by-complainant-advocate" and c.complainant_advocate and v in c.complainant_advocate.lower():
                results.append(c)
            elif kind == "by-respondent-advocate" and c.respondent_advocate and v in c.respondent_advocate.lower():
                results.append(c)
        return results
