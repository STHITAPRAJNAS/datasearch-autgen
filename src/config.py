import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_host: str = os.environ.get("DATABASE_HOST")
    database_port: str = os.environ.get("DATABASE_PORT")
    database_user: str = os.environ.get("DATABASE_USER")
    database_password: str = os.environ.get("DATABASE_PASSWORD")
    database_name: str = os.environ.get("DATABASE_NAME")

    bedrock_client: str = os.environ.get("BEDROCK_CLIENT")
    model_id: str = os.environ.get("MODEL_ID")
    embedding_model_id: str = os.environ.get("EMBEDDING_MODEL_ID")
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()