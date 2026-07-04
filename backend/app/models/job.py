"""Job Description and Resume Generation models."""
import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String(255), nullable=True)
    job_title = Column(String(255), nullable=True)
    job_url = Column(String(1000), nullable=True)
    raw_text = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="job_descriptions")
    analysis = relationship("JDAnalysis", back_populates="job_description", uselist=False, cascade="all, delete-orphan")
    generated_resumes = relationship("GeneratedResume", back_populates="job_description")

class JDAnalysis(Base):
    __tablename__ = "jd_analyses"

    id = Column(Integer, primary_key=True, index=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False)
    detected_role = Column(String(255), nullable=True)
    seniority = Column(String(50), nullable=True)
    required_experience = Column(String(100), nullable=True)
    mandatory_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    tools = Column(JSON, default=list)
    technologies = Column(JSON, default=list)
    responsibilities = Column(JSON, default=list)
    domain_keywords = Column(JSON, default=list)
    ats_keywords = Column(JSON, default=list)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    job_description = relationship("JobDescription", back_populates="analysis")

class GeneratedResume(Base):
    __tablename__ = "generated_resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="draft")  # draft, approved, archived

    # Match metrics
    keyword_coverage = Column(Float, nullable=True)
    mandatory_skills_match = Column(Float, nullable=True)
    preferred_skills_match = Column(Float, nullable=True)
    experience_alignment = Column(Float, nullable=True)
    technology_alignment = Column(Float, nullable=True)
    overall_match = Column(Float, nullable=True)

    # Matched/Missing skills
    matched_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    partial_skills = Column(JSON, default=list)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="generated_resumes")
    job_description = relationship("JobDescription", back_populates="generated_resumes")
    sections = relationship("ResumeSection", back_populates="resume", cascade="all, delete-orphan")
    versions = relationship("ResumeVersion", back_populates="resume", cascade="all, delete-orphan")

class ResumeSection(Base):
    __tablename__ = "resume_sections"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("generated_resumes.id", ondelete="CASCADE"), nullable=False)
    section_type = Column(String(50), nullable=False)  # header, summary, skills, experience, projects, education, certifications
    content = Column(Text, nullable=False)
    display_order = Column(Integer, default=0)
    is_ai_generated = Column(Boolean, default=True)
    is_edited = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    resume = relationship("GeneratedResume", back_populates="sections")

class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("generated_resumes.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    sections_snapshot = Column(JSON, nullable=False)
    change_summary = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    resume = relationship("GeneratedResume", back_populates="versions")
