from zai import ZaiClient
import asyncio
import json
from pydantic import BaseModel, Field

from config.settings import settings

from monitoring.decorators import track_dependency

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
    @track_dependency("glm")
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

        response_json = str(response.choices[0].message.content)

        return JobEvaluationResult.model_validate_json(response_json)

    async def message(self, system_prompt : str, user_prompt : str):
        result = await asyncio.to_thread(self.send_message, system_prompt, user_prompt)
        return result