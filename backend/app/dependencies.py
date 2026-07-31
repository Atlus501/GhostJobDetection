# dependencies.py
from fastapi import Request

from services.ghost_job_predictor import GhostJobPredictor
from services.ghost_job_reporter import GhostJobReporter
from services.llm_record_keeper import LLMRecordKeeper
from services.text_evaluator import TextEvaluator

def get_ghost_job_predictor(request: Request) -> GhostJobPredictor:
    return request.app.state.ghost_job_predictor

def get_ghost_job_reporter(request: Request) -> GhostJobReporter:
    return request.app.state.ghost_job_reporter

def get_llm_record_keeper(request : Request) -> LLMRecordKeeper:
    return request.app.state.llm_record_keeper

def get_text_evaluator(request : Request) -> TextEvaluator:
    return requst.app.state.text_evaluator