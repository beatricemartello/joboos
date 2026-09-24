from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CV
from ..services.cv import extract_text
from pathlib import Path
import uuid

router = APIRouter()

UPLOAD_DIR = Path("/data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_cv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    path = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
    path.write_bytes(await file.read())
    text = extract_text(str(path))
    cv = CV(filename=file.filename, text=text, is_master=True)
    db.query(CV).update({CV.is_master: False})
    db.add(cv); db.commit(); db.refresh(cv)
    return {"id": cv.id, "filename": cv.filename, "characters": len(text)}

@router.get("/")
def list_cvs(db: Session = Depends(get_db)):
    return [{"id": x.id, "filename": x.filename, "is_master": x.is_master} for x in db.query(CV).all()]
