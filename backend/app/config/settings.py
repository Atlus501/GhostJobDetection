from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from pathlib import Path
from typing import Literal

#env_path = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    AWS_ACCESS_KEY: str
    AWS_SECRET_ACCESS_KEY: str
    ZAI_API : str  # Changed from ZAI_API_KEY to zai_api to match likely environment variable name
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
    S3_BUCKET : str

    @field_validator("*", mode="before")
    @classmethod
    def strip_carriage_returns(cls, v):
        if isinstance(v, str):
            return v.strip("\r\n ")
        return v

    #model_config = SettingsConfigDict(env_file=env_path, extra="ignore")
    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()