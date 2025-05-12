from schemas.schema import QueryResponse
from rag_handler.graph_handler import build_graph
from utils.logger import logger

app_graph = build_graph()


async def run_query(question: str, model_choice: str) -> QueryResponse:
    state = {
        "question": question,
        "model_choice": model_choice.lower(),
        "documents": [],
        "openai_answer": "",
        "claude_answer": ""
    }
    logger.info(f"state: {state}.")
    result = app_graph.invoke(state)
    logger.info(f"result: {result}.")
    return QueryResponse(
        openai_answer=result.get("openai_answer"),
        claude_answer=result.get("claude_answer")
    )
