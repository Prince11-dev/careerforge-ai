"""Profile-to-JD matching service."""
from typing import Dict, List, Any, Set

class ProfileMatcherService:
    """Service for calculating match metrics between profile and job description."""

    def calculate_match(self, profile_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        profile_skills = self._extract_profile_skills(profile_data)
        profile_tech = self._extract_profile_technologies(profile_data)

        mandatory = set(s.lower() for s in job_analysis.get("mandatory_skills", []))
        preferred = set(s.lower() for s in job_analysis.get("preferred_skills", []))
        tools = set(t.lower() for t in job_analysis.get("tools", []))
        technologies = set(t.lower() for t in job_analysis.get("technologies", []))

        all_required = mandatory | preferred | tools | technologies

        matched = []
        missing = []
        partial = []

        for req in all_required:
            if req in profile_skills or req in profile_tech:
                matched.append(req.title())
            elif any(req in ps or ps in req for ps in profile_skills):
                partial.append(req.title())
            else:
                missing.append(req.title())

        # Calculate metrics
        total_required = len(all_required) if all_required else 1
        keyword_coverage = len(matched) / total_required * 100

        mandatory_total = len(mandatory) if mandatory else 1
        mandatory_match = len([m for m in matched if m.lower() in mandatory]) / mandatory_total * 100

        preferred_total = len(preferred) if preferred else 1
        preferred_match = len([m for m in matched if m.lower() in preferred]) / preferred_total * 100

        tech_total = len(technologies) if technologies else 1
        tech_match = len([m for m in matched if m.lower() in technologies]) / tech_total * 100

        # Experience alignment (simplified)
        exp_years = self._estimate_experience_years(profile_data)
        req_exp = job_analysis.get("required_experience", "")
        exp_alignment = self._calculate_experience_alignment(exp_years, req_exp)

        overall = (keyword_coverage + mandatory_match + preferred_match + tech_match + exp_alignment) / 5

        return {
            "keyword_coverage": round(keyword_coverage, 1),
            "mandatory_skills_match": round(mandatory_match, 1),
            "preferred_skills_match": round(preferred_match, 1),
            "experience_alignment": round(exp_alignment, 1),
            "technology_alignment": round(tech_match, 1),
            "overall_match": round(overall, 1),
            "matched_skills": matched[:20],
            "missing_skills": missing[:20],
            "partial_skills": partial[:20]
        }

    def _extract_profile_skills(self, profile_data: Dict) -> Set[str]:
        skills = set()
        for skill in profile_data.get("skills", []):
            skills.add(skill.get("name", "").lower())
        return skills

    def _extract_profile_technologies(self, profile_data: Dict) -> Set[str]:
        tech = set()
        for exp in profile_data.get("experiences", []):
            tech_text = exp.get("technologies_used", "").lower()
            tech.update(t.strip() for t in tech_text.split(",") if t.strip())
        for proj in profile_data.get("projects", []):
            tech_text = proj.get("technologies", "").lower()
            tech.update(t.strip() for t in tech_text.split(",") if t.strip())
        return tech

    def _estimate_experience_years(self, profile_data: Dict) -> int:
        # Simplified: count number of experiences
        return len(profile_data.get("experiences", [])) * 2

    def _calculate_experience_alignment(self, years: int, required: str) -> float:
        import re
        match = re.search(r"(\d+)", required)
        if not match:
            return 80.0
        req_years = int(match.group(1))
        if years >= req_years:
            return 100.0
        return max(0, (years / req_years) * 100)

profile_matcher_service = ProfileMatcherService()
