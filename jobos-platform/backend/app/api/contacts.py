from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Contact

router = APIRouter()

@router.get("/")
def list_contacts(db: Session = Depends(get_db)):
    return [
        {"id": x.id, "job_id": x.job_id, "name": x.name, "role": x.role,
         "company": x.company, "linkedin_url": x.linkedin_url, "email": x.email}
        for x in db.query(Contact).all()
    ]
