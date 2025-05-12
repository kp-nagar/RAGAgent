import os
from langchain.chat_models import init_chat_model

from config.config import settings
from constants.constants import OPENAI_MODEL
from rag_handler.models_handler.base import get_prompt, clean_response
from rag_handler.state_types import AgentState


def run_openai(state: AgentState):
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    model = init_chat_model(OPENAI_MODEL, model_provider="openai")
    prompt = get_prompt(state)
    response = model.invoke(prompt)
    cleaned_response = clean_response(response.content)
    state["openai_answer"] = cleaned_response
    return state
