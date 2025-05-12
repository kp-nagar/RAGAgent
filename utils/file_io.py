import os
from fastapi import UploadFile

from utils.logger import logger


async def save_uploaded_file(file: UploadFile, directory: str) -> str:
    """
    THis function of save file into give directory.
    :param file:
    :param directory:
    :return: file path.
    """
    try:
        logger.info(f"saving file: {file.filename}")
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"saved file: {file.filename}")
    except Exception as e:
        logger.error(f"Error: save_uploaded_file: {e}")
        raise Exception("Facing issue in file upload please try after sometime.")
    else:
        return file_path
