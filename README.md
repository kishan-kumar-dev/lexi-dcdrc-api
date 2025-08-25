```markdown
# Lexi DCDRC API (Take-Home Assignment)

This project is a **FastAPI backend** built for the Lexi Take-Home assignment.  
It queries **District Consumer Courts (DCDRC)** case data from the Jagriti portal.

> ⚠️ Currently, it can operate in **mock mode** for testing. Live integration with e-Jagriti endpoints is implemented.

---

## 🚀 Features

- REST API built with **FastAPI**
- Endpoints to search cases by:
  - Case number
  - Complainant
  - Respondent
  - Complainant Advocate
  - Respondent Advocate
  - Industry Type
  - Judge
- Additional endpoints:
  - `/states` → List all states with IDs
  - `/commissions/{state_id}` → List commissions for a given state
- Returns **mock or live case data** (configurable)
- Fully documented with **Swagger UI** (`/docs`)

---

## 🛠 Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Requests (for live data fetching)

---

## 📁 Project Structure
```

lexi-dcdrc-api/
│
├─ app/
│ ├─ main.py # FastAPI app and routes
│ ├─ models.py # Pydantic models for request/response
│ └─ services/
│ └─ jagriti_client.py # Fetches live data from Jagriti portal
│
├─ .venv/ # Python virtual environment
├─ requirements.txt
├─ run.bat # Windows script to run the app
└─ README.md

````

---

## 📦 Installation & Run Locally

Clone the repo:

```bash
git clone https://github.com/kishan-kumar-dev/lexi-dcdrc-api.git
cd lexi-dcdrc-api
````

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
# Activate venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn app.main:app --reload --port 8000
```

Open in browser:

👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Endpoints

### States

```
GET /states
```

### Commissions (by state)

```
GET /commissions/{state_id}
```

### Case Search

```
POST /cases/by-case-number
POST /cases/by-complainant
POST /cases/by-respondent
POST /cases/by-complainant-advocate
POST /cases/by-respondent-advocate
POST /cases/by-industry-type
POST /cases/by-judge
```

### Example Request

```bash
curl -X POST "http://localhost:8000/cases/by-complainant-advocate" \
-H "Content-Type: application/json" \
-d '{"state": "KARNATAKA", "commission": "Bangalore 1st & Rural Additional", "search_value": "Reddy"}'
```

### Example Response

```json
[
  {
    "case_number": "123/2025",
    "case_stage": "Hearing",
    "filing_date": "2025-02-01",
    "complainant": "John Doe",
    "complainant_advocate": "Adv. Reddy",
    "respondent": "XYZ Ltd.",
    "respondent_advocate": "Adv. Mehta",
    "document_link": "https://e-jagriti.gov.in/.../case123"
  }
]
```

---

## ⚙️ Notes

- Switch between **mock data** and **live Jagriti data** by configuring `app/services/jagriti_client.py`.
- Live data integration requires the e-Jagriti endpoints to be accessible.
- `/docs` shows interactive Swagger API documentation.

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Description"`
4. Push to branch: `git push origin feature-name`
5. Open a Pull Request

---

## 📜 License

MIT License

```