"""Mock AI Provider for local development without API keys."""
import re
from typing import Dict, List, Any
from app.ai.base import AIProvider

class MockAIProvider(AIProvider):
    """Deterministic mock AI provider for testing and demo mode."""

    def __init__(self):
        self.skill_keywords = [
            "python", "javascript", "typescript", "react", "node.js", "sql", "aws",
            "docker", "kubernetes", "git", "agile", "ci/cd", "rest", "graphql",
            "machine learning", "data analysis", "project management", "leadership",
            "communication", "teamwork", "problem solving", "java", "c++", "go",
            "rust", "postgresql", "mongodb", "redis", "kafka", "terraform",
            "azure", "gcp", "linux", "microservices", "api design", "testing"
        ]

        self.tool_keywords = [
            "jira", "confluence", "slack", "github", "gitlab", "jenkins", "circleci",
            "travis", "docker", "kubernetes", "terraform", "ansible", "prometheus",
            "grafana", "elasticsearch", "kibana", "vscode", "pycharm", "intellij"
        ]

        self.seniority_patterns = {
            "senior": ["senior", "sr.", "lead", "principal", "staff", "architect"],
            "mid": ["mid-level", "mid level", "intermediate", "associate"],
            "junior": ["junior", "jr.", "entry", "entry-level", "intern", "graduate"]
        }

    async def analyze_job_description(self, raw_text: str) -> Dict[str, Any]:
        """Deterministic keyword-based JD analysis."""
        text_lower = raw_text.lower()

        # Detect role
        role_patterns = [
            r"(software engineer|developer|architect|manager|director|analyst|scientist|designer|consultant|specialist)",
            r"(frontend|backend|full[- ]stack|devops|data|machine learning|ai|cloud|security|mobile|web)"
        ]
        detected_role = "Software Engineer"
        for pattern in role_patterns:
            match = re.search(pattern, text_lower)
            if match:
                detected_role = match.group(0).title()
                break

        # Detect seniority
        seniority = "mid"
        for level, patterns in self.seniority_patterns.items():
            for p in patterns:
                if p in text_lower:
                    seniority = level
                    break

        # Extract skills
        mandatory_skills = []
        preferred_skills = []
        for skill in self.skill_keywords:
            if skill in text_lower:
                if "preferred" in text_lower or "nice to have" in text_lower or "plus" in text_lower:
                    preferred_skills.append(skill.title())
                else:
                    mandatory_skills.append(skill.title())

        # Extract tools
        tools = []
        for tool in self.tool_keywords:
            if tool in text_lower:
                tools.append(tool.title())

        # Extract responsibilities - avoid raw strings with special chars
        responsibilities = []
        # Simple line-based extraction for bullet points
        lines = raw_text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("-") or line.startswith("*") or line.startswith(chr(8226)):
                clean = line.lstrip("-*" + chr(8226)).strip()
                if 15 < len(clean) < 150 and clean not in responsibilities:
                    responsibilities.append(clean)

        # Also try pattern-based extraction
        resp_pattern = r"(?:responsible for|will be|you will|duties include)[\s:]+([^\n]{10,200})"
        matches = re.findall(resp_pattern, raw_text, re.IGNORECASE)
        for m in matches[:5]:
            if isinstance(m, tuple):
                m = m[0]
            clean = m.strip().rstrip(".").strip()
            if len(clean) > 15 and clean not in responsibilities:
                responsibilities.append(clean)

        if not responsibilities:
            responsibilities = [
                "Develop and maintain software applications",
                "Collaborate with cross-functional teams",
                "Write clean, maintainable code",
                "Participate in code reviews",
                "Troubleshoot and debug issues"
            ]

        # Domain keywords
        domain_keywords = []
        domains = ["fintech", "healthcare", "e-commerce", "saas", "enterprise", "startup", "b2b", "b2c", "ai", "ml"]
        for d in domains:
            if d in text_lower:
                domain_keywords.append(d.title())

        return {
            "detected_role": detected_role,
            "seniority": seniority,
            "required_experience": "3+ years" if seniority == "senior" else "1-3 years" if seniority == "mid" else "0-2 years",
            "mandatory_skills": list(set(mandatory_skills))[:10],
            "preferred_skills": list(set(preferred_skills))[:10],
            "tools": list(set(tools))[:8],
            "technologies": list(set(mandatory_skills + preferred_skills))[:12],
            "responsibilities": responsibilities[:6],
            "domain_keywords": domain_keywords or ["Software Development"],
            "ats_keywords": list(set(mandatory_skills + tools))[:15]
        }

    async def parse_resume_content(self, raw_text: str) -> Dict[str, Any]:
        """Parse resume text into structured data using deterministic extraction."""
        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
        text_lower = raw_text.lower()

        # Extract name (first line or capitalized phrase)
        name = lines[0] if lines else "Unknown"
        if len(name) > 50 or "@" in name:
            name = "Candidate Name"

        # Extract email
        email_match = re.search(r"[\w.-]+@[\w.-]+\.\w+", raw_text)
        email = email_match.group(0) if email_match else ""

        # Extract phone
        phone_match = re.search(r"[\(]?\d{3}[\)]?[\s.-]?\d{3}[\s.-]?\d{4}", raw_text)
        phone = phone_match.group(0) if phone_match else ""

        # Extract skills
        skills = []
        for skill in self.skill_keywords:
            if skill in text_lower:
                skills.append({"name": skill.title(), "category": self._categorize_skill(skill)})

        # Extract experience
        experiences = []
        company_pattern = r"([A-Z][\w\s&]+)[\s|,|\-]*([A-Z][\w\s]+)?[\s|,|\-]*(\d{4})"
        matches = re.findall(company_pattern, raw_text)
        for i, match in enumerate(matches[:3]):
            company = match[0].strip() if match[0] else f"Company {i+1}"
            role = match[1].strip() if match[1] else "Software Engineer"
            experiences.append({
                "company": company,
                "role": role,
                "employment_type": "Full-time",
                "description": "Responsible for software development and team collaboration.",
                "verified_responsibilities": "- Developed key features\n- Collaborated with team",
                "verified_achievements": "- Improved performance by 20%",
                "technologies_used": "Python, React, AWS"
            })

        if not experiences:
            experiences = [{
                "company": "Example Company",
                "role": "Software Engineer",
                "employment_type": "Full-time",
                "description": "Developed and maintained software applications.",
                "verified_responsibilities": "- Developed features\n- Fixed bugs",
                "verified_achievements": "- Improved system performance",
                "technologies_used": "Python, JavaScript"
            }]

        return {
            "personal_info": {
                "full_name": name,
                "professional_headline": "Software Engineer",
                "email": email,
                "phone": phone,
                "city": "",
                "state": "",
                "country": "",
                "linkedin_url": "",
                "github_url": "",
                "portfolio_url": ""
            },
            "professional_summary_facts": "Experienced software engineer with a passion for building scalable applications.",
            "skills": skills[:15],
            "experiences": experiences,
            "projects": [{
                "name": "Sample Project",
                "description": "A project demonstrating technical skills.",
                "technologies": "Python, React",
                "responsibilities": "- Built frontend\n- Designed API",
                "features": "User authentication, Dashboard"
            }],
            "education": [{
                "institution": "University",
                "degree": "Bachelor of Science",
                "field": "Computer Science"
            }],
            "certifications": []
        }

    async def generate_resume(self, profile_data: Dict, job_analysis: Dict) -> Dict[str, Any]:
        """Generate tailored resume using only verified profile data."""
        personal = profile_data.get("personal_info", {})

        # Filter skills by relevance to job
        profile_skills = profile_data.get("skills", [])
        job_skills = job_analysis.get("mandatory_skills", []) + job_analysis.get("preferred_skills", [])
        job_skills_lower = [s.lower() for s in job_skills]

        relevant_skills = []
        other_skills = []
        for skill in profile_skills:
            if skill["name"].lower() in job_skills_lower:
                relevant_skills.append(skill)
            else:
                other_skills.append(skill)

        sorted_skills = relevant_skills + other_skills

        # Filter experiences by relevance
        experiences = profile_data.get("experiences", [])
        job_tech = [t.lower() for t in job_analysis.get("technologies", [])]

        def exp_relevance(exp):
            tech = exp.get("technologies_used", "").lower()
            return sum(1 for t in job_tech if t in tech)

        sorted_experiences = sorted(experiences, key=exp_relevance, reverse=True)

        # Filter projects similarly
        projects = profile_data.get("projects", [])
        def proj_relevance(proj):
            tech = proj.get("technologies", "").lower()
            return sum(1 for t in job_tech if t in tech)
        sorted_projects = sorted(projects, key=proj_relevance, reverse=True)

        # Generate professional summary from verified facts
        summary_facts = profile_data.get("professional_summary_facts", "")
        summary = self._generate_summary(summary_facts, job_analysis, personal)

        sections = [
            {
                "section_type": "header",
                "content": self._format_header(personal),
                "display_order": 0
            },
            {
                "section_type": "summary",
                "content": summary,
                "display_order": 1
            },
            {
                "section_type": "skills",
                "content": self._format_skills(sorted_skills),
                "display_order": 2
            },
            {
                "section_type": "experience",
                "content": self._format_experiences(sorted_experiences),
                "display_order": 3
            },
            {
                "section_type": "projects",
                "content": self._format_projects(sorted_projects),
                "display_order": 4
            },
            {
                "section_type": "education",
                "content": self._format_education(profile_data.get("education", [])),
                "display_order": 5
            },
            {
                "section_type": "certifications",
                "content": self._format_certifications(profile_data.get("certifications", [])),
                "display_order": 6
            }
        ]

        return {"sections": [s for s in sections if s["content"].strip()]}

    async def regenerate_section(self, section_type: str, current_content: str, profile_data: Dict, job_analysis: Dict) -> str:
        """Regenerate a specific section with fresh wording."""
        if section_type == "summary":
            return self._generate_summary(
                profile_data.get("professional_summary_facts", ""),
                job_analysis,
                profile_data.get("personal_info", {})
            )
        elif section_type == "skills":
            return self._format_skills(profile_data.get("skills", []))
        elif section_type == "experience":
            return self._format_experiences(profile_data.get("experiences", []))
        elif section_type == "projects":
            return self._format_projects(profile_data.get("projects", []))
        return current_content

    def _categorize_skill(self, skill: str) -> str:
        categories = {
            "programming_languages": ["python", "javascript", "typescript", "java", "c++", "go", "rust", "c#", "ruby", "php"],
            "backend": ["node.js", "django", "flask", "fastapi", "spring", "express", "graphql", "rest"],
            "frontend": ["react", "vue", "angular", "html", "css", "tailwind", "bootstrap"],
            "databases": ["sql", "postgresql", "mysql", "mongodb", "redis", "sqlite", "dynamodb"],
            "cloud": ["aws", "azure", "gcp", "cloud", "serverless"],
            "devops": ["docker", "kubernetes", "terraform", "ansible", "jenkins", "ci/cd", "github actions"],
            "ai_ml": ["machine learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy"],
            "tools": ["git", "jira", "confluence", "slack", "vscode"]
        }
        for cat, skills in categories.items():
            if skill.lower() in skills:
                return cat
        return "other"

    def _generate_summary(self, facts: str, job_analysis: Dict, personal: Dict) -> str:
        role = job_analysis.get("detected_role", "Software Engineer")
        seniority = job_analysis.get("seniority", "mid")

        seniority_word = "experienced" if seniority == "senior" else "skilled" if seniority == "mid" else "motivated"

        summary = f"{seniority_word.title()} {role} with a strong background in software development."
        if facts:
            summary += f" {facts}"

        key_skills = job_analysis.get("mandatory_skills", [])[:3]
        if key_skills:
            summary += f" Proficient in {', '.join(key_skills)}."

        return summary

    def _format_header(self, personal: Dict) -> str:
        lines = []
        if personal.get("full_name"):
            lines.append(personal["full_name"])
        if personal.get("professional_headline"):
            lines.append(personal["professional_headline"])
        contact = []
        if personal.get("email"): contact.append(personal["email"])
        if personal.get("phone"): contact.append(personal["phone"])
        if personal.get("city"): contact.append(personal["city"])
        if personal.get("linkedin_url"): contact.append(personal["linkedin_url"])
        if contact:
            lines.append(" | ".join(contact))
        return "\n".join(lines)

    def _format_skills(self, skills: List[Dict]) -> str:
        if not skills:
            return ""
        by_category = {}
        for skill in skills:
            cat = skill.get("category", "other")
            by_category.setdefault(cat, []).append(skill["name"])

        lines = []
        cat_names = {
            "programming_languages": "Programming Languages",
            "backend": "Backend",
            "frontend": "Frontend",
            "databases": "Databases",
            "cloud": "Cloud",
            "devops": "DevOps",
            "ai_ml": "AI/ML",
            "tools": "Tools",
            "other": "Other Skills"
        }
        for cat, skill_list in by_category.items():
            lines.append(f"{cat_names.get(cat, cat)}: {', '.join(skill_list)}")
        return "\n".join(lines)

    def _format_experiences(self, experiences: List[Dict]) -> str:
        if not experiences:
            return ""
        lines = []
        for exp in experiences:
            header = f"{exp.get('role', 'Role')} at {exp.get('company', 'Company')}"
            if exp.get("employment_type"):
                header += f" ({exp['employment_type']})"
            lines.append(header)
            if exp.get("location"):
                lines.append(f"Location: {exp['location']}")
            if exp.get("description"):
                lines.append(exp["description"])
            if exp.get("verified_responsibilities"):
                lines.append("Responsibilities:")
                for resp in exp["verified_responsibilities"].split("\n"):
                    if resp.strip():
                        lines.append(f"  {resp.strip()}")
            if exp.get("verified_achievements"):
                lines.append("Achievements:")
                for ach in exp["verified_achievements"].split("\n"):
                    if ach.strip():
                        lines.append(f"  {ach.strip()}")
            if exp.get("technologies_used"):
                lines.append(f"Technologies: {exp['technologies_used']}")
            lines.append("")
        return "\n".join(lines)

    def _format_projects(self, projects: List[Dict]) -> str:
        if not projects:
            return ""
        lines = []
        for proj in projects:
            lines.append(f"{proj.get('name', 'Project')}")
            if proj.get("description"):
                lines.append(proj["description"])
            if proj.get("technologies"):
                lines.append(f"Technologies: {proj['technologies']}")
            if proj.get("responsibilities"):
                for resp in proj["responsibilities"].split("\n"):
                    if resp.strip():
                        lines.append(f"  {resp.strip()}")
            if proj.get("github_url"):
                lines.append(f"GitHub: {proj['github_url']}")
            lines.append("")
        return "\n".join(lines)

    def _format_education(self, education: List[Dict]) -> str:
        if not education:
            return ""
        lines = []
        for edu in education:
            line = f"{edu.get('degree', 'Degree')}"
            if edu.get("field"):
                line += f" in {edu['field']}"
            line += f", {edu.get('institution', 'Institution')}"
            lines.append(line)
        return "\n".join(lines)

    def _format_certifications(self, certifications: List[Dict]) -> str:
        if not certifications:
            return ""
        lines = []
        for cert in certifications:
            line = f"{cert.get('name', 'Certification')}"
            if cert.get("issuing_organization"):
                line += f" - {cert['issuing_organization']}"
            lines.append(line)
        return "\n".join(lines)
