from typing import Type
from pydantic import BaseModel
from openai import AzureOpenAI, AsyncAzureOpenAI

from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.llm_interface import (
    LLMInterface,
)
from cognee.shared.rate_limiting import llm_rate_limiter_context_manager
from cognee.modules.observability.get_observe import get_observe

observe = get_observe()


class AzureOpenAIAdapter(LLMInterface):
    name = "AzureOpenAI"

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        api_version: str,
        model: str,
        max_completion_tokens: int,
    ):
        self.model = model
        self.max_completion_tokens = max_completion_tokens

        self.client = AzureOpenAI(
            api_key=api_key,
            base_url=endpoint,
            api_version=api_version,
        )

        self.aclient = AsyncAzureOpenAI(
            api_key=api_key,
            base_url=endpoint,
            api_version=api_version,
        )

    # -------------------------------
    # ASYNC
    # -------------------------------
    @observe(as_type="generation")
    async def acreate_structured_output(
        self,
        text_input: str,
        system_prompt: str,
        response_model: Type[BaseModel],
        **kwargs,
    ) -> BaseModel:
        async with llm_rate_limiter_context_manager():
            resp = await self.aclient.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_input},
                ],
                max_completion_tokens=self.max_completion_tokens,
            )

        content = resp.choices[0].message.content

        # Caso especial: response_model == str
        if response_model is str:
            return content

        # Caso normal: Pydantic model
        #return response_model(content=content)
    
        return response_model(
            summary=content,
            description=content
        )

    # -------------------------------
    # SYNC
    # -------------------------------
    def create_structured_output(
        self,
        text_input: str,
        system_prompt: str,
        response_model: Type[BaseModel],
        **kwargs,
    ) -> BaseModel:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_input},
            ],
            max_tokens=self.max_completion_tokens,
        )

        content = resp.choices[0].message.content

        # Caso especial: response_model == str
        if response_model is str:
            return content

        # Caso normal: Pydantic model
        #return response_model(content=content)

        return response_model(
            summary=content,
            description=content
        )
