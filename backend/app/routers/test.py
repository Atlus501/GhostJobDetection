from fastapi import APIRouter, Depends, status
from typing import Annotated

from services.ghost_job_predictor import GhostJobPredictor
from services.llm_record_keeper import LLMRecordKeeper
from services.text_evaluator import TextEvaluator

from schemas.request import TestRequest
from schemas.job import Job
from schemas.llmresponse import LLMResponse
from schemas.model import Predictors  # Imported with standard PascalCase class name

from dependencies import (
    get_ghost_job_predictor,
    get_llm_record_keeper,
    get_text_evaluator,
)

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK)
async def test(
    test_request: TestRequest,
    ghost_job_predictor: Annotated[GhostJobPredictor, Depends(get_ghost_job_predictor)],
    llm_record_keeper: Annotated[LLMRecordKeeper, Depends(get_llm_record_keeper)],
    text_evaluator: Annotated[TextEvaluator, Depends(get_text_evaluator)],
):
    # 1. Search vector DB for existing evaluation record
    # Fixed typo: test_request.position
    found, record = await llm_record_keeper.search_record(
        test_request.company,
        test_request.position,
        test_request.description
    )

    score = record.score if found else None

    # 2. If not found, run LLM evaluation
    if not found:
        # Convert TestRequest -> Job schema (extra fields dropped automatically)
        job = Job(**test_request.model_dump())
        record_text = await text_evaluator.rate_job(job)

        record_text = record_text.strip()
        # Fixed typo: "Final Rating: " instead of "Final Ranting: "
        split = record_text.rsplit("Final Rating: ", 1)

        # Parse score safely
        score = float(split[-1].strip()) if len(split) > 1 else 0.0

        # Construct LLM response payload
        llm_payload = test_request.model_dump()
        llm_payload["ghost_job_risk"] = score
        llm_payload["response"] = record_text

        llm_response_obj = LLMResponse(**llm_payload)
        await llm_record_keeper.upsert_record(llm_response_obj)

    # 3. Prepare features for tabular ML classifier
    predictor_data = test_request.model_dump()
    predictor_data["vagueness_score"] = score
    predictor_data["salary_present"] = "salary" in predictor_data

    # Fixed: Unpack dictionary into schema (**predictor_data)
    predictors_obj = Predictors(**predictor_data)

    # 4. Predict ghost job class & probability
    prediction, probability = ghost_job_predictor.predict(predictors_obj)

    return {
        "prediction": prediction,
        "probability": probability,
        "evaluation_notes": record if found else record_text
    }