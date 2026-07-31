from schemas.llmresponse import LLMResponse

"""
Class for keeping records about the kinds of llm responses
"""
class LLMRecordKeeper:
    def __init__ (self, db):
        self.vector_db = db

    async def search_record(self, company, position, description):
        search_text = f"Company:{company}/ Position:{position}/ Description:{description[:1000]}"
        response_fields = ["ghost_job_risk", "response"]

        response = await self.vector_db.search(search_text, response_fields)
        return response

    async def upsert_record(self, record : LLMResponse):
        record = record.to_pinecone_record(text_field_name="chunk_text")

        response = await self.vector_db.upsert(record)
        return response
