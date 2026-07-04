"""Resume parsing service for PDF and DOCX files."""
import os
import io
from typing import Dict, Any
from PyPDF2 import PdfReader
from docx import Document
from app.core.config import settings
from app.ai.provider import ai_provider

class ResumeParserService:
    """Service for parsing uploaded resume files."""

    ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}

    def validate_file(self, filename: str, content: bytes) -> tuple[bool, str]:
        ext = os.path.splitext(filename.lower())[1]
        if ext not in self.ALLOWED_EXTENSIONS:
            return False, f"Invalid file type. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
        if len(content) > settings.max_upload_size:
            return False, f"File too large. Max size: {settings.max_upload_size / 1024 / 1024}MB"
        return True, ""

    def extract_text(self, filename: str, content: bytes) -> str:
        ext = os.path.splitext(filename.lower())[1]
        if ext == ".pdf":
            return self._extract_pdf(content)
        elif ext in {".docx", ".doc"}:
            return self._extract_docx(content)
        return ""

    def _extract_pdf(self, content: bytes) -> str:
        try:
            reader = PdfReader(io.BytesIO(content))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")

    def _extract_docx(self, content: bytes) -> str:
        try:
            doc = Document(io.BytesIO(content))
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            return text.strip()
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")

    async def parse_resume(self, filename: str, content: bytes) -> Dict[str, Any]:
        valid, error = self.validate_file(filename, content)
        if not valid:
            raise ValueError(error)

        raw_text = self.extract_text(filename, content)
        if not raw_text:
            raise ValueError("Could not extract text from file")

        structured_data = await ai_provider.parse_resume_content(raw_text)
        return {
            "raw_text": raw_text,
            "structured_data": structured_data
        }

resume_parser_service = ResumeParserService()
