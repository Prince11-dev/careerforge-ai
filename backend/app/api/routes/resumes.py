"""Resume generation and management routes."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.models.user import User
from app.models.profile import MasterProfile
from app.models.job import JobDescription, JDAnalysis, GeneratedResume, ResumeSection, ResumeVersion
from app.schemas.job import (
    ResumeGenerateRequest, ResumeUpdateRequest, ResumeResponse,
    ResumeListItem, MatchAnalysis
)
from app.services.resume_generator import resume_generator_service
from app.services.document_generator import document_generator_service
from app.services.profile_matcher import profile_matcher_service

router = APIRouter(prefix="/resumes", tags=["Resumes"])

def profile_to_dict(profile: MasterProfile) -> dict:
    return {
        "personal_info": {
            "full_name": profile.full_name,
            "professional_headline": profile.professional_headline,
            "email": profile.email,
            "phone": profile.phone,
            "city": profile.city,
            "state": profile.state,
            "country": profile.country,
            "linkedin_url": profile.linkedin_url,
            "github_url": profile.github_url,
            "portfolio_url": profile.portfolio_url
        },
        "professional_summary_facts": profile.professional_summary_facts,
        "skills": [{"name": s.name, "category": s.category} for s in profile.skills],
        "experiences": [{
            "company": e.company,
            "role": e.role,
            "employment_type": e.employment_type,
            "description": e.description,
            "verified_responsibilities": e.verified_responsibilities,
            "verified_achievements": e.verified_achievements,
            "technologies_used": e.technologies_used
        } for e in profile.experiences],
        "projects": [{
            "name": p.name,
            "description": p.description,
            "technologies": p.technologies,
            "responsibilities": p.responsibilities,
            "features": p.features
        } for p in profile.projects],
        "education": [{
            "institution": e.institution,
            "degree": e.degree,
            "field": e.field
        } for e in profile.education],
        "certifications": [{
            "name": c.name,
            "issuing_organization": c.issuing_organization,
            "issue_date": c.issue_date.isoformat() if c.issue_date else None,
            "credential_url": c.credential_url
        } for c in profile.certifications]
    }

@router.post("/generate", response_model=ResumeResponse)
async def generate_resume(
    data: ResumeGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get job description and analysis
    job = db.query(JobDescription).filter(
        JobDescription.id == data.job_description_id,
        JobDescription.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")

    analysis = job.analysis
    if not analysis:
        raise HTTPException(status_code=404, detail="Job analysis not found")

    # Get profile
    profile = db.query(MasterProfile).filter(
        MasterProfile.user_id == current_user.id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_data = profile_to_dict(profile)
    job_analysis = {
        "detected_role": analysis.detected_role,
        "seniority": analysis.seniority,
        "required_experience": analysis.required_experience,
        "mandatory_skills": analysis.mandatory_skills or [],
        "preferred_skills": analysis.preferred_skills or [],
        "tools": analysis.tools or [],
        "technologies": analysis.technologies or [],
        "responsibilities": analysis.responsibilities or [],
        "domain_keywords": analysis.domain_keywords or [],
        "ats_keywords": analysis.ats_keywords or []
    }

    # Generate resume
    try:
        result = await resume_generator_service.generate_resume(profile_data, job_analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume generation failed: {str(e)}")

    # Save to database
    match = result.get("match_analysis", {})
    resume = GeneratedResume(
        user_id=current_user.id,
        job_description_id=job.id,
        title=data.title or f"Resume for {job.job_title or 'Position'}",
        keyword_coverage=match.get("keyword_coverage"),
        mandatory_skills_match=match.get("mandatory_skills_match"),
        preferred_skills_match=match.get("preferred_skills_match"),
        experience_alignment=match.get("experience_alignment"),
        technology_alignment=match.get("technology_alignment"),
        overall_match=match.get("overall_match"),
        matched_skills=match.get("matched_skills", []),
        missing_skills=match.get("missing_skills", []),
        partial_skills=match.get("partial_skills", [])
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    # Save sections
    for section_data in result["sections"]:
        section = ResumeSection(
            resume_id=resume.id,
            section_type=section_data["section_type"],
            content=section_data["content"],
            display_order=section_data.get("display_order", 0),
            is_ai_generated=True
        )
        db.add(section)

    db.commit()
    db.refresh(resume)

    return _build_resume_response(resume)

@router.get("", response_model=List[ResumeListItem])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resumes = db.query(GeneratedResume).filter(
        GeneratedResume.user_id == current_user.id
    ).order_by(GeneratedResume.created_at.desc()).all()

    result = []
    for r in resumes:
        item = {
            "id": r.id,
            "title": r.title,
            "company_name": r.job_description.company_name if r.job_description else None,
            "job_title": r.job_description.job_title if r.job_description else None,
            "status": r.status,
            "overall_match": r.overall_match,
            "created_at": r.created_at
        }
        result.append(item)
    return result

@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(GeneratedResume).filter(
        GeneratedResume.id == resume_id,
        GeneratedResume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return _build_resume_response(resume)

@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: int,
    data: ResumeUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(GeneratedResume).filter(
        GeneratedResume.id == resume_id,
        GeneratedResume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # Save version before update
    version = ResumeVersion(
        resume_id=resume.id,
        version_number=len(resume.versions) + 1,
        sections_snapshot=[{"section_type": s.section_type, "content": s.content} for s in resume.sections],
        change_summary="User manual edit"
    )
    db.add(version)

    # Update sections
    for section in resume.sections:
        db.delete(section)

    for section_data in data.sections:
        section = ResumeSection(
            resume_id=resume.id,
            section_type=section_data.section_type,
            content=section_data.content,
            display_order=section_data.display_order,
            is_ai_generated=False,
            is_edited=True
        )
        db.add(section)

    db.commit()
    db.refresh(resume)
    return _build_resume_response(resume)

@router.post("/{resume_id}/regenerate-section")
async def regenerate_section(
    resume_id: int,
    section_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(GeneratedResume).filter(
        GeneratedResume.id == resume_id,
        GeneratedResume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    section = next((s for s in resume.sections if s.section_type == section_type), None)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    # Get profile and job analysis
    profile = db.query(MasterProfile).filter(MasterProfile.user_id == current_user.id).first()
    job = resume.job_description
    analysis = job.analysis if job else None

    if not profile or not analysis:
        raise HTTPException(status_code=400, detail="Profile or job analysis missing")

    profile_data = profile_to_dict(profile)
    job_analysis = {
        "detected_role": analysis.detected_role,
        "seniority": analysis.seniority,
        "required_experience": analysis.required_experience,
        "mandatory_skills": analysis.mandatory_skills or [],
        "preferred_skills": analysis.preferred_skills or [],
        "tools": analysis.tools or [],
        "technologies": analysis.technologies or [],
        "responsibilities": analysis.responsibilities or [],
        "domain_keywords": analysis.domain_keywords or [],
        "ats_keywords": analysis.ats_keywords or []
    }

    new_content = await resume_generator_service.regenerate_section(
        section_type, section.content, profile_data, job_analysis
    )

    section.content = new_content
    section.is_edited = True
    db.commit()
    db.refresh(section)

    return {"success": True, "content": new_content}

@router.post("/{resume_id}/approve")
def approve_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(GeneratedResume).filter(
        GeneratedResume.id == resume_id,
        GeneratedResume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume.status = "approved"
    db.commit()
    return {"success": True, "status": "approved"}

@router.get("/{resume_id}/export/pdf")
def export_pdf(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(GeneratedResume).filter(
        GeneratedResume.id == resume_id,
        GeneratedResume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    sections = [{"section_type": s.section_type, "content": s.content, "display_order": s.display_order} for s in resume.sections]
    pdf_bytes = document_generator_service.generate_pdf(sections, resume.title)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{resume.title.replace(" ", "_")}.pdf"'}
    )

@router.get("/{resume_id}/export/docx")
def export_docx(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(GeneratedResume).filter(
        GeneratedResume.id == resume_id,
        GeneratedResume.user_id == current_user.id
    ).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    sections = [{"section_type": s.section_type, "content": s.content, "display_order": s.display_order} for s in resume.sections]
    docx_bytes = document_generator_service.generate_docx(sections, resume.title)

    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{resume.title.replace(" ", "_")}.docx"'}
    )

def _build_resume_response(resume: GeneratedResume) -> dict:
    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "job_description_id": resume.job_description_id,
        "title": resume.title,
        "status": resume.status,
        "match_analysis": {
            "keyword_coverage": resume.keyword_coverage or 0,
            "mandatory_skills_match": resume.mandatory_skills_match or 0,
            "preferred_skills_match": resume.preferred_skills_match or 0,
            "experience_alignment": resume.experience_alignment or 0,
            "technology_alignment": resume.technology_alignment or 0,
            "overall_match": resume.overall_match or 0,
            "matched_skills": resume.matched_skills or [],
            "missing_skills": resume.missing_skills or [],
            "partial_skills": resume.partial_skills or []
        },
        "sections": [
            {
                "id": s.id,
                "section_type": s.section_type,
                "content": s.content,
                "display_order": s.display_order,
                "is_ai_generated": s.is_ai_generated,
                "is_edited": s.is_edited
            }
            for s in sorted(resume.sections, key=lambda x: x.display_order)
        ],
        "created_at": resume.created_at,
        "updated_at": resume.updated_at
    }
