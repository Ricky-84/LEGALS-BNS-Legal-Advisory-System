"""
Semantic Similarity Service
Provides semantic matching for legal action terms using sentence transformers
Implemented by: Vaishnav
"""
import pickle
import logging
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer, util
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class SemanticMappingService:
    """
    Service for semantic similarity matching of legal action terms.
    Uses sentence transformers to find semantically similar terms.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_path: str = "data/semantic_cache.pkl"):
        """
        Initialize the semantic mapping service.
        
        Args:
            model_name: Name of the sentence transformer model to use
            cache_path: Path to cache pre-computed embeddings
        """
        self.model_name = model_name
        self.cache_path = Path(cache_path)
        self.model = SentenceTransformer(model_name)
        
        # Legal action terms database
        self.legal_terms = {
            "theft": ["stole", "stolen", "took", "shoplifted", "burglarized", "robbery", "thief"],
            "fraud": ["scammed", "deceived", "cheated", "conned", "defrauded", "misrepresented"],
            "assault": ["attacked", "punched", "hit", "beat", "struck", "violent"],
            "theft_return": ["borrowed", "lent", "didn't return", "failed to return", "never gave back"],
            "trespassing": ["entered illegally", "broke in", "invaded", "unauthorized entry"],
            "blackmail": ["extorted", "threatened", "coerced", "demanded money"],
            "harassment": ["bullied", "threatened", "intimidated", "harassed", "stalked"],
            "vandalism": ["damaged", "destroyed", "defaced", "graffiti", "property damage"],
            "forgery": ["forged", "faked", "fabricated", "falsified", "counterfeited"],
            "embezzlement": ["misappropriated", "stole funds", "took money", "diverted funds"]
        }
        
        self.legal_terms_embeddings = {}
        self._load_or_compute_embeddings()

    def _load_or_compute_embeddings(self):
        """Load embeddings from cache or compute them."""
        if self.cache_path.exists():
            try:
                logger.info(f"Loading embeddings from cache: {self.cache_path}")
                with open(self.cache_path, 'rb') as f:
                    self.legal_terms_embeddings = pickle.load(f)
                logger.info("Successfully loaded cached embeddings")
            except Exception as e:
                logger.error(f"Failed to load cache: {e}. Computing new embeddings.")
                self._compute_embeddings()
        else:
            self._compute_embeddings()

    def _compute_embeddings(self):
        """Compute and cache embeddings for all legal terms."""
        logger.info("Computing embeddings for legal terms...")
        
        for category, terms in self.legal_terms.items():
            embeddings = self.model.encode(terms, convert_to_tensor=True)
            self.legal_terms_embeddings[category] = {
                "terms": terms,
                "embeddings": embeddings
            }
        
        # Cache the embeddings
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, 'wb') as f:
            pickle.dump(self.legal_terms_embeddings, f)
        logger.info(f"Embeddings cached to {self.cache_path}")

    def find_semantic_matches(
        self,
        user_actions: List[str],
        threshold: float = 0.75
    ) -> Dict[str, List[Tuple[str, float]]]:
        """
        Find semantic matches for user actions against legal terms.
        
        Args:
            user_actions: List of action terms from user query
            threshold: Similarity threshold (0-1)
            
        Returns:
            Dictionary mapping legal categories to matched terms with similarity scores
        """
        matches = {}
        
        if not user_actions:
            return matches
        
        # Encode user actions
        user_embeddings = self.model.encode(user_actions, convert_to_tensor=True)
        
        # Find matches for each legal category
        for category, data in self.legal_terms_embeddings.items():
            legal_embeddings = data["embeddings"]
            legal_terms = data["terms"]
            
            # Compute cosine similarities
            similarities = util.pytorch_cos_sim(user_embeddings, legal_embeddings)
            
            # Extract matches above threshold
            category_matches = []
            for user_idx, user_action in enumerate(user_actions):
                for legal_idx, legal_term in enumerate(legal_terms):
                    similarity_score = float(similarities[user_idx][legal_idx])
                    if similarity_score >= threshold:
                        category_matches.append((legal_term, similarity_score))
            
            if category_matches:
                # Remove duplicates and sort by similarity
                unique_matches = {}
                for term, score in category_matches:
                    if term not in unique_matches or score > unique_matches[term]:
                        unique_matches[term] = score
                matches[category] = sorted(
                    unique_matches.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
        
        return matches

    def enhance_actions(
        self,
        user_actions: List[str],
        threshold: float = 0.75
    ) -> Dict[str, any]:
        """
        Enhance user actions with semantic similarity matches.
        
        Args:
            user_actions: Original action terms from user query
            threshold: Similarity threshold
            
        Returns:
            Enhanced actions dictionary with matches and confidence scores
        """
        matches = self.find_semantic_matches(user_actions, threshold)
        
        enhanced = {
            "original_actions": user_actions,
            "semantic_matches": matches,
            "categories_detected": list(matches.keys()),
            "confidence_scores": {}
        }
        
        # Calculate confidence scores for each detected category
        for category, matched_terms in matches.items():
            if matched_terms:
                # Average similarity score for the category
                avg_score = sum(score for _, score in matched_terms) / len(matched_terms)
                enhanced["confidence_scores"][category] = float(avg_score)
        
        return enhanced

    def get_similarity_score(self, term1: str, term2: str) -> float:
        """
        Get similarity score between two terms.
        
        Args:
            term1: First term
            term2: Second term
            
        Returns:
            Similarity score (0-1)
        """
        embedding1 = self.model.encode(term1, convert_to_tensor=True)
        embedding2 = self.model.encode(term2, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(embedding1, embedding2)
        return float(similarity[0][0])

    def add_custom_term(self, category: str, term: str, recompute: bool = True):
        """
        Add a custom term to the legal terms database.
        
        Args:
            category: Category name
            term: New term to add
            recompute: Whether to recompute embeddings
        """
        if category not in self.legal_terms:
            self.legal_terms[category] = []
        
        if term not in self.legal_terms[category]:
            self.legal_terms[category].append(term)
            if recompute:
                self._compute_embeddings()
            logger.info(f"Added term '{term}' to category '{category}'")


class SemanticCache:
    """
    Caching layer for semantic similarity computations.
    Stores frequently computed similarities to improve performance.
    """

    def __init__(self, max_size: int = 1000, cache_file: str = "data/semantic_query_cache.pkl"):
        """
        Initialize the semantic cache.
        
        Args:
            max_size: Maximum cache size
            cache_file: Path to persistence file
        """
        self.max_size = max_size
        self.cache_file = Path(cache_file)
        self.cache = {}
        self._load_cache()

    def _load_cache(self):
        """Load cache from disk if it exists."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
                logger.info(f"Loaded cache with {len(self.cache)} entries")
            except Exception as e:
                logger.error(f"Failed to load cache: {e}")
                self.cache = {}

    def get(self, key: str) -> any:
        """Get value from cache."""
        return self.cache.get(key)

    def put(self, key: str, value: any):
        """Put value in cache with LRU eviction."""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple FIFO for now)
            self.cache.pop(next(iter(self.cache)))
        
        self.cache[key] = value
        self._save_cache()

    def _save_cache(self):
        """Save cache to disk."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)

    def clear(self):
        """Clear the cache."""
        self.cache.clear()
        if self.cache_file.exists():
            self.cache_file.unlink()
        logger.info("Cache cleared")

    def stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "usage": f"{len(self.cache)}/{self.max_size}"
        }
