import uuid
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from processar_cognee import ProcessarCognee

app = Flask(__name__)
CORS(app)
tasks = {}
cognee_lock = threading.Lock()


def worker_processamento(task_id, dados_para_processar):
    """
    Função que executa o trabalho pesado em uma thread separada.
    """
    with cognee_lock:
        app.logger.info(f"Lock adquirido. Iniciando processamento para a tarefa: {task_id}")
        try:
            tasks[task_id]['status'] = 'PROCESSING'

            processador = ProcessarCognee()
            resultado_final = processador.executar(dados_para_processar["selectedQuestion"])
            
            tasks[task_id]['status'] = 'SUCCESS'
            tasks[task_id]['result'] = resultado_final
            app.logger.info(f"Tarefa {task_id} concluída com sucesso.")

        except Exception as e:
            app.logger.error(f"Erro na tarefa {task_id}: {e}", exc_info=True)
            tasks[task_id]['status'] = 'FAILURE'
            tasks[task_id]['result'] = {"erro": "Um erro inesperado ocorreu durante o processamento.", "detalhes": str(e)}

    app.logger.info(f"Lock liberado para a tarefa: {task_id}")






@app.route('/runquestion', methods=['POST'])
def run_question_async():
    """
    Endpoint que INICIA uma tarefa de processamento em background.
    """
    try:
        dados_recebidos = request.get_json()
        if dados_recebidos is None:
            return jsonify({"erro": "Corpo da requisição inválido ou não é JSON."}), 400
    except Exception:
        return jsonify({"erro": "Erro ao decodificar o JSON da requisição."}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'PENDING', 'result': None}
    
    thread = threading.Thread(target=worker_processamento, args=(task_id, dados_recebidos))
    thread.start()

    app.logger.info(f"Tarefa {task_id} criada e enfileirada para processamento.")
    return jsonify({"task_id": task_id}), 202







@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """
    Endpoint para verificar o status de uma tarefa.
    """
    task = tasks.get(task_id)
    
    if not task:
        app.logger.warning(f"Tentativa de acesso a uma tarefa inexistente: {task_id}")
        return jsonify({"erro": "ID da tarefa não encontrado."}), 404

    response_data = {
        "task_id": task_id,
        "status": task['status']
    }
    
    if task['status'] in ['SUCCESS', 'FAILURE']:
        response_data['result'] = task['result']
        
    return jsonify(response_data), 200






if __name__ == '__main__':
    app.run(debug=False, port=5000)




########################################################################################################
########################################################################################################



# import uuid
# import threading
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from processar_cognee import ProcessarCognee

# # 1. Inicializa a aplicação Flask
# app = Flask(__name__)
# CORS(app)

# tasks = {}

# def worker_processamento(task_id, dados_para_processar):
#     """
#     Função que executa o trabalho pesado em uma thread separada.
#     Isso evita que o endpoint principal fique bloqueado.
#     """
#     app.logger.info(f"Iniciando processamento para a tarefa: {task_id}")
#     try:
#         # Atualiza o status da tarefa para 'PROCESSING'
#         tasks[task_id]['status'] = 'PROCESSING'

#         # 2. Cria a instância e executa a lógica pesada (demorada)
#         processador = ProcessarCognee()
#         resultado_final = processador.executar(dados_para_processar["selectedQuestion"])
        
#         # 3. Se tudo deu certo, atualiza o status e armazena o resultado
#         tasks[task_id]['status'] = 'SUCCESS'
#         tasks[task_id]['result'] = resultado_final
#         app.logger.info(f"Tarefa {task_id} concluída com sucesso.")

#     except Exception as e:
#         # 4. Se ocorrer um erro, atualiza o status e armazena a mensagem de erro
#         app.logger.error(f"Erro na tarefa {task_id}: {e}", exc_info=True)
#         tasks[task_id]['status'] = 'FAILURE'
#         tasks[task_id]['result'] = {"erro": "Um erro inesperado ocorreu durante o processamento.", "detalhes": str(e)}


# @app.route('/runquestion', methods=['POST'])
# def run_question_async():
#     """
#     Endpoint que INICIA uma tarefa de processamento em background
#     e retorna imediatamente um ID para acompanhamento.
#     """
#     try:
#         dados_recebidos = request.get_json()
        
#         if dados_recebidos is None:
#             return jsonify({"erro": "Corpo da requisição inválido ou não é JSON."}), 400
        
#         #print("dados recebidos da interface:")
#         #print(dados_recebidos)
#     except Exception:
#         return jsonify({"erro": "Erro ao decodificar o JSON da requisição."}), 400

#     # 1. Gera um ID único para a nova tarefa
#     task_id = str(uuid.uuid4())
#     print("nova task criada: ", task_id)

#     # 2. Adiciona a tarefa ao nosso dicionário com o status inicial 'PENDING'
#     tasks[task_id] = {'status': 'PENDING', 'result': None}
    
#     # 3. Cria e inicia a thread para executar o worker em segundo plano
#     thread = threading.Thread(target=worker_processamento, args=(task_id, dados_recebidos))
#     thread.start()
#     print("nova thread")

#     # 4. Retorna uma resposta imediata (202 Accepted) com o ID da tarefa
#     return jsonify({"task_id": task_id}), 202


# @app.route('/status/<task_id>', methods=['GET'])
# def get_status(task_id):
#     """
#     Endpoint para verificar o status de uma tarefa iniciada anteriormente.
#     """
#     task = tasks.get(task_id)
    
#     # Se a tarefa não for encontrada, retorna 404
#     if not task:
#         return jsonify({"erro": "ID da tarefa não encontrado."}), 404

#     response_data = {
#         "task_id": task_id,
#         "status": task['status']
#     }
    
#     # Se a tarefa já foi concluída (com sucesso ou falha), inclui o resultado
#     if task['status'] in ['SUCCESS', 'FAILURE']:
#         response_data['result'] = task['result']
        
#     return jsonify(response_data), 200


# # Permite executar o servidor com 'python app.py'
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)