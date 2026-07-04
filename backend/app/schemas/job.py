"""Job Description and Resume schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class JobDescriptionCreate(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    job_url: Optional[str] = None
    raw_text: str = Field(..., min_length=50)

class JDAnalysisResponse(BaseModel):
    id: int
    job_description_id: int
    detected_role: Optional[str]
    seniority: Optional[str]
    required_experience: Optional[str]
    mandatory_skills: List[str]
    preferred_skills: List[str]
    tools: List[str]
    technologies: List[str]
    responsibilities: List[str]
    domain_keywords: List[str]
    ats_keywords: List[str]

    class Config:
        from_attributes = True

class MatchAnalysis(BaseModel):
    keyword_coverage: float
    mandatory_skills_match: float
    preferred_skills_match: float
    experience_alignment: float
    technology_alignment: float
    overall_match: float
    matched_skills: List[str]
    missing_skills: List[str]
    partial_skills: List[str]

class ResumeSectionCreate(BaseModel):
    section_type: str
    content: str
    display_order: int = 0

class ResumeSectionResponse(BaseModel):
    id: int
    section_type: str
    content: str
    display_order: int
    is_ai_generated: bool
    is_edited: bool

    class Config:
        from_attributes = True

class ResumeGenerateRequest(BaseModel):
    job_description_id: int
    title: Optional[str] = "Tailored Resume"

class ResumeUpdateRequest(BaseModel):
    sections: List[ResumeSectionCreate]

class ResumeResponse(BaseModel):
    id: int
    user_id: int
    job_description_id: Optional[int]
    title: str
    status: str
    match_analysis: Optional[MatchAnalysis]
    sections: List[ResumeSectionResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResumeListItem(BaseModel):
    id: int
    title: str
    company_name: Optional[str]
    job_title: Optional[str]
    status: str
    overall_match: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
