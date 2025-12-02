#!/usr/bin/env python3
"""
Quick Start Script for Sentence Transformers Implementation
Demonstrates the semantic enhancement system with interactive examples
"""
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ensure_data_directory():
    """Ensure data directory exists."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    logger.info("✓ Data directory ready")


def test_imports():
    """Test that all imports work."""
    logger.info("\n📦 Testing imports...")
    try:
        from semantic_service import SemanticMappingService, SemanticCache
        logger.info("✓ semantic_service imported")
        
        from semantic_config import EMBEDDING_MODEL, SEMANTIC_SIMILARITY_THRESHOLD
        logger.info(f"✓ semantic_config imported (model: {EMBEDDING_MODEL})")
        
        from semantic_integration import SemanticEnhancedEntityExtraction
        logger.info("✓ semantic_integration imported")
        
        return True
    except ImportError as e:
        logger.error(f"✗ Import failed: {e}")
        logger.error("Run: pip install -r requirements-semantic.txt")
        return False


def initialize_service():
    """Initialize semantic service."""
    logger.info("\n🔄 Initializing semantic service...")
    logger.info("(First run will download model ~22MB and compute embeddings)")
    
    try:
        from semantic_service import SemanticMappingService
        service = SemanticMappingService()
        logger.info("✓ SemanticMappingService initialized")
        logger.info(f"  - Model: all-MiniLM-L6-v2 (22MB)")
        logger.info(f"  - Categories: {len(service.legal_terms)}")
        logger.info(f"  - Total terms: {sum(len(v) for v in service.legal_terms.values())}")
        return service
    except Exception as e:
        logger.error(f"✗ Initialization failed: {e}")
        return None


def demo_semantic_matching(service):
    """Demonstrate semantic matching."""
    logger.info("\n🎯 Semantic Matching Demo\n")
    
    if service is None:
        logger.error("Service not initialized")
        return
    
    test_cases = [
        ("stole", 0.75),
        ("borrowed", 0.75),
        ("scammed", 0.75),
        ("attacked", 0.75),
        ("broke in", 0.75),
    ]
    
    for action, threshold in test_cases:
        logger.info(f"Query: '{action}' (threshold: {threshold})")
        matches = service.find_semantic_matches([action], threshold=threshold)
        
        if matches:
            for category, terms in matches.items():
                logger.info(f"  📌 {category}:")
                for term, score in terms[:3]:  # Show top 3
                    logger.info(f"     - {term:20s} ({score:.1%})")
        else:
            logger.info("  (no matches)")
        logger.info("")


def demo_entity_enhancement():
    """Demonstrate entity extraction enhancement."""
    logger.info("\n🚀 Entity Enhancement Demo\n")
    
    try:
        from semantic_integration import SemanticEnhancedEntityExtraction
        
        enhancer = SemanticEnhancedEntityExtraction()
        
        test_queries = [
            {
                "query": "He borrowed my laptop and never returned it",
                "actions": ["borrowed", "never returned"]
            },
            {
                "query": "Someone broke into my house and took my TV",
                "actions": ["broke in", "took"]
            },
            {
                "query": "He scammed me out of $500",
                "actions": ["scammed"]
            },
        ]
        
        for test in test_queries:
            logger.info(f"Query: {test['query']}")
            logger.info(f"Detected actions: {test['actions']}")
            
            original_entities = {
                "actions": test["actions"],
                "detected_crimes": []
            }
            
            enhanced = enhancer.enhance_entity_extraction(
                test["query"],
                original_entities
            )
            
            confidence = enhanced.get("semantic_confidence", 0)
            logger.info(f"Semantic confidence: {confidence:.1%}")
            
            detected = enhanced.get("detected_crimes", [])
            if detected:
                logger.info(f"Detected crimes: {[c['type'] for c in detected]}")
            
            logger.info("")
    
    except Exception as e:
        logger.error(f"Demo failed: {e}")


def run_tests():
    """Run test suite."""
    logger.info("\n✅ Running Test Suite\n")
    
    try:
        from test_semantic import run_tests as run_all_tests
        results = run_all_tests()
        
        logger.info("")
        logger.info("=" * 60)
        logger.info(f"Tests run: {results.testsRun}")
        logger.info(f"Failures: {len(results.failures)}")
        logger.info(f"Errors: {len(results.errors)}")
        
        if results.wasSuccessful():
            logger.info("✓ All tests passed!")
        else:
            logger.warning("✗ Some tests failed")
        
        return results.wasSuccessful()
    
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return False


def show_statistics():
    """Show system statistics."""
    logger.info("\n📊 System Statistics\n")
    
    try:
        from semantic_config import (
            EMBEDDING_MODEL,
            SEMANTIC_SIMILARITY_THRESHOLD,
            SEMANTIC_CACHE_SIZE
        )
        from semantic_service import SemanticMappingService
        
        logger.info("Configuration:")
        logger.info(f"  - Model: {EMBEDDING_MODEL}")
        logger.info(f"  - Threshold: {SEMANTIC_SIMILARITY_THRESHOLD}")
        logger.info(f"  - Cache size: {SEMANTIC_CACHE_SIZE}")
        
        service = SemanticMappingService()
        logger.info(f"\nLegal Terms Database:")
        logger.info(f"  - Categories: {len(service.legal_terms)}")
        
        for category, terms in service.legal_terms.items():
            logger.info(f"    • {category}: {len(terms)} terms")
        
        total_terms = sum(len(v) for v in service.legal_terms.values())
        logger.info(f"  - Total terms: {total_terms}")
        
    except Exception as e:
        logger.error(f"Failed to show statistics: {e}")


def main():
    """Main execution."""
    logger.info("=" * 60)
    logger.info("🎯 Sentence Transformers - Quick Start")
    logger.info("=" * 60)
    
    # Step 1: Setup
    ensure_data_directory()
    
    # Step 2: Test imports
    if not test_imports():
        logger.error("\n❌ Setup failed. Please install dependencies:")
        logger.error("   pip install -r requirements-semantic.txt")
        return False
    
    # Step 3: Initialize service
    service = initialize_service()
    
    # Step 4: Run demos
    if service:
        demo_semantic_matching(service)
        demo_entity_enhancement()
        show_statistics()
    
    # Step 5: Run tests (optional - takes longer)
    logger.info("\n" + "=" * 60)
    logger.info("Would you like to run the full test suite? (Y/n)")
    response = input().strip().lower()
    
    if response != 'n':
        test_success = run_tests()
    else:
        logger.info("Skipping tests")
        test_success = True
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("✅ Setup Complete!")
    logger.info("=" * 60)
    logger.info("\nNext steps:")
    logger.info("1. Review SETUP_GUIDE.md for detailed documentation")
    logger.info("2. Integrate SemanticEnhancedEntityExtraction with your app")
    logger.info("3. Update your crime detection flow")
    logger.info("4. Test with production data")
    logger.info("\nKey files created:")
    logger.info("  - semantic_service.py (core service)")
    logger.info("  - semantic_config.py (configuration)")
    logger.info("  - semantic_integration.py (integration layer)")
    logger.info("  - test_semantic.py (test suite)")
    logger.info("  - SETUP_GUIDE.md (documentation)")
    logger.info("")
    
    return test_success


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        sys.exit(1)
