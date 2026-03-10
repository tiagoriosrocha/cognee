from typing import Type
from pydantic import BaseModel, ValidationError
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

    # ------------------------------------------------
    # REPAIR PROMPT BUILDERS
    # ------------------------------------------------

    def _build_repair_prompt(self, previous_output: str, validation_error: str) -> str:
        return f"""
    The previous JSON output failed validation against the required Pydantic schema.

    Validation error:
    {validation_error}

    Previous invalid JSON:
    {previous_output}

    You must fix the JSON so it strictly matches the required schema.

    REQUIRED JSON STRUCTURE

    {{
    "nodes": [
        {{
        "id": "uuid-v4-string",
        "name": "string",
        "type": "string",
        "description": "string"
        }}
    ],
    "edges": [
        {{
        "source_node_id": "uuid-v4-string",
        "target_node_id": "uuid-v4-string",
        "relationship_name": "string"
        }}
    ]
    }}

    FIELD RULES

    Nodes MUST contain:
    - id
    - name
    - type
    - description

    Edges MUST contain:
    - source_node_id
    - target_node_id
    - relationship_name

    UUID RULES

    All node IDs must be valid UUID v4 strings.

    Format:
    xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx

    Rules:
    - lowercase only
    - hexadecimal characters only (0-9, a-f)
    - 36 characters total

    VALID EXAMPLE

    {{
    "nodes": [
        {{
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Townsend Coleman",
        "type": "Person",
        "description": "American voice actor known for animated television roles."
        }},
        {{
        "id": "1f0d2b3a-0c45-4f34-9a62-b0f6c9d6e2f1",
        "name": "United States",
        "type": "Country",
        "description": "Country of nationality."
        }}
    ],
    "edges": [
        {{
        "source_node_id": "550e8400-e29b-41d4-a716-446655440000",
        "target_node_id": "1f0d2b3a-0c45-4f34-9a62-b0f6c9d6e2f1",
        "relationship_name": "has_nationality"
        }}
    ]
    }}

    REPAIR INSTRUCTIONS

    - Do not remove valid information
    - Only repair invalid or missing fields
    - Ensure the final output is valid JSON
    - Ensure all required fields exist
    - Ensure UUID format is correct
    - Preserve the original meaning of the graph

    Return ONLY the corrected JSON.
    """

    # ------------------------------------------------
    # REPAIR FUNCTIONS
    # ------------------------------------------------

    async def _repair_structured_output_async(
        self,
        system_prompt: str,
        previous_output: str,
        validation_error: str,
    ) -> str:

        repair_prompt = self._build_repair_prompt(previous_output, validation_error)

        async with llm_rate_limiter_context_manager():
            resp = await self.aclient.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": repair_prompt},
                ],
                max_completion_tokens=self.max_completion_tokens,
            )

        return resp.choices[0].message.content

    def _repair_structured_output_sync(
        self,
        system_prompt: str,
        previous_output: str,
        validation_error: str,
    ) -> str:

        repair_prompt = self._build_repair_prompt(previous_output, validation_error)

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": repair_prompt},
            ],
            max_tokens=self.max_completion_tokens,
        )

        return resp.choices[0].message.content

    # ------------------------------------------------
    # SAFE VALIDATION
    # ------------------------------------------------

    async def _safe_validate_async(
        self,
        content: str,
        response_model: Type[BaseModel],
        system_prompt: str,
        max_retries: int = 2,
    ) -> BaseModel:

        for attempt in range(max_retries + 1):

            try:
                return response_model.model_validate_json(content)

            except ValidationError as e:

                if attempt >= max_retries:
                    raise

                print("⚠ Structured output validation failed. Attempting repair...")
                print(e)

                content = await self._repair_structured_output_async(
                    system_prompt,
                    content,
                    str(e),
                )

    def _safe_validate_sync(
        self,
        content: str,
        response_model: Type[BaseModel],
        system_prompt: str,
        max_retries: int = 2,
    ) -> BaseModel:

        for attempt in range(max_retries + 1):

            try:
                return response_model.model_validate_json(content)

            except ValidationError as e:

                if attempt >= max_retries:
                    raise

                print("⚠ Structured output validation failed. Attempting repair...")
                print(e)

                content = self._repair_structured_output_sync( #gera novamente o content corrigido...
                    system_prompt,
                    content,
                    str(e),
                )

    # ------------------------------------------------
    # ASYNC GENERATION
    # ------------------------------------------------

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

        if response_model is str:
            return content

        return await self._safe_validate_async(
            content,
            response_model,
            system_prompt,
        )

    # ------------------------------------------------
    # SYNC GENERATION
    # ------------------------------------------------

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

        if response_model is str:
            return content

        return self._safe_validate_sync(
            content,
            response_model,
            system_prompt,
        )