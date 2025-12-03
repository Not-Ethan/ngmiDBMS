import os
from langchain_community.document_loaders import PyPDFLoader

class ResumeParseError(Exception):
    pass

class ResumeParser:
    def __init__(self, max_chars: int = 12000):
        self.max_chars = max_chars

    def _load_pdf(self, file_path: str) -> str:
        try:
            if not os.path.exists(file_path):
                raise ResumeParseError("Resume file not found")

            ext = os.path.splitext(file_path)[1].lower()
            if ext != ".pdf":
                raise ResumeParseError("Resume must be a PDF file")

            loader = PyPDFLoader(file_path)
            pages = loader.load()

            if not pages:
                raise ResumeParseError("PDF appears to be empty or corrupted")

            if len(pages) > 3:  # Allow up to 3 pages instead of just 1
                raise ResumeParseError(f"Resume too long ({len(pages)} pages). Maximum 3 pages allowed")

            # Combine all pages
            content = "\n".join(page.page_content for page in pages)
            
            if not content.strip():
                raise ResumeParseError("PDF contains no readable text")
                
            return content

        except ResumeParseError:
            raise
        except Exception as e:
            raise ResumeParseError(f"Failed to parse PDF: {str(e)}")

    def _clean_text(self, text: str) -> str:
        if not text:
            raise ResumeParseError("No text to clean")
            
        cleaned = " ".join(text.split())
        if len(cleaned) > self.max_chars:
            cleaned = cleaned[:self.max_chars] + "\n...[truncated]"
        return cleaned
