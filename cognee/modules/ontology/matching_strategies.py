import difflib
import re
import unicodedata
from abc import ABC, abstractmethod
from typing import List, Optional


def normalize_matching_text(text: str) -> str:
    """Normalize text for resilient ontology matching."""
    if not text:
        return ""

    nfkd_form = unicodedata.normalize("NFKD", text)
    clean_text = "".join(char for char in nfkd_form if not unicodedata.combining(char))
    clean_text = clean_text.casefold().replace("_", " ")
    clean_text = re.sub(r"[^\w\s-]", " ", clean_text)
    clean_text = re.sub(r"[-\s]+", " ", clean_text)
    return clean_text.strip()


def normalize_lookup_key(text: str) -> str:
    """Normalize text for ontology lookup dictionary keys."""
    return normalize_matching_text(text).replace(" ", "_")


class MatchingStrategy(ABC):
    """Abstract base class for ontology entity matching strategies."""

    @abstractmethod
    def find_match(self, name: str, candidates: List[str]) -> Optional[str]:
        """Find the best match for a given name from a list of candidates.

        Args:
            name: The name to match
            candidates: List of candidate names to match against

        Returns:
            The best matching candidate name, or None if no match found
        """
        pass


class FuzzyMatchingStrategy(MatchingStrategy):
    """Fuzzy matching strategy using difflib for approximate string matching."""

    def __init__(self, cutoff: float = 0.8):
        """Initialize fuzzy matching strategy.

        Args:
            cutoff: Minimum similarity score (0.0 to 1.0) for a match to be considered valid
        """
        self.cutoff = cutoff

    def find_match(self, name: str, candidates: List[str]) -> Optional[str]:
        """Find the closest fuzzy match for a given name.

        Args:
            name: The normalized name to match
            candidates: List of normalized candidate names

        Returns:
            The best matching candidate name, or None if no match meets the cutoff
        """
        if not candidates:
            return None

        # Check for exact match first
        if name in candidates:
            return name

        # Find fuzzy match
        best_match = difflib.get_close_matches(name, candidates, n=1, cutoff=self.cutoff)
        return best_match[0] if best_match else None


class SemanticMatchingStrategy(MatchingStrategy):
    """Estratégia de match semântico que ignora acentos e converte underscores em espaços."""

    def __init__(self, cutoff: float = 0.8):
        self.cutoff = cutoff

    def _normalize(self, text: str) -> str:
        return normalize_matching_text(text)

    def find_match(self, name: str, candidates: List[str]) -> Optional[str]:
        if not candidates:
            return None

        name_clean = self._normalize(name)
        # Mapeia os candidatos limpos para os originais
        clean_candidates = {
            normalized_candidate: candidate
            for candidate in candidates
            if (normalized_candidate := self._normalize(candidate))
        }

        # Match exato primeiro
        if name_clean in clean_candidates:
            return clean_candidates[name_clean]

        # Fuzzy match
        best_match = difflib.get_close_matches(
            name_clean,
            list(clean_candidates.keys()),
            n=1,
            cutoff=self.cutoff,
        )

        return clean_candidates[best_match[0]] if best_match else None
