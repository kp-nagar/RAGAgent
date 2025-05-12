from langgraph.graph import StateGraph, END

from rag_handler.display import display_result
from rag_handler.models_handler.claude_runner import run_claude
from rag_handler.models_handler.openai_runner import run_openai
from rag_handler.retriever import retrieve_docs
from rag_handler.routing import model_router, openai_router
from rag_handler.state_types import AgentState


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("retrieve_docs", retrieve_docs)
    graph.add_node("run_openai", run_openai)
    graph.add_node("run_claude", run_claude)
    graph.add_node("display", display_result)

    graph.set_entry_point("retrieve_docs")

    graph.add_conditional_edges("retrieve_docs", model_router, {
        "openai": "run_openai",
        "claude": "run_claude",
        "both": "run_openai"
    })
    graph.add_conditional_edges("run_openai", openai_router, {
        "run_claude": "run_claude",
        "display": "display"
    })
    graph.add_edge("run_claude", "display")
    graph.add_edge("display", END)

    return graph.compile()
