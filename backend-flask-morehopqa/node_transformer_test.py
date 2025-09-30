import json
from node_transformer import NodeTransformer

nodes_data = [('c374b21e-c57e-5fb4-95c5-d881f9c3ad30', {'id': 'c374b21e-c57e-5fb4-95c5-d881f9c3ad30', 'text': 'Champ Bailey', 'chunk_index': 0, 'chunk_size': 5, 'updated_at': 1759254644133, 'cut_type': 'sentence_cut', 'ontology_valid': False, 'created_at': 1759254623157, 'topological_rank': 0, 'type': 'DocumentChunk', 'metadata': '{"index_fields": ["text"]}', 'version': 1}), ('c18fa801-2fef-5f9d-b032-32a04e607d31', {'id': 'c18fa801-2fef-5f9d-b032-32a04e607d31', 'updated_at': 1759254849951, 'description': 'Former NFL cornerback', 'name': 'champ bailey', 'ontology_valid': False, 'created_at': 1759254838981, 'topological_rank': 0, 'type': 'Entity', 'metadata': '{"index_fields": ["name"]}', 'version': 1}), ('d072ba0f-e1a9-58bf-9974-e1802adc8134', {'id': 'd072ba0f-e1a9-58bf-9974-e1802adc8134', 'updated_at': 1759254849951, 'description': 'person', 'name': 'person', 'ontology_valid': False, 'created_at': 1759254838981, 'topological_rank': 0, 'type': 'EntityType', 'metadata': '{"index_fields": ["name"]}', 'version': 1})] # Adicione o resto dos seus nós aqui
edges_data = [('c374b21e-c57e-5fb4-95c5-d881f9c3ad30', 'c18fa801-2fef-5f9d-b032-32a04e607d31', 'contains', {'updated_at': '2025-09-30 17:50:32', 'source_node_id': 'c374b21e-c57e-5fb4-95c5-d881f9c3ad30', 'target_node_id': 'c18fa801-2fef-5f9d-b032-32a04e607d31', 'relationship_name': 'contains'}), ('c18fa801-2fef-5f9d-b032-32a04e607d31', 'd072ba0f-e1a9-58bf-9974-e1802adc8134', 'is_a', {'updated_at': '2025-09-30 17:50:32', 'source_node_id': 'c18fa801-2fef-5f9d-b032-32a04e607d31', 'target_node_id': 'd072ba0f-e1a9-58bf-9974-e1802adc8134', 'relationship_name': 'is_a'}), ('c374b21e-c57e-5fb4-95c5-d881f9c3ad30', 'a0fbd29f-f529-51a5-b5de-616938f8c14a', 'contains', {'updated_at': '2025-09-30 17:50:32', 'source_node_id': 'c374b21e-c57e-5fb4-95c5-d881f9c3ad30', 'target_node_id': 'a0fbd29f-f529-51a5-b5de-616938f8c14a', 'relationship_name': 'contains'})] # Adicione o resto das suas arestas aqui

if __name__ == "__main__":
    print("--- INICIANDO PROCESSAMENTO DO GRAFO ---")

    # Processando os Nós
    try:
        node_transformer = NodeTransformer()
        nodes_result = node_transformer.transform(nodes_data)
        print("\n--- RESULTADO (NODES) ---")
        print(json.dumps(nodes_result, indent=4, ensure_ascii=False))
    except ValueError as e:
        print(f"\n--- ERRO AO PROCESSAR NÓS ---")
        print(f"Detalhes: {e}")
