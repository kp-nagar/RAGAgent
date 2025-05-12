from typing_extensions import TypedDict
from typing import List


class AgentState(TypedDict):
    question: str
    model_choice: str
    documents: List[str]
    openai_answer: str
    claude_answer: str
