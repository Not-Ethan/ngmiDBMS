from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class User:
    user_id: Optional[int]
    email: str
    full_name: str
    password_hash: str
    created_at: Optional[datetime] = None

@dataclass
class Resume:
    resume_id: Optional[int]
    user_id: int
    file_name: str
    file_path: str
    raw_text: Optional[str] = None
    uploaded_at: Optional[datetime] = None

@dataclass
class Skill:
    skill_id: Optional[int]
    name: str

@dataclass
class JobPosting:
    job_id: Optional[int]
    title: str
    company: str
    description: str

@dataclass
class Application:
    application_id: Optional[int]
    user_id: int
    job_id: int
    resume_id: int
    applied_at: Optional[datetime] = None
    status: str = 'submitted'

@dataclass
class NGMIRecord:
    ngmi_id: Optional[int]
    application_id: int
    ngmi_score: float
    match_score: Optional[float]
    ngmi_comment: str
    generated_at: Optional[datetime] = None