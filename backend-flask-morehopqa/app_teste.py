# simple_app.py
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# 1. Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app) 

@app.route('/runquestion', methods=['POST'])
def handle_run_question():
    """
    Este endpoint recebe um JSON, imprime no terminal e retorna outro JSON de teste.
    """
    # 2. Tenta obter o JSON da requisição
    try:
        dados_recebidos = request.get_json()
        if dados_recebidos is None:
            return jsonify({"erro": "Requisição inválida. O corpo deve ser um JSON válido."}), 400
    except Exception:
        return jsonify({"erro": "JSON mal formatado na requisição."}), 400

    # 3. Imprime o JSON recebido no terminal
    print("\n--- JSON Recebido do Cliente ---")
    print(json.dumps(dados_recebidos, indent=2, ensure_ascii=False))
    print("--------------------------------\n")

    # 4. Cria e retorna um JSON de resposta fixo
    json_de_resposta = {
        "final_answer": "The director of the 2004 film where Kam Heskin plays Paige Morgan (\"The Prince and Me\") is Martha Coolidge...",
        "nodes": {
            "803c8a2a-b00a-50a6-8b0f-9f813d689532": {
            "name": "Node 803c8a2a...",
            "item": 123,
            "outro": "teste",
            },
            "6bd2234d-5266-5519-bfa9-f2a746931895": {
            "name": "text_253becda393cc4221094e8eb3cabf879",
            "outro": "teste",
            },
            "b661854d-2f9b-5b09-93f9-77be0be05db9": {
            "name": "rachel elizabeth lynne mckee wallingford",
            "outro": "teste",
            }
        },
        "edges": {
            "edge1": {
            "source": "803c8a2a-b00a-50a6-8b0f-9f813d689532",
            "target": "6bd2234d-5266-5519-bfa9-f2a746931895"
            },
            "edge2": {
            "source": "803c8a2a-b00a-50a6-8b0f-9f813d689532",
            "target": "b661854d-2f9b-5b09-93f9-77be0be05db9"
            }
        }
    }
    
    return jsonify(json_de_resposta), 200

# Bloco para permitir a execução direta do script
if __name__ == '__main__':
    app.run(debug=True, port=5000)