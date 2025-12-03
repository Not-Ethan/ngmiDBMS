from src.llm_driver.prompts.prompt_templates import (
    NGMI_BASE_PROMPT, SKILL_EXTRACTION_PROMPT
)

class PromptManager:

    @staticmethod
    def get_feedback_prompt(scoring_rubric: str, resume_text: str, job_description: str) -> str:
        return NGMI_BASE_PROMPT.format(
            scoring_rubric=scoring_rubric,
            resume_text=resume_text,
            job_description=job_description
        )
    
    @staticmethod
    def get_skill_extraction_prompt(resume_text: str) -> str:
        return SKILL_EXTRACTION_PROMPT.format(
            resume_text=resume_text
        )