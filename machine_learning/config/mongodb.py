from pydantic import BaseSettings, SettingsDict
from pathlib import Path

current_dir = Path(__file__).resolve().parent
env_path = current_dir.parent /".env"

class MongodbSettings(BaseSettings):
    MONGODB_USERNAME : str
    MONGODB_PASSWORD : str

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")

mongodb_config = MongodbSettings()