from src.llm_driver.prompts.prompt_manager import PromptManager
from src.llm_driver.agents.agents import AgentFactory, LLMProvider
from pydantic import BaseModel
from typing import Union

class LLMDriver:
    def __init__(self, model_name: str, provider: LLMProvider, response_model: BaseModel, temperature: Union[float, None] = None):
        self.prompt_manager = PromptManager()
        self.provider = provider
        self.agent_factory = AgentFactory(provider)
        self.recommendation_agent = self.agent_factory.create_agent(
            model_name=model_name,
            temperature=temperature,
            response_model=response_model
        )

    def get_feedback(self, scoring_rubric: str, resume_text: str, job_description: str):
        prompt= self.prompt_manager.get_feedback_prompt(
            scoring_rubric=scoring_rubric,
            resume_text=resume_text,
            job_description=job_description,
        )

        response = self.recommendation_agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]}
        )
       
        return response["structured_response"]

    def extract_skils(self, resume_text: str):
        prompt = self.prompt_manager.get_skill_extraction_prompt(
            resume_text=resume_text
        )

        response = self.recommendation_agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]}
        )

        return response["structured_response"].skills
    
    def extract_job_details(self, job_description: str):
        prompt = self.prompt_manager.get_job_description_details_prompt(
            job_description=job_description
        )

        response = self.recommendation_agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]}
        )

        return response["structured_response"]
    
    async def get_feedback_async(self, scoring_rubric: str, resume_text: str, job_description: str):
        prompt = self.prompt_manager.get_feedback_prompt(
            scoring_rubric=scoring_rubric,
            resume_text=resume_text,
            job_description=job_description,
        )
        
        response = await self.recommendation_agent.ainvoke(
            {"messages": [{"role": "user", "content": prompt}]}
        )
        return response["structured_response"]
    

    
    
