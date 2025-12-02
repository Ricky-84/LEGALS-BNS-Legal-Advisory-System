"""
Integration of Semantic Service with existing crime detection system
Implemented by: Vaishnav
"""
import logging
from typing import List, Dict, Any
from .semantic_service import SemanticMappingService, SemanticCache
from .semantic_config import (
    SEMANTIC_SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL,
    ENABLE_SEMANTIC_ENHANCEMENT
)

logger = logging.getLogger(__name__)


class SemanticEnhancedEntityExtraction:
    """
    Enhanced entity extraction that combines Phi-3 SLM extraction
    with semantic similarity matching.
    """

    def __init__(self):
        """Initialize semantic services."""
        if ENABLE_SEMANTIC_ENHANCEMENT:
            self.semantic_service = SemanticMappingService(model_name=EMBEDDING_MODEL)
            self.semantic_cache = SemanticCache()
            logger.info("Semantic enhancement enabled")
        else:
            self.semantic_service = None
            self.semantic_cache = None
            logger.info("Semantic enhancement disabled")

    def enhance_entity_extraction(self, user_query: str, original_entities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance entity extraction with semantic matching.
        
        Args:
            user_query: Original user query
            original_entities: Entities extracted by Phi-3 SLM
            
        Returns:
            Enhanced entities with semantic matches
        """
        if not ENABLE_SEMANTIC_ENHANCEMENT or self.semantic_service is None:
            return original_entities

        try:
            # Extract action terms from original entities
            actions = original_entities.get("actions", [])
            
            if not actions:
                return original_entities

            # Check cache first
            cache_key = f"semantic_{user_query}_{str(actions)}"
            cached_result = self.semantic_cache.get(cache_key)
            if cached_result:
                logger.debug("Returning cached semantic enhancement")
                return cached_result

            # Layer 1: Current extraction (already done)
            logger.debug(f"Original actions detected: {actions}")

            # Layer 2: Semantic similarity enhancement
            enhanced_actions = self.semantic_service.enhance_actions(
                actions,
                threshold=SEMANTIC_SIMILARITY_THRESHOLD
            )

            logger.debug(f"Semantic enhancement result: {enhanced_actions}")

            # Layer 3: Merge results
            enriched_entities = self._merge_results(original_entities, enhanced_actions)

            # Cache the result
            self.semantic_cache.put(cache_key, enriched_entities)

            return enriched_entities

        except Exception as e:
            logger.error(f"Error in semantic enhancement: {e}")
            # Graceful degradation - return original entities
            return original_entities

    def _merge_results(self, original_entities: Dict, semantic_enhancement: Dict) -> Dict:
        """
        Merge original entities with semantic enhancement results.
        
        Args:
            original_entities: Original extracted entities
            semantic_enhancement: Semantic enhancement result
            
        Returns:
            Merged entities dictionary
        """
        merged = original_entities.copy()

        # Add semantic match information
        merged["semantic_enhancements"] = semantic_enhancement

        # Update categories based on semantic matches
        detected_categories = semantic_enhancement.get("categories_detected", [])
        confidence_scores = semantic_enhancement.get("confidence_scores", {})

        if "detected_crimes" not in merged:
            merged["detected_crimes"] = []

        for category in detected_categories:
            confidence = confidence_scores.get(category, 0.75)
            merged["detected_crimes"].append({
                "type": category,
                "source": "semantic_enhancement",
                "confidence": confidence
            })

        # Calculate overall confidence
        if confidence_scores:
            merged["semantic_confidence"] = sum(confidence_scores.values()) / len(confidence_scores)
        else:
            merged["semantic_confidence"] = 0.0

        logger.debug(f"Merged entities: {merged}")
        return merged

    def get_semantic_explanation(self, user_query: str, actions: List[str]) -> Dict[str, Any]:
        """
        Get a detailed explanation of semantic matching for user actions.
        
        Args:
            user_query: User's original query
            actions: Detected action terms
            
        Returns:
            Detailed explanation of semantic matches
        """
        if not ENABLE_SEMANTIC_ENHANCEMENT or self.semantic_service is None:
            return {"explanation": "Semantic enhancement is disabled"}

        try:
            matches = self.semantic_service.find_semantic_matches(
                actions,
                threshold=SEMANTIC_SIMILARITY_THRESHOLD
            )

            explanation = {
                "user_query": user_query,
                "detected_actions": actions,
                "semantic_matches": {}
            }

            for category, matched_terms in matches.items():
                explanation["semantic_matches"][category] = [
                    {
                        "term": term,
                        "similarity": f"{score:.2%}"
                    }
                    for term, score in matched_terms
                ]

            return explanation

        except Exception as e:
            logger.error(f"Error generating semantic explanation: {e}")
            return {"error": str(e)}

    def benchmark_semantic_enhancement(self, test_queries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Benchmark semantic enhancement performance.
        
        Args:
            test_queries: List of test queries with expected results
            
        Returns:
            Benchmark results
        """
        if not ENABLE_SEMANTIC_ENHANCEMENT:
            return {"status": "Semantic enhancement is disabled"}

        results = {
            "total_tests": len(test_queries),
            "passed": 0,
            "failed": 0,
            "accuracy": 0.0,
            "details": []
        }

        for query_data in test_queries:
            user_query = query_data.get("query", "")
            expected_crimes = set(query_data.get("expected_crimes", []))
            
            # Extract entities (simplified - in production use actual extraction)
            original_entities = {
                "actions": query_data.get("actions", []),
                "detected_crimes": []
            }

            # Enhance
            enhanced = self.enhance_entity_extraction(user_query, original_entities)
            detected_crimes = {crime["type"] for crime in enhanced.get("detected_crimes", [])}

            # Compare
            matched = expected_crimes == detected_crimes
            results["passed"] += 1 if matched else 0
            results["failed"] += 0 if matched else 1

            results["details"].append({
                "query": user_query,
                "expected": list(expected_crimes),
                "detected": list(detected_crimes),
                "passed": matched
            })

        results["accuracy"] = results["passed"] / len(test_queries) if test_queries else 0

        return results


class SemanticIntegrationExample:
    """Example usage of semantic enhancement."""

    @staticmethod
    def demo():
        """Run a demonstration of semantic enhancement."""
        logger.info("Starting semantic enhancement demo...")

        enhancer = SemanticEnhancedEntityExtraction()

        # Test cases
        test_cases = [
            {
                "query": "He borrowed my laptop and never returned it",
                "actions": ["borrowed", "never returned"],
                "expected_crimes": ["theft_return"]
            },
            {
                "query": "Someone broke into my house and took my TV",
                "actions": ["broke in", "took"],
                "expected_crimes": ["trespassing", "theft"]
            },
            {
                "query": "He scammed me out of $500",
                "actions": ["scammed"],
                "expected_crimes": ["fraud"]
            }
        ]

        logger.info("\n" + "="*60)
        logger.info("SEMANTIC ENHANCEMENT DEMO")
        logger.info("="*60)

        for i, test in enumerate(test_cases, 1):
            logger.info(f"\nTest Case {i}: {test['query']}")
            logger.info(f"Detected actions: {test['actions']}")

            original_entities = {
                "actions": test["actions"],
                "detected_crimes": []
            }

            enhanced = enhancer.enhance_entity_extraction(test['query'], original_entities)
            
            logger.info(f"Semantic confidence: {enhanced.get('semantic_confidence', 0):.2%}")
            
            explanation = enhancer.get_semantic_explanation(test['query'], test['actions'])
            
            if "semantic_matches" in explanation:
                for category, matches in explanation["semantic_matches"].items():
                    logger.info(f"  {category}: {matches}")

        logger.info("\n" + "="*60)
        logger.info("Benchmark Results:")
        logger.info("="*60)

        benchmark = enhancer.benchmark_semantic_enhancement(test_cases)
        logger.info(f"Accuracy: {benchmark['accuracy']:.1%} ({benchmark['passed']}/{benchmark['total_tests']})")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    SemanticIntegrationExample.demo()
