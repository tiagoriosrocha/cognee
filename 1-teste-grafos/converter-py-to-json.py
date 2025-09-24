import ast
import json

# Arquivo de entrada (formato errado com '|')
entrada = "grafo.py"
# Arquivo de saída (JSON válido)
saida = "grafo.json"

with open(entrada, "r", encoding="utf-8") as f:
    data = f.read().strip()

# Divide pelos separadores "|"
partes = [p.strip() for p in data.split("|") if p.strip()]

# Converte cada parte (que é um dict Python) em objeto Python
objetos = [ast.literal_eval(p) for p in partes]

# Salva em formato JSON válido
with open(saida, "w", encoding="utf-8") as f:
    json.dump(objetos, f, indent=2, ensure_ascii=False)

print(f"✅ Conversão concluída! Arquivo salvo em {saida}")
