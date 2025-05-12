from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
