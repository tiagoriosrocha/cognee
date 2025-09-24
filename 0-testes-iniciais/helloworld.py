import cognee
import asyncio

async def main():

    # Create a clean slate for cognee -- reset data and system state
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    
    # Add sample content
    text = """
    A história da internet é uma narrativa de colaboração, inovação e descentralização que transformou radicalmente a comunicação humana. Suas origens remontam ao final da década de 1960, com a criação da ARPANET (Advanced Research Projects Agency Network) pelo Departamento de Defesa dos Estados Unidos. O objetivo inicial era criar uma rede de comunicação robusta e descentralizada que pudesse sobreviver a uma falha em um de seus pontos, como em um cenário de guerra. O primeiro nó foi instalado na UCLA (Universidade da Califórnia, Los Angeles) e, logo depois, no Stanford Research Institute, na UC Santa Barbara e na Universidade de Utah.

    Um dos pilares fundamentais da internet, o protocolo TCP/IP (Transmission Control Protocol/Internet Protocol), foi desenvolvido por Vinton Cerf e Robert Kahn na década de 1970. Esse conjunto de regras permitiu que diferentes redes de computadores se comunicassem entre si, criando uma "rede de redes". A adoção do TCP/IP pela ARPANET em 1º de janeiro de 1983 é considerada por muitos como o nascimento oficial da internet como a conhecemos.

    Avançando para a década de 1990, a internet começou a tomar uma forma mais acessível ao público. Em 1989, no CERN (Organização Europeia para a Pesquisa Nuclear), o cientista britânico Tim Berners-Lee propôs um sistema de gerenciamento de informações que usava hipertexto para ligar documentos em uma rede global. Ele desenvolveu o primeiro navegador web, chamado WorldWideWeb, o primeiro servidor web, e as tecnologias subjacentes como HTML (HyperText Markup Language), URI (Uniform Resource Identifier) e HTTP (Hypertext Transfer Protocol). Essa invenção, a World Wide Web, tornou a internet um espaço navegável e visualmente rico, impulsionando sua popularidade.

    Com a popularização da Web, surgiram os primeiros provedores de acesso à internet comerciais e empresas que viriam a se tornar gigantes da tecnologia. A Netscape Communications lançou seu navegador Navigator em 1994, que dominou o mercado inicial. Pouco depois, a Microsoft integrou o Internet Explorer em seu sistema operacional Windows, dando início à chamada "guerra dos navegadores". Paralelamente, empresas como a Amazon, fundada por Jeff Bezos em 1994, começaram a explorar o potencial do comércio eletrônico, vendendo livros online. No mesmo período, o Google foi fundado por Larry Page e Sergey Brin, revolucionando a forma como as pessoas encontram informações online com seu inovador algoritmo de busca, o PageRank. A transição para o século XXI viu a ascensão das redes sociais, com plataformas como Facebook e Twitter redefinindo a interação social e a disseminação de informações.
    """
    await cognee.add(text)
    
    # Process with LLMs to build the knowledge graph
    await cognee.cognify()
    
    # Search the knowledge graph
    results = await cognee.search(
        query_text="Quem desenvolveu o protocolo TCP/IP e em qual década?"
    )
    
    # Print
    for result in results:
        print(result)

if __name__ == '__main__':
    asyncio.run(main())
