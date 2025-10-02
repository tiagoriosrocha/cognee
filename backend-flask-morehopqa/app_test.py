import uuid
import threading
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
tasks = {}

#######################################################################################################
#######################################################################################################
#######################################################################################################
FIXED_RESULT = {
    "final_answer": "Esta é uma resposta de teste gerada pelo servidor mock. O processamento real não foi executado.",
    "nodes": {
        "node1": {"id": 1, "name": "Nó de Teste 1", "type" : "ontolgy", "propX" : "abcd", "propY" : 123},
        "node2": {"id": 2, "name": "Nó de Teste 2", "type" : "entity", "propX" : "abcd", "propY" : 123},
        "node3": {"id": 3, "name": "Nó de Teste 3", "type" : "individual", "propX" : "abcd", "propY" : 123},
        "node4": {"id": 4, "name": "Nó de Teste 3", "type" : "ontolgy", "propX" : "abcd", "propY" : 123},
        "node5": {"id": 5, "name": "Nó de Teste 3", "type" : "individual", "propX" : "abcd", "propY" : 123},
        "node6": {"id": 6, "name": "Nó de Teste 3", "type" : "ontolgy", "propX" : "abcd", "propY" : 123},
        "node7": {"id": 7, "name": "Nó de Teste 3", "type" : "individual", "propX" : "abcd", "propY" : 123},
        "node8": {"id": 8, "name": "Nó de Teste 3", "type" : "individual", "propX" : "abcd", "propY" : 123},
        "node9": {"id": 9, "name": "Nó de Teste 3", "type" : "entity", "propX" : "abcd", "propY" : 123},
        "node10": {"id": 10, "name": "Nó de Teste 3", "type" : "entity", "propX" : "abcd", "propY" : 123}
    },
    "edges": {
        "edge1": {"source": "node1", "target": "node2", "label": "link1"},
        "edge2": {"source": "node2", "target": "node3", "label": "link2"},
        "edge3": {"source": "node3", "target": "node4", "label": "link2"},
        "edge4": {"source": "node4", "target": "node5", "label": "link2"},
        "edge5": {"source": "node5", "target": "node6", "label": "link2"},
        "edge6": {"source": "node6", "target": "node7", "label": "link2"},
        "edge7": {"source": "node7", "target": "node8", "label": "link2"},
        "edge8": {"source": "node8", "target": "node9", "label": "link2"},
        "edge9": {"source": "node9", "target": "node10", "label": "link2"},
        "edge10": {"source": "node10", "target": "node1", "label": "link2"},
    }
}


#######################################################################################################
#######################################################################################################
#######################################################################################################
def worker_mock_processamento(task_id):
    try:
        tasks[task_id]['status'] = 'PROCESSING'
        time.sleep(1)
        tasks[task_id]['status'] = 'SUCCESS'
        tasks[task_id]['result'] = FIXED_RESULT
    except Exception as e:
        app.logger.error(f"Erro na tarefa simulada {task_id}: {e}")
        tasks[task_id]['status'] = 'FAILURE'
        tasks[task_id]['result'] = {"erro": "Ocorreu um erro no worker de teste.", "detalhes": str(e)}


#######################################################################################################
#######################################################################################################
#######################################################################################################
@app.route('/runquestion', methods=['POST'])
def run_question_async_mock():
    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'PENDING', 'result': None}
    thread = threading.Thread(target=worker_mock_processamento, args=(task_id,))
    thread.start()
    return jsonify({"task_id": task_id}), 202


#######################################################################################################
#######################################################################################################
#######################################################################################################
@app.route('/status/<task_id>', methods=['GET'])
def get_status_mock(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"erro": "ID da tarefa não encontrado."}), 404
    response_data = {
        "task_id": task_id,
        "status": task['status']
    }
    if task['status'] in ['SUCCESS', 'FAILURE']:
        response_data['result'] = task['result']   
    return jsonify(response_data), 200


#######################################################################################################
#######################################################################################################
#######################################################################################################
if __name__ == '__main__':
    app.run(debug=True, port=5000)






# # simple_app.py
# import json
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# # 1. Inicializa a aplicação Flask
# app = Flask(__name__)
# CORS(app) 

# @app.route('/runquestion', methods=['POST'])
# def handle_run_question():
#     """
#     Este endpoint recebe um JSON, imprime no terminal e retorna outro JSON de teste.
#     """
#     # 2. Tenta obter o JSON da requisição
#     try:
#         dados_recebidos = request.get_json()
#         if dados_recebidos is None:
#             return jsonify({"erro": "Requisição inválida. O corpo deve ser um JSON válido."}), 400
#     except Exception:
#         return jsonify({"erro": "JSON mal formatado na requisição."}), 400

#     # 3. Imprime o JSON recebido no terminal
#     print("\n--- JSON Recebido do Cliente ---")
#     print(json.dumps(dados_recebidos, indent=2, ensure_ascii=False))
#     print("--------------------------------\n")

#     # 4. Cria e retorna um JSON de resposta fixo
#     json_de_resposta = {
#     "final_answer": "To solve this question, we need to identify the year Rodney \"Boss\" Bailey was drafted by the Washington Redskins and then find the closest palindrome number to that year.\\n\\n1. **Identifying the Draft Year:**\\n   - Rodney \"Boss\" Bailey played in the NFL as a linebacker. He attended college at the University of Georgia before being drafted.\\n   - He was selected in the first round by the Washington Redskins during the 2000 NFL Draft, specifically as the sixth overall pick.\\n\\n2. **Finding the Closest Palindrome:**\\n   - The year Rodney \"Boss\" Bailey was drafted is 2000.\\n   - We look for palindrome numbers around this year. A palindrome number reads the same forwards and backwards.\\n   - Numbers close to 2000 that are palindromes include 1991, 2002, 2112, etc. \\n   - Comparing the differences: |2000 - 1991| = 9 and |2000 - 2002| = 2.\\n   - The closest palindrome number to 2000 is therefore 2002.\\n\\nIn conclusion, the closest palindrome number to the year Rodney \"Boss\" Bailey was drafted (2000) is 2002.",
#     "nodes": {
#         "2b9783d7-b4d6-5f1d-89b3-9f4f125c0c92": {
#             "id": "2b9783d7-b4d6-5f1d-89b3-9f4f125c0c92",
#             "text": "Champ Bailey",
#             "chunk_index": 0,
#             "chunk_size": 5,
#             "updated_at": 1759256205607,
#             "cut_type": "sentence_cut",
#             "ontology_valid": False,
#             "created_at": 1759256183984,
#             "topological_rank": 0,
#             "type": "DocumentChunk",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "3ca182b9-9df6-5957-be0e-9f7662c28bb2": {
#             "id": "3ca182b9-9df6-5957-be0e-9f7662c28bb2",
#             "updated_at": 1759256205607,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_09d8a77cb3f0fe83548c3252b63b7324.txt",
#             "mime_type": "text/plain",
#             "name": "text_09d8a77cb3f0fe83548c3252b63b7324",
#             "ontology_valid": False,
#             "created_at": 1759256183166,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "c18fa801-2fef-5f9d-b032-32a04e607d31": {
#             "id": "c18fa801-2fef-5f9d-b032-32a04e607d31",
#             "updated_at": 1759256205607,
#             "description": "American former professional football player known as one of the best cornerbacks in NFL history.",
#             "name": "champ bailey",
#             "ontology_valid": False,
#             "created_at": 1759256194014,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "d072ba0f-e1a9-58bf-9974-e1802adc8134": {
#             "id": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
#             "updated_at": 1759256325738,
#             "description": "person",
#             "name": "person",
#             "ontology_valid": False,
#             "created_at": 1759256313890,
#             "topological_rank": 0,
#             "type": "EntityType",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "02ec146d-df93-5e88-bba2-f1821a783a27": {
#             "id": "02ec146d-df93-5e88-bba2-f1821a783a27",
#             "updated_at": 1759256325738,
#             "description": "A professional American football league which is one of the two major professional sports leagues in North America, and constitutes the highest level of professional football in the world.",
#             "name": "national football league",
#             "ontology_valid": False,
#             "created_at": 1759256313890,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d": {
#             "id": "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d",
#             "updated_at": 1759256325738,
#             "description": "organization",
#             "name": "organization",
#             "ontology_valid": False,
#             "created_at": 1759256313890,
#             "topological_rank": 0,
#             "type": "EntityType",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "a0fbd29f-f529-51a5-b5de-616938f8c14a": {
#             "id": "a0fbd29f-f529-51a5-b5de-616938f8c14a",
#             "updated_at": 1759256205607,
#             "description": "An NFL team based in Denver, Colorado.",
#             "name": "denver broncos",
#             "ontology_valid": False,
#             "created_at": 1759256194014,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "6c4a98d7-f823-5b75-a645-71a523838203": {
#             "id": "6c4a98d7-f823-5b75-a645-71a523838203",
#             "updated_at": 1759256205607,
#             "description": "sports_team",
#             "name": "sports_team",
#             "ontology_valid": False,
#             "created_at": 1759256194014,
#             "topological_rank": 0,
#             "type": "EntityType",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "97b04ecd-b187-55b9-a913-63e83f79d6a4": {
#             "id": "97b04ecd-b187-55b9-a913-63e83f79d6a4",
#             "updated_at": 1759256205607,
#             "description": "A defensive position in American football tasked with defending against passes and running backs behind the line of scrimmage.",
#             "name": "defensive back",
#             "ontology_valid": False,
#             "created_at": 1759256194014,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "3bb13835-c4cd-52cd-bbd9-c2daa16183d2": {
#             "id": "3bb13835-c4cd-52cd-bbd9-c2daa16183d2",
#             "updated_at": 1759256205607,
#             "description": "position",
#             "name": "position",
#             "ontology_valid": False,
#             "created_at": 1759256194014,
#             "topological_rank": 0,
#             "type": "EntityType",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "e2cac170-c267-5e05-949c-429d2cd560f3": {
#             "id": "e2cac170-c267-5e05-949c-429d2cd560f3",
#             "text": "Champ Bailey is a renowned former American football cornerback.",
#             "updated_at": 1759256205607,
#             "ontology_valid": False,
#             "created_at": 1759256203065,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "4b15e4b9-3cd5-55ff-aa38-53cc6a0668d6": {
#             "text": "Roland \"Champ\" Bailey Jr. (born June 22, 1978) is a former American football cornerback in the National Football League (NFL).",
#             "ontology_valid": False,
#             "topological_rank": 0,
#             "contains": [],
#             "type": "DocumentChunk",
#             "version": 1,
#             "id": "4b15e4b9-3cd5-55ff-aa38-53cc6a0668d6",
#             "chunk_index": 0,
#             "chunk_size": 57,
#             "updated_at": 1759256228334,
#             "cut_type": "sentence_end",
#             "created_at": 1759256210064,
#             "metadata": "{\"index_fields\": [\"text\"]}"
#         },
#         "3df054e6-fdfd-519e-bdfe-4e662fe1668e": {
#             "id": "3df054e6-fdfd-519e-bdfe-4e662fe1668e",
#             "updated_at": 1759256228334,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_a0845e15010152ac25f6dec7d1cef9e9.txt",
#             "mime_type": "text/plain",
#             "name": "text_a0845e15010152ac25f6dec7d1cef9e9",
#             "ontology_valid": False,
#             "created_at": 1759256209269,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "dfb75ade-55d0-5442-84b2-609379973a53": {
#             "id": "dfb75ade-55d0-5442-84b2-609379973a53",
#             "text": "Roland 'Champ' Bailey Jr. is a former American NFL cornerback.",
#             "updated_at": 1759256228334,
#             "ontology_valid": False,
#             "created_at": 1759256225992,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "ace7a60b-b602-55a5-b3e4-b2f7e0790417": {
#             "id": "ace7a60b-b602-55a5-b3e4-b2f7e0790417",
#             "text": " He played college football for Georgia, where he earned consensus All-American honors, and was drafted by the Washington Redskins in the first round of the 1999 NFL Draft.",
#             "chunk_index": 0,
#             "chunk_size": 70,
#             "updated_at": 1759256253120,
#             "cut_type": "sentence_end",
#             "ontology_valid": False,
#             "created_at": 1759256232447,
#             "topological_rank": 0,
#             "type": "DocumentChunk",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "ddee2e4e-1347-5948-afcd-57541ace70fc": {
#             "id": "ddee2e4e-1347-5948-afcd-57541ace70fc",
#             "updated_at": 1759256253120,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_23ca204fe99a22e48ae4c709e8833441.txt",
#             "mime_type": "text/plain",
#             "name": "text_23ca204fe99a22e48ae4c709e8833441",
#             "ontology_valid": False,
#             "created_at": 1759256231960,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "76615a34-8ed8-5b2c-ade4-622b0d0036f1": {
#             "id": "76615a34-8ed8-5b2c-ade4-622b0d0036f1",
#             "updated_at": 1759256253120,
#             "description": "A college football team",
#             "name": "georgia",
#             "ontology_valid": False,
#             "created_at": 1759256241442,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "2a90b479-03f1-5c91-98a7-e9cc71f059f0": {
#             "id": "2a90b479-03f1-5c91-98a7-e9cc71f059f0",
#             "updated_at": 1759256253120,
#             "description": "college",
#             "name": "college",
#             "ontology_valid": False,
#             "created_at": 1759256241442,
#             "topological_rank": 0,
#             "type": "EntityType",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "0f9a0f57-01cb-5995-bc40-cba2f1f53fbc": {
#             "id": "0f9a0f57-01cb-5995-bc40-cba2f1f53fbc",
#             "updated_at": 1759256253120,
#             "description": "A Player who played college football for Georgia, earned consensus All-American honors, and was drafted by the Washington Redskins in the first round of the 1999 NFL Draft.",
#             "name": "player_1",
#             "ontology_valid": False,
#             "created_at": 1759256241442,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "cb41920c-fc8e-5dfa-9d2d-3bcb10c7ef5e": {
#             "id": "cb41920c-fc8e-5dfa-9d2d-3bcb10c7ef5e",
#             "updated_at": 1759256253120,
#             "description": "An NFL team that drafted Player_1 in the first round of the 1999 NFL Draft",
#             "name": "washington redskins",
#             "ontology_valid": False,
#             "created_at": 1759256241442,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "d3913304-f3e7-54fb-b5bb-a3a9965d3279": {
#             "id": "d3913304-f3e7-54fb-b5bb-a3a9965d3279",
#             "updated_at": 1759256349505,
#             "description": "nfl team",
#             "name": "nfl team",
#             "ontology_valid": False,
#             "created_at": 1759256338665,
#             "topological_rank": 0,
#             "type": "EntityType",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "2a3cb39a-5a6e-5a31-a660-576a1b2e2f9e": {
#             "id": "2a3cb39a-5a6e-5a31-a660-576a1b2e2f9e",
#             "text": "A college football player from Georgia earned consensus All-American recognition and was selected by the Washington Redskins in the first round of the 1999 NFL Draft.",
#             "updated_at": 1759256253120,
#             "ontology_valid": False,
#             "created_at": 1759256250356,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "47361189-4f7f-58c6-9a70-bb544b343ceb": {
#             "id": "47361189-4f7f-58c6-9a70-bb544b343ceb",
#             "text": " He is the brother of former NFL linebacker Boss Bailey.",
#             "chunk_index": 0,
#             "chunk_size": 25,
#             "updated_at": 1759256275226,
#             "cut_type": "sentence_end",
#             "ontology_valid": False,
#             "created_at": 1759256256707,
#             "topological_rank": 0,
#             "type": "DocumentChunk",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "cb822c97-8ff0-54ba-b28e-8202b1e2a056": {
#             "id": "cb822c97-8ff0-54ba-b28e-8202b1e2a056",
#             "updated_at": 1759256275226,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_6901c278c621d933eaaa34d29f365229.txt",
#             "mime_type": "text/plain",
#             "name": "text_6901c278c621d933eaaa34d29f365229",
#             "ontology_valid": False,
#             "created_at": 1759256255878,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "464387cf-beb4-568f-83d2-6d4effbf02e4": {
#             "id": "464387cf-beb4-568f-83d2-6d4effbf02e4",
#             "updated_at": 1759256299921,
#             "description": "A character mentioned with the designation of 'boss'.",
#             "name": "boss bailey",
#             "ontology_valid": False,
#             "created_at": 1759256288130,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "8484fc68-3468-56c0-97d8-a238fba76111": {
#             "id": "8484fc68-3468-56c0-97d8-a238fba76111",
#             "updated_at": 1759256275226,
#             "description": "This person is the brother of former NFL linebacker Boss Bailey.",
#             "name": "brother of boss bailey",
#             "ontology_valid": False,
#             "created_at": 1759256264180,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "628912ec-3a0b-5859-a7d9-5e46c8840ac3": {
#             "id": "628912ec-3a0b-5859-a7d9-5e46c8840ac3",
#             "text": "He is the sibling of former NFL linebacker Boss Bailey.",
#             "updated_at": 1759256275226,
#             "ontology_valid": False,
#             "created_at": 1759256272510,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "2c47d805-b18d-56e7-9e37-aed57dd775a9": {
#             "id": "2c47d805-b18d-56e7-9e37-aed57dd775a9",
#             "text": "Boss Bailey",
#             "chunk_index": 0,
#             "chunk_size": 5,
#             "updated_at": 1759256299921,
#             "cut_type": "sentence_cut",
#             "ontology_valid": False,
#             "created_at": 1759256281014,
#             "topological_rank": 0,
#             "type": "DocumentChunk",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "fad90c87-8671-53fb-a1b4-f96d2c37d0a8": {
#             "id": "fad90c87-8671-53fb-a1b4-f96d2c37d0a8",
#             "updated_at": 1759256299921,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_c6eb131a7bb5d292cbb7dca846969f84.txt",
#             "mime_type": "text/plain",
#             "name": "text_c6eb131a7bb5d292cbb7dca846969f84",
#             "ontology_valid": False,
#             "created_at": 1759256280179,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "5c4c6d38-e8a1-53b4-a933-094fe3732f5d": {
#             "id": "5c4c6d38-e8a1-53b4-a933-094fe3732f5d",
#             "text": "Boss Bailey",
#             "updated_at": 1759256299921,
#             "ontology_valid": False,
#             "created_at": 1759256297098,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "d4af720d-f462-5587-9b53-bd5c6c3f4b33": {
#             "id": "d4af720d-f462-5587-9b53-bd5c6c3f4b33",
#             "text": "Rodney \"Boss\" Bailey (born October 14, 1979) is a former American football linebacker who played in the National Football League.",
#             "chunk_index": 0,
#             "chunk_size": 56,
#             "updated_at": 1759256325738,
#             "cut_type": "sentence_end",
#             "ontology_valid": False,
#             "created_at": 1759256305499,
#             "topological_rank": 0,
#             "type": "DocumentChunk",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "8637e44d-d9fd-52e5-b9d2-dcac466c649f": {
#             "id": "8637e44d-d9fd-52e5-b9d2-dcac466c649f",
#             "updated_at": 1759256325738,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_d929daba4082a3acf99643393b43922f.txt",
#             "mime_type": "text/plain",
#             "name": "text_d929daba4082a3acf99643393b43922f",
#             "ontology_valid": False,
#             "created_at": 1759256304580,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "cf7e33cc-d156-5d50-8a46-0e4dded46109": {
#             "id": "cf7e33cc-d156-5d50-8a46-0e4dded46109",
#             "updated_at": 1759256325738,
#             "description": "Former American football linebacker who played in the National Football League.",
#             "name": "rodney boss bailey",
#             "ontology_valid": False,
#             "created_at": 1759256313890,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "85dec54b-d041-5445-8e44-29909a235549": {
#             "id": "85dec54b-d041-5445-8e44-29909a235549",
#             "text": "Rodney \"Boss\" Bailey is a former American football linebacker born on October 14, 1979, who played professionally in the National Football League.",
#             "updated_at": 1759256325738,
#             "ontology_valid": False,
#             "created_at": 1759256323293,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "dae814d3-c437-5985-952c-f3228b9877d4": {
#             "id": "dae814d3-c437-5985-952c-f3228b9877d4",
#             "text": " He was originally drafted by the Detroit Lions in the second round of the 2003 NFL Draft.",
#             "chunk_index": 0,
#             "chunk_size": 42,
#             "updated_at": 1759256349505,
#             "cut_type": "sentence_end",
#             "ontology_valid": False,
#             "created_at": 1759256330695,
#             "topological_rank": 0,
#             "type": "DocumentChunk",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "c71de1d3-52d0-50ff-beb2-9f3c74786440": {
#             "id": "c71de1d3-52d0-50ff-beb2-9f3c74786440",
#             "updated_at": 1759256349505,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_4c2f8383731535204357f2f11dd9cf47.txt",
#             "mime_type": "text/plain",
#             "name": "text_4c2f8383731535204357f2f11dd9cf47",
#             "ontology_valid": False,
#             "created_at": 1759256329856,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "eb0e23b2-6c8e-5671-aa43-d84f85d08e7c": {
#             "id": "eb0e23b2-6c8e-5671-aa43-d84f85d08e7c",
#             "updated_at": 1759256349505,
#             "description": "The Detroit Lions are a professional American football team based in the Detroit area.",
#             "name": "detroit lions",
#             "ontology_valid": False,
#             "created_at": 1759256338665,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "1737e934-a105-52c6-aa47-7750d4087016": {
#             "id": "1737e934-a105-52c6-aa47-7750d4087016",
#             "updated_at": 1759256349505,
#             "description": "An annual event where National Football League teams select eligible college football players to join the league.",
#             "name": "2003 nfl draft",
#             "ontology_valid": False,
#             "created_at": 1759256338665,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "c5ea3068-2d2d-5c0d-9ca4-5d3049d88b61": {
#             "id": "c5ea3068-2d2d-5c0d-9ca4-5d3049d88b61",
#             "updated_at": 1759256349505,
#             "description": "event",
#             "name": "event",
#             "ontology_valid": False,
#             "created_at": 1759256338665,
#             "topological_rank": 0,
#             "type": "EntityType",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "7cfacd0f-e781-54e8-9a7b-0cf6efd3bdbc": {
#             "id": "7cfacd0f-e781-54e8-9a7b-0cf6efd3bdbc",
#             "text": "A player was initially selected by the Detroit Lions during the second round of the 2003 NFL Draft.",
#             "updated_at": 1759256349505,
#             "ontology_valid": False,
#             "created_at": 1759256347335,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "e3e1df41-1407-5915-b792-7b2e9a895dc3": {
#             "id": "e3e1df41-1407-5915-b792-7b2e9a895dc3",
#             "text": " He played college football at the University of Georgia.",
#             "chunk_index": 0,
#             "chunk_size": 19,
#             "updated_at": 1759256372322,
#             "cut_type": "sentence_end",
#             "ontology_valid": False,
#             "created_at": 1759256354639,
#             "topological_rank": 0,
#             "type": "DocumentChunk",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "7631b456-5d95-51f9-9676-292dbbbe3174": {
#             "id": "7631b456-5d95-51f9-9676-292dbbbe3174",
#             "updated_at": 1759256372322,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_fdfd47ade2b79ebb26482d75fb80270f.txt",
#             "mime_type": "text/plain",
#             "name": "text_fdfd47ade2b79ebb26482d75fb80270f",
#             "ontology_valid": False,
#             "created_at": 1759256353839,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "f92cdcf5-1b0b-5720-99fa-b8c10d4290fe": {
#             "id": "f92cdcf5-1b0b-5720-99fa-b8c10d4290fe",
#             "updated_at": 1759256372322,
#             "description": "A public university located in Athens, Georgia.",
#             "name": "university of georgia",
#             "ontology_valid": False,
#             "created_at": 1759256361127,
#             "topological_rank": 0,
#             "type": "Entity",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "912b273c-683d-53ea-8ffe-aadef0b84237": {
#             "id": "912b273c-683d-53ea-8ffe-aadef0b84237",
#             "updated_at": 1759256372322,
#             "description": "educational institution",
#             "name": "educational institution",
#             "ontology_valid": False,
#             "created_at": 1759256361127,
#             "topological_rank": 0,
#             "type": "EntityType",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "6b70bfc1-ea47-5b6d-b768-9b8d2b92435a": {
#             "id": "6b70bfc1-ea47-5b6d-b768-9b8d2b92435a",
#             "text": "He played college football at the University of Georgia.",
#             "updated_at": 1759256372322,
#             "ontology_valid": False,
#             "created_at": 1759256369737,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         },
#         "61be7fc5-3023-5074-855c-826717f243eb": {
#             "text": " He is the brother of former NFL cornerback Champ Bailey.",
#             "ontology_valid": False,
#             "topological_rank": 0,
#             "contains": [],
#             "type": "DocumentChunk",
#             "version": 1,
#             "id": "61be7fc5-3023-5074-855c-826717f243eb",
#             "chunk_index": 0,
#             "chunk_size": 24,
#             "updated_at": 1759256395180,
#             "cut_type": "sentence_end",
#             "created_at": 1759256377559,
#             "metadata": "{\"index_fields\": [\"text\"]}"
#         },
#         "82581f58-8085-5910-8aab-e1a13960b435": {
#             "id": "82581f58-8085-5910-8aab-e1a13960b435",
#             "updated_at": 1759256395180,
#             "raw_data_location": "file:///home/tiagoriosrocha/Documents/cognee/.venv/lib/python3.12/site-packages/cognee/.data_storage/text_b8e074f9fddf9b739fcb232f09d54ada.txt",
#             "mime_type": "text/plain",
#             "name": "text_b8e074f9fddf9b739fcb232f09d54ada",
#             "ontology_valid": False,
#             "created_at": 1759256376766,
#             "topological_rank": 0,
#             "external_metadata": "{}",
#             "type": "TextDocument",
#             "metadata": "{\"index_fields\": [\"name\"]}",
#             "version": 1
#         },
#         "7c7e3074-0682-544b-b2b3-aea6c6ede3bd": {
#             "id": "7c7e3074-0682-544b-b2b3-aea6c6ede3bd",
#             "text": "He shares familial ties with Champ Bailey, a former NFL cornerback.",
#             "updated_at": 1759256395180,
#             "ontology_valid": False,
#             "created_at": 1759256393109,
#             "topological_rank": 0,
#             "type": "TextSummary",
#             "metadata": "{\"index_fields\": [\"text\"]}",
#             "version": 1
#         }
#     },
#     "edges": {
#         "edge1": {
#             "target": "8484fc68-3468-56c0-97d8-a238fba76111",
#             "source": "47361189-4f7f-58c6-9a70-bb544b343ceb",
#             "label": "contains"
#         },
#         "edge2": {
#             "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
#             "source": "8484fc68-3468-56c0-97d8-a238fba76111",
#             "label": "is_a"
#         },
#         "edge3": {
#             "target": "464387cf-beb4-568f-83d2-6d4effbf02e4",
#             "source": "8484fc68-3468-56c0-97d8-a238fba76111",
#             "label": "brother_of"
#         },
#         "edge4": {
#             "target": "47361189-4f7f-58c6-9a70-bb544b343ceb",
#             "source": "628912ec-3a0b-5859-a7d9-5e46c8840ac3",
#             "label": "made_from"
#         },
#         "edge5": {
#             "target": "fad90c87-8671-53fb-a1b4-f96d2c37d0a8",
#             "source": "2c47d805-b18d-56e7-9e37-aed57dd775a9",
#             "label": "is_part_of"
#         },
#         "edge6": {
#             "target": "464387cf-beb4-568f-83d2-6d4effbf02e4",
#             "source": "2c47d805-b18d-56e7-9e37-aed57dd775a9",
#             "label": "contains"
#         },
#         "edge7": {
#             "target": "2c47d805-b18d-56e7-9e37-aed57dd775a9",
#             "source": "5c4c6d38-e8a1-53b4-a933-094fe3732f5d",
#             "label": "made_from"
#         },
#         "edge8": {
#             "target": "8637e44d-d9fd-52e5-b9d2-dcac466c649f",
#             "source": "d4af720d-f462-5587-9b53-bd5c6c3f4b33",
#             "label": "is_part_of"
#         },
#         "edge9": {
#             "target": "cf7e33cc-d156-5d50-8a46-0e4dded46109",
#             "source": "d4af720d-f462-5587-9b53-bd5c6c3f4b33",
#             "label": "contains"
#         },
#         "edge10": {
#             "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
#             "source": "cf7e33cc-d156-5d50-8a46-0e4dded46109",
#             "label": "is_a"
#         },
#         "edge11": {
#             "target": "02ec146d-df93-5e88-bba2-f1821a783a27",
#             "source": "d4af720d-f462-5587-9b53-bd5c6c3f4b33",
#             "label": "contains"
#         },
#         "edge12": {
#             "target": "02ec146d-df93-5e88-bba2-f1821a783a27",
#             "source": "cf7e33cc-d156-5d50-8a46-0e4dded46109",
#             "label": "played_in"
#         },
#         "edge13": {
#             "target": "d4af720d-f462-5587-9b53-bd5c6c3f4b33",
#             "source": "85dec54b-d041-5445-8e44-29909a235549",
#             "label": "made_from"
#         },
#         "edge14": {
#             "target": "c71de1d3-52d0-50ff-beb2-9f3c74786440",
#             "source": "dae814d3-c437-5985-952c-f3228b9877d4",
#             "label": "is_part_of"
#         },
#         "edge15": {
#             "target": "eb0e23b2-6c8e-5671-aa43-d84f85d08e7c",
#             "source": "dae814d3-c437-5985-952c-f3228b9877d4",
#             "label": "contains"
#         },
#         "edge16": {
#             "target": "d3913304-f3e7-54fb-b5bb-a3a9965d3279",
#             "source": "eb0e23b2-6c8e-5671-aa43-d84f85d08e7c",
#             "label": "is_a"
#         },
#         "edge17": {
#             "target": "1737e934-a105-52c6-aa47-7750d4087016",
#             "source": "dae814d3-c437-5985-952c-f3228b9877d4",
#             "label": "contains"
#         },
#         "edge18": {
#             "target": "c5ea3068-2d2d-5c0d-9ca4-5d3049d88b61",
#             "source": "1737e934-a105-52c6-aa47-7750d4087016",
#             "label": "is_a"
#         },
#         "edge19": {
#             "target": "1737e934-a105-52c6-aa47-7750d4087016",
#             "source": "eb0e23b2-6c8e-5671-aa43-d84f85d08e7c",
#             "label": "held_draft_in"
#         },
#         "edge20": {
#             "target": "dae814d3-c437-5985-952c-f3228b9877d4",
#             "source": "7cfacd0f-e781-54e8-9a7b-0cf6efd3bdbc",
#             "label": "made_from"
#         },
#         "edge21": {
#             "target": "7631b456-5d95-51f9-9676-292dbbbe3174",
#             "source": "e3e1df41-1407-5915-b792-7b2e9a895dc3",
#             "label": "is_part_of"
#         },
#         "edge22": {
#             "target": "f92cdcf5-1b0b-5720-99fa-b8c10d4290fe",
#             "source": "e3e1df41-1407-5915-b792-7b2e9a895dc3",
#             "label": "contains"
#         },
#         "edge23": {
#             "target": "912b273c-683d-53ea-8ffe-aadef0b84237",
#             "source": "f92cdcf5-1b0b-5720-99fa-b8c10d4290fe",
#             "label": "is_a"
#         },
#         "edge24": {
#             "target": "e3e1df41-1407-5915-b792-7b2e9a895dc3",
#             "source": "6b70bfc1-ea47-5b6d-b768-9b8d2b92435a",
#             "label": "made_from"
#         },
#         "edge25": {
#             "target": "82581f58-8085-5910-8aab-e1a13960b435",
#             "source": "61be7fc5-3023-5074-855c-826717f243eb",
#             "label": "is_part_of"
#         },
#         "edge26": {
#             "target": "61be7fc5-3023-5074-855c-826717f243eb",
#             "source": "7c7e3074-0682-544b-b2b3-aea6c6ede3bd",
#             "label": "made_from"
#         },
#         "edge27": {
#             "target": "ace7a60b-b602-55a5-b3e4-b2f7e0790417",
#             "source": "2a3cb39a-5a6e-5a31-a660-576a1b2e2f9e",
#             "label": "made_from"
#         },
#         "edge28": {
#             "target": "cb822c97-8ff0-54ba-b28e-8202b1e2a056",
#             "source": "47361189-4f7f-58c6-9a70-bb544b343ceb",
#             "label": "is_part_of"
#         },
#         "edge29": {
#             "target": "464387cf-beb4-568f-83d2-6d4effbf02e4",
#             "source": "47361189-4f7f-58c6-9a70-bb544b343ceb",
#             "label": "contains"
#         },
#         "edge30": {
#             "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
#             "source": "464387cf-beb4-568f-83d2-6d4effbf02e4",
#             "label": "is_a"
#         },
#         "edge31": {
#             "target": "3ca182b9-9df6-5957-be0e-9f7662c28bb2",
#             "source": "2b9783d7-b4d6-5f1d-89b3-9f4f125c0c92",
#             "label": "is_part_of"
#         },
#         "edge32": {
#             "target": "c18fa801-2fef-5f9d-b032-32a04e607d31",
#             "source": "2b9783d7-b4d6-5f1d-89b3-9f4f125c0c92",
#             "label": "contains"
#         },
#         "edge33": {
#             "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
#             "source": "c18fa801-2fef-5f9d-b032-32a04e607d31",
#             "label": "is_a"
#         },
#         "edge34": {
#             "target": "02ec146d-df93-5e88-bba2-f1821a783a27",
#             "source": "2b9783d7-b4d6-5f1d-89b3-9f4f125c0c92",
#             "label": "contains"
#         },
#         "edge35": {
#             "target": "d3d7b6b4-9b0d-52e8-9e09-a9e9cf4b5a4d",
#             "source": "02ec146d-df93-5e88-bba2-f1821a783a27",
#             "label": "is_a"
#         },
#         "edge36": {
#             "target": "a0fbd29f-f529-51a5-b5de-616938f8c14a",
#             "source": "2b9783d7-b4d6-5f1d-89b3-9f4f125c0c92",
#             "label": "contains"
#         },
#         "edge37": {
#             "target": "6c4a98d7-f823-5b75-a645-71a523838203",
#             "source": "a0fbd29f-f529-51a5-b5de-616938f8c14a",
#             "label": "is_a"
#         },
#         "edge38": {
#             "target": "97b04ecd-b187-55b9-a913-63e83f79d6a4",
#             "source": "2b9783d7-b4d6-5f1d-89b3-9f4f125c0c92",
#             "label": "contains"
#         },
#         "edge39": {
#             "target": "3bb13835-c4cd-52cd-bbd9-c2daa16183d2",
#             "source": "97b04ecd-b187-55b9-a913-63e83f79d6a4",
#             "label": "is_a"
#         },
#         "edge40": {
#             "target": "a0fbd29f-f529-51a5-b5de-616938f8c14a",
#             "source": "c18fa801-2fef-5f9d-b032-32a04e607d31",
#             "label": "played_for"
#         },
#         "edge41": {
#             "target": "02ec146d-df93-5e88-bba2-f1821a783a27",
#             "source": "c18fa801-2fef-5f9d-b032-32a04e607d31",
#             "label": "member_of"
#         },
#         "edge42": {
#             "target": "97b04ecd-b187-55b9-a913-63e83f79d6a4",
#             "source": "c18fa801-2fef-5f9d-b032-32a04e607d31",
#             "label": "played_position"
#         },
#         "edge43": {
#             "target": "2b9783d7-b4d6-5f1d-89b3-9f4f125c0c92",
#             "source": "e2cac170-c267-5e05-949c-429d2cd560f3",
#             "label": "made_from"
#         },
#         "edge44": {
#             "target": "3df054e6-fdfd-519e-bdfe-4e662fe1668e",
#             "source": "4b15e4b9-3cd5-55ff-aa38-53cc6a0668d6",
#             "label": "is_part_of"
#         },
#         "edge45": {
#             "target": "4b15e4b9-3cd5-55ff-aa38-53cc6a0668d6",
#             "source": "dfb75ade-55d0-5442-84b2-609379973a53",
#             "label": "made_from"
#         },
#         "edge46": {
#             "target": "ddee2e4e-1347-5948-afcd-57541ace70fc",
#             "source": "ace7a60b-b602-55a5-b3e4-b2f7e0790417",
#             "label": "is_part_of"
#         },
#         "edge47": {
#             "target": "76615a34-8ed8-5b2c-ade4-622b0d0036f1",
#             "source": "ace7a60b-b602-55a5-b3e4-b2f7e0790417",
#             "label": "contains"
#         },
#         "edge48": {
#             "target": "2a90b479-03f1-5c91-98a7-e9cc71f059f0",
#             "source": "76615a34-8ed8-5b2c-ade4-622b0d0036f1",
#             "label": "is_a"
#         },
#         "edge49": {
#             "target": "0f9a0f57-01cb-5995-bc40-cba2f1f53fbc",
#             "source": "ace7a60b-b602-55a5-b3e4-b2f7e0790417",
#             "label": "contains"
#         },
#         "edge50": {
#             "target": "d072ba0f-e1a9-58bf-9974-e1802adc8134",
#             "source": "0f9a0f57-01cb-5995-bc40-cba2f1f53fbc",
#             "label": "is_a"
#         },
#         "edge51": {
#             "target": "cb41920c-fc8e-5dfa-9d2d-3bcb10c7ef5e",
#             "source": "ace7a60b-b602-55a5-b3e4-b2f7e0790417",
#             "label": "contains"
#         },
#         "edge52": {
#             "target": "d3913304-f3e7-54fb-b5bb-a3a9965d3279",
#             "source": "cb41920c-fc8e-5dfa-9d2d-3bcb10c7ef5e",
#             "label": "is_a"
#         },
#         "edge53": {
#             "target": "76615a34-8ed8-5b2c-ade4-622b0d0036f1",
#             "source": "0f9a0f57-01cb-5995-bc40-cba2f1f53fbc",
#             "label": "played_for_college"
#         },
#         "edge54": {
#             "target": "cb41920c-fc8e-5dfa-9d2d-3bcb10c7ef5e",
#             "source": "0f9a0f57-01cb-5995-bc40-cba2f1f53fbc",
#             "label": "drafted_by_team"
#         }
#     }
# }


#     return jsonify(json_de_resposta), 200

# # Bloco para permitir a execução direta do script
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)