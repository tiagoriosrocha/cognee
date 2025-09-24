import cognee
import asyncio
import json
import csv
import os
import logging
from cognee.modules.search.types import SearchType # Importado para usar os tipos de busca

async def main():
    # --- 1. CARREGAMENTO DOS DADOS DE UM ARQUIVO EXTERNO ---
    json_input_filename = 'dataset.json'
    csv_output_filename = 'respostas.csv'

    try:
        with open(json_input_filename, 'r', encoding='utf-8') as f:
            # json.load() lê de um arquivo, ao contrário de json.loads() que lê de uma string
            records = json.load(f)
        print(f"Sucesso: {len(records)} registros carregados de '{json_input_filename}'.")
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{json_input_filename}' não foi encontrado. Certifique-se de que ele está no mesmo diretório que o script.")
        return
    except json.JSONDecodeError:
        print(f"ERRO: O arquivo '{json_input_filename}' contém um JSON inválido. Verifique a formatação.")
        return


    # --- 2. PREPARAÇÃO DO ARQUIVO DE SAÍDA CSV ---
    # Escreve o cabeçalho uma única vez, com colunas para cada tipo de busca.
    with open(csv_output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            'resposta_esperada', 'pergunta', 'chunks',
            'graph_completion', 'graph_summary_completion',
            'graph_completion_cot', 'cypher_result'
        ])


    # --- 3. PROCESSAMENTO DE CADA REGISTRO ---
    total_records = len(records)
    # Usando enumerate para acompanhar o progresso
    for i, record in enumerate(records):
        # Para cada registro, limpa os dados e o estado do sistema do cognee
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(metadata=True)

        # Extração e Formatação dos Dados
        try:
            context_data = record["context"]
            query_text = record["question"]
            expected_answer = record["answer"]
        except KeyError as e:
            print(f"AVISO: Registro {i + 1}/{total_records} pulado por não conter a chave esperada: {e}")
            continue # Pula para o próximo registro

        print(f"Processando registro {i + 1}/{total_records}: {query_text}")

        text_parts = []
        for title, sentences in context_data:
            text_parts.append(f"{title}\n{' '.join(sentences)}")
        text = "\n\n".join(text_parts)

        # Processamento com Cognee
        await cognee.add(text)
        await cognee.cognify()

        # --- Executa os múltiplos tipos de busca ---
        print(f" -> Executando buscas para o registro {i + 1}...")
        results_chunks = await cognee.search(query_text=query_text, query_type=SearchType.CHUNKS)
        results_graph_completion = await cognee.search(query_text=query_text, query_type=SearchType.GRAPH_COMPLETION)
        results_graph_summary = await cognee.search(query_text=query_text, query_type=SearchType.GRAPH_SUMMARY_COMPLETION)
        results_graph_cot = await cognee.search(query_text=query_text, query_type=SearchType.GRAPH_COMPLETION_COT)

        # Para Cypher, usamos uma consulta genérica pois o input não é em linguagem natural
        cypher_query = "MATCH (n) RETURN n.id, labels(n) as labels LIMIT 10"
        results_cypher = await cognee.search(query_text=cypher_query, query_type=SearchType.CYPHER)

        # Formata todas as respostas para string
        generated_chunks = " | ".join(map(str, results_chunks)) if results_chunks else "Nenhuma resposta"
        generated_graph_completion = " | ".join(map(str, results_graph_completion)) if results_graph_completion else "Nenhuma resposta"
        generated_graph_summary = " | ".join(map(str, results_graph_summary)) if results_graph_summary else "Nenhuma resposta"
        generated_graph_cot = " | ".join(map(str, results_graph_cot)) if results_graph_cot else "Nenhuma resposta"
        generated_cypher = " | ".join(map(str, results_cypher)) if results_cypher else "Nenhuma resposta"

        # Abre o CSV em modo 'append' para adicionar a nova linha com todos os resultados
        with open(csv_output_filename, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                expected_answer, query_text, generated_chunks,
                generated_graph_completion, generated_graph_summary,
                generated_graph_cot, generated_cypher
            ])

        print(f" -> Registro {i + 1} salvo em '{csv_output_filename}'.\n")

    print(f"Processamento concluído. Verifique o arquivo '{csv_output_filename}'.")


if __name__ == '__main__':
    asyncio.run(main())
