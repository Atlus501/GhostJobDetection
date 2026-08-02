from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Literal

current_dir = Path(__file__).resolve().parent
env_path = current_dir.parent /".env"

class Settings(BaseSettings):
  ZAI_API : str # Changed from ZAI_API_KEY to zai_api to match likely environment variable name
  GLM_MODEL : str
  PINECONE_API : str
  PINECONE_INDEX_NAME : str
  PINECONE_NAMESPACE : str
  LOGGER_FILE : str
  MONGODB_USERNAME : str
  MONGODB_PASSWORD : str
  HOST : str
  PORT : int
  ENVIRONMENT : Literal["testing", "development", "production"]

  model_config = SettingsConfigDict(env_file=env_path, 
                                    env_file_encoding="utf-8", 
                                    extra="ignore")

settings = Settings()