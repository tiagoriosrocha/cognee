from typing import List
from openai import AzureOpenAI
import asyncio

from cognee.infrastructure.databases.vector.embeddings.EmbeddingEngine import (
    EmbeddingEngine,
)
from cognee.infrastructure.databases.exceptions import EmbeddingException
from cognee.shared.rate_limiting import embedding_rate_limiter_context_manager
from cognee.shared.logging_utils import get_logger

from cognee.infrastructure.llm.tokenizer.TikToken import TikTokenTokenizer
import os

logger = get_logger("AzureOpenAIEmbeddingEngine")


class AzureOpenAIEmbeddingEngine(EmbeddingEngine):
    """
    Embedding engine usando o SDK oficial AzureOpenAI.
    Compatível com o gateway Petrobras (OpenAI-compatible).
    """

    def __init__(
        self,
        model: str,
        dimensions: int,
        api_key: str,
        endpoint: str,
        api_version: str,
        max_completion_tokens: int = 8192,
        batch_size: int = 100,
    ):
        self.model = model
        self.dimensions = dimensions
        self.batch_size = batch_size
        self.max_completion_tokens = max_completion_tokens

        self.tokenizer_model = os.getenv(
            "EMBEDDING_TOKENIZER_MODEL",
            "text-embedding-3-small"
        )

        self.tokenizer = TikTokenTokenizer(
            model=self.tokenizer_model,
            max_completion_tokens=self.max_completion_tokens,
        )


        self.client = AzureOpenAI(
            api_key=api_key,
            base_url=endpoint,
            api_version=api_version,
        )

    # --------------------------------------------------
    # EMBEDDINGS (async — Cognee espera async)
    # --------------------------------------------------
    async def embed_text(self, texts: List[str]) -> List[List[float]]:
        try:
            async with embedding_rate_limiter_context_manager():
                # AzureOpenAI é sync → roda em thread
                response = await asyncio.to_thread(
                    self.client.embeddings.create,
                    model=self.model,
                    input=texts,
                )

            return [item.embedding for item in response.data]

        except Exception as e:
            logger.error(f"AzureOpenAI embedding error: {e}")
            raise EmbeddingException(
                f"Failed to create embeddings using model {self.model}"
            ) from e

    # --------------------------------------------------
    # METADADOS
    # --------------------------------------------------
    def get_vector_size(self) -> int:
        return self.dimensions

    def get_batch_size(self) -> int:
        return self.batch_size
