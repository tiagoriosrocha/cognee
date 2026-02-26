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
            resp = await self.aclient.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": text_input},
                    {"role": "system", "content": system_prompt},
                ],
                # Define o formato da resposta usando JSON Schema baseado no modelo Pydantic
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": response_model.__name__, # Nome da classe (ex: KnowledgeGraph)
                        "schema": response_model.model_json_schema(), # Gera o esquema JSON esperado
                    },
                },
                max_completion_tokens=self.max_completion_tokens,
                **kwargs,
            )

        # Extrai o conteúdo da resposta do assistente
        content = resp.choices[0].message.content

        # Debug: Imprime no console o que a Azure retornou antes de tentar validar
        print(f"Content recebido do Azure OpenAI  (assíncrono): {content}")

        # Converte a string JSON recebida de volta em um objeto Pydantic validado
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
        Versão síncrona do método acima. Utilizada em partes do código
        que não suportam await/async.
        """

        # Lógica idêntica ao assíncrono, mas usando o cliente síncrono (self.client)
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

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": text_input},
                {"role": "system", "content": system_prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "schema": response_model.model_json_schema(),
                },
            },
            max_completion_tokens=self.max_completion_tokens,
            **kwargs,
        )

        content = resp.choices[0].message.content

        # Debug: Imprime no console o que a Azure retornou antes de tentar validar
        print(f"Content recebido do Azure OpenAI (síncrono): {content}")

        # Validação final do JSON contra o modelo Pydantic
        return response_model.model_validate_json(content)