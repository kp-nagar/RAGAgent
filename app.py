from fastapi import FastAPI
import os

from constants.constants import TEMP_DIR_STORE_FILES
from routes.router import router
from utils.logger import logger

app = FastAPI()

logger.info("Starting FastAPI app...")

#This will execute if temp folder not created.
if not os.path.exists(TEMP_DIR_STORE_FILES):
    os.makedirs(TEMP_DIR_STORE_FILES)


app.include_router(router)
