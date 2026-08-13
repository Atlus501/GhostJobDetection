import logging 

from pinecone import AsyncPinecone, ServerlessSpec

from config.settings import settings

from monitoring.decorators import track_dependency

"""
Class for managing the pinecone database
"""
class PineconeDB:
    """
    Constructor for the pinecone manager
    """
    def __init__(self, index_name):
        self.pc = AsyncPinecone(api_key=settings.PINECONE_API)
        self.index_name = index_name
        self.index_host: str | None = None
        self.namespace = settings.PINECONE_NAMESPACE
        self.logger = logging.getLogger(__name__)

    """
    Initializes the index of the pinecone database
    """
    async def initialize(self) -> None:
        """Set up index for Integrated Embeddings and cache the host."""
        # Create integrated index if it doesn't exist
        try:
            if not await self.pc.has_index(self.index_name):
                await self.pc.create_index_for_model(
                    name=self.index_name,
                    cloud="aws",
                    region="us-east-1",
                    embed={
                        "model": "multilingual-e5-large",
                        "field_map": {"text": "chunk_text"}  # Maps 'chunk_text' field to embeddings
                    }
                )

            desc = await self.pc.describe_index(self.index_name)
            self.index_host = desc.host

            self.logger.info("Pinecone connection has successfully been set")

        except Exception as e:
            self.logger.error(f"Something has gone wrong with index initialization. {str(e)}")
            raise RuntimeError("Something has gone wrong with index initialization.")

    """
    async function for upserting a job record
    """
    @track_dependency('pinecone')
    async def upsert(self, record: dict) -> None:
        """Upsert job text and metadata using Pinecone's server-side embedding generation."""

        try:
            if not self.index_host:
                raise RuntimeError("PineconeManager must be initialized before upserting.")

            index = self.pc.IndexAsyncio(host=self.index_host)

            await index.upsert_records(
                records=[record],
                namespace=self.namespace,
            )
        except Exception as e:
            self.logger.error(f"Something has gone wrong with pinecone upsertion. {str(e)}")
            raise RuntimeError("Something has gone wrong with pinecone upsertion.")

    """
    async function for searching a job record
    """
    @track_dependency('pinecone')
    async def search(self, search_text, response_fields, threshold=0.85, top_k=2):
        if not self.index_host:
            raise RuntimeError("PineconeManager must be initialized before searching data")

        try: 
            index = self.pc.IndexAsyncio(host=self.index_host)

            results = await index.search_records(
                namespace=self.namespace,
                query={
                    "inputs": {"text": search_text},
                    "top_k": top_k,
                },
                fields=response_fields,
            )

            for item in results.result.hits:
                score = getattr(item, "score", None) or item.get("_score", 0.0)
                if score > threshold:
                    return True, item

            return False, None

        except Exception as e:
            self.logger.error(f"A problem gone wrong with pinecone search. {str(e)}")
            raise RuntimeError("Something has gone wrong with database collection")
      

    """
    Function to close the Pinecone connection
    """
    async def close(self) -> None:
        """Gracefully close HTTP client connections."""
        if self.pc:
            await self.pc.close()

        self.logger.info("The pinecone conenction ahs shut down")