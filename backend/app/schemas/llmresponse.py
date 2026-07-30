from datetime import datetime
from pydantic import BaseModel, Field

from infrastructure.hash import id_hash

"""
Class for the datatype used for storing database records
"""
class LLMResponse(BaseModel):
    company: str
    position: str
    ghost_job_risk: float
    response: str
    created: datetime = Field(default_factory=datetime.utcnow)
    job_description : str

    @property
    def record_id(self) -> str:
        """Generate a deterministic ID based on company and position."""
        raw_key = f"{self.company}:{self.position}"
        return id_hash(raw_key)

    def to_pinecone_record(self, text_field_name: str = "chunk_text") -> dict:
        """Convert Pydantic model into a valid Pinecone record with _id."""
        data = self.model_dump(mode="json")  # Serializes datetime to ISO-string
        data["_id"] = self.record_id
        data[text_field_name] = f"Company:{self.company}/ Position:{self.position}/ Description:{self.job_description[:1000]}"
        return data