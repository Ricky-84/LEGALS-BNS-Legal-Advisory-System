"""
Unit tests for Semantic Similarity Service
"""
import unittest
import logging
from semantic_service import SemanticMappingService, SemanticCache
from semantic_config import SEMANTIC_SIMILARITY_THRESHOLD

logging.basicConfig(level=logging.INFO)


class TestSemanticMappingService(unittest.TestCase):
    """Tests for SemanticMappingService"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.service = SemanticMappingService()

    def test_initialization(self):
        """Test service initialization."""
        self.assertIsNotNone(self.service.model)
        self.assertIsNotNone(self.service.legal_terms_embeddings)
        self.assertTrue(len(self.service.legal_terms) > 0)

    def test_find_semantic_matches_theft(self):
        """Test semantic matching for theft-related terms."""
        actions = ["stole"]
        matches = self.service.find_semantic_matches(actions, threshold=0.5)
        
        self.assertTrue(len(matches) > 0)
        self.assertIn("theft", matches)

    def test_find_semantic_matches_fraud(self):
        """Test semantic matching for fraud-related terms."""
        actions = ["scammed"]
        matches = self.service.find_semantic_matches(actions, threshold=0.5)
        
        self.assertTrue(len(matches) > 0)
        self.assertIn("fraud", matches)

    def test_find_semantic_matches_high_threshold(self):
        """Test with high similarity threshold."""
        actions = ["borrowed"]
        matches = self.service.find_semantic_matches(actions, threshold=0.95)
        
        # Should have fewer or no matches with high threshold
        self.assertIsInstance(matches, dict)

    def test_enhance_actions(self):
        """Test action enhancement."""
        actions = ["took", "didn't return"]
        enhanced = self.service.enhance_actions(actions, threshold=0.5)
        
        self.assertIn("original_actions", enhanced)
        self.assertIn("semantic_matches", enhanced)
        self.assertIn("categories_detected", enhanced)
        self.assertIn("confidence_scores", enhanced)
        
        self.assertEqual(enhanced["original_actions"], actions)

    def test_get_similarity_score(self):
        """Test similarity score calculation."""
        score = self.service.get_similarity_score("stole", "theft")
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)
        self.assertGreater(score, 0.5)  # Should be reasonably similar

    def test_add_custom_term(self):
        """Test adding custom terms."""
        initial_count = len(self.service.legal_terms.get("custom_crime", []))
        
        self.service.add_custom_term("custom_crime", "new_term", recompute=False)
        
        updated_count = len(self.service.legal_terms.get("custom_crime", []))
        self.assertGreater(updated_count, initial_count)

    def test_empty_actions(self):
        """Test with empty actions list."""
        actions = []
        matches = self.service.find_semantic_matches(actions)
        
        self.assertEqual(len(matches), 0)

    def test_none_actions(self):
        """Test with None actions."""
        matches = self.service.find_semantic_matches(None)
        self.assertEqual(len(matches), 0)


class TestSemanticCache(unittest.TestCase):
    """Tests for SemanticCache"""

    def setUp(self):
        """Set up test fixtures."""
        self.cache = SemanticCache(max_size=10)

    def tearDown(self):
        """Clean up after tests."""
        self.cache.clear()

    def test_cache_initialization(self):
        """Test cache initialization."""
        self.assertIsNotNone(self.cache.cache)
        self.assertEqual(len(self.cache.cache), 0)

    def test_put_and_get(self):
        """Test putting and getting values."""
        self.cache.put("key1", {"data": "value1"})
        
        result = self.cache.get("key1")
        self.assertIsNotNone(result)
        self.assertEqual(result["data"], "value1")

    def test_get_nonexistent(self):
        """Test getting non-existent key."""
        result = self.cache.get("nonexistent")
        self.assertIsNone(result)

    def test_cache_size_limit(self):
        """Test cache respects size limit."""
        for i in range(15):
            self.cache.put(f"key_{i}", f"value_{i}")
        
        self.assertLessEqual(len(self.cache.cache), self.cache.max_size)

    def test_cache_stats(self):
        """Test cache statistics."""
        self.cache.put("key1", "value1")
        stats = self.cache.stats()
        
        self.assertIn("size", stats)
        self.assertIn("max_size", stats)
        self.assertIn("usage", stats)
        self.assertEqual(stats["size"], 1)
        self.assertEqual(stats["max_size"], self.cache.max_size)

    def test_cache_clear(self):
        """Test clearing cache."""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        
        self.assertGreater(len(self.cache.cache), 0)
        
        self.cache.clear()
        self.assertEqual(len(self.cache.cache), 0)


class TestSemanticIntegration(unittest.TestCase):
    """Integration tests for semantic enhancement"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        from semantic_integration import SemanticEnhancedEntityExtraction
        cls.enhancer = SemanticEnhancedEntityExtraction()

    def test_enhance_entity_extraction(self):
        """Test entity extraction enhancement."""
        query = "borrowed laptop never returned"
        original_entities = {
            "actions": ["borrowed", "never returned"],
            "detected_crimes": []
        }
        
        enhanced = self.enhancer.enhance_entity_extraction(query, original_entities)
        
        self.assertIn("semantic_enhancements", enhanced)
        self.assertIn("semantic_confidence", enhanced)

    def test_get_semantic_explanation(self):
        """Test semantic explanation generation."""
        query = "He stole my bike"
        actions = ["stole"]
        
        explanation = self.enhancer.get_semantic_explanation(query, actions)
        
        self.assertIn("user_query", explanation)
        self.assertIn("detected_actions", explanation)
        self.assertIn("semantic_matches", explanation)

    def test_benchmark_semantic_enhancement(self):
        """Test benchmark functionality."""
        test_queries = [
            {
                "query": "He took my phone",
                "actions": ["took"],
                "expected_crimes": ["theft"]
            },
            {
                "query": "He lied and cheated me",
                "actions": ["lied", "cheated"],
                "expected_crimes": ["fraud"]
            }
        ]
        
        results = self.enhancer.benchmark_semantic_enhancement(test_queries)
        
        self.assertIn("total_tests", results)
        self.assertIn("passed", results)
        self.assertIn("accuracy", results)
        self.assertEqual(results["total_tests"], len(test_queries))


class TestRealWorldScenarios(unittest.TestCase):
    """Real-world scenario tests"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        from semantic_integration import SemanticEnhancedEntityExtraction
        cls.enhancer = SemanticEnhancedEntityExtraction()

    def test_scenario_theft_variation(self):
        """Test various ways to describe theft."""
        scenarios = [
            {"query": "He stole my wallet", "key_action": "stole"},
            {"query": "Someone took my phone", "key_action": "took"},
            {"query": "My car was shoplifted", "key_action": "shoplifted"},
            {"query": "The money was burglarized", "key_action": "burglarized"},
        ]
        
        for scenario in scenarios:
            original_entities = {
                "actions": [scenario["key_action"]],
                "detected_crimes": []
            }
            
            enhanced = self.enhancer.enhance_entity_extraction(
                scenario["query"],
                original_entities
            )
            
            self.assertGreater(
                enhanced.get("semantic_confidence", 0),
                0,
                f"Failed for: {scenario['query']}"
            )

    def test_scenario_fraud_variation(self):
        """Test various ways to describe fraud."""
        scenarios = [
            {"query": "He scammed me", "key_action": "scammed"},
            {"query": "I was deceived", "key_action": "deceived"},
            {"query": "They cheated me out of money", "key_action": "cheated"},
            {"query": "I was conned", "key_action": "conned"},
        ]
        
        for scenario in scenarios:
            original_entities = {
                "actions": [scenario["key_action"]],
                "detected_crimes": []
            }
            
            enhanced = self.enhancer.enhance_entity_extraction(
                scenario["query"],
                original_entities
            )
            
            self.assertGreater(
                enhanced.get("semantic_confidence", 0),
                0,
                f"Failed for: {scenario['query']}"
            )


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticMappingService))
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticCache))
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestRealWorldScenarios))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return results
    return result


if __name__ == "__main__":
    run_tests()
