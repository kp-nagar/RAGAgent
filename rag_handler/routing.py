from rag_handler.state_types import AgentState


def model_router(state: AgentState):
    if state["model_choice"] == "openai":
        return "openai"
    elif state["model_choice"] == "claude":
        return "claude"
    elif state["model_choice"] == "both":
        return "both"
    else:
        raise ValueError("Invalid model choice")


def openai_router(state: AgentState):
    return "run_claude" if state["model_choice"] == "both" else "display"
