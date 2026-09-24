from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .api import jobs, applications, cvs, contacts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JOBOS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])
app.include_router(cvs.router, prefix="/api/cvs", tags=["cvs"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["contacts"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "jobos"}
