import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from config.config import settings
from constants.constants import VECTOR_DB_DIR
from utils.logger import logger


async def documents_vector_store(documents):
    """
    Function which create index od given documents
    :param documents:
    :return:
    """
    try:
        logger.info(f"embedding documents")
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        embeddings = OpenAIEmbeddings()
        logger.info(f"laoded embedding model.")
        db = FAISS.from_documents(chunks, embeddings)
        logger.info(f"embedding done for documents.")
        db.save_local(VECTOR_DB_DIR)
        logger.info(f"saved embedding to dir: {VECTOR_DB_DIR}")
    except Exception as e:
        logger.error(f"Error: process_and_index_documents: {e}")
        raise Exception("Facing issue in file upload please try after sometime.")
