import os

from langchain.chat_models import init_chat_model

from config.config import settings
from constants.constants import ANTHROPIC_MODEL
from rag_handler.models_handler.base import get_prompt, clean_response
from rag_handler.state_types import AgentState


def run_claude(state: AgentState):
    os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY
    model = init_chat_model(ANTHROPIC_MODEL, model_provider="anthropic")
    prompt = get_prompt(state)
    response = model.invoke(prompt)
    print(response.content)
    cleaned_response = clean_response(response.content)
    print(cleaned_response)
    state["claude_answer"] = cleaned_response
    return state
