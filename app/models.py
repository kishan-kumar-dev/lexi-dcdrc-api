from pydantic import BaseModel
from typing import Optional

class State(BaseModel):
    id: str
    name: str

class Commission(BaseModel):
    id: str
    name: str
    state_id: str

class CaseResult(BaseModel):
    case_number: str
    case_stage: str
    filing_date: str
    complainant: Optional[str] = None
    complainant_advocate: Optional[str] = None
    respondent: Optional[str] = None
    respondent_advocate: Optional[str] = None
    document_link: Optional[str] = None
