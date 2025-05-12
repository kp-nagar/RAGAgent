import uvicorn
from config.config import settings


if __name__ == "__main__":
    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
