from fastapi import APIRouter, status, Request, Depends
from typing import Annotated

from dependencies import get_ghost_job_reporter

from services.ghost_job_reporter import GhostJobReporter

from schemas.model import data_entry

router = APIRouter()

"""
Route for posting confirm ghost or non-ghost job postings
"""
@router.post("/", status_code=status.HTTP_200_OK)
async def report(entry : data_entry, 
                ghost_job_reporter : Annotated[GhostJobReporter, Depends(get_ghost_job_reporter)],
                request Request):

    result = await ghost_job_reporter.report(entry)
    return {"status" : result} 