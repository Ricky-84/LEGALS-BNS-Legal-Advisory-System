"""
Quick integration test for semantic enhancement
Tests that the semantic service is properly integrated into ollama_service
"""
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_semantic_integration():
    """Test that semantic enhancement is integrated"""
    print("\n" + "="*60)
    print("SEMANTIC INTEGRATION TEST")
    print("="*60 + "\n")

    # Test 1: Check imports
    print("Test 1: Checking if semantic modules can be imported...")
    try:
        from app.services.semantic_service import SemanticMappingService
        from app.services.semantic_integration import SemanticEnhancedEntityExtraction
        from app.services.semantic_config import SEMANTIC_SIMILARITY_THRESHOLD
        print("✓ All semantic modules imported successfully")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

    # Test 2: Check OllamaService integration
    print("\nTest 2: Checking OllamaService integration...")
    try:
        from app.services.ollama_service import OllamaService
        service = OllamaService()

        if hasattr(service, 'semantic_enhancer'):
            print(f"✓ OllamaService has semantic_enhancer: {service.semantic_enhancer is not None}")
        else:
            print("✗ OllamaService missing semantic_enhancer attribute")
            return False
    except Exception as e:
        print(f"✗ OllamaService integration check failed: {e}")
        return False

    # Test 3: Test entity extraction with semantic enhancement
    print("\nTest 3: Testing entity extraction with semantic enhancement...")
    try:
        test_queries = [
            "He borrowed my laptop and never returned it",
            "Someone took my phone without permission",
            "He scammed me out of 5000 rupees"
        ]

        for query in test_queries:
            print(f"\nQuery: '{query}'")
            entities = service.extract_entities(query)

            # Check for semantic enhancement fields
            if 'semantic_enhancements' in entities:
                print("  ✓ Semantic enhancement applied")
                print(f"  ✓ Semantic confidence: {entities.get('semantic_confidence', 0):.2%}")
                print(f"  ✓ Categories detected: {entities.get('semantic_enhancements', {}).get('categories_detected', [])}")
            else:
                print("  ⚠ No semantic enhancement (may be disabled or failed)")

            print(f"  Actions detected: {entities.get('actions', [])}")

    except Exception as e:
        print(f"✗ Entity extraction test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "="*60)
    print("INTEGRATION TEST COMPLETE")
    print("="*60)
    return True


if __name__ == "__main__":
    success = test_semantic_integration()
    sys.exit(0 if success else 1)
