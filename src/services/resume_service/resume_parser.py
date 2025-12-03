import os
from langchain_community.document_loaders import PyPDFLoader

class ResumeParser:
    def __init__(self, max_chars: int = 12000):
        self.max_chars = max_chars

    def _load_pdf(self, file_path: str) -> str:

        if not os.path.exists(file_path):
            raise FileNotFoundError("Resume file not found")

        ext = os.path.splitext(file_path)[1].lower()
        if ext != ".pdf":
            raise ValueError("Resume must be a PDF file.")

        loader = PyPDFLoader(file_path)
        pages = loader.load()

        if len(pages) != 1:
            raise ValueError(f"Resume must be exactly 1 page. Provided PDF has {len(pages)} pages.")

        return pages[0].page_content

    def _clean_text(self, text: str) -> str:
        cleaned = " ".join(text.split())
        if len(cleaned) > self.max_chars:
            cleaned = cleaned[: self.max_chars] + "\n...[truncated]"
        return cleaned
