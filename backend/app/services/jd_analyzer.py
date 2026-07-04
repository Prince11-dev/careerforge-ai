"""Job Description analysis service."""
from typing import Dict, Any
from app.ai.provider import ai_provider

class JDAnalyzerService:
    """Service for analyzing job descriptions."""

    async def analyze(self, raw_text: str) -> Dict[str, Any]:
        if not raw_text or len(raw_text.strip()) < 50:
            raise ValueError("Job description must be at least 50 characters")

        analysis = await ai_provider.analyze_job_description(raw_text)
        return analysis

jd_analyzer_service = JDAnalyzerService()
