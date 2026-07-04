"""Seed database with demo data."""
import sys
sys.path.insert(0, ".")

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User
from app.models.profile import MasterProfile, Experience, Skill, Project, Education, Certification

def seed_demo_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if demo user exists
        demo = db.query(User).filter(User.email == "demo@careerforge.ai").first()
        if demo:
            print("Demo user already exists")
            return

        # Create demo user
        user = User(
            email="demo@careerforge.ai",
            hashed_password=get_password_hash("demo12345"),
            full_name="Alex Demo",
            is_demo=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create profile
        profile = MasterProfile(
            user_id=user.id,
            full_name="Alex Demo",
            professional_headline="Senior Full-Stack Software Engineer",
            email="alex.demo@email.com",
            phone="(555) 123-4567",
            city="San Francisco",
            state="CA",
            country="USA",
            linkedin_url="https://linkedin.com/in/alexdemo",
            github_url="https://github.com/alexdemo",
            professional_summary_facts="Passionate about building scalable web applications and leading engineering teams. 8+ years of experience in SaaS development.",
            completion_percentage=85,
            is_verified=True
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

        # Add skills
        skills = [
            ("Python", "programming_languages", "expert"),
            ("JavaScript", "programming_languages", "expert"),
            ("TypeScript", "programming_languages", "advanced"),
            ("React", "frontend", "expert"),
            ("Node.js", "backend", "advanced"),
            ("FastAPI", "backend", "advanced"),
            ("PostgreSQL", "databases", "advanced"),
            ("MongoDB", "databases", "intermediate"),
            ("AWS", "cloud", "advanced"),
            ("Docker", "devops", "advanced"),
            ("Kubernetes", "devops", "intermediate"),
            ("Git", "tools", "expert"),
            ("CI/CD", "devops", "advanced"),
            ("Machine Learning", "ai_ml", "intermediate"),
        ]
        for name, cat, prof in skills:
            db.add(Skill(profile_id=profile.id, name=name, category=cat, proficiency=prof))

        # Add experiences
        experiences = [
            {
                "company": "TechCorp Inc.",
                "role": "Senior Software Engineer",
                "employment_type": "Full-time",
                "location": "San Francisco, CA",
                "description": "Leading backend development for core platform services.",
                "verified_responsibilities": "- Architected and built microservices handling 10M+ daily requests\n- Mentored team of 5 junior engineers\n- Improved API response times by 40% through caching strategies",
                "verified_achievements": "- Reduced infrastructure costs by 25% via AWS optimization\n- Led migration from monolith to microservices",
                "technologies_used": "Python, FastAPI, PostgreSQL, AWS, Docker, Kubernetes"
            },
            {
                "company": "StartupXYZ",
                "role": "Full-Stack Developer",
                "employment_type": "Full-time",
                "location": "Remote",
                "description": "Built full-stack features for B2B SaaS platform.",
                "verified_responsibilities": "- Developed React frontend and Node.js backend\n- Implemented real-time collaboration features\n- Designed and optimized database schemas",
                "verified_achievements": "- Increased user engagement by 35% with UI improvements\n- Built automated testing pipeline reducing bugs by 50%",
                "technologies_used": "React, Node.js, MongoDB, TypeScript, AWS"
            },
            {
                "company": "DataSystems LLC",
                "role": "Junior Developer",
                "employment_type": "Full-time",
                "location": "New York, NY",
                "description": "Developed data processing pipelines and internal tools.",
                "verified_responsibilities": "- Built Python scripts for data ETL processes\n- Maintained internal dashboard applications\n- Collaborated with data science team on ML models",
                "verified_achievements": "- Automated reporting saving 20 hours/week\n- Contributed to open-source data library",
                "technologies_used": "Python, SQL, Pandas, Scikit-learn, Flask"
            }
        ]
        for exp in experiences:
            db.add(Experience(profile_id=profile.id, **exp))

        # Add projects
        projects = [
            {
                "name": "OpenSource Analytics",
                "description": "Real-time analytics dashboard for open-source projects.",
                "technologies": "React, TypeScript, FastAPI, PostgreSQL, Redis",
                "responsibilities": "- Designed system architecture\n- Implemented real-time data pipeline\n- Built responsive dashboard UI",
                "features": "Real-time updates, GitHub integration, Custom alerts",
                "github_url": "https://github.com/alexdemo/analytics"
            },
            {
                "name": "AI Resume Parser",
                "description": "NLP-powered resume parsing and analysis tool.",
                "technologies": "Python, SpaCy, FastAPI, React",
                "responsibilities": "- Trained custom NLP model for entity extraction\n- Built REST API for parsing service\n- Created frontend for visualization",
                "features": "Entity extraction, Skill matching, PDF parsing",
                "github_url": "https://github.com/alexdemo/resume-parser"
            }
        ]
        for proj in projects:
            db.add(Project(profile_id=profile.id, **proj))

        # Add education
        educations = [
            {
                "institution": "University of California, Berkeley",
                "degree": "Bachelor of Science",
                "field": "Computer Science"
            },
            {
                "institution": "Stanford University",
                "degree": "Master of Science",
                "field": "Artificial Intelligence"
            }
        ]
        for edu in educations:
            db.add(Education(profile_id=profile.id, **edu))

        # Add certifications
        certifications = [
            {
                "name": "AWS Certified Solutions Architect",
                "issuing_organization": "Amazon Web Services",
                "credential_url": "https://aws.amazon.com/certification"
            },
            {
                "name": "Certified Kubernetes Administrator",
                "issuing_organization": "Cloud Native Computing Foundation",
                "credential_url": "https://cncf.io/certification"
            }
        ]
        for cert in certifications:
            db.add(Certification(profile_id=profile.id, **cert))

        db.commit()
        print("Demo data seeded successfully!")
        print("Demo credentials: demo@careerforge.ai / demo12345")
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
