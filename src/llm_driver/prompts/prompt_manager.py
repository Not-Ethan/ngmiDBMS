from src.llm_driver.prompts.prompt_templates import (
    NGMI_PROMPT_TEMPLATE, SKILL_EXTRACTION_PROMPT_TEMPLATE, JOB_DESCRIPTION_DETAILS_PROMPT_TEMPLATE
)

class PromptManager:

    @staticmethod
    def get_feedback_prompt(scoring_rubric: str, resume_text: str, job_description: str) -> str:
        return NGMI_PROMPT_TEMPLATE.format(
            scoring_rubric=scoring_rubric,
            resume_text=resume_text,
            job_description=job_description
        )
    
    @staticmethod
    def get_skill_extraction_prompt(resume_text: str) -> str:
        return SKILL_EXTRACTION_PROMPT_TEMPLATE.format(
            resume_text=resume_text
        )
    
    @staticmethod
    def get_job_description_details_prompt(job_description: str) -> str:
        return JOB_DESCRIPTION_DETAILS_PROMPT_TEMPLATE.format(
            job_description_text=job_description
        )