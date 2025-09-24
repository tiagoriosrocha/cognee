import cognee
import asyncio
import logging
import os

from cognee.api.v1.search import SearchType
from cognee.api.v1.visualize.visualize import visualize_graph
#from cognee.shared.utils import setup_logging

# Define your text data (insert your full texts for text_1 and text_2)
text_1 = '''
Audi is a CarManufacturer that originatesFrom Germany.
Audi produces the Audi A4, which is a CarModel.
The Audi A4 hasType Sedan.
The Audi A4 hasEngine TFSI Engine.
The TFSI Engine usesFuel Petrol.
The Audi A4 hasFeature Quattro All-Wheel Drive.
The Audi A4 hasSafetyFeature Airbags.
The Audi A4 introducedIn Year 1994.
Audi also produces the Audi Q7.
The Audi Q7 hasType SUV.
The Audi Q7 hasEngine V6 Engine.
The V6 Engine usesFuel Diesel.
The Audi Q7 hasFeature Adaptive Cruise Control.
The Audi Q7 hasSafetyFeature Lane Assist.
The Audi Q7 introducedIn Year 2005.
BMW is a CarManufacturer that originatesFrom Germany.
BMW produces the BMW 3 Series.
The BMW 3 Series hasType Sedan.
The BMW 3 Series hasEngine TwinPower Turbo Engine.
The TwinPower Turbo Engine usesFuel Petrol.
The BMW 3 Series hasFeature Rear-Wheel Drive.
The BMW 3 Series hasSafetyFeature Stability Control.
The BMW 3 Series introducedIn Year 1975.
BMW also produces the BMW X5.
The BMW X5 hasType SUV.
The BMW X5 hasEngine Inline 6 Engine.
The Inline 6 Engine usesFuel Diesel.
The BMW X5 hasFeature All-Wheel Drive.
The BMW X5 hasSafetyFeature Blind Spot Detection.
The BMW X5 introducedIn Year 1999.
Mercedes-Benz is a CarManufacturer that originatesFrom Germany.
Mercedes-Benz produces the Mercedes C-Class.
The Mercedes C-Class hasType Sedan.
The Mercedes C-Class hasEngine M274 Engine.
The M274 Engine usesFuel Petrol.
The Mercedes C-Class hasFeature Rear-Wheel Drive.
The Mercedes C-Class hasSafetyFeature ABS Brakes.
The Mercedes C-Class introducedIn Year 1993.
Mercedes-Benz also produces the Mercedes GLE.
The Mercedes GLE hasType SUV.
The Mercedes GLE hasEngine V8 Engine.
The V8 Engine usesFuel Diesel.
The Mercedes GLE hasFeature Air Suspension.
The Mercedes GLE hasSafetyFeature Collision Prevention Assist.
The Mercedes GLE introducedIn Year 1997.
Porsche is a CarManufacturer that originatesFrom Germany.
Porsche produces the Porsche 911.
The Porsche 911 hasType Sports Car.
The Porsche 911 hasEngine Flat-Six Engine.
The Flat-Six Engine usesFuel Petrol.
The Porsche 911 hasFeature Rear-Engine Layout.
The Porsche 911 hasSafetyFeature Advanced Braking System.
The Porsche 911 introducedIn Year 1964.
Porsche also produces the Porsche Cayenne.
The Porsche Cayenne hasType SUV.
The Porsche Cayenne hasEngine V6 Turbo Engine.
The V6 Turbo Engine usesFuel Petrol.
The Porsche Cayenne hasFeature Adaptive Suspension.
The Porsche Cayenne hasSafetyFeature Traction Control.
The Porsche Cayenne introducedIn Year 2002.
Volkswagen is a CarManufacturer that originatesFrom Germany.
Volkswagen produces the Volkswagen Golf.
The Volkswagen Golf hasType Hatchback.
The Volkswagen Golf hasEngine TSI Engine.
The TSI Engine usesFuel Petrol.
The Volkswagen Golf hasFeature Front-Wheel Drive.
The Volkswagen Golf hasSafetyFeature ABS Brakes.
The Volkswagen Golf introducedIn Year 1974.
Volkswagen also produces the Volkswagen Tiguan.
The Volkswagen Tiguan hasType SUV.
The Volkswagen Tiguan hasEngine TDI Engine.
The TDI Engine usesFuel Diesel.
The Volkswagen Tiguan hasFeature 4Motion Drive.
The Volkswagen Tiguan hasSafetyFeature Lane Assist.
The Volkswagen Tiguan introducedIn Year 2007.
Toyota is a CarManufacturer that originatesFrom Japan.
Toyota produces the Toyota Corolla.
The Toyota Corolla hasType Sedan.
The Toyota Corolla hasEngine VVT-i Engine.
The VVT-i Engine usesFuel Petrol.
The Toyota Corolla hasFeature Front-Wheel Drive.
The Toyota Corolla hasSafetyFeature Stability Control.
The Toyota Corolla introducedIn Year 1966.
Toyota also produces the Toyota RAV4.
The Toyota RAV4 hasType SUV.
The Toyota RAV4 hasEngine Hybrid Engine.
The Hybrid Engine usesFuel Petrol and Electricity.
The Toyota RAV4 hasFeature Electric Motor Assist.
The Toyota RAV4 hasSafetyFeature Collision Avoidance System.
The Toyota RAV4 introducedIn Year 1994.
Tesla is a CarManufacturer that originatesFrom United States.
Tesla produces the Tesla Model S.
The Tesla Model S hasType Sedan.
The Tesla Model S hasEngine Electric Powertrain.
The Electric Powertrain usesFuel Electricity.
The Tesla Model S hasFeature Autopilot.
The Tesla Model S hasSafetyFeature Full Self-Driving Assist.
The Tesla Model S introducedIn Year 2012.
Tesla also produces the Tesla Model X.
The Tesla Model X hasType SUV.
'''

