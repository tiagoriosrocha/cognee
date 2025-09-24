# app.py
import subprocess
import sys
import json
from flask import Flask, request, jsonify

# Inicializa a aplicação Flask
app = Flask(__name__)

@app.route('/runquestion', methods=['POST'])
def run_question():
    """
    Endpoint que recebe um JSON, passa para um script externo e retorna a resposta.
    """
    # 1. Obter os dados JSON da requisição
    try:
        dados_recebidos = request.get_json()
        if dados_recebidos is None:
            return jsonify({"erro": "Corpo da requisição inválido ou não é JSON."}), 400
            
        # ################### INÍCIO DA ALTERAÇÃO ###################
        #
        # Imprime o JSON recebido no terminal de forma formatada (pretty-print)
        #print("\n================ JSON Recebido ================")
        #print(json.dumps(dados_recebidos, indent=4, ensure_ascii=False))
        #print("=============================================\n")
        #
        # #################### FIM DA ALTERAÇÃO #####################

    except Exception:
        return jsonify({"erro": "Erro ao decodificar o JSON."}), 400

    try:
        # 2. Converter o dicionário Python de volta para uma string JSON para enviar ao script
        dados_para_script = json.dumps(dados_recebidos)

        # 3. Chamar o script 'processar_cognee.py' como um subprocesso
        processo = subprocess.run(
            [sys.executable, 'processar_cognee.py'],
            input=dados_para_script,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8' # Garante a codificação correta
        )

        # 4. A saída do script (stdout) é a nossa resposta. Convertemos de volta para JSON.
        resposta_do_script = json.loads(processo.stdout)
        
        # 5. Retornar a resposta do script para o cliente
        return jsonify(resposta_do_script), 200

    except FileNotFoundError:
        return jsonify({"erro": "Script de processamento não encontrado."}), 500
        
    except subprocess.CalledProcessError as e:
        erro_retornado = e.stderr.strip()
        try:
            erro_json = json.loads(erro_retornado)
            return jsonify(erro_json), 500
        except json.JSONDecodeError:
            return jsonify({"erro": "Erro interno no script de processamento.", "detalhes": erro_retornado}), 500

    except json.JSONDecodeError:
        return jsonify({"erro": "A resposta do script de processamento não é um JSON válido."}), 500
        
    except Exception as e:
        return jsonify({"erro": "Um erro inesperado ocorreu no servidor.", "detalhes": str(e)}), 500

# Permite executar o servidor com 'python app.py'
if __name__ == '__main__':
    app.run(debug=True, port=5000)