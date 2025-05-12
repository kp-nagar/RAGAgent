from typing import List
from fastapi import UploadFile
from langchain_community.document_loaders import PDFPlumberLoader

from constants.constants import TEMP_DIR_STORE_FILES
from rag_handler.vector_store_handler import documents_vector_store
from utils.file_io import save_uploaded_file
from utils.logger import logger


async def process_and_index_documents(files: List[UploadFile]):
    """
    Function which takes files and copy them into temp folder and load them using PDFPlumberLoader.
    then pass documents to documents_vector_store function which help for indexing.
    :param files:
    :return:
    """
    try:
        documents = []
        logger.info(f"loading files.")
        for file in files:
            file_path = await save_uploaded_file(file, TEMP_DIR_STORE_FILES)

            loader = PDFPlumberLoader(file_path)
            docs = loader.load()
            documents.extend(docs)
        logger.info(f"all files loaded.")
        await documents_vector_store(documents)
    except Exception as e:
        logger.error(f"Error: process_and_index_documents: {e}")
        raise Exception("Facing issue in file upload please try after sometime.")
