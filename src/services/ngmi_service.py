from src.llm_driver.llm_driver import LLMDriver
from src.llm_driver.prompts.prompt_templates import NGMI_RUBRIC
from src.llm_driver.agents.agents import LLMProvider, ModelNames
from src.llm_driver.schemas.response_schemas import NotGonnaMakeItScoreResponseSchema

def generate_ngmi(resume_text: str, job_description: str) -> tuple[float, str]:
    llm_driver = LLMDriver(model_name=ModelNames.GPT_4O_MINI, provider=LLMProvider.OPENAI, response_model=NotGonnaMakeItScoreResponseSchema, temperature=0.6)

    return llm_driver.get_feedback(
        scoring_rubric=NGMI_RUBRIC,
        resume_text=resume_text,
        job_description=job_description
    )