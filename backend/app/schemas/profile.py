"""Profile schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class PersonalInfo(BaseModel):
    full_name: Optional[str] = None
    professional_headline: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None

class ExperienceCreate(BaseModel):
    company: str
    role: str
    employment_type: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    currently_working: bool = False
    description: Optional[str] = None
    verified_responsibilities: Optional[str] = None
    verified_achievements: Optional[str] = None
    technologies_used: Optional[str] = None
    display_order: int = 0

class ExperienceResponse(ExperienceCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SkillCreate(BaseModel):
    name: str
    category: str
    proficiency: Optional[str] = None
    display_order: int = 0

class SkillResponse(SkillCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: Optional[str] = None
    responsibilities: Optional[str] = None
    features: Optional[str] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    display_order: int = 0

class ProjectResponse(ProjectCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EducationCreate(BaseModel):
    institution: str
    degree: str
    field: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    display_order: int = 0

class EducationResponse(EducationCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CertificationCreate(BaseModel):
    name: str
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None
    credential_url: Optional[str] = None
    display_order: int = 0

class CertificationResponse(CertificationCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MasterProfileCreate(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    professional_summary_facts: Optional[str] = None

class MasterProfileUpdate(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    professional_summary_facts: Optional[str] = None
    is_verified: Optional[bool] = None

class MasterProfileResponse(BaseModel):
    id: int
    user_id: int
    personal_info: PersonalInfo
    professional_summary_facts: Optional[str]
    completion_percentage: int
    is_verified: bool
    experiences: List[ExperienceResponse]
    skills: List[SkillResponse]
    projects: List[ProjectResponse]
    education: List[EducationResponse]
    certifications: List[CertificationResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResumeUploadResponse(BaseModel):
    success: bool
    message: str
    extracted_data: Optional[dict] = None
