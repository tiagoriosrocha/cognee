# processar_cognee.py
import sys
import json

def processar_dados(dados):
    """
    Função que simula o processamento dos dados recebidos.
    Aqui você colocaria a sua lógica principal.
    
    Para este exemplo, vamos apenas adicionar uma chave "status" ao dicionário.
    """
    # Exemplo: Adiciona um status e a origem do processamento
    dados['status'] = 'processado_com_sucesso'
    dados['processado_por'] = 'processar_cognee.py'
    return dados

if __name__ == "__main__":
    try:
        # 1. Lê os dados da entrada padrão (enviados pelo Flask)
        dados_de_entrada_str = sys.stdin.read()
        
        # 2. Converte a string JSON para um dicionário Python
        dados_json = json.loads(dados_de_entrada_str)
        
        # 3. Chama a função de processamento
        resultado = processar_dados(dados_json)
        
        # 4. Converte o resultado de volta para uma string JSON
        resultado_json_str = json.dumps(resultado, indent=4)
        
        # 5. Imprime o resultado na saída padrão para o Flask capturar
        print(resultado_json_str)
        
    except Exception as e:
        # Em caso de erro, cria um JSON de erro e o imprime na saída de erro
        erro_json = json.dumps({
            "status": "erro_no_processamento",
            "detalhe": str(e)
        })
        # Imprime na saída de erro padrão (stderr)
        print(erro_json, file=sys.stderr)
        sys.exit(1) # Termina o script com um código de erro
