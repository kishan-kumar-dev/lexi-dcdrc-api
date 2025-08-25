
@echo off
REM Activate the virtual environment
call .\.venv\Scripts\activate

REM Run the FastAPI server
uvicorn app.main:app --reload