text_2 = '''
CarManufacturers play a central role in the global automotive industry.
Every CarManufacturer originatesFrom a specific Country.
German manufacturers are often associated with precision engineering.
Japanese manufacturers are known for reliability and efficiency.
American manufacturers frequently emphasize innovation and scale.
A CarManufacturer usually produces more than one CarModel.
Each CarModel hasType, such as Sedan, SUV, Hatchback, or Sports Car.
Sedans are popular because they balance comfort and practicality.
SUVs are valued for their spacious interiors and versatility.
Sports Cars emphasize performance and speed.
Hatchbacks are compact and convenient for city driving.
Every CarModel hasEngine, defining its core performance.
An Engine usesFuel, which can vary across manufacturers.
Petrol remains a common FuelType for many cars.
Diesel engines are still significant in large vehicles like SUVs.
Hybrid engines combine traditional fuel with electricity.
Fully electric powertrains rely entirely on Electricity.
A CarModel may haveFeature that enhances comfort or performance.
Features can include advanced navigation, all-wheel drive, or suspension systems.
Safety is also essential in the ontology.
Every CarModel hasSafetyFeature to protect passengers.
Common safety features include airbags, stability control, and ABS brakes.
Newer safety systems include collision avoidance and lane assist.
A CarModel introducedIn a given Year shows the evolution of automotive design.
Some CarModels remain in production for decades.
Others are quickly replaced by newer generations.
CarManufacturers often competeWith one another globally.
Competition can be regional or international.
German CarManufacturers like Audi, BMW, and Mercedes-Benz are direct rivals.
Japanese CarManufacturers like Toyota and Honda compete in mass markets.
American CarManufacturers like Ford and Tesla compete through innovation.
Audi is an example of a CarManufacturer that originatesFrom Germany.
BMW is another German CarManufacturer.
Mercedes-Benz also originatesFrom Germany.
Porsche is well known as a German Sports Car manufacturer.
Volkswagen is a German CarManufacturer with a wide product range.
Toyota is a CarManufacturer that originatesFrom Japan.
Honda also originatesFrom Japan.
Nissan is another Japanese CarManufacturer.
Tesla is a CarManufacturer that originatesFrom the United States.
Ford is another American CarManufacturer.
General Motors belongsToGroup with brands like Chevrolet and Cadillac.
Each CarManufacturer has a reputation linked to quality and identity.
German brands emphasize performance and luxury.
Japanese brands emphasize durability and affordability.
American brands emphasize technology and scale.
CarModels are often associated with CarType to attract different customers.
Luxury Sedans aim at executives and professionals.
Compact Hatchbacks aim at young urban drivers.
SUVs attract families needing space and flexibility.
Sports Cars attract enthusiasts seeking speed.
Engines are central to classification in the ontology.
Petrol engines are efficient for small to medium cars.
Diesel engines provide torque for large vehicles.
Hybrid engines reduce emissions and fuel use.
Electric powertrains represent a major technological shift.
Manufacturers invest heavily in new Engine technology.
Some governments encourage electric adoption with incentives.
Hybrid technology represents a transitional stage.
Fully electric adoption is accelerating globally.
Features differentiate one CarModel from another.
Comfort features may include climate control and leather seats.
Performance features may include adaptive suspension and turbocharging.
Safety features are increasingly mandatory worldwide.
Advanced driver-assistance systems are growing in use.
Lane assist and blind spot detection increase driver awareness.
Collision prevention systems reduce accidents.
Autonomous driving is an emerging Feature.
Tesla emphasizes Autopilot and Full Self-Driving Assist.
Traditional manufacturers are also investing in automation.
Each CarModel belongsToGroup of vehicles in its CarManufacturer portfolio.
Volkswagen Group includes Audi, Porsche, and Lamborghini.
Toyota Group includes Lexus.
Honda Group includes Acura.
Global competition drives technological change.
Japanese manufacturers pioneered hybrid technology.
German manufacturers pioneered turbocharging and diesel efficiency.
American manufacturers pioneered electric powertrains.
The ontology captures this diversity in structured relationships.
A CarManufacturer is linked to CarModel via produces.
A CarModel is linked to CarType via hasType.
A CarModel is linked to Engine via hasEngine.
An Engine is linked to FuelType via usesFuel.
A CarModel is linked to Feature via hasFeature.
A CarModel is linked to SafetyFeature via hasSafetyFeature.
A CarModel is linked to Year via introducedIn.
A CarManufacturer is linked to Country via originatesFrom.
CarManufacturers are linked to each other via competesWith.
Groups of CarManufacturers are linked via belongsToGroup.
This web of relationships forms a Knowledge Graph.
The Knowledge Graph enables reasoning beyond the text.
For example, if a CarModel uses Diesel and hasType SUV, one can infer efficiency focus.
if a CarManufacturer originatesFrom Japan and produces Hybrid models, one can infer eco-friendly strategy.
If a CarManufacturer originatesFrom Germany and produces Sports Cars, one can infer performance strategy.
Ontologies help LLMs structure answers to complex queries.
Cognee uses ontologies to enrich Knowledge Graph construction.
This allows better alignment between text and structured data.
The text plus ontology create a consistent semantic layer.
From that, descriptive metrics and inferences become possible.
Ultimately, the ontology bridges human language and machine reasoning.
'''

