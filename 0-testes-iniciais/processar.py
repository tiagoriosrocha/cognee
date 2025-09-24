import cognee
import asyncio
import json
import csv
import os
import logging

# --- CONFIGURAÇÃO DE LOGS (Opcional, para um terminal mais limpo) ---
# Silencia as mensagens de nível 'INFO' da biblioteca cognee e outras
logging.getLogger("cognee").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


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
    # Escreve o cabeçalho uma única vez, apagando qualquer conteúdo anterior.
    with open(csv_output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['resposta_esperada', 'resposta_gerada', 'pergunta'])


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
        results = await cognee.search(query_text=query_text)

        generated_answer = " | ".join(map(str, results)) if results else "Nenhuma resposta gerada"

        # Abre o CSV em modo 'append' para adicionar a nova linha e fecha em seguida
        with open(csv_output_filename, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Adicionada a pergunta no CSV para melhor contexto
            csv_writer.writerow([expected_answer, generated_answer, query_text])

        print(f" -> Registro {i + 1} salvo em '{csv_output_filename}'.\n")

    print(f"Processamento concluído. Verifique o arquivo '{csv_output_filename}'.")


if __name__ == '__main__':
    asyncio.run(main())
