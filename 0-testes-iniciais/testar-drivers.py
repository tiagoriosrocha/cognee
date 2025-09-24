from neo4j import GraphDatabase
import psycopg

print("Drivers carregados com sucesso!")

# Teste Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
with driver.session() as session:
    result = session.run("RETURN 1 AS test")
    print("Neo4j:", result.single()["test"])

# Teste Postgres
with psycopg.connect("dbname=cognee user=cognee password=cognee host=localhost") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        print("Postgres:", cur.fetchone())
