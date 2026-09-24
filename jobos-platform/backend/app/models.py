from sqlalchemy import String, Text, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    company: Mapped[str] = mapped_column(String(300))
    location: Mapped[str] = mapped_column(String(300), default="")
    url: Mapped[str] = mapped_column(String(1000), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    salary: Mapped[str] = mapped_column(String(300), default="")
    sponsorship: Mapped[bool] = mapped_column(Boolean, default=False)
    relocation: Mapped[bool] = mapped_column(Boolean, default=False)
    match_score: Mapped[int] = mapped_column(Integer, default=0)

class CV(Base):
    __tablename__ = "cvs"
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(500))
    text: Mapped[str] = mapped_column(Text, default="")
    is_master: Mapped[bool] = mapped_column(Boolean, default=False)

class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int | None] = mapped_column(ForeignKey("jobs.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(300), default="")
    role: Mapped[str] = mapped_column(String(300), default="")
    company: Mapped[str] = mapped_column(String(300), default="")
    linkedin_url: Mapped[str] = mapped_column(String(1000), default="")
    email: Mapped[str] = mapped_column(String(500), default="")

class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    cv_id: Mapped[int | None] = mapped_column(ForeignKey("cvs.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    tailored_cv_text: Mapped[str] = mapped_column(Text, default="")
    cover_letter: Mapped[str] = mapped_column(Text, default="")
    email_body: Mapped[str] = mapped_column(Text, default="")
