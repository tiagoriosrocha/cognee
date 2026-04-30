import difflib
import os
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Any, Union, IO

import numpy
from rdflib import Graph, URIRef, RDF, RDFS, OWL, SKOS

from cognee.shared.logging_utils import get_logger
from cognee.modules.ontology.exceptions import (
    OntologyInitializationError,
    FindClosestMatchError,
    GetSubgraphError,
)
from cognee.modules.ontology.base_ontology_resolver import BaseOntologyResolver
from cognee.modules.ontology.models import AttachedOntologyNode
from cognee.modules.ontology.matching_strategies import (
    MatchingStrategy,
    FuzzyMatchingStrategy,
    normalize_lookup_key,
)

logger = get_logger("OntologyAdapter")


@dataclass(frozen=True)
class OntologyEmbeddingCandidate:
    key: str
    text: str


class RDFLibOntologyResolver(BaseOntologyResolver):
    """RDFLib-based ontology resolver implementation.

    This implementation uses RDFLib to parse and work with RDF/OWL ontology files.
    It provides fuzzy matching and subgraph extraction capabilities for ontology entities.
    """

    max_logged_comparisons = 50

    def __init__(
        self,
        ontology_file: Optional[Union[str, List[str], IO, List[IO]]] = None,
        matching_strategy: Optional[MatchingStrategy] = None,
    ) -> None:
        super().__init__(matching_strategy)
        self.ontology_file = ontology_file
        try:
            self.graph = None
            if ontology_file is not None:
                files_to_load = []
                file_objects = []

                if hasattr(ontology_file, "read"):
                    file_objects = [ontology_file]
                elif isinstance(ontology_file, str):
                    files_to_load = [ontology_file]
                elif isinstance(ontology_file, list):
                    if all(hasattr(item, "read") for item in ontology_file):
                        file_objects = ontology_file
                    else:
                        files_to_load = ontology_file
                else:
                    raise ValueError(
                        f"ontology_file must be a string, list of strings, file-like object, list of file-like objects, or None. Got: {type(ontology_file)}"
                    )

                if file_objects:
                    self.graph = Graph()
                    loaded_objects = []
                    for file_obj in file_objects:
                        try:
                            content = file_obj.read()
                            self.graph.parse(data=content, format="xml")
                            loaded_objects.append(file_obj)
                            logger.info("Ontology loaded successfully from file object")
                        except Exception as e:
                            logger.warning("Failed to parse ontology file object: %s", str(e))

                    if not loaded_objects:
                        logger.info(
                            "No valid ontology file objects found. No owl ontology will be attached to the graph."
                        )
                        self.graph = None
                    else:
                        logger.info("Total ontology file objects loaded: %d", len(loaded_objects))

                elif files_to_load:
                    self.graph = Graph()
                    loaded_files = []
                    for file_path in files_to_load:
                        if os.path.exists(file_path):
                            self.graph.parse(file_path)
                            loaded_files.append(file_path)
                            logger.info("Ontology loaded successfully from file: %s", file_path)
                        else:
                            logger.warning(
                                "Ontology file '%s' not found. Skipping this file.",
                                file_path,
                            )

                    if not loaded_files:
                        logger.info(
                            "No valid ontology files found. No owl ontology will be attached to the graph."
                        )
                        self.graph = None
                    else:
                        logger.info("Total ontology files loaded: %d", len(loaded_files))
                else:
                    logger.info(
                        "No ontology file provided. No owl ontology will be attached to the graph."
                    )
            else:
                logger.info(
                    "No ontology file provided. No owl ontology will be attached to the graph."
                )
                self.graph = None

            self.build_lookup()
        except Exception as e:
            logger.error("Failed to load ontology", exc_info=e)
            raise OntologyInitializationError() from e

    def _uri_to_key(self, uri: URIRef) -> str:
        uri_str = str(uri)
        if "#" in uri_str:
            name = uri_str.split("#")[-1]
        else:
            name = uri_str.rstrip("/").split("/")[-1]
        return self._normalize_lookup_key(name)

    def _normalize_lookup_key(self, value: str) -> str:
        return normalize_lookup_key(value)

    def _get_text_matching_log_label(self) -> str:
        return "fuzzy"

    def _set_lookup_entry(self, category: str, key: str, uri: URIRef, source: str) -> None:
        self.lookup[category][key] = uri
        existing_sources = self.lookup_sources[category].setdefault(key, [])
        if source not in existing_sources:
            existing_sources.append(source)

    def _get_candidate_sources(self, category: str, candidate_key: str) -> str:
        sources = self.lookup_sources.get(category, {}).get(candidate_key, [])
        return ", ".join(sources) if sources else "unknown"

    def _log_text_comparisons(self, name: str, normalized_name: str, category: str) -> None:
        strategy_label = self._get_text_matching_log_label()
        candidates = list(self.lookup.get(category, {}).keys())

        logger.info(
            "[%s] Starting textual matching for input='%s' normalized='%s' category='%s' candidates=%d",
            strategy_label,
            name,
            normalized_name,
            category,
            len(candidates),
        )

        if not candidates:
            logger.info("[%s] No candidates available for category '%s'", strategy_label, category)
            return

        scored_candidates = [
            (
                candidate,
                difflib.SequenceMatcher(None, normalized_name, candidate).ratio(),
                self._get_candidate_sources(category, candidate),
            )
            for candidate in candidates
        ]
        scored_candidates.sort(key=lambda item: item[1], reverse=True)

        for candidate, similarity_score, sources in scored_candidates[
            : self.max_logged_comparisons
        ]:
            logger.info(
                "[%s] Compared input='%s' with candidate='%s' sources='%s' similarity=%.4f",
                strategy_label,
                normalized_name,
                candidate,
                sources,
                similarity_score,
            )

        if len(scored_candidates) > self.max_logged_comparisons:
            logger.info(
                "[%s] Comparison log truncated: showing top %d of %d candidates",
                strategy_label,
                self.max_logged_comparisons,
                len(scored_candidates),
            )

    def _log_text_match_result(
        self, name: str, normalized_name: str, category: str, matched_candidate: Optional[str]
    ) -> None:
        strategy_label = self._get_text_matching_log_label()
        if matched_candidate:
            logger.info(
                "[%s] Final textual match for input='%s' normalized='%s' category='%s': candidate='%s' sources='%s'",
                strategy_label,
                name,
                normalized_name,
                category,
                matched_candidate,
                self._get_candidate_sources(category, matched_candidate),
            )
        else:
            logger.info(
                "[%s] No textual match found for input='%s' normalized='%s' category='%s'",
                strategy_label,
                name,
                normalized_name,
                category,
            )

    def build_lookup(self) -> None:
        try:
            self.lookup: Dict[str, Dict[str, URIRef]] = {
                "classes": {},
                "individuals": {},
            }
            self.lookup_sources: Dict[str, Dict[str, List[str]]] = {
                "classes": {},
                "individuals": {},
            }

            if not self.graph:
                return None

            for cls in self.graph.subjects(RDF.type, OWL.Class):
                key = self._uri_to_key(cls)
                self._set_lookup_entry("classes", key, cls, "uri")

            for subj, _, obj in self.graph.triples((None, RDF.type, None)):
                if obj in self.lookup["classes"].values():
                    key = self._uri_to_key(subj)
                    self._set_lookup_entry("individuals", key, subj, "uri")

            logger.info(
                "Lookup built: %d classes, %d individuals",
                len(self.lookup["classes"]),
                len(self.lookup["individuals"]),
            )

            return None
        except Exception as e:
            logger.error("Failed to build lookup dictionary: %s", str(e))
            raise RuntimeError("Lookup build failed") from e

    def refresh_lookup(self) -> None:
        self.build_lookup()
        logger.info("Ontology lookup refreshed.")

    def find_closest_match(self, name: str, category: str) -> Optional[str]:
        try:
            normalized_name = self._normalize_lookup_key(name)
            possible_matches = list(self.lookup.get(category, {}).keys())

            self._log_text_comparisons(name, normalized_name, category)
            matched_candidate = self.matching_strategy.find_match(normalized_name, possible_matches)
            self._log_text_match_result(name, normalized_name, category, matched_candidate)

            return matched_candidate
        except Exception as e:
            logger.error("Error in find_closest_match: %s", str(e))
            raise FindClosestMatchError() from e

    def _get_category(self, uri: URIRef) -> str:
        if uri in self.lookup.get("classes", {}).values():
            return "classes"
        if uri in self.lookup.get("individuals", {}).values():
            return "individuals"
        return "unknown"

    def get_subgraph(
        self, node_name: str, node_type: str = "individuals", directed: bool = True
    ) -> Tuple[
        List[AttachedOntologyNode], List[Tuple[str, str, str]], Optional[AttachedOntologyNode]
    ]:
        nodes_set = set()
        edges: List[Tuple[str, str, str]] = []
        visited = set()
        queue = deque()

        try:
            closest_match = self.find_closest_match(name=node_name, category=node_type)
            if not closest_match:
                logger.info("No close match found for '%s' in category '%s'", node_name, node_type)
                return [], [], None

            node = self.lookup[node_type].get(closest_match)
            if node is None:
                logger.info("Node '%s' not found in lookup.", closest_match)
                return [], [], None

            logger.info("%s match was found for found for '%s' node", node, node_name)

            queue.append(node)
            visited.add(node)
            nodes_set.add(node)

            obj_props = set(self.graph.subjects(RDF.type, OWL.ObjectProperty))

            while queue:
                current = queue.popleft()
                current_label = self._uri_to_key(current)

                if node_type == "individuals":
                    for parent in self.graph.objects(current, RDF.type):
                        parent_label = self._uri_to_key(parent)
                        edges.append((current_label, "is_a", parent_label))
                        if parent not in visited:
                            visited.add(parent)
                            queue.append(parent)
                        nodes_set.add(parent)

                for parent in self.graph.objects(current, RDFS.subClassOf):
                    parent_label = self._uri_to_key(parent)
                    edges.append((current_label, "is_a", parent_label))
                    if parent not in visited:
                        visited.add(parent)
                        queue.append(parent)
                    nodes_set.add(parent)

                for prop in obj_props:
                    prop_label = self._uri_to_key(prop)
                    for target in self.graph.objects(current, prop):
                        target_label = self._uri_to_key(target)
                        edges.append((current_label, prop_label, target_label))
                        if target not in visited:
                            visited.add(target)
                            queue.append(target)
                        nodes_set.add(target)
                    if not directed:
                        for source in self.graph.subjects(prop, current):
                            source_label = self._uri_to_key(source)
                            edges.append((source_label, prop_label, current_label))
                            if source not in visited:
                                visited.add(source)
                                queue.append(source)
                            nodes_set.add(source)

            rdf_nodes = [
                AttachedOntologyNode(uri=uri, category=self._get_category(uri))
                for uri in list(nodes_set)
            ]
            rdf_root = (
                AttachedOntologyNode(uri=node, category=self._get_category(node))
                if node is not None
                else None
            )

            return rdf_nodes, edges, rdf_root
        except Exception as e:
            logger.error("Error in get_subgraph: %s", str(e))
            raise GetSubgraphError() from e


class EnhancedOntologyResolver(RDFLibOntologyResolver):
    """Resolver customizado que extrai rdfs:label para melhorar o match de entidades."""

    def __init__(
        self,
        ontology_file: Optional[Union[str, List[str], IO, List[IO]]] = None,
        matching_strategy: Optional[MatchingStrategy] = None,
    ) -> None:
        super().__init__(ontology_file=ontology_file, matching_strategy=matching_strategy)

    def build_lookup(self) -> None:
        super().build_lookup()

        if not getattr(self, "graph", None):
            return

        for propriedade, source_name in (
            (RDFS.label, "rdfs:label"),
            (SKOS.altLabel, "skos:altLabel"),
        ):
            for subj, obj in self.graph.subject_objects(propriedade):
                label_key = self._normalize_lookup_key(str(obj))
                if not label_key:
                    continue

                if subj in self.lookup.get("classes", {}).values():
                    self._set_lookup_entry("classes", label_key, subj, source_name)

                elif subj in self.lookup.get("individuals", {}).values():
                    self._set_lookup_entry("individuals", label_key, subj, source_name)

        logger.info("Enhanced lookup applied: rdfs:labels and skos:altLabels added to index.")

    def _get_text_matching_log_label(self) -> str:
        return "labeld"


class EmbeddingEnhancedOntologyResolver(EnhancedOntologyResolver):
    """Resolver that uses label/altLabel text lookup first, then embedding similarity."""

    embedding_model_name = "ibm-granite/granite-embedding-278m-multilingual"
    similarity_threshold = 0.9
    batch_size = 32
    max_sequence_length = 512

    def __init__(
        self,
        ontology_file: Optional[Union[str, List[str], IO, List[IO]]] = None,
        matching_strategy: Optional[MatchingStrategy] = None,
    ) -> None:
        self._embedding_candidates: Dict[str, List[OntologyEmbeddingCandidate]] = {
            "classes": [],
            "individuals": [],
        }
        self._embedding_matrices: Dict[str, numpy.ndarray] = {}
        self._query_embedding_cache: Dict[str, Optional[numpy.ndarray]] = {}
        self._embedding_backend_available: Optional[bool] = None
        self._tokenizer = None
        self._model = None
        self._torch = None
        self._device = "cpu"
        self._tokenizer_max_length = self.max_sequence_length

        super().__init__(ontology_file=ontology_file, matching_strategy=matching_strategy)

    def build_lookup(self) -> None:
        super().build_lookup()
        self._embedding_candidates = {"classes": [], "individuals": []}
        self._embedding_matrices = {}
        self._query_embedding_cache = {}

        if not getattr(self, "graph", None):
            return

        for category in ("classes", "individuals"):
            unique_uris = list(dict.fromkeys(self.lookup.get(category, {}).values()))
            self._embedding_candidates[category] = [
                OntologyEmbeddingCandidate(key=self._uri_to_key(uri), text=embedding_text)
                for uri in unique_uris
                if (embedding_text := self._build_embedding_text(uri))
            ]
            logger.info(
                "[embedding] Prepared %d embedding candidates for category '%s'",
                len(self._embedding_candidates[category]),
                category,
            )

    def find_closest_match(self, name: str, category: str) -> Optional[str]:
        logger.info(
            "[embedding] Starting resolver flow for input='%s' category='%s': textual pre-check followed by embedding fallback if needed",
            name,
            category,
        )
        text_match = super().find_closest_match(name, category)
        if text_match:
            logger.info(
                "[embedding] Textual pre-check matched input='%s' category='%s' with candidate='%s'. Embedding comparison skipped.",
                name,
                category,
                text_match,
            )
            return text_match

        logger.info(
            "[embedding] No textual pre-check match for input='%s' category='%s'. Proceeding to embedding comparison.",
            name,
            category,
        )
        return self._find_embedding_match(name, category)

    def _get_text_matching_log_label(self) -> str:
        return "embedding:textual_precheck"

    def _build_embedding_text(self, uri: URIRef) -> str:
        labels: List[str] = []
        for predicate in (RDFS.label, SKOS.altLabel):
            for label in self.graph.objects(uri, predicate):
                cleaned_label = str(label).strip()
                if cleaned_label:
                    labels.append(cleaned_label)

        return " ; ".join(dict.fromkeys(labels))

    def _prepare_embedding_query(self, name: str) -> str:
        return name.replace("_", " ").strip()

    def _ensure_embedding_backend(self) -> bool:
        if self._embedding_backend_available is not None:
            return self._embedding_backend_available

        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
        except ImportError as error:
            logger.warning(
                "Embedding fallback disabled because torch/transformers are unavailable: %s",
                str(error),
            )
            self._embedding_backend_available = False
            return False

        try:
            self._torch = torch
            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            self._tokenizer = AutoTokenizer.from_pretrained(self.embedding_model_name)
            self._model = AutoModel.from_pretrained(self.embedding_model_name).to(self._device)
            self._model.eval()

            model_max_length = getattr(
                self._tokenizer, "model_max_length", self.max_sequence_length
            )
            if not isinstance(model_max_length, int) or model_max_length <= 0:
                model_max_length = self.max_sequence_length

            self._tokenizer_max_length = min(model_max_length, self.max_sequence_length)
            self._embedding_backend_available = True
        except Exception as error:
            logger.warning(
                "Embedding fallback disabled because model '%s' could not be loaded: %s",
                self.embedding_model_name,
                str(error),
            )
            self._embedding_backend_available = False

        return self._embedding_backend_available

    def _encode_texts(self, texts: List[str]) -> numpy.ndarray:
        if not texts or not self._ensure_embedding_backend():
            return numpy.empty((0, 0))

        batches: List[numpy.ndarray] = []
        with self._torch.no_grad():
            for start in range(0, len(texts), self.batch_size):
                batch = texts[start : start + self.batch_size]
                tokenized = self._tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=self._tokenizer_max_length,
                    return_tensors="pt",
                )
                tokenized = {key: value.to(self._device) for key, value in tokenized.items()}

                model_output = self._model(**tokenized)
                batch_embeddings = model_output[0][:, 0]
                batch_embeddings = self._torch.nn.functional.normalize(batch_embeddings, dim=1)
                batches.append(batch_embeddings.cpu().numpy())

        return numpy.vstack(batches)

    def _get_category_embeddings(self, category: str) -> numpy.ndarray:
        if category not in self._embedding_matrices:
            candidates = self._embedding_candidates.get(category, [])
            texts = [candidate.text for candidate in candidates]
            self._embedding_matrices[category] = self._encode_texts(texts)

        return self._embedding_matrices[category]

    def _get_query_embedding(self, name: str) -> Optional[numpy.ndarray]:
        query_text = self._prepare_embedding_query(name)
        if not query_text:
            return None

        if query_text not in self._query_embedding_cache:
            encoded_query = self._encode_texts([query_text])
            self._query_embedding_cache[query_text] = (
                encoded_query[0] if encoded_query.size else None
            )

        return self._query_embedding_cache[query_text]

    def _find_embedding_match(self, name: str, category: str) -> Optional[str]:
        candidates = self._embedding_candidates.get(category, [])
        if not candidates:
            logger.info(
                "[embedding] No embedding candidates available for input='%s' category='%s'",
                name,
                category,
            )
            return None

        query_text = self._prepare_embedding_query(name)
        logger.info(
            "[embedding] Comparing query_text='%s' against %d embedding candidates in category='%s' using model='%s' threshold=%.2f",
            query_text,
            len(candidates),
            category,
            self.embedding_model_name,
            self.similarity_threshold,
        )

        query_embedding = self._get_query_embedding(name)
        candidate_embeddings = self._get_category_embeddings(category)
        if query_embedding is None or candidate_embeddings.size == 0:
            logger.info(
                "[embedding] Embedding comparison aborted for input='%s' category='%s' because query or candidate embeddings are unavailable",
                name,
                category,
            )
            return None

        similarity_scores = candidate_embeddings @ query_embedding
        ranked_indexes = numpy.argsort(similarity_scores)[::-1]

        for candidate_index in ranked_indexes[: self.max_logged_comparisons]:
            candidate = candidates[int(candidate_index)]
            logger.info(
                "[embedding] Compared query_text='%s' with candidate_key='%s' candidate_text='%s' cosine_similarity=%.4f",
                query_text,
                candidate.key,
                candidate.text,
                float(similarity_scores[int(candidate_index)]),
            )

        if len(ranked_indexes) > self.max_logged_comparisons:
            logger.info(
                "[embedding] Comparison log truncated: showing top %d of %d candidates",
                self.max_logged_comparisons,
                len(ranked_indexes),
            )

        best_index = int(similarity_scores.argmax())
        best_score = float(similarity_scores[best_index])
        best_match = candidates[best_index]

        logger.info(
            "Best embedding match for '%s' in category '%s' is '%s' with score %.4f",
            name,
            category,
            best_match.key,
            best_score,
        )

        if best_score >= self.similarity_threshold:
            logger.info(
                "[embedding] Match accepted for input='%s' category='%s': candidate='%s' score=%.4f",
                name,
                category,
                best_match.key,
                best_score,
            )
            return best_match.key

        logger.info(
            "[embedding] Match rejected for input='%s' category='%s': best candidate='%s' score=%.4f is below threshold %.2f",
            name,
            category,
            best_match.key,
            best_score,
            self.similarity_threshold,
        )
        return None
