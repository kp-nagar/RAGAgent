import logging

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT
)

for noisy_logger in ["pdfminer", "urllib3", "langchain", "faiss", "httpx"]:
    logging.getLogger(noisy_logger).setLevel(logging.ERROR)

logger = logging.getLogger("rag-agent")
