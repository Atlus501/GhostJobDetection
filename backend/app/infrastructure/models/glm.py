from zai import ZaiClient
import asyncio
import json
from pydantic import BaseModel, Field

from config.settings import settings

class JobEvaluationResult(BaseModel):
    reasoning: str
    risk_factors: list[str]
    final_rating: float = Field(..., ge=0.0, le=10.0)

"""
Class for connecting with GLM to evalute job posting vaguness
"""
class GLM:
    """
    Constructor for the GLM class
    """
    def __init__(self, model):
        self.model_name = model
        self.client = ZaiClient(api_key=settings.ZAI_API)

    """
    Function for sending messages
    """
    def send_message(self, system_prompt : str, user_prompt : str):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role" : "user",
                    "content" : user_prompt,
                },
            ],
            thinking={
                "type": "enabled",  # Optional: "disabled" or "enabled", default is "enabled"
            },
            max_tokens=4096,
            temperature=0.0,
        )

        return JobEvaluationResult.model_validate_json(response.choices[0].message.content)

    async def message(self, message : str):
        result = await asyncio.to_thread(send_message, message)
        return result