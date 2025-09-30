import json
from processar_cognee import ProcessarCognee

# Dados de exemplo que seriam enviados pela interface
dados_de_exemplo = {
    'selectedQuestion': {
        '_id': '5ae738f75542991bbc9761c4_3',
        'question': 'What is the closest palindrome number to the year the brother of this first round draft pick by the Washington Redskins was drafted?',
        'answer': '2002',
        'previous_question': 'What year was the brother of this first round draft pick by the Washington Redskins drafted?',
        'previous_answer': '2003',
        'question_decomposition': [
            {
                'sub_id': '1',
                'question': 'Who is the brother of this first round draft pick by the Washington Redskins?',
                'answer': 'Boss Bailey',
                'paragraph_support_title': 'Champ Bailey'
            },
            {
                'sub_id': '2',
                'question': 'What year was Boss Bailey drafted?',
                'answer': '2003',
                'paragraph_support_title': 'Boss Bailey'
            },
            {
                'sub_id': '3',
                'question': 'What is the closest palindrome number to 2003?',
                'answer': '2002',
                'paragraph_support_title': '',
                'details': []
            }
        ],
        'context': [
            [
                'Champ Bailey',
                [
                    'Roland "Champ" Bailey Jr. (born June 22, 1978) is a former American football cornerback in the National Football League (NFL).',
                    ' He played college football for Georgia, where he earned consensus All-American honors, and was drafted by the Washington Redskins in the first round of the 1999 NFL Draft.',
                    ' He is the brother of former NFL linebacker Boss Bailey.'
                ]
            ],
            [
                'Boss Bailey',
                [
                    'Rodney "Boss" Bailey (born October 14, 1979) is a former American football linebacker who played in the National Football League.',
                    ' He was originally drafted by the Detroit Lions in the second round of the 2003 NFL Draft.',
                    ' He played college football at the University of Georgia.',
                    ' He is the brother of former NFL cornerback Champ Bailey.'
                ]
            ]
        ],
        'answer_type': 'number',
        'previous_answer_type': 'year',
        'no_of_hops': 1,
        'reasoning_type': 'Commonsense, Arithmetic',
        'pattern': 'What is the closest palindrome number to #Year?',
        'subquestion_patterns': [''],
        'cutted_question': 'the year the brother of this first round draft pick by the Washington Redskins was drafted',
        'ques_on_last_hop': 'What is the closest palindrome number to the year Boss Bailey was drafted?'
    },
    'processingType': 1
}

def main():
    """
    Função principal que executa o teste.
    """
    print("--- Iniciando o processamento via terminal ---")
    
    # A classe ProcessarCognee espera receber o dicionário que contém 'context' e 'question'.
    # No seu exemplo, este dicionário está dentro da chave 'selectedQuestion'.
    dados_para_processar = dados_de_exemplo['selectedQuestion']

    print("\n--- Dados que serão enviados para o construtor da classe ---")
    print(json.dumps(dados_para_processar, indent=2))
    
    try:
        # 1. Cria uma instância da nossa classe de processamento,
        #    passando os dados diretamente para o construtor.
        processador = ProcessarCognee(dados_para_processar)

        print("\n--- Executando o processamento do Cognee (isso pode levar um tempo)... ---")
        
        # 2. Chama o método que executa toda a lógica.
        resultado_final = processador.executar()
        
        # 3. Imprime o resultado final de forma legível.
        print("\n--- Resultado Final do Processamento ---")
        print(json.dumps(resultado_final, indent=4, ensure_ascii=False))
        print("\n--- Processamento concluído com sucesso! ---")

    except Exception as e:
        print(f"\n--- OCORREU UM ERRO DURANTE O PROCESSAMENTO ---")
        print(f"Detalhes do erro: {e}")

# Ponto de entrada padrão para scripts Python
if __name__ == "__main__":
    main()