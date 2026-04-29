from cognee.modules.ontology.base_ontology_resolver import BaseOntologyResolver
from cognee.modules.ontology.rdf_xml.RDFLibOntologyResolver import (
    RDFLibOntologyResolver,
    EnhancedOntologyResolver,
    EmbeddingEnhancedOntologyResolver,
)
from cognee.modules.ontology.matching_strategies import (
    FuzzyMatchingStrategy,
    SemanticMatchingStrategy,
)


def get_default_ontology_resolver() -> BaseOntologyResolver:
    return EmbeddingEnhancedOntologyResolver(
        ontology_file=None, matching_strategy=FuzzyMatchingStrategy()
    )


def get_ontology_resolver_from_env(
    ontology_resolver: str = "", matching_strategy: str = "", ontology_file_path: str = ""
) -> BaseOntologyResolver:
    """
    Create and return an ontology resolver instance based on environment parameters.

    This factory supports RDFLib resolvers with three matching modes:
    - fuzzy: URI/local-name lookup with fuzzy text matching
    - semantic: label/altLabel-aware text lookup
    - hybrid: label/altLabel-aware text lookup plus embedding fallback

    Args:
        ontology_resolver (str): The ontology resolver type to use.
            Supported value: "rdflib".
        matching_strategy (str): The matching strategy to apply.
            Supported values: "fuzzy", "semantic", "hybrid", "embedding".
        ontology_file_path (str): Path to the ontology file(s) required for the resolver.
            Can be a single path or comma-separated paths for multiple files.

    Returns:
        BaseOntologyResolver: An instance of the requested ontology resolver.

    Raises:
        EnvironmentError: If the provided resolver or strategy is unsupported,
            or if required parameters are missing.
    """
    if ontology_resolver != "rdflib" or not ontology_file_path:
        raise EnvironmentError(
            f"Unsupported ontology resolver: {ontology_resolver}. "
            "Supported resolvers are: rdflib with fuzzy, semantic, or hybrid matching."
        )

    if "," in ontology_file_path:
        file_paths = [path.strip() for path in ontology_file_path.split(",")]
    else:
        file_paths = ontology_file_path

    if matching_strategy == "fuzzy":
        return RDFLibOntologyResolver(
            matching_strategy=FuzzyMatchingStrategy(), ontology_file=file_paths
        )

    if matching_strategy == "labeld":
        return EnhancedOntologyResolver(
            matching_strategy=SemanticMatchingStrategy(), ontology_file=file_paths
        )

    if matching_strategy in {"embedding"}:
        return EmbeddingEnhancedOntologyResolver(
            matching_strategy=FuzzyMatchingStrategy(), ontology_file=file_paths
        )

    raise EnvironmentError(
        f"Unsupported ontology resolver: {ontology_resolver}. "
        "Supported resolvers are: rdflib with fuzzy, semantic, or hybrid matching."
    )
