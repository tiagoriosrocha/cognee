#!/usr/bin/env bash
set -e

# ==========================
# CONFIGURAÇÕES
# ==========================
NEO4J_VERSION="2025.08.0"
APOC_JAR="apoc-${NEO4J_VERSION}-core.jar"
APOC_URL="https://github.com/neo4j/apoc/releases/download/${NEO4J_VERSION}/${APOC_JAR}"
PLUGIN_DIR="/var/lib/neo4j/plugins"
NEO4J_CONF="/etc/neo4j/neo4j.conf"
VENV_DIR="$HOME/Documents/cognee/.venv"

# ==========================
# DEPENDÊNCIAS
# ==========================
echo " Atualizando pacotes..."
sudo apt update
sudo apt install -y python3.12-venv python3-pip wget

# ==========================
# AMBIENTE VIRTUAL
# ==========================
echo " Configurando ambiente virtual..."
cd ~/Documents/cognee
rm -rf .venv
python3 -m venv .venv --without-pip
source "$VENV_DIR/bin/activate"

pip install --upgrade pip setuptools wheel

echo " Instalando pacotes Python..."
pip install "neo4j>=5.0,<6.0"
pip install "psycopg[binary]>=3.1"
pip install cognee
pip install transformers
pip install torch
pip install sentence-transformers
pip install asyncpg
pip install "sqlalchemy[asyncio]" psycopg2-binary asyncpg

deactivate

# ==========================
# APOC PLUGIN
# ==========================
echo " Baixando APOC $NEO4J_VERSION..."
wget -q "$APOC_URL" -O "/tmp/$APOC_JAR"
echo " Copiando APOC para $PLUGIN_DIR..."
sudo mkdir -p "$PLUGIN_DIR"
sudo cp "/tmp/$APOC_JAR" "$PLUGIN_DIR/"
sudo chown neo4j:neo4j "$PLUGIN_DIR/$APOC_JAR"

# ==========================
# CONFIG NEO4J
# ==========================
echo " Configurando Neo4j..."
sudo sed -i '/dbms.security.procedures.unrestricted/d' "$NEO4J_CONF"
sudo sed -i '/dbms.security.procedures.allowlist/d' "$NEO4J_CONF"

echo "dbms.security.procedures.unrestricted=apoc.*" | sudo tee -a "$NEO4J_CONF"
echo "dbms.security.procedures.allowlist=apoc.*" | sudo tee -a "$NEO4J_CONF"

# ==========================
# RESTART NEO4J
# ==========================
echo " Reiniciando Neo4j..."
sudo systemctl restart neo4j

echo ""
echo " Ambiente pronto!"
echo "  Ative o venv com:"
echo "   source $VENV_DIR/bin/activate"
echo ""
echo "  Teste o APOC com:"
echo "   cypher-shell -u neo4j -p 'sua_senha' \"CALL apoc.help('addLabels');\""
