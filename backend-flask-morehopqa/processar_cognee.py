import asyncio
import os
from logging import Logger
from cognee.shared.logging_utils import get_logger
import cognee
from cognee.modules.visualization.cognee_network_visualization import (
    cognee_network_visualization,
)
from cognee.infrastructure.databases.graph import get_graph_engine
from cognee.api.v1.search import SearchType

from node_transformer import NodeTransformer
from edge_transformer import EdgeTransformer

# Criamos uma instância do logger para usar na classe
logger = get_logger("ProcessarCognee")

class ProcessarCognee:
    """
    Encapsula toda a lógica de processamento do Cognee.
    O processamento é iniciado pelo método executar(), que recebe os dados.
    """
        
    async def _executar_processamento_assincrono(self, dados_recebidos: dict) -> dict:
        """
        Método privado que contém a lógica assíncrona do cognee.
        """
        logger.info("Dados recebidos da interface: %s", dados_recebidos)

        context_texts = []
        for title, paragraphs in dados_recebidos.get("context", []):
            context_texts.append(title)
            context_texts.extend(paragraphs)

        question = dados_recebidos.get("question")

        if not context_texts or not question:
            raise ValueError("Não foi possível encontrar 'context' ou 'question' nos dados recebidos.")

        # Passo 1: Redefinir sistema
        logger.info("Realizando prune dos dados e do sistema...")
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)

        # Passo 2: Adicionar dados de contexto
        logger.info("Adicionando contexto...")
        await cognee.add(context_texts)

        # Passo 3: carregando a ontologia
        ontology_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "schemaorg_complete_formato_cognee.owl"
        )   

        # Passo 4: Criar o grafo de conhecimento
        logger.info("Iniciando cognify...")
        await cognee.cognify(ontology_file_path=ontology_path)

        # Passo 5: Executando a consulta
        logger.info("Executando a busca no grafo...")
        final_answer = await cognee.search(
            query_type=SearchType.GRAPH_COMPLETION,
            query_text=question,
        )

        # Passo 6: Carregando o grafo completo
        logger.info("Carregando dados do grafo para visualização...")
        graph_engine = await get_graph_engine()
        graph_data = await graph_engine.get_graph_data()

        # Passo 7: Transforma os nós e arestas para o formato do front-end
        nodeTransformer = NodeTransformer()
        transformed_nodes = nodeTransformer.transform(graph_data[0])

        edgeTransformer = EdgeTransformer()
        transformed_edges = edgeTransformer.transform(graph_data[1])

        # Passo 8: Monta o dicionário final
        final_output = {
            "final_answer": str(final_answer).strip("[]'\""),
            "nodes": transformed_nodes["nodes"],
            "edges": transformed_edges["edges"],
        }
        
        logger.info("Processamento concluído com sucesso.")
        return final_output

    # ################### ESTA É A PARTE CORRIGIDA ###################
    def executar(self, dados_recebidos: dict) -> dict:
        """
        Ponto de entrada síncrono que o Flask irá chamar.
        Gerencia o loop de eventos asyncio de forma segura para threads,
        garantindo que cada thread tenha seu próprio loop ativo.
        """
        try:
            # Tenta obter o loop de eventos já existente para a thread atual.
            loop = asyncio.get_running_loop()
        except RuntimeError:  # 'RuntimeError: There is no current event loop...'
            # Se não houver loop na thread, cria um novo e o define como o atual.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Garante que o loop está rodando para executar a tarefa.
        if loop.is_running():
            # Se já está rodando (caso raro, mas possível), cria uma task futura.
            future = asyncio.run_coroutine_threadsafe(self._executar_processamento_assincrono(dados_recebidos), loop)
            return future.result()
        else:
            # Se não está rodando, usa 'run_until_complete', que é o caso mais comum.
            return loop.run_until_complete(self._executar_processamento_assincrono(dados_recebidos))








# import asyncio
# import os
# from logging import Logger
# from cognee.shared.logging_utils import get_logger
# import cognee
# from cognee.modules.visualization.cognee_network_visualization import (
#     cognee_network_visualization,
# )
# from cognee.infrastructure.databases.graph import get_graph_engine
# from cognee.api.v1.search import SearchType

# from node_transformer import NodeTransformer
# from edge_transformer import EdgeTransformer

# # Criamos uma instância do logger para usar na classe
# logger = get_logger("ProcessarCognee")

# class ProcessarCognee:
#     """
#     Encapsula toda a lógica de processamento do Cognee.
#     O processamento é iniciado pelo método executar(), que recebe os dados.
#     """
    
#     # O logger pode ser passado no construtor para integrar com o do Flask,
#     # ou podemos usar um logger próprio como feito acima.
#     # def __init__(self, logger: Logger):
#     #     self.logger = logger
        
#     async def _executar_processamento_assincrono(self, dados_recebidos: dict) -> dict:
#         """
#         Método privado que contém a lógica assíncrona do cognee.
#         """
#         # ALTERADO: Usando o logger em vez de print
#         logger.info("Dados recebidos da interface: %s", dados_recebidos)

#         # ALTERADO: Usando o parâmetro 'dados_recebidos' diretamente
#         context_texts = []
#         for title, paragraphs in dados_recebidos.get("context", []):
#             context_texts.append(title)
#             context_texts.extend(paragraphs)

#         question = dados_recebidos.get("question")

#         if not context_texts or not question:
#             raise ValueError("Não foi possível encontrar 'context' ou 'question' nos dados recebidos.")

#         # Passo 1: Redefinir sistema
#         logger.info("Realizando prune dos dados e do sistema...")
#         await cognee.prune.prune_data()
#         await cognee.prune.prune_system(metadata=True)

#         # Passo 2: Adicionar dados de contexto
#         logger.info("Adicionando contexto...")
#         await cognee.add(context_texts)

#         # Passo 3: carregando a ontologia
#         ontology_path = os.path.join(
#             os.path.dirname(os.path.abspath(__file__)), "schemaorg.rdf"
#         )   

#         # Passo 4: Criar o grafo de conhecimento
#         logger.info("Iniciando cognify...")
#         await cognee.cognify(ontology_file_path=ontology_path)

#         # Passo 5: Executando a consulta
#         logger.info("Executando a busca no grafo...")
#         final_answer = await cognee.search(
#             query_type=SearchType.GRAPH_COMPLETION,
#             query_text=question,
#         )

#         # Passo 6: Carregando o grafo completo
#         logger.info("Carregando dados do grafo para visualização...")
#         graph_engine = await get_graph_engine()
#         graph_data = await graph_engine.get_graph_data()

#         # Passo 7: Transforma os nós e arestas para o formato do front-end
#         nodeTransformer = NodeTransformer()
#         transformed_nodes = nodeTransformer.transform(graph_data[0])

#         edgeTransformer = EdgeTransformer()
#         transformed_edges = edgeTransformer.transform(graph_data[1])

#         # Passo 8: Monta o dicionário final
#         final_output = {
#             "final_answer": str(final_answer).strip("[]'\""),
#             "nodes": transformed_nodes["nodes"],
#             "edges": transformed_edges["edges"],
#         }
        
#         logger.info("Processamento concluído com sucesso.")
#         return final_output

#     def executar(self, dados_recebidos: dict) -> dict:
#         """
#         Ponto de entrada síncrono que o Flask irá chamar.
#         Inicia o loop de eventos asyncio para rodar o processamento.
#         """
#         return asyncio.run(self._executar_processamento_assincrono(dados_recebidos))