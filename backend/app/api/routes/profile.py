"""Profile management routes."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.models.user import User
from app.models.profile import MasterProfile, Experience, Skill, Project, Education, Certification
from app.schemas.profile import (
    MasterProfileCreate, MasterProfileUpdate, MasterProfileResponse,
    ExperienceCreate, ExperienceResponse,
    SkillCreate, SkillResponse,
    ProjectCreate, ProjectResponse,
    EducationCreate, EducationResponse,
    CertificationCreate, CertificationResponse,
    ResumeUploadResponse, PersonalInfo
)
from app.services.resume_parser import resume_parser_service

router = APIRouter(prefix="/profile", tags=["Profile"])

def get_or_create_profile(db: Session, user_id: int) -> MasterProfile:
    profile = db.query(MasterProfile).filter(MasterProfile.user_id == user_id).first()
    if not profile:
        profile = MasterProfile(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

def profile_to_dict(profile: MasterProfile) -> dict:
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "personal_info": PersonalInfo(
            full_name=profile.full_name,
            professional_headline=profile.professional_headline,
            email=profile.email,
            phone=profile.phone,
            city=profile.city,
            state=profile.state,
            country=profile.country,
            linkedin_url=profile.linkedin_url,
            github_url=profile.github_url,
            portfolio_url=profile.portfolio_url
        ),
        "professional_summary_facts": profile.professional_summary_facts,
        "completion_percentage": profile.completion_percentage,
        "is_verified": profile.is_verified,
        "experiences": profile.experiences,
        "skills": profile.skills,
        "projects": profile.projects,
        "education": profile.education,
        "certifications": profile.certifications,
        "created_at": profile.created_at,
        "updated_at": profile.updated_at
    }

def calculate_completion(profile: MasterProfile) -> int:
    fields = [
        profile.full_name, profile.professional_headline, profile.email,
        profile.phone, profile.city, profile.linkedin_url
    ]
    base = sum(1 for f in fields if f) / len(fields) * 50

    sections = [
        len(profile.experiences) > 0,
        len(profile.skills) > 0,
        len(profile.education) > 0,
        len(profile.projects) > 0,
        len(profile.certifications) > 0
    ]
    section_score = sum(1 for s in sections if s) / len(sections) * 50

    return int(base + section_score)

@router.get("", response_model=MasterProfileResponse)
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = get_or_create_profile(db, current_user.id)
    profile.completion_percentage = calculate_completion(profile)
    db.commit()
    return profile_to_dict(profile)

@router.put("", response_model=MasterProfileResponse)
def update_profile(
    data: MasterProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)

    if data.personal_info:
        pi = data.personal_info
        profile.full_name = pi.full_name or profile.full_name
        profile.professional_headline = pi.professional_headline or profile.professional_headline
        profile.email = pi.email or profile.email
        profile.phone = pi.phone or profile.phone
        profile.city = pi.city or profile.city
        profile.state = pi.state or profile.state
        profile.country = pi.country or profile.country
        profile.linkedin_url = pi.linkedin_url or profile.linkedin_url
        profile.github_url = pi.github_url or profile.github_url
        profile.portfolio_url = pi.portfolio_url or profile.portfolio_url

    if data.professional_summary_facts is not None:
        profile.professional_summary_facts = data.professional_summary_facts

    if data.is_verified is not None:
        profile.is_verified = data.is_verified

    profile.completion_percentage = calculate_completion(profile)
    db.commit()
    db.refresh(profile)
    return profile_to_dict(profile)

@router.post("/resume-upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    content = await file.read()

    try:
        result = await resume_parser_service.parse_resume(file.filename, content)
        structured = result["structured_data"]

        # Update profile with extracted data
        profile = get_or_create_profile(db, current_user.id)

        pi = structured.get("personal_info", {})
        profile.full_name = pi.get("full_name") or profile.full_name
        profile.email = pi.get("email") or profile.email
        profile.phone = pi.get("phone") or profile.phone
        profile.professional_summary_facts = structured.get("professional_summary_facts") or profile.professional_summary_facts

        # Add skills
        for skill_data in structured.get("skills", []):
            existing = db.query(Skill).filter(
                Skill.profile_id == profile.id,
                Skill.name.ilike(skill_data["name"])
            ).first()
            if not existing:
                skill = Skill(
                    profile_id=profile.id,
                    name=skill_data["name"],
                    category=skill_data.get("category", "other")
                )
                db.add(skill)

        # Add experiences
        for exp_data in structured.get("experiences", []):
            exp = Experience(
                profile_id=profile.id,
                company=exp_data["company"],
                role=exp_data["role"],
                employment_type=exp_data.get("employment_type"),
                description=exp_data.get("description"),
                verified_responsibilities=exp_data.get("verified_responsibilities"),
                verified_achievements=exp_data.get("verified_achievements"),
                technologies_used=exp_data.get("technologies_used")
            )
            db.add(exp)

        # Add projects
        for proj_data in structured.get("projects", []):
            proj = Project(
                profile_id=profile.id,
                name=proj_data["name"],
                description=proj_data.get("description"),
                technologies=proj_data.get("technologies"),
                responsibilities=proj_data.get("responsibilities"),
                features=proj_data.get("features")
            )
            db.add(proj)

        # Add education
        for edu_data in structured.get("education", []):
            edu = Education(
                profile_id=profile.id,
                institution=edu_data["institution"],
                degree=edu_data["degree"],
                field=edu_data.get("field")
            )
            db.add(edu)

        profile.completion_percentage = calculate_completion(profile)
        db.commit()
        db.refresh(profile)

        return {
            "success": True,
            "message": "Resume parsed successfully. Please review and verify the extracted data.",
            "extracted_data": structured
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

# Experience CRUD
@router.post("/experiences", response_model=ExperienceResponse)
def create_experience(
    data: ExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    exp = Experience(profile_id=profile.id, **data.dict())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    profile.completion_percentage = calculate_completion(profile)
    db.commit()
    return exp

@router.put("/experiences/{exp_id}", response_model=ExperienceResponse)
def update_experience(
    exp_id: int,
    data: ExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    exp = db.query(Experience).filter(
        Experience.id == exp_id,
        Experience.profile_id == profile.id
    ).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")

    for key, value in data.dict().items():
        setattr(exp, key, value)
    db.commit()
    db.refresh(exp)
    return exp

@router.delete("/experiences/{exp_id}")
def delete_experience(
    exp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    exp = db.query(Experience).filter(
        Experience.id == exp_id,
        Experience.profile_id == profile.id
    ).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    db.delete(exp)
    db.commit()
    return {"success": True}

# Skill CRUD
@router.post("/skills", response_model=SkillResponse)
def create_skill(
    data: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    skill = Skill(profile_id=profile.id, **data.dict())
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill

@router.put("/skills/{skill_id}", response_model=SkillResponse)
def update_skill(
    skill_id: int,
    data: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.profile_id == profile.id
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    for key, value in data.dict().items():
        setattr(skill, key, value)
    db.commit()
    db.refresh(skill)
    return skill

@router.delete("/skills/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    skill = db.query(Skill).filter(
        Skill.id == skill_id,
        Skill.profile_id == profile.id
    ).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"success": True}

# Project CRUD
@router.post("/projects", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    proj = Project(profile_id=profile.id, **data.dict())
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@router.put("/projects/{proj_id}", response_model=ProjectResponse)
def update_project(
    proj_id: int,
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    proj = db.query(Project).filter(
        Project.id == proj_id,
        Project.profile_id == profile.id
    ).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, value in data.dict().items():
        setattr(proj, key, value)
    db.commit()
    db.refresh(proj)
    return proj

@router.delete("/projects/{proj_id}")
def delete_project(
    proj_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    proj = db.query(Project).filter(
        Project.id == proj_id,
        Project.profile_id == profile.id
    ).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(proj)
    db.commit()
    return {"success": True}

# Education CRUD
@router.post("/education", response_model=EducationResponse)
def create_education(
    data: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    edu = Education(profile_id=profile.id, **data.dict())
    db.add(edu)
    db.commit()
    db.refresh(edu)
    return edu

@router.put("/education/{edu_id}", response_model=EducationResponse)
def update_education(
    edu_id: int,
    data: EducationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    edu = db.query(Education).filter(
        Education.id == edu_id,
        Education.profile_id == profile.id
    ).first()
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found")
    for key, value in data.dict().items():
        setattr(edu, key, value)
    db.commit()
    db.refresh(edu)
    return edu

@router.delete("/education/{edu_id}")
def delete_education(
    edu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    edu = db.query(Education).filter(
        Education.id == edu_id,
        Education.profile_id == profile.id
    ).first()
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found")
    db.delete(edu)
    db.commit()
    return {"success": True}

# Certification CRUD
@router.post("/certifications", response_model=CertificationResponse)
def create_certification(
    data: CertificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    cert = Certification(profile_id=profile.id, **data.dict())
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.put("/certifications/{cert_id}", response_model=CertificationResponse)
def update_certification(
    cert_id: int,
    data: CertificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    cert = db.query(Certification).filter(
        Certification.id == cert_id,
        Certification.profile_id == profile.id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    for key, value in data.dict().items():
        setattr(cert, key, value)
    db.commit()
    db.refresh(cert)
    return cert

@router.delete("/certifications/{cert_id}")
def delete_certification(
    cert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = get_or_create_profile(db, current_user.id)
    cert = db.query(Certification).filter(
        Certification.id == cert_id,
        Certification.profile_id == profile.id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    db.delete(cert)
    db.commit()
    return {"success": True}
