import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from typing import Union
from enum import StrEnum

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class ModelNames(StrEnum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"
    GPT_o3_MINI = "o3-mini"
    GPT_o4_MINI = "o4-mini"
    GPT_4_1 = "gpt-4.1-2025-04-14"
    GPT_5 = "gpt-5-2025-08-07"

class LLMProvider:
    OPENAI = "openai"

def create_openai_agent(model_name: str, response_model: BaseModel, temperature: Union[float, None] = None):

    if temperature is None:
        return create_agent(
            model = ChatOpenAI(model=model_name, api_key=OPENAI_API_KEY),
            response_format = response_model
        )
    
    return create_agent(
        model = ChatOpenAI(model=model_name, api_key=OPENAI_API_KEY, temperature=temperature),
        response_format = response_model
    )

class AgentFactory:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def create_agent(self, model_name: str, response_model: BaseModel, temperature: Union[float, None] = None):
        if self.provider == LLMProvider.OPENAI:
            return create_openai_agent(model_name, response_model, temperature)