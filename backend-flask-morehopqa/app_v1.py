import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from processar_cognee_v2 import ProcessarCognee

# 1. Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app) 

@app.route('/runquestion', methods=['POST'])
def run_question():
    """
    Endpoint que recebe um JSON, o processa usando a classe ProcessarCognee
    e retorna a resposta diretamente.
    """
    # 1. Obter os dados JSON da requisição
    try:
        dados_recebidos = request.get_json()
        if dados_recebidos is None:
            return jsonify({"erro": "Corpo da requisição inválido ou não é JSON."}), 400
    except Exception:
        return jsonify({"erro": "Erro ao decodificar o JSON da requisição."}), 400

    try:
        # 2. Criar uma instância da nossa classe de processamento,
        #    passando os dados recebidos no construtor.
        processador = ProcessarCognee(dados_recebidos)

        # 3. Chamar o método que executa toda a lógica.
        resultado_final = processador.executar()
        
        # 4. Retornar a resposta do processamento para o cliente.
        return jsonify(resultado_final), 200

    except ValueError as e:
        # Captura erros de validação (ex: falta de 'context' ou 'question')
        return jsonify({"erro": "Dados de entrada inválidos.", "detalhes": str(e)}), 400

    except Exception as e:
        # Captura qualquer outro erro que possa ocorrer durante o processamento do Cognee.
        # É uma boa prática logar o erro completo no servidor para depuração.
        app.logger.error(f"Erro inesperado durante o processamento: {e}", exc_info=True)
        return jsonify({"erro": "Um erro inesperado ocorreu no servidor durante o processamento.", "detalhes": str(e)}), 500

# Permite executar o servidor com 'python app.py'
if __name__ == '__main__':
    app.run(debug=True, port=5000)
