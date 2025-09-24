import cognee
import asyncio
import json
import logging
import os

from cognee.api.v1.search import SearchType
from cognee.api.v1.visualize.visualize import visualize_graph
#from cognee.shared.utils import setup_logging

# Dados JSON recebidos
json_data_string = """
{
    "_id": "5ae789615542997ec2727695_12",
    "question": "How many letters are there between the first and last letters of the first name of the director of a 2004 film where Kam Heskin plays Paige Morgan in?",
    "answer": "4",
    "previous_question": "Kam Heskin plays Paige Morgan in a 2004 film directed by who?",
    "previous_answer": "Martha Coolidge",
    "question_decomposition": [
        {
            "sub_id": "1",
            "question": "Kam Heskin plays Paige Morgan in which 2004 film?",
            "answer": "The Prince and Me",
            "paragraph_support_title": "Kam Heskin"
        },
        {
            "sub_id": "2",
            "question": "The Prince and Me is directed by who?",
            "answer": "Martha Coolidge",
            "paragraph_support_title": "The Prince and Me"
        },
        {
            "sub_id": "3",
            "question": "How many letters are there between the first and last letters of the first name of Martha Coolidge?",
            "answer": "4",
            "paragraph_support_title": "",
            "details": [
                {
                    "sub_id": "3_1",
                    "question": "What is the first name of Martha Coolidge?",
                    "answer": "Martha",
                    "paragraph_support_title": ""
                },
                {
                    "sub_id": "3_2",
                    "question": "How many letters are there between the first and last letters of Martha?",
                    "answer": "4",
                    "paragraph_support_title": ""
                }
            ]
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
    ],
    "answer_type": "number",
    "previous_answer_type": "person",
    "no_of_hops": 2,
    "reasoning_type": "Commonsense, Arithmetic",
    "pattern": "How many letters are there between the first and last letters of the first name of #Name?",
    "subquestion_patterns": [
        "What is the first name of #Name?",
        "How many letters are there between the first and last letters of #Ans1?"
    ],
    "cutted_question": "the director of a 2004 film where Kam Heskin plays Paige Morgan in",
    "ques_on_last_hop": "How many letters are there between the first and last letters of the first name of the director of The Prince and Me?"
}
"""

async def main():
    # Carrega e prepara os dados do JSON
    print("Carregando e processando dados do JSON...")
    data = json.loads(json_data_string)

    #carrega a ontologia
    ontology_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "wikidata-20250919-lexemes-BETA.ttl"
    )

    context_texts = []
    for title, paragraphs in data.get("context", []):
        context_texts.append(title)
        context_texts.extend(paragraphs)

    question = data.get("question")
    
    if not context_texts or not question:
        print("Erro: Não foi possível encontrar 'context' ou 'question' no JSON.")
        return

    print(f"Contexto extraído com {len(context_texts)} sentenças.")
    print(f"Pergunta a ser feita: '{question}'")


    # Passo 1: Redefinir sistema
    print("\nPasso 1: Redefinindo dados e estado do sistema...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    print("Sistema redefinido.")

    # Passo 2: Adicionar dados
    print("\nPasso 2: Adicionando dados de contexto do JSON...")
    await cognee.add(context_texts)
    print("Dados adicionados.")

    # Passo 3: Criar o grafo de conhecimento carregando a ontologia
    print("\nPasso 3: Criando o grafo de conhecimento...")
    await cognee.cognify(ontology_file_path=ontology_path)
    print("Grafo de conhecimento criado.")

    # Passo 4: Consultar o grafo com a pergunta principal
    print("\nPasso 4: Consultando o grafo com a pergunta do JSON...")
    final_answer = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text=question,
    )
    print("\n--- RESULTADO DA PESQUISA ---")
    print(final_answer)
    print("-----------------------------")

    # Passo 5: Exportar as relações do grafo
    print("\nPasso 5: Exportando as relações do grafo...")
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
    graph_relations = await cognee.search(query_text=cypher_query_all_relations, query_type=SearchType.CYPHER)
    print("Relações do grafo exportadas.")

    # Passo 6: Gerar o arquivo JSON de saída
    print("\nPasso 6: Gerando o arquivo de saída 'resultado_final.json'...")
    
    final_output = {
        "final_answer": str(final_answer).strip("[]'\""),
        "graph_relations": graph_relations,
    }

    output_filename = "resultado_final.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)
    
    print(f"Arquivo '{output_filename}' criado com sucesso.")
    
    # (Opcional) Passo 7: Visualizar o grafo
    print("\nPasso 7: Gerando visualização do grafo em 'graph.html'...")
    await visualize_graph()
    print("Visualização concluída.")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())