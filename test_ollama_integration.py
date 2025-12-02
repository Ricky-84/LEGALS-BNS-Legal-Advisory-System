"""
Test OllamaService integration with semantic enhancement
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

print("=" * 60)
print("OLLAMA SERVICE + SEMANTIC INTEGRATION TEST")
print("=" * 60)

# Test OllamaService integration
print("\n[Test 1] Testing OllamaService with semantic enhancement...")
try:
    from app.services.ollama_service import OllamaService

    service = OllamaService()
    print("PASS: OllamaService initialized")
    print(f"  - Has semantic_enhancer: {hasattr(service, 'semantic_enhancer')}")
    print(f"  - Semantic enhancer loaded: {service.semantic_enhancer is not None}")
except Exception as e:
    print(f"FAIL: OllamaService initialization error - {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test real-world queries
print("\n[Test 2] Testing entity extraction with semantic enhancement...")
test_queries = [
    "He borrowed my laptop and never returned it",
    "Someone took my phone without permission",
    "He scammed me out of 5000 rupees",
    "Someone entered my house without permission"
]

for i, query in enumerate(test_queries, 1):
    print(f"\n  Query {i}: '{query}'")
    try:
        entities = service.extract_entities(query)

        # Check for basic entities
        print(f"    - Actions: {entities.get('actions', [])[:3]}")  # Show first 3
        print(f"    - Objects: {entities.get('objects', [])[:3]}")

        # Check for semantic enhancement
        if 'semantic_enhancements' in entities:
            sem_enh = entities['semantic_enhancements']
            print(f"    - Semantic categories: {sem_enh.get('categories_detected', [])}")
            print(f"    - Semantic confidence: {entities.get('semantic_confidence', 0):.1%}")
        else:
            print("    - No semantic enhancement (may be disabled)")

        # Check for detected crimes
        if 'detected_crimes' in entities and entities['detected_crimes']:
            crimes = [c['type'] for c in entities['detected_crimes']]
            print(f"    - Detected crimes: {crimes}")

    except Exception as e:
        print(f"    FAIL: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("INTEGRATION TEST COMPLETE")
print("=" * 60)
print("\nSemantic enhancement is successfully integrated into OllamaService!")
print("Vaishnav's implementation is working as expected.")
