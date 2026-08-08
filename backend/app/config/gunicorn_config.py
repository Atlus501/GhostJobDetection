import multiprocessing
from typing import Literal
from pydantic import model_validator
from pydantic_settings import BaseSettings

class GunicornSettings(BaseSettings):
    environment: Literal["production", "development", "testing"] = "production"
    cpu_cores: int = multiprocessing.cpu_count()
    workers: int | None = None
    worker_connections: int = 1000

    # Model validator calculates dynamic defaults AFTER the instance is initialized
    @model_validator(mode="after")
    def set_dynamic_workers(self) -> "GunicornSettings":
        if self.workers is None:
            if self.environment == "development":
                self.workers = 1
            elif self.environment == "testing":
                self.workers = 2
            else:
                self.workers = min(self.cpu_cores * 2, 4)
        return self


# Instantiate settings (Pydantic will automatically load ENV variables like ENVIRONMENT=development)
_settings = GunicornSettings()

# ------------------------------------------------------------------
# Global Gunicorn Variables (Gunicorn automatically reads these!)
# ------------------------------------------------------------------
bind = "0.0.0.0:80"
worker_class = "uvicorn.workers.UvicornWorker"
workers = _settings.workers
worker_connections = _settings.worker_connections

if _settings.environment == "development":
    reload = True
    reload_dirs = ["/app"]
    loglevel = "debug"
    timeout = 0
else:
    preload_app = True
    max_requests = 5000
    max_requests_jitter = 1000
    timeout = 30
    keepalive = 5
    loglevel = "info"

#activate the gunicorn instance with the following command: gunicorn -c ./config/gunicorn_config.py app:app