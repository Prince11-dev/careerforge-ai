"""CareerForge AI - FastAPI Application Entry Point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, profile, jobs, resumes

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="One Profile. Every Job. A Better Resume.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(resumes.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.app_name, "mock_ai_mode": settings.mock_ai_mode}

@app.get("/")
def root():
    return {"message": "Welcome to CareerForge AI API", "docs": "/docs"}
