from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Job
from ..schemas import JobCreate, JobOut
from ..services.matcher import score_job

router = APIRouter()

@router.post("/", response_model=JobOut)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = Job(**payload.model_dump())
    job.match_score = score_job(job.title, job.location, job.description)
    db.add(job); db.commit(); db.refresh(job)
    return job

@router.get("/", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).order_by(Job.match_score.desc()).all()

@router.post("/seed")
def seed(db: Session = Depends(get_db)):
    samples = [
        JobCreate(title="AI Creative Technologist", company="Demo AI Studio", location="Lisbon, Portugal",
                  description="AI, 3D, Unity, creative technology, interactive experiences", relocation=True, sponsorship=True),
        JobCreate(title="3D/XR Designer", company="Demo XR Lab", location="Nice, France",
                  description="3D design, Blender, Unity, immersive experiences", relocation=True),
    ]
    created=[]
    for p in samples:
        job=Job(**p.model_dump())
        job.match_score=score_job(job.title, job.location, job.description)
        db.add(job); created.append(job)
    db.commit()
    return {"created": len(created)}
