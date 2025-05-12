from langchain.prompts import ChatPromptTemplate
import re

from rag_handler.models_handler.prompts import SYSTEM_PROMPT
from rag_handler.state_types import AgentState


def get_prompt(state: AgentState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"Context: {state['documents']}\nQuestion: {state['question']}")
    ]).format()
    return prompt


def clean_response(text: str) -> str:
    return re.sub(r'\s*\n\s*', ' ', text).strip()
