# processar_cognee.py
import sys
import json
import asyncio
import cognee
from cognee.api.v1.search import SearchType

def processar_dados(dados_recebidos):
    """
    Função síncrona que serve como ponto de entrada.
    Ela define e executa a rotina assíncrona principal.
    """
    async def executar_processamento_assincrono(dados):
        """
        Esta função contém toda a lógica assíncrona do cognee.
        É uma adaptação direta do seu script de processamento principal.
        """
        # Extrai o contexto e a pergunta dos dados recebidos
        context_texts = []
        for title, paragraphs in dados.get("context", []):
            context_texts.append(title)
            context_texts.extend(paragraphs)

        question = dados.get("question")

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
        
        # Retorna o dicionário para ser convertido em JSON
        return final_output

    # Aqui é a "ponte": chamamos a função assíncrona a partir da síncrona
    # e esperamos ela terminar para obter o resultado.
    return asyncio.run(executar_processamento_assincrono(dados_recebidos))


if __name__ == "__main__":
    try:
        # 1. Lê os dados da entrada padrão (enviados pelo Flask)
        dados_de_entrada_str = sys.stdin.read()
        
        # 2. Converte a string JSON para um dicionário Python
        dados_json = json.loads(dados_de_entrada_str)
        
        # 3. Chama a função de processamento principal
        resultado = processar_dados(dados_json)
        
        # 4. Converte o resultado de volta para uma string JSON
        # Usamos separadores compactos para a resposta da API
        resultado_json_str = json.dumps(resultado, separators=(',', ':'))
        
        # 5. Imprime o resultado na saída padrão para o Flask capturar
        print(resultado_json_str)
        
    except Exception as e:
        # Em caso de erro, cria um JSON de erro e o imprime na saída de erro
        erro_json = json.dumps({
            "status": "erro_no_processamento",
            "detalhe": str(e)
        })
        # Imprime na saída de erro padrão (stderr)
        print(erro_json, file=sys.stderr)
        sys.exit(1) # Termina o script com um código de erro