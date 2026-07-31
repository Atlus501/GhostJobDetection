from pydantic_settings import BaseSettings

class MlflowConfig(BaseSettings):
    bind : str = "127.0.0.1:5000"
    application : str = "GhostJob"

mlflow_config = MlflowConfig()