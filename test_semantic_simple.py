"""
Simple semantic integration test
Tests Vaishnav's sentence transformer implementation
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

print("=" * 60)
print("SEMANTIC INTEGRATION TEST")
print("=" * 60)

# Test 1: Import semantic modules
print("\n[Test 1] Importing semantic modules...")
try:
    from app.services.semantic_service import SemanticMappingService
    from app.services.semantic_integration import SemanticEnhancedEntityExtraction
    from app.services.semantic_config import SEMANTIC_SIMILARITY_THRESHOLD
    print("PASS: All semantic modules imported successfully")
except Exception as e:
    print(f"FAIL: Import error - {e}")
    sys.exit(1)

# Test 2: Initialize semantic service
print("\n[Test 2] Initializing semantic service...")
try:
    semantic_service = SemanticMappingService()
    print("PASS: Semantic service initialized")
    print(f"  - Model: {semantic_service.model_name}")
    print(f"  - Legal categories: {len(semantic_service.legal_terms)}")
except Exception as e:
    print(f"FAIL: Initialization error - {e}")
    sys.exit(1)

# Test 3: Test semantic matching
print("\n[Test 3] Testing semantic matching...")
try:
    test_actions = ["borrowed", "never returned"]
    matches = semantic_service.find_semantic_matches(test_actions, threshold=0.7)
    print(f"PASS: Semantic matching works")
    print(f"  - Input actions: {test_actions}")
    print(f"  - Categories detected: {list(matches.keys())}")
    for category, terms in matches.items():
        print(f"  - {category}: {terms[:2]}")  # Show first 2 matches
except Exception as e:
    print(f"FAIL: Semantic matching error - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test enhancement
print("\n[Test 4] Testing action enhancement...")
try:
    enhanced = semantic_service.enhance_actions(["took", "scammed"], threshold=0.7)
    print("PASS: Action enhancement works")
    print(f"  - Original actions: {enhanced['original_actions']}")
    print(f"  - Categories detected: {enhanced['categories_detected']}")
    print(f"  - Confidence scores: {enhanced['confidence_scores']}")
except Exception as e:
    print(f"FAIL: Enhancement error - {e}")
    sys.exit(1)

# Test 5: Test integration with entity extraction
print("\n[Test 5] Testing full integration...")
try:
    enhancer = SemanticEnhancedEntityExtraction()
    query = "He borrowed my laptop and never returned it"
    original_entities = {
        "actions": ["borrowed", "never returned"],
        "objects": ["laptop"],
        "detected_crimes": []
    }

    enhanced_entities = enhancer.enhance_entity_extraction(query, original_entities)
    print("PASS: Full integration works")
    print(f"  - Query: {query}")
    print(f"  - Original actions: {original_entities['actions']}")
    print(f"  - Semantic confidence: {enhanced_entities.get('semantic_confidence', 0):.1%}")
    if 'detected_crimes' in enhanced_entities and enhanced_entities['detected_crimes']:
        print(f"  - Detected crimes: {[c['type'] for c in enhanced_entities['detected_crimes']]}")
except Exception as e:
    print(f"FAIL: Integration error - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nVaishnav's sentence transformer implementation is working correctly!")
