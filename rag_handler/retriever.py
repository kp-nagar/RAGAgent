from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from config.config import settings
from constants.constants import VECTOR_DB_DIR
from rag_handler.state_types import AgentState


embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)


def retrieve_docs(state: AgentState):
    vector_store = FAISS.load_local(VECTOR_DB_DIR, embeddings, allow_dangerous_deserialization=True)
    results = vector_store.similarity_search(state["question"], k=5)
    state["documents"] = [doc.page_content for doc in results]
    return state
