# JOBOS — AI Career Agent Platform

Modular, approval-first AI career operating system.

### Current platform
- Next.js dashboard
- FastAPI backend
- SQLite by default / PostgreSQL-ready
- CV master upload and PDF/DOCX parsing
- Job matching
- Tailored application package
- Contact/recruiter records
- Application pipeline
- Configurable target roles, countries, salary, sponsorship and relocation
- Explicit approval gate before outbound actions

### Run
Backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000
API docs: http://localhost:8000/docs

The provider integrations are intentionally separated so real job sources, an LLM, Gmail and permitted social workflows can be connected later without rewriting the core application.

JOBOS must not be used for spam or actions that violate platform terms. Outbound applications/messages remain approval-first.
