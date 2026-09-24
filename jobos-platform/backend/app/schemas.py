from pydantic import BaseModel, ConfigDict

class JobCreate(BaseModel):
    title: str
    company: str
    location: str = ""
    url: str = ""
    description: str = ""
    salary: str = ""
    sponsorship: bool = False
    relocation: bool = False

class JobOut(JobCreate):
    id: int
    match_score: int
    model_config = ConfigDict(from_attributes=True)

class ApplicationCreate(BaseModel):
    job_id: int
    cv_id: int | None = None

class ApplicationOut(BaseModel):
    id: int
    job_id: int
    cv_id: int | None
    status: str
    tailored_cv_text: str
    cover_letter: str
    email_body: str
    model_config = ConfigDict(from_attributes=True)
