from fastapi import APIRouter
from fastapi import Form

from schemas.schema import QueryResponse, ModelChoice
from services.query_service import run_query
from utils.logger import logger

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_model(
    question: str = Form(..., description="You can ask query."),
    model_choice: ModelChoice = Form(..., description="You can choice one options from openai, claude or both.")
):
    """
    This endpoint give answer from model given by model_choice.
    :param question:
    :param model_choice:
    :return:
    """
    logger.info(f"query: {question} and model: {model_choice}")
    return await run_query(question, model_choice)
