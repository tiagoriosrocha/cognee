import json
import ast
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

# Arquivos
INPUT_FILE = "grafo.txt"   # contém lista de dicionários Python
JSON_FILE = "grafo.json"   # saída intermediária em JSON válido
RDF_FILE = "grafo.rdf"     # saída final em RDF (XML)

# Define namespace base
EX = Namespace("http://example.org/")

# Cria grafo RDF
g = Graph()
g.bind("ex", EX)

# A função add_node_properties não é mais necessária, pois os dados não contêm propriedades.
# def add_node_properties(node_uri, properties: dict):
#     """Adiciona propriedades de um nó ao grafo RDF"""
#     for key, value in properties.items():
#         if isinstance(value, bool):
#             g.add((node_uri, EX[key], Literal(value, datatype=XSD.boolean)))
#         elif isinstance(value, int):
#             g.add((node_uri, EX[key], Literal(value, datatype=XSD.integer)))
#         else:
#             g.add((node_uri, EX[key], Literal(str(value))))

# --- Etapa 1: Converter lista de dicionários Python para JSON ---
# Esta parte já estava funcionando corretamente.
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    python_data = ast.literal_eval(f.read())

with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(python_data, f, indent=2, ensure_ascii=False)

print(f"Arquivo {JSON_FILE} criado com sucesso!")

# --- Etapa 2: Ler JSON válido e converter para RDF (CORRIGIDO) ---
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    # CORREÇÃO: Usando as chaves corretas do arquivo grafo.txt
    source_uri = URIRef(EX[entry["source_node_id"]])
    target_uri = URIRef(EX[entry["target_node_id"]])

    # CORREÇÃO: Usando as chaves de labels corretas
    for lbl in entry.get("source_node_labels", []):
        g.add((source_uri, RDF.type, EX[lbl]))

    for lbl in entry.get("target_node_labels", []):
        g.add((target_uri, RDF.type, EX[lbl]))

    # REMOÇÃO: A chamada para propriedades foi removida, pois não há 'properties' nos dados.
    # add_node_properties(source_uri, entry.get("source_properties", {}))
    # add_node_properties(target_uri, entry.get("target_properties", {}))

    # CORREÇÃO: Usando a chave de relacionamento correta
    rel = entry.get("relationship_type")
    if rel:
        g.add((source_uri, EX[rel], target_uri))

# --- Exporta RDF ---
g.serialize(destination=RDF_FILE, format="xml")

print(f"Grafo RDF exportado para {RDF_FILE}")