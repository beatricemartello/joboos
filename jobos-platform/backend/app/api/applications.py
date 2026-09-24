from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Application, Job, CV
from ..schemas import ApplicationCreate, ApplicationOut
from ..services.ai import build_tailored_package

router = APIRouter()

@router.post("/prepare", response_model=ApplicationOut)
def prepare(payload: ApplicationCreate, db: Session = Depends(get_db)):
    job = db.get(Job, payload.job_id)
    if not job: raise HTTPException(404, "Job not found")
    cv = db.get(CV, payload.cv_id) if payload.cv_id else db.query(CV).filter(CV.is_master == True).first()
    cv_text = cv.text if cv else ""
    tailored, cover, email = build_tailored_package(cv_text, job.title, job.company, job.description)
    app = Application(job_id=job.id, cv_id=cv.id if cv else None,
                      status="ready_for_approval", tailored_cv_text=tailored,
                      cover_letter=cover, email_body=email)
    db.add(app); db.commit(); db.refresh(app)
    return app

@router.get("/", response_model=list[ApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.id.desc()).all()

@router.post("/{application_id}/approve", response_model=ApplicationOut)
def approve(application_id: int, db: Session = Depends(get_db)):
    app=db.get(Application, application_id)
    if not app: raise HTTPException(404, "Application not found")
    app.status="approved"
    db.commit(); db.refresh(app)
    return app
