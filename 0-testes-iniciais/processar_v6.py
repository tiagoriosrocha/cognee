import cognee
import asyncio
import json
import csv
import os
import logging
from cognee.modules.search.types import SearchType  # Importado para usar os tipos de busca

TEXT_LIMIT = 200  # Limite para truncar textos longos

def truncate_text_fields_only(graph_results, limit=TEXT_LIMIT):
    """
    Trunca apenas os campos 'text' dentro de source_properties e target_properties,
    mantendo intacta toda a estrutura do grafo.
    """
    truncated = []
    for item in graph_results:
        item_copy = item.copy()
        # Trunca texto do nó de origem, se existir
        if 'source_properties' in item_copy and 'text' in item_copy['source_properties']:
            item_copy['source_properties'] = item_copy['source_properties'].copy()
            text = item_copy['source_properties']['text']
            if len(text) > limit:
                item_copy['source_properties']['text'] = text[:limit] + " ...[TRUNCADO]"
        # Trunca texto do nó de destino, se existir
        if 'target_properties' in item_copy and 'text' in item_copy['target_properties']:
            item_copy['target_properties'] = item_copy['target_properties'].copy()
            text = item_copy['target_properties']['text']
            if len(text) > limit:
                item_copy['target_properties']['text'] = text[:limit] + " ...[TRUNCADO]"
        truncated.append(item_copy)
    return truncated


async def main():
    # --- 1. CARREGAMENTO DOS DADOS DE UM ARQUIVO EXTERNO ---
    json_input_filename = 'dataset.json'
    csv_output_filename = 'respostas_v6.csv'

    try:
        with open(json_input_filename, 'r', encoding='utf-8') as f:
            records = json.load(f)
        print(f"Sucesso: {len(records)} registros carregados de '{json_input_filename}'.")
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{json_input_filename}' não foi encontrado. Certifique-se de que ele está no mesmo diretório que o script.")
        return
    except json.JSONDecodeError:
        print(f"ERRO: O arquivo '{json_input_filename}' contém um JSON inválido. Verifique a formatação.")
        return

    # --- 2. PREPARAÇÃO DO ARQUIVO DE SAÍDA CSV ---
    with open(csv_output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'pergunta','resposta_esperada','graph_completion_cot', 'cypher_result'
        ])

    # --- 3. PROCESSAMENTO DE CADA REGISTRO ---
    total_records = len(records)
    for i, record in enumerate(records):
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)

        try:
            context_data = record["context"]
            query_text = record["question"]
            expected_answer = record["answer"]
        except KeyError as e:
            print(f"AVISO: Registro {i + 1}/{total_records} pulado por não conter a chave esperada: {e}")
            continue

        print(f"Processando registro {i + 1}/{total_records}: {query_text}")

        text_parts = []
        for title, sentences in context_data:
            text_parts.append(f"{title}\n{' '.join(sentences)}")
        text = "\n\n".join(text_parts)

        # Processamento com Cognee
        await cognee.add(text)
        await cognee.cognify()

        print(f" -> Executando buscas para o registro {i + 1}...")
        # results_chunks = await cognee.search(query_text=query_text, query_type=SearchType.CHUNKS, top_k=3)
        # results_graph_completion = await cognee.search(query_text=query_text, query_type=SearchType.GRAPH_COMPLETION, top_k=5)
        # results_graph_summary = await cognee.search(query_text=query_text, query_type=SearchType.GRAPH_SUMMARY_COMPLETION, top_k=5)
        results_graph_cot = await cognee.search(query_text=query_text, query_type=SearchType.GRAPH_COMPLETION_COT, top_k=7)

        # --- Consulta Cypher para retornar entidades e relacionamentos ---
        cypher_query = """
        MATCH (n)-[r]->(m)
        RETURN n.id AS source_id, labels(n) AS source_labels, properties(n) AS source_properties,
            type(r) AS relationship,
            m.id AS target_id, labels(m) AS target_labels, properties(m) AS target_properties
        """
        results_cypher_raw = await cognee.search(query_text=cypher_query, query_type=SearchType.CYPHER)
        results_cypher = truncate_text_fields_only(results_cypher_raw, limit=TEXT_LIMIT)

        # Formata respostas para CSV
        generated_graph_cot = " | ".join(map(str, results_graph_cot)) if results_graph_cot else "Nenhuma resposta"
        generated_cypher = " | ".join(map(str, results_cypher)) if results_cypher else "Nenhuma resposta"

        # Salva no CSV
        with open(csv_output_filename, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                query_text,
                expected_answer,
                # generated_chunks,
                # generated_graph_completion,
                # generated_graph_summary,
                generated_graph_cot,
                generated_cypher
            ])

        print(f" -> Registro {i + 1} salvo em '{csv_output_filename}'.\n")

    print(f"Processamento concluído. Verifique o arquivo '{csv_output_filename}'.")


if __name__ == '__main__':
    asyncio.run(main())
