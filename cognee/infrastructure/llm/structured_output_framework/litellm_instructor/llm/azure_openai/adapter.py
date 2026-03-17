from typing import Type
from pydantic import BaseModel
from openai import AzureOpenAI, AsyncAzureOpenAI

from cognee.infrastructure.llm.structured_output_framework.litellm_instructor.llm.llm_interface import (
    LLMInterface,
)
from cognee.shared.rate_limiting import llm_rate_limiter_context_manager
from cognee.modules.observability.get_observe import get_observe

# Inicializa o decorador de observabilidade para monitorar as gerações do LLM
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
        # Armazena as configurações básicas do modelo e limite de tokens
        self.model = model
        self.max_completion_tokens = max_completion_tokens

        # Inicializa o cliente síncrono da Azure OpenAI
        self.client = AzureOpenAI(
            api_key=api_key,
            base_url=endpoint, # URL do recurso Azure
            api_version=api_version,
        )

        # Inicializa o cliente assíncrono da Azure OpenAI (usado em pipelines de alta performance)
        self.aclient = AsyncAzureOpenAI(
            api_key=api_key,
            base_url=endpoint,
            api_version=api_version,
        )

    # -------------------------------
    # Helper único: build_response_format
    # -------------------------------
    def build_response_format(self, response_model: Type[BaseModel]):
        return {
            "type": "json_schema",
            "json_schema": {
                "name": response_model.__name__,
                "schema": response_model.model_json_schema(),
                "strict": False 
            }
        }

    # -------------------------------
    # ASYNC (Método Assíncrono)
    # -------------------------------
    @observe(as_type="generation")
    async def acreate_structured_output(
        self,
        text_input: str,
        system_prompt: str,
        response_model: Type[BaseModel],
        **kwargs,
    ) -> BaseModel:
        """
        Gera uma saída estruturada de forma assíncrona.
        Se o modelo esperado for uma string, retorna texto puro.
        Caso contrário, força o LLM a seguir um esquema JSON específico.
        """

        # Caso especial: Se o Cognee pedir apenas uma string (ex: teste de conexão ou resumo simples)
        if response_model is str:
            async with llm_rate_limiter_context_manager():
                resp = await self.aclient.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": text_input},
                        {"role": "system", "content": system_prompt},
                    ],
                    max_completion_tokens=self.max_completion_tokens,
                    **kwargs,
                )
            return resp.choices[0].message.content

        # Fluxo Principal: Saída Estruturada (Pydantic)

        system_prompt = f"""
        {system_prompt}

        IMPORTANT:
        You must generate IDs strictly as valid UUID v4 strings.

        UUID format:
        - 36 characters
        - Lowercase
        - Only hexadecimal characters (0-9, a-f)
        - Pattern: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
        - Example: 550e8400-e29b-41d4-a716-446655440000

        Do NOT generate custom IDs like 'rule-01' or 'ruleset-123'.
        Only valid UUID strings are allowed.
        """

        async with llm_rate_limiter_context_manager():
            resp = await self.aclient.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "user", "content": text_input},
                    {"role": "system", "content": system_prompt},
                ],
                # Define o formato da resposta usando JSON Schema baseado no modelo Pydantic
                
                #versao 1
                #response_format=response_model,
                
                #versao 2
                #response_format={
                #    "type": "json_schema",
                #    "json_schema": {
                #        "name": response_model.__name__,
                #        "schema": response_model.model_json_schema(),
                #    },
                #},

                #versao 3 -> evita erro de "Unexpected keyword argument 'strict' in response_format" que ocorre com algumas versões da Azure OpenAI
                response_format=self.build_response_format(response_model),

                max_completion_tokens=self.max_completion_tokens,
                **kwargs,
            )

        # tenta usar parsed automaticamente
        parsed = resp.choices[0].message.parsed
        if parsed is not None:
            print(f"[DEBUG][ASYNC][PARSED]: {parsed}")
            return parsed

        # Extrai o conteúdo da resposta do assistente
        content = resp.choices[0].message.content

        print(f"[DEBUG][ASYNC][RAW]: {content}")

        if content is None:
            raise ValueError("Resposta do modelo veio vazia (content=None)")

        return response_model.model_validate_json(content)

    # -------------------------------
    # SYNC (Método Síncrono)
    # -------------------------------
    def create_structured_output(
        self,
        text_input: str,
        system_prompt: str,
        response_model: Type[BaseModel],
        **kwargs,
    ) -> BaseModel:
        """
        Versão síncrona do método acima.
        """

        if response_model is str:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": text_input},
                    {"role": "system", "content": system_prompt},
                ],
                max_completion_tokens=self.max_completion_tokens,
                **kwargs,
            )
            return resp.choices[0].message.content

        system_prompt = f"""
        {system_prompt}

        IMPORTANT:
        You must generate IDs strictly as valid UUID v4 strings.
        """

        resp = self.client.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "user", "content": text_input},
                {"role": "system", "content": system_prompt},
            ],
            #versao 1
            #response_format=response_model,
            
            #versao 2
            #response_format={
            #    "type": "json_schema",
            #    "json_schema": {
            #        "name": response_model.__name__,
            #        "schema": response_model.model_json_schema(),
            #    },
            #},

            #versao 3
            response_format=self.build_response_format(response_model),

            max_completion_tokens=self.max_completion_tokens,
            **kwargs,
        )

        parsed = resp.choices[0].message.parsed
        if parsed is not None:
            print(f"[DEBUG][SYNC][PARSED]: {parsed}")
            return parsed

        content = resp.choices[0].message.content

        print(f"[DEBUG][SYNC][RAW]: {content}")

        if content is None:
            raise ValueError("Resposta do modelo veio vazia (content=None)")

        return response_model.model_validate_json(content)