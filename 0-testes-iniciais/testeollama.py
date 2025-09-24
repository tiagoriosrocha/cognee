import ollama

# Defina o modelo que deseja usar
model_name = "phi4:latest"

# Crie um prompt no formato de lista de mensagens
prompt = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

# Opções do modelo
temperature = 0.0
max_tokens = 256

# Chama o modelo
response = ollama.chat(
    model=model_name,
    messages=prompt,
    options={
        'temperature': temperature,
        'max_tokens': max_tokens
    }
)

# Converte a resposta em texto
answer = str(response)
print(answer)
