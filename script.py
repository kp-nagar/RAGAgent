from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END
from langchain.prompts import ChatPromptTemplate
from typing_extensions import TypedDict
from typing import List
from enum import Enum
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chat_models import init_chat_model
import logging
from termcolor import colored

load_dotenv()

logging.basicConfig(level=logging.INFO)
for noisy_logger in ["pdfminer", "urllib3", "langchain", "faiss", "httpx"]:
    logging.getLogger(noisy_logger).setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


DOCS_DIR = "./docs"
VECTOR_DB_DIR = "faiss_index"
OPENAI_MODEL = "gpt-3.5-turbo"
ANTHROPIC_MODEL = "claude-3-5-sonnet-latest"
SYSTEM_PROMPT = """You are a helpful assistant. Use only the information provided in the context and previous 
questions to answer the user's current question. 

Do not use any external knowledge or make assumptions beyond the context. 
If the answer is not found in the context, respond with:

"I’m sorry, but I couldn’t find the answer to your question in the provided documents."
Don't give any answer other than the one in the above sentence.

Be concise, accurate, and do not invent or infer information."""


class ModelChoice(str, Enum):
    OPENAI = "openai"
    CLAUDE = "claude"
    BOTH = "both"


class AgentState(TypedDict):
    question: str
    model_choice: ModelChoice
    documents: List[str]
    openai_answer: str
    claude_answer: str
    previous_qna: List[str]


prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Context: {context}\n\nPrevious Questions:\n{history}\n\nCurrent Question:\n{question}")
])


def build_history(state: AgentState):
    return "\n".join(state["previous_qna"][-3:])


def get_prompt(state: AgentState):
    history = build_history(state)
    return prompt_template.format(context=state['documents'], question=state['question'], history=history)


logger.info("Initializing vector store...")
embeddings = OpenAIEmbeddings()


def get_vector_store():
    if os.path.exists(VECTOR_DB_DIR):
        logger.info("Loading existing vector store...")
        vector_db = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)
        return vector_db
    logger.info("Creating new vector store...")
    pdf_files = [os.path.join(DOCS_DIR, file) for file in os.listdir(DOCS_DIR) if file.lower().endswith(".pdf")]
    documents = []
    for file in pdf_files:
        logger.info(f"Loading file: {file}")
        loader = PDFPlumberLoader(file)
        documents.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local(VECTOR_DB_DIR)
    return vector_db


vector_store = get_vector_store()

open_model = init_chat_model(OPENAI_MODEL, model_provider="openai")
claude_model = init_chat_model(ANTHROPIC_MODEL, model_provider="anthropic")


def ask_user(_):
    question = input("\nAsk your question (or type 'exit' to stop.): ")
    if question.strip().lower() == "exit":
        raise SystemExit("You requested to exit.")
    while True:
        model_choice = input("Choose model (openai/claude/both): ").strip().lower()
        if model_choice in ["openai", "claude", "both"]:
            break
        logger.info("Invalid choice. Please choose 'openai', 'claude', or 'both'.")
    return {
        "question": question,
        "model_choice": model_choice,
        "documents": [],
        "openai_answer": "",
        "claude_answer": "",
        "previous_qna": []
    }


def retrieve_docs(state: AgentState):
    if state["previous_qna"]:
        context = " ".join(state["previous_qna"][-3:])
    else:
        context = state["question"]

    results = vector_store.similarity_search(context, k=5)
    state["documents"] = [doc.page_content for doc in results]
    return state


def run_openai(state: AgentState):
    prompt = get_prompt(state)
    response = open_model.invoke(prompt)
    state["openai_answer"] = response.content.strip()
    return state


def run_claude(state: AgentState):
    prompt = get_prompt(state)
    response = claude_model.invoke(prompt)
    state["claude_answer"] = response.content.strip()
    return state


def display_result(state: AgentState):
    q = state["question"]
    if state.get("openai_answer"):
        print(colored("\n>> OpenAI Answer:\n", "cyan"))
        print(state["openai_answer"])
        state["previous_qna"].append(f"User: {q}\nOpenAI: {state['openai_answer']}")
    if state.get("claude_answer"):
        print(colored("\n>> Claude Answer:\n", "magenta"))
        print(state["claude_answer"])
        state["previous_qna"].append(f"User: {q}\nClaude: {state['claude_answer']}")
    return state


def model_router(state: AgentState):
    return state["model_choice"]


def openai_router(state: AgentState):
    return "run_claude" if state["model_choice"] == "both" else "display"


# Start Workflow
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

app = graph.compile()


persistent_state = {
    "previous_qna": []
}

while True:
    try:
        user_state = ask_user({})
        user_state["previous_qna"] = persistent_state["previous_qna"]
        updated_state = app.invoke(user_state)
        persistent_state["previous_qna"] = updated_state["previous_qna"]
    except SystemExit as e:
        logger.info(str(e))
        break
    except Exception as e:
        logger.exception(e)
        exit()