async def main():
    # Passo 1: Redefinir dados e estado do sistema
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    # Passo 2: Adicionar dados de texto
    text_list = [text_1, text_2]
    await cognee.add(text_list)

    # Passo 3: Criar o grafo de conhecimento usando a ontologia personalizada
    ontology_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "ontology_cars.xml"
    )
    pipeline_run = await cognee.cognify(ontology_file_path=ontology_path)
    print("Grafo de conhecimento com ontologia criado.")

    # Passo 4: Calcular métricas descritivas (opcional, mantido comentado)
    #await cognee.get_pipeline_run_metrics(pipeline_run, include_optional=True)
    #print("Métricas descritivas do grafo salvas no banco de dados.")

    
    # Step 5: Query insights from the graph
    search_results = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="Which manufacturers produce SUVs with diesel engines, and from which countries do these manufacturers originate?",
    )
    print(search_results)

    # Passo 5: Exportar todas as entidades nomeadas (nós do grafo)
    print("\n--- EXPORTANDO ENTIDADES NOMEADAS ---")
    cypher_query_entities = """
    MATCH (n)
    RETURN n.id AS id, labels(n) AS labels, properties(n) AS properties
    """
    entity_results = await cognee.search(query_text=cypher_query_entities, query_type=SearchType.CYPHER)
    print(entity_results)


    # Passo 6: Exportar TODAS as relações para entender a estrutura do grafo
    print("\n--- EXPORTANDO TODAS AS RELAÇÕES NO GRAFO ---")
    # A consulta anterior falhou porque o padrão `(entity)-[:HAS_MENTION]->(word)` não foi encontrado.
    # Esta nova consulta é mais genérica: ela pega QUALQUER nó (n) conectado a QUALQUER outro nó (m)
    # através de QUALQUER relação (r). Isso nos ajudará a ver a estrutura real do grafo e
    # a criar consultas mais específicas depois.
    cypher_query_all_relations = """
    MATCH (n)-[r]->(m)
    RETURN
        n.id AS source_node_id,
        labels(n) AS source_node_labels,
        type(r) AS relationship_type,
        m.id AS target_node_id,
        labels(m) AS target_node_labels
    LIMIT 100
    """
    relation_results = await cognee.search(query_text=cypher_query_all_relations, query_type=SearchType.CYPHER)
    print(relation_results)


    # Passo 7: Visualizar o grafo de conhecimento e salvá-lo em HTML (opcional)
    print("\nVisualização do grafo sendo gerada em 'graph.html'...")
    await visualize_graph()
    print("Visualização concluída.")


if __name__ == "__main__":
#    setup_logging(logging.INFO)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())