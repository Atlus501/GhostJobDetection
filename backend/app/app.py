from fastpi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.config.settings import settings

from app.infrastructure.databases.pinecone_manager import PineconeManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO, file=settings.LOGGER_FILE)

    app.state.pinecone = PineconeManager()
    await app.state.pinecone.initialize()

    logging.info("ghost job detection has begun")

    yield

    await app.state.pinecone.close()

    logging.info("ghost job detection shutdown is completed")

app = FastAPI(
    title="GhostJob",
    version="1.0.0",
    description="This is the async backend for detecting potenial ghost jobs",
    lifespan=lifespan,
)