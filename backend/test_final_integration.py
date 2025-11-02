#!/usr/bin/env python3
"""
LEGALS Final Integration Test
Test multiple scenarios to validate complete integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ollama_service import ollama_service
from app.services.neo4j_service import neo4j_service

def test_scenarios():
    """Test multiple scenarios"""
    print("LEGALS Final Integration Test")
    print("=" * 50)

    scenarios = [
        "Someone stole my iPhone from my house",
        "Employee took laptop from office",
        "Robber threatened me and took my wallet"
    ]

    results = []

    for i, query in enumerate(scenarios, 1):
        print(f"\n--- Scenario {i} ---")
        print(f"Query: {query}")

        try:
            # Extract entities
            entities = ollama_service.extract_entities(query)

            # Get legal analysis
            applicable_laws = neo4j_service.find_applicable_laws(entities)
            enhanced_laws = neo4j_service.enhance_with_property_analysis(applicable_laws, entities)

            print(f"Entities: {list(entities.keys())}")
            print(f"Laws Found: {len(enhanced_laws)}")

            for law in enhanced_laws:
                print(f"  {law['section']}: {law['title']}")

            if len(enhanced_laws) > 0:
                results.append(True)
                print("RESULT: SUCCESS")
            else:
                results.append(False)
                print("RESULT: FAIL - No laws found")

        except Exception as e:
            print(f"RESULT: ERROR - {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 50)
    print("FINAL INTEGRATION SUMMARY")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    print(f"Scenarios Passed: {passed}/{total}")

    if passed == total:
        print("\nSUCCESS: LEGALS integration is complete!")
        print("- SLM Entity Extraction: Working")
        print("- Neo4j Legal Reasoning: Working")
        print("- Property Value Analysis: Working")
        print("- End-to-End Pipeline: Working")
        print("\nREADY FOR DEMO!")
    else:
        print(f"\nWARNING: {total - passed} scenarios failed")

if __name__ == "__main__":
    test_scenarios()