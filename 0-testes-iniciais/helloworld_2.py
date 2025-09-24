import cognee
import asyncio

async def main():

    # Create a clean slate for cognee -- reset data and system state
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    
    # Add sample content
    text = """
    "Blind Shaft" é um filme de 2003 sobre um par de vigaristas que operam nas minas de carvão ilegais do norte da China. O filme foi escrito e dirigido por Li Yang e é baseado no conto "Shen Mu (Sacred Wood)" do escritor chinês Liu Qingbang.

    Outro filme notável é "The Mask of Fu Manchu", uma aventura pré-Código de 1932 dirigida por Charles Brabin e baseada no romance de Sax Rohmer. Estrelado por Boris Karloff como Fu Manchu e Myrna Loy como sua filha depravada, o filme gira em torno da busca de Fu Manchu pela espada e máscara douradas de Gêngis Khan. Este filme inspirou "Les Trottoirs de Bangkok" (1984), um thriller erótico dirigido por Jean Rollin.

    O personagem Dr. Fu Manchu apareceu em vários outros filmes. O primeiro da era sonora foi "The Mysterious Dr. Fu Manchu" (1929), dirigido por Rowland V. Lee e estrelado por Warner Oland. Como foi um período de transição, uma versão silenciosa também foi lançada. Sua sequência, "The Return of Dr. Fu Manchu" (1930), traz Oland de volta ao papel, buscando vingança.

    Mais tarde, uma série de cinco filmes estrelada por Christopher Lee como o vilão foi produzida por Harry Alan Towers. O primeiro foi "The Face of Fu Manchu" (1965), uma coprodução britânico-alemã-ocidental dirigida por Don Sharp. Foi seguido por "The Brides of Fu Manchu" (1966), também dirigido por Sharp, com a ação ocorrendo principalmente em Londres. A série continuou com "The Vengeance of Fu Manchu" (1967), "The Blood of Fu Manchu" (1968), filmado na Espanha e no Brasil, e concluiu com "The Castle of Fu Manchu" (1969), o quinto e último filme de Lee no papel.

    A lista também inclui "The Mask of the Gorilla", um filme de ação francês de 1958 dirigido por Bernard Borderie.
    """
    await cognee.add(text)
    
    # Process with LLMs to build the knowledge graph
    await cognee.cognify()
    
    # Search the knowledge graph
    results = await cognee.search(
        query_text="Which film came out first, Blind Shaft or The Mask Of Fu Manchu?"
    )
    
    # Print
    for result in results:
        print(result)

if __name__ == '__main__':
    asyncio.run(main())
