from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List

from schemas.schema import UploadResponse
from services.file_processor import process_and_index_documents
from utils.logger import logger

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_file(files: List[UploadFile] = File(..., description="Upload one or more PDF files to be indexed.")):
    """
    Using this endpoint you can upload multiple files and it will upload files in temp directory and index them.
    :param files:
    :return: json message.
    """
    try:
        logger.info(f"uploading files: {len(files)}")
        await process_and_index_documents(files)
        logger.info(f"uploaded all files.")
        return {"status": "success", "message": "Documents processed and indexed."}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
