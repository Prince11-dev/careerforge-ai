"""Base AI Provider interface."""
from abc import ABC, abstractmethod
from typing import Dict, List, Any

class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    async def analyze_job_description(self, raw_text: str) -> Dict[str, Any]:
        """Analyze a job description and extract structured information."""
        pass

    @abstractmethod
    async def parse_resume_content(self, raw_text: str) -> Dict[str, Any]:
        """Parse raw resume text into structured profile data."""
        pass

    @abstractmethod
    async def generate_resume(self, profile_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """Generate a tailored resume based on profile and job analysis."""
        pass

    @abstractmethod
    async def regenerate_section(self, section_type: str, current_content: str, profile_data: Dict, job_analysis: Dict) -> str:
        """Regenerate a specific section of the resume."""
        pass
