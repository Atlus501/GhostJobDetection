from zai import ZaiClient
import asyncio

from config.settings import settings

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
    def send_message(self, message : str):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": message,
                },
            ],
            thinking={
                "type": "enabled",  # Optional: "disabled" or "enabled", default is "enabled"
            },
            max_tokens=4096,
            temperature=0.6,
        )

        return response.choices[0].message.content

    async def message(self, message : str):
        result = await asyncio.to_thread(send_message, message)
        return result