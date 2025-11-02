#!/usr/bin/env python3
"""
LEGALS Ollama + Phi-3 Integration Test (Run after Ollama installation)
Test the SLM connection and entity extraction
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import json
from app.services.ollama_service import ollama_service

def test_ollama_connection():
    """Test basic Ollama connection"""
    print("Testing Ollama Connection...")

    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print(f"SUCCESS: Ollama connected! Available models:")
            for model in models.get('models', []):
                print(f"  - {model['name']}")
            return True
        else:
            print(f"FAIL: Ollama responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL: Ollama connection failed: {e}")
        print("Make sure Ollama is installed and running")
        return False

def test_phi3_model():
    """Test if Phi-3 model is available"""
    print("\nTesting Phi-3 Model...")

    try:
        response = requests.post("http://localhost:11434/api/generate",
            json={
                "model": "phi3:latest",
                "prompt": "Hello, can you help me?",
                "stream": False
            })

        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Phi-3 model working!")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
            return True
        else:
            print(f"FAIL: Phi-3 model request failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL: Phi-3 model test failed: {e}")
        return False

def test_entity_extraction_service():
    """Test the entity extraction service"""
    print("\nTesting Entity Extraction Service...")

    try:
        # Test simple entity extraction
        test_query = "Someone stole my iPhone from my house last night"

        print(f"Test Query: {test_query}")

        if not ollama_service.is_available():
            print("INFO: Ollama service not available, will use fallback")
            return False

        entities = ollama_service.extract_entities(test_query)

        print("SUCCESS: Entity extraction working!")
        print("Extracted entities:")
        for category, items in entities.items():
            if items:
                print(f"  {category}: {items}")

        return True

    except Exception as e:
        print(f"FAIL: Entity extraction failed: {e}")
        return False

def test_enhanced_entity_schema():
    """Test the enhanced entity extraction with property values"""
    print("\nTesting Enhanced Entity Schema...")

    test_cases = [
        {
            "query": "My iPhone was stolen from my house",
            "expected": ["iPhone", "house", "stolen"]
        },
        {
            "query": "Employee took cash and laptop from office",
            "expected": ["employee", "cash", "laptop", "office", "took"]
        },
        {
            "query": "Robber threatened me with knife and took my wallet",
            "expected": ["robber", "threatened", "knife", "wallet"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['query']}")

        try:
            entities = ollama_service.extract_entities(test_case['query'])

            print(f"Results:")
            for category, items in entities.items():
                if items:
                    print(f"  {category}: {items}")

        except Exception as e:
            print(f"FAIL: Test case {i} failed: {e}")
            return False

    return True

def test_complete_pipeline():
    """Test the complete SLM + Neo4j pipeline"""
    print("\nTesting Complete SLM + Neo4j Pipeline...")

    try:
        from app.services.legal_processing_service import LegalProcessingService

        legal_service = LegalProcessingService()

        test_query = "Someone broke into my house and stole my iPhone and wallet while I was sleeping"

        print(f"Query: {test_query}")

        # Test the complete pipeline with Ollama entity extraction
        if ollama_service.is_available():
            print("Testing with Ollama entity extraction...")
            entities = ollama_service.extract_entities(test_query)
            print(f"Extracted entities: {entities}")

            # Test legal reasoning with extracted entities
            applicable_laws = legal_service.neo4j_service.find_applicable_laws(entities)
            enhanced_laws = legal_service.neo4j_service.enhance_with_property_analysis(applicable_laws, entities)

            print("SUCCESS: Complete pipeline test!")
            print(f"Found {len(enhanced_laws)} applicable laws")
            for law in enhanced_laws:
                print(f"  - {law['section']}: {law['title']} (confidence: {law['confidence']})")

            return True
        else:
            print("INFO: Ollama not available, using fallback")
            return False

    except Exception as e:
        print(f"FAIL: Complete pipeline test failed: {e}")
        return False

def main():
    """Run all SLM integration tests"""
    print("LEGALS SLM Integration Test Suite")
    print("=" * 50)

    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Phi-3 Model", test_phi3_model),
        ("Entity Extraction Service", test_entity_extraction_service),
        ("Enhanced Entity Schema", test_enhanced_entity_schema),
        ("Complete Pipeline", test_complete_pipeline)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            print(f"\nRunning: {test_name}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"FAIL: {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("SLM INTEGRATION TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} {test_name}")

    print(f"\nResults: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("SUCCESS: SLM integration is working!")
        print("INFO: Ready for complete LEGALS pipeline testing!")
    else:
        print("WARNING: Some SLM tests failed.")
        if passed == 0:
            print("INFO: Install Ollama and download Phi-3 model first:")
            print("  1. Download Ollama from https://ollama.ai/")
            print("  2. Run: ollama pull phi3:latest")
            print("  3. Test again")

if __name__ == "__main__":
    main()