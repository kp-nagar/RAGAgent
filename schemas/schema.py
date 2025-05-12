from enum import Enum
from pydantic import BaseModel


class UploadResponse(BaseModel):
    status: str
    message: str


class QueryResponse(BaseModel):
    openai_answer: str
    claude_answer: str


class ModelChoice(str, Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    BOTH = "both"
