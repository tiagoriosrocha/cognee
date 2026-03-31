from cognee.modules.ontology.base_ontology_resolver import BaseOntologyResolver
from cognee.modules.ontology.rdf_xml.RDFLibOntologyResolver import RDFLibOntologyResolver, EnhancedOntologyResolver
from cognee.modules.ontology.matching_strategies import FuzzyMatchingStrategy, SemanticMatchingStrategy


def get_default_ontology_resolver() -> BaseOntologyResolver:
    #Código original
    #return RDFLibOntologyResolver(ontology_file=None, matching_strategy=FuzzyMatchingStrategy())

    #Código alterado
    return EnhancedOntologyResolver(ontology_file=None, matching_strategy=SemanticMatchingStrategy())


def get_ontology_resolver_from_env(
    ontology_resolver: str = "", matching_strategy: str = "", ontology_file_path: str = ""
) -> BaseOntologyResolver:
    """
    Create and return an ontology resolver instance based on environment parameters.

    Currently, this function supports only the RDFLib-based ontology resolver
    with a fuzzy matching strategy.

    Args:
        ontology_resolver (str): The ontology resolver type to use.
            Supported value: "rdflib".
        matching_strategy (str): The matching strategy to apply.
            Supported value: "fuzzy".
        ontology_file_path (str): Path to the ontology file(s) required for the resolver.
            Can be a single path or comma-separated paths for multiple files.

    Returns:
        BaseOntologyResolver: An instance of the requested ontology resolver.

    Raises:
        EnvironmentError: If the provided resolver or strategy is unsupported,
            or if required parameters are missing.
    """
    if ontology_resolver == "rdflib" and matching_strategy == "fuzzy" and ontology_file_path:
        if "," in ontology_file_path:
            file_paths = [path.strip() for path in ontology_file_path.split(",")]
        else:
            file_paths = ontology_file_path

        #Código original
        #return RDFLibOntologyResolver( 
        #    matching_strategy=FuzzyMatchingStrategy(), ontology_file=file_paths
        #)

        #Código alterado
        return EnhancedOntologyResolver(
            matching_strategy=SemanticMatchingStrategy(), ontology_file=file_paths
        )
    else:
        raise EnvironmentError(
            f"Unsupported ontology resolver: {ontology_resolver}. "
            f"Supported resolvers are: RdfLib with FuzzyMatchingStrategy."
        )
