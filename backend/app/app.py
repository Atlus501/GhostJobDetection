from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import uvicorn

from config.settings import settings

from error_handling.setup import setup_error_handlers
from middlewares.setup import setup_middlewares

from infrastructure.databases.mongodb import MongoDB
from infrastructure.databases.pinecone_db import PineconeDB
from infrastructure.models.boosted_tree import BoostedTree
from infrastructure.models.glm import GLM

from routers.report import router as report_router
from routers.test import router as test_router

from services.ghost_job_predictor import GhostJobPredictor
from services.ghost_job_reporter import GhostJobReporter
from services.llm_record_keeper import LLMRecordKeeper
from services.text_evaluator import TextEvaluator

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO, filename=settings.LOGGER_FILE)

    #sets up mongodbs
    ghost_job_db = MongoDB("GhostJobInfo")
    await ghost_job_db.setup_index(["company", "position"])
    llmresponse_db = PineconeDB("ghostjobs")
    await llmresponse_db.initialize()
    boosted_tree = BoostedTree()
    glm = GLM("glm-4.7-flash")

    app.state.ghost_job_predictor = GhostJobPredictor(boosted_tree)
    app.state.ghost_job_reporter = GhostJobReporter(ghost_job_db)
    app.state.llm_record_keeper = LLMRecordKeeper(llmresponse_db)
    app.state.text_evaluator = TextEvaluator(glm)

    logging.info("ghost job detection has begun")

    yield

    await llmresponse_db.close()

    logging.info("ghost job detection shutdown is completed")

app = FastAPI(
    title="GhostJob",
    version="1.0.0",
    description="This is the async backend for detecting potenial ghost jobs",
    lifespan=lifespan,
    docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
    redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
    openapi_url=None if settings.ENVIRONMENT == "production" else "/openapi.json",
)

#adds the middleware
setup_middlewares(app)

#sets up error handling
setup_error_handlers(app)

app.include_router(report_router, prefix="/report")
app.include_router(test_router, prefix="/test")

if __name__ == "__main__":
    logging.info("uvicorn server has begun listening")
    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)