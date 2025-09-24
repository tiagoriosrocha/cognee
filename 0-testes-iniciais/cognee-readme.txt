1. Atualizar pacotes e instalar Python + venv
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip -y

2. instalando uv
curl -LsSf https://astral.sh/uv/install.sh | sh

3. ativando o ambiente virtual
uv venv && source .venv/bin/activate

4. criando um arquivo para as variáveis de ambiente
nano .env

5. instalar o postgres
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql
CREATE USER cognee WITH PASSWORD 'cognee';
CREATE DATABASE cognee OWNER cognee;
\q

6. instalar outras dependências
uv pip install openai psycopg2-binary python-dotenv

7. instalar o cognee
sudo apt install -y libpq-dev gcc python3-dev
uv pip install "cognee[postgres]"
uv pip install transformers


8. configurando as variáveis de ambiente
LLM_API_KEY="AAAAC3NzaC1lZDI1NTE5AAAAIBLBgACsVq8WvGJVodY73BZUK3G7tevgowknqTXG0m6z"
LLM_MODEL="phi4:latest"
LLM_PROVIDER="ollama"
LLM_ENDPOINT="http://localhost:11434/v1"
EMBEDDING_PROVIDER="ollama"
EMBEDDING_MODEL="avr/sfr-embedding-mistral:latest"
EMBEDDING_ENDPOINT="http://localhost:11434/api/embeddings"
EMBEDDING_DIMENSIONS=4096
HUGGINGFACE_TOKENIZER="Salesforce/SFR-Embedding-Mistral"
DB_PROVIDER=postgres
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=cognee
DB_PASSWORD=cognee
DB_NAME=cognee

ou

LLM_API_KEY="ollama"
LLM_MODEL="gpt-oss:20b"
LLM_PROVIDER="ollama"
LLM_ENDPOINT="http://localhost:11434/v1"
EMBEDDING_PROVIDER="ollama"
EMBEDDING_MODEL="gpt-oss:20b"
EMBEDDING_ENDPOINT="http://localhost:11434/api/embeddings"
EMBEDDING_DIMENSIONS=4096
HUGGINFACE_TOKENIZER="gpt-oss:20b"


