"""Master Career Profile models."""
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class MasterProfile(Base):
    __tablename__ = "master_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Personal Information
    full_name = Column(String(255), nullable=True)
    professional_headline = Column(String(500), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    portfolio_url = Column(String(500), nullable=True)

    # Professional Summary Facts
    professional_summary_facts = Column(Text, nullable=True)

    # Completion tracking
    completion_percentage = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="profile", cascade="all, delete-orphan")

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("master_profiles.id", ondelete="CASCADE"), nullable=False)
    company = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    employment_type = Column(String(50), nullable=True)  # Full-time, Contract, etc.
    location = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    currently_working = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    verified_responsibilities = Column(Text, nullable=True)
    verified_achievements = Column(Text, nullable=True)
    technologies_used = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("MasterProfile", back_populates="experiences")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("master_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # programming_languages, backend, frontend, databases, cloud, devops, ai_ml, tools, other
    proficiency = Column(String(20), nullable=True)  # beginner, intermediate, advanced, expert
    display_order = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("MasterProfile", back_populates="skills")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("master_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    technologies = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    features = Column(Text, nullable=True)
    github_url = Column(String(500), nullable=True)
    live_url = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("MasterProfile", back_populates="projects")

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("master_profiles.id", ondelete="CASCADE"), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    field = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    display_order = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("MasterProfile", back_populates="education")

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("master_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    issuing_organization = Column(String(255), nullable=True)
    issue_date = Column(Date, nullable=True)
    credential_url = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("MasterProfile", back_populates="certifications")
