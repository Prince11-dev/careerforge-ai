"""Job Description analysis routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.routes.auth import get_current_user
from app.models.user import User
from app.models.job import JobDescription, JDAnalysis
from app.schemas.job import JobDescriptionCreate, JDAnalysisResponse
from app.services.jd_analyzer import jd_analyzer_service

router = APIRouter(prefix="/jobs", tags=["Job Descriptions"])

@router.post("/analyze", response_model=JDAnalysisResponse)
async def analyze_job_description(
    data: JobDescriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Save job description
    jd = JobDescription(
        user_id=current_user.id,
        company_name=data.company_name,
        job_title=data.job_title,
        job_url=data.job_url,
        raw_text=data.raw_text
    )
    db.add(jd)
    db.commit()
    db.refresh(jd)

    # Analyze
    try:
        analysis_data = await jd_analyzer_service.analyze(data.raw_text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    analysis = JDAnalysis(
        job_description_id=jd.id,
        **analysis_data
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis

@router.get("/history")
def get_job_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    jobs = db.query(JobDescription).filter(
        JobDescription.user_id == current_user.id
    ).order_by(JobDescription.created_at.desc()).all()

    result = []
    for job in jobs:
        item = {
            "id": job.id,
            "company_name": job.company_name,
            "job_title": job.job_title,
            "job_url": job.job_url,
            "raw_text": job.raw_text[:200] + "..." if len(job.raw_text) > 200 else job.raw_text,
            "created_at": job.created_at,
            "analysis": None
        }
        if job.analysis:
            item["analysis"] = {
                "detected_role": job.analysis.detected_role,
                "seniority": job.analysis.seniority,
                "mandatory_skills": job.analysis.mandatory_skills,
                "preferred_skills": job.analysis.preferred_skills
            }
        result.append(item)
    return result
