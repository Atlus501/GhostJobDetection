from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import pathlib

current_dir = Path(__file__).resolve().parent
env_path = current_dir.parent.parent /".env"

class Settings(BaseSettings):
  ZAI_API : str # Changed from ZAI_API_KEY to zai_api to match likely environment variable name
  PINECONE_API : str
  PINECONE_INDEX_NAME : str
  PINECONE_NAMESPACE : str
  LOGGER_FILE : str
  MONGODB_USERNAME : str
  MONGODB_PASSWORD : str

  model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")

settings = Settings()