import asyncio
import cognee
from cognee.api.v1.search import SearchType

class ProcessarCognee:
    """
    Encapsula toda a lógica de processamento do Cognee.
    Os dados são recebidos no construtor e o processamento é
    iniciado pelo método executar().
    """
    def __init__(self, dados_recebidos: dict):
        """
        Construtor da classe. Recebe os dados JSON como um dicionário Python.
        """
        self.dados = dados_recebidos
        
    async def _executar_processamento_assincrono(self) -> dict:
        """
        Método privado que contém a lógica assíncrona do cognee.
        """
        # Extrai o contexto e a pergunta dos dados armazenados na instância
        context_texts = []
        for title, paragraphs in self.dados.get("context", []):
            context_texts.append(title)
            context_texts.extend(paragraphs)
            #print("context: ", title, paragraphs)

        question = self.dados.get("question")

        if not context_texts or not question:
            raise ValueError("Não foi possível encontrar 'context' ou 'question' nos dados recebidos.")

        # Passo 1: Redefinir sistema (essencial para cada nova requisição)
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)

        # Passo 2: Adicionar dados de contexto
        await cognee.add(context_texts)

        # Passo 3: Criar o grafo de conhecimento
        await cognee.cognify()

        # Passo 4: Consultar o grafo com a pergunta principal
        final_answer = await cognee.search(
            query_type=SearchType.GRAPH_COMPLETION,
            query_text=question,
        )

        # Passo 5: Exportar as relações do grafo
        cypher_query_all_relations = """
        MATCH (n)-[r]->(m)
        RETURN
            n.id AS source_node_id,
            labels(n) AS source_node_labels,
            properties(n).name as source_node_name,
            type(r) AS relationship_type,
            m.id AS target_node_id,
            labels(m) AS target_node_labels,
            properties(m).name as target_node_name
        LIMIT 100
        """
        graph_relations = await cognee.search(
            query_text=cypher_query_all_relations,
            query_type=SearchType.CYPHER
        )

        # Passo 6: Montar o dicionário de saída
        final_output = {
            "final_answer": str(final_answer).strip("[]'\""),
            "graph_relations": graph_relations,
        }
        
        return final_output

    def executar(self) -> dict:
        """
        Ponto de entrada síncrono que o Flask irá chamar.
        Inicia o loop de eventos asyncio para rodar o processamento.
        """
        return asyncio.run(self._executar_processamento_assincrono())
