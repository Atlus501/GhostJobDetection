from fastapi import FastAPI

from infrastructure.databases.pinecone_manager import PineconeManager
from infrastructure.databases.ghost_job import GhostJobDB

async def setup_infrastructure(app : FastAPI):
    app.state.pinecone = PineconeManager()
    await app.state.pinecone.initialize()

    app.state.ghost_job = GhostJobDB()

async def close_infrastructure(app : FastAPI):
    await app.state.pinecone.close()