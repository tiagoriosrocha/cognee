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

def add_node_properties(node_uri, properties: dict):
    """Adiciona propriedades de um nó ao grafo RDF"""
    for key, value in properties.items():
        if isinstance(value, bool):
            g.add((node_uri, EX[key], Literal(value, datatype=XSD.boolean)))
        elif isinstance(value, int):
            g.add((node_uri, EX[key], Literal(value, datatype=XSD.integer)))
        else:
            g.add((node_uri, EX[key], Literal(str(value))))

# --- Etapa 1: Converter lista de dicionários Python para JSON ---
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    python_data = ast.literal_eval(f.read())   # interpreta como objeto Python

# Salva em JSON válido
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(python_data, f, indent=2, ensure_ascii=False)

print(f"Arquivo {JSON_FILE} criado com sucesso!")

# --- Etapa 2: Ler JSON válido e converter para RDF ---
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for entry in data:
    source_uri = URIRef(EX[entry["source_id"]])
    target_uri = URIRef(EX[entry["target_id"]])

    # Labels como tipos RDF
    for lbl in entry.get("source_labels", []):
        g.add((source_uri, RDF.type, EX[lbl]))

    for lbl in entry.get("target_labels", []):
        g.add((target_uri, RDF.type, EX[lbl]))

    # Propriedades
    add_node_properties(source_uri, entry.get("source_properties", {}))
    add_node_properties(target_uri, entry.get("target_properties", {}))

    # Relação
    rel = entry.get("relationship")
    if rel:
        g.add((source_uri, EX[rel], target_uri))

# --- Exporta RDF ---
g.serialize(destination=RDF_FILE, format="xml")

print(f"Grafo RDF exportado para {RDF_FILE}")
