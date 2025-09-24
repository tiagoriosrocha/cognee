import json
from pyvis.network import Network

# --- 1. Carregar JSON do grafo ---
json_filename = "grafo.json"  # Coloque o caminho correto do seu arquivo JSON
with open(json_filename, "r", encoding="utf-8") as f:
    edges_data = json.load(f)

# --- 2. Criar o grafo PyVis ---
net = Network(height="750px", width="100%", notebook=False, directed=True)
net.force_atlas_2based()  # Melhor visualização automática

# --- 3. Definir cores por tipo de nó ---
type_colors = {
    "DocumentChunk": "orange",
    "TextDocument": "lightblue",
    "Entity": "green",
    "EntityType": "red"
}

# --- 4. Adicionar nós e arestas ---
nodes_added = set()
for edge in edges_data:
    src_id = edge["source_id"]
    tgt_id = edge["target_id"]

    # Determinar tipo do nó principal
    src_type = None
    for label in edge["source_labels"]:
        if label not in ["__Node__"]:
            src_type = label
    tgt_type = None
    for label in edge["target_labels"]:
        if label not in ["__Node__"]:
            tgt_type = label

    # Adicionar nós se ainda não existirem
    if src_id not in nodes_added:
        net.add_node(src_id, label=src_type or src_id, title=str(edge["source_labels"]), color=type_colors.get(src_type, "gray"))
        nodes_added.add(src_id)
    if tgt_id not in nodes_added:
        net.add_node(tgt_id, label=tgt_type or tgt_id, title=str(edge["target_labels"]), color=type_colors.get(tgt_type, "gray"))
        nodes_added.add(tgt_id)

    # Adicionar aresta com o relacionamento
    net.add_edge(src_id, tgt_id, label=edge["relationship"], arrows="to")

# --- 5. Gerar HTML interativo ---
output_file = "grafo_interativo.html"
net.show(output_file, notebook=False)
print(f"Grafo gerado: {output_file}. Abra no navegador para visualizar interativamente.")
