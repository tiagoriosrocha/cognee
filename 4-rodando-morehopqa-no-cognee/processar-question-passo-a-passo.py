import cognee
import asyncio
import json
import logging
import os

from cognee.api.v1.search import SearchType
from cognee.api.v1.visualize.visualize import visualize_graph

# Dados JSON recebidos
json_data_string = """
{
    "_id": "5ae789615542997ec2727695_12",
    "question": "How many letters are there between the first and last letters of the first name of the director of a 2004 film where Kam Heskin plays Paige Morgan in?",
    "answer_type": "number",
    "reasoning_type": "Commonsense, Arithmetic",
    "question_decomposition": [
        {
            "sub_id": "1",
            "question": "Kam Heskin plays Paige Morgan in which 2004 film?",
            "answer": "The Prince and Me"
        },
        {
            "sub_id": "2",
            "question": "Who is the director of The Prince and Me?",
            "answer": "Martha Coolidge"
        },
        {
            "sub_id": "3",
            "question": "What is the first name of Martha Coolidge?",
            "answer": "Martha"
        },
        {
            "sub_id": "4",
            "question": "How many letters are between the first and last letter of 'Martha'?",
            "answer": "4"
        }
    ],
    "context": [
        [
            "The Prince and Me",
            [
                "The Prince and Me is a 2004 romantic comedy film directed by Martha Coolidge, and starring Julia Stiles, Luke Mably, and Ben Miller, with Miranda Richardson, James Fox, and Alberta Watson.",
                " The film focuses on Paige Morgan, a pre-med college student in Wisconsin, who is pursued by a prince posing as a normal college student."
            ]
        ],
        [
            "Kam Heskin",
            [
                "Kam Heskin (born Kam Erika Heskin on May 8, 1973) is an American actress.",
                " She began her career playing Caitlin Richards Deschanel on the NBC daytime soap opera \\"Sunset Beach\\" (1998–1999), before appearing in films \\"Planet of the Apes\\" (2001 and \\"Catch Me If You Can\\" (2002).",
                " Heskin went to play Elizabeth Bennet in the 2003 independent film \\"\\", and Paige Morgan in the \\"The Prince and Me\\" film franchise (2006–2010)."
            ]
        ]
    ]
}
"""

async def main():
    # 1. CARREGAR E PREPARAR DADOS
    print(" PASSO 1: Carregando e preparando dados do JSON...")
    data = json.loads(json_data_string)

    # Extrai os textos de contexto originais
    initial_context_texts = []
    for title, paragraphs in data.get("context", []):
        initial_context_texts.append(title)
        initial_context_texts.extend(paragraphs)

    # Adiciona metadados como contexto para "preparar" o modelo
    initial_context_texts.append(f"O tipo de resposta esperada para a pergunta final é: {data.get('answer_type')}.")
    initial_context_texts.append(f"O tipo de raciocínio necessário é: {data.get('reasoning_type')}.")

    # Extrai as perguntas
    main_question = data.get("question")
    sub_questions = [item['question'] for item in data.get("question_decomposition", [])]
    
    print(f"Contexto inicial com {len(initial_context_texts)} sentenças.")
    print(f"Pergunta principal: '{main_question}'")
    print("Sub-perguntas a serem executadas em ordem:")
    for i, sq in enumerate(sub_questions, 1):
        print(f"  {i}. {sq}")

    # 2. CRIAR O GRAFO DE CONHECIMENTO INICIAL
    print("\n PASSO 2: Criando o Grafo de Conhecimento inicial...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    await cognee.add(initial_context_texts)
    await cognee.cognify()
    print("Grafo de conhecimento inicial criado.")

    # 3. EXECUTAR SUB-PERGUNTAS EM CADEIA
    print("\n PASSO 3: Executando sub-perguntas para testar o raciocínio em cadeia...")
    sub_question_results = []
    for question_text in sub_questions:
        print(f"\n  > Perguntando: '{question_text}'")
        search_result = await cognee.search(
            query_type=SearchType.GRAPH_COMPLETION,
            query_text=question_text,
        )
        print(f"  < Resposta recebida: {search_result}")
        sub_question_results.append({
            "sub_question": question_text,
            "answer": search_result,
        })

    # 4. EXECUTAR PERGUNTA PRINCIPAL
    print("\n PASSO 4: Executando a pergunta principal...")
    final_answer = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text=main_question,
    )
    print(f"Resposta final recebida: {final_answer}")

    # 5. EXPORTAR O GRAFO FINAL
    print("\n PASSO 5: Exportando o estado final do grafo de conhecimento...")
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
    final_graph_relations = await cognee.search(query_text=cypher_query_all_relations, query_type=SearchType.CYPHER)
    print("Exportação do grafo concluída.")

    # 6. GERAR O JSON FINAL
    print("\n PASSO 6: Gerando o arquivo de saída 'resultado_final.json'...")
    final_output = {
        "sub_question_results": sub_question_results,
        "final_answer": final_answer,
        "final_graph_relations": final_graph_relations,
    }

    output_filename = "resultado_final.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)
    
    print(f"Arquivo '{output_filename}' criado com sucesso.")

    # (Opcional) Visualizar o grafo final
    print("\n(Opcional) Gerando visualização do grafo em 'graph.html'...")
    await visualize_graph()
    print("Visualização concluída.")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())