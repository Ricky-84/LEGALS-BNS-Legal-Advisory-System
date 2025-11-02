#!/usr/bin/env python3
"""Test Neo4j directly with the correct entities"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.neo4j_service import neo4j_service

def test_neo4j_direct():
    print("Testing Neo4j with correct entities...")

    # These are the CORRECT entities from the working extraction
    entities = {
        "persons": ["me"],
        "objects": ["laptop", "iPhone"],
        "locations": ["my house"],
        "actions": ["broke into", "stole"],
        "intentions": [],
        "circumstances": ["last night", "while I was sleeping"],
        "relationships": []
    }

    print("Testing with entities:", entities)
    print()

    # Test the detection methods
    print("=== DETECTION TESTS ===")
    print(f"Has theft elements: {neo4j_service._has_theft_elements(entities)}")
    print(f"Has dwelling theft: {neo4j_service._has_dwelling_theft_elements(entities)}")
    print(f"Has employee theft: {neo4j_service._has_employee_theft_elements(entities)}")
    print(f"Has robbery: {neo4j_service._has_robbery_elements(entities)}")

    print()
    print("=== LEGAL REASONING TEST ===")

    # Test the full legal reasoning
    try:
        applicable_laws = neo4j_service.find_applicable_laws(entities)
        print(f"Laws found: {len(applicable_laws)}")

        for law in applicable_laws:
            print(f"- {law['section']}: {law['title']} (confidence: {law['confidence']})")
            print(f"  Reasoning: {law['reasoning']}")

    except Exception as e:
        print(f"Error in legal reasoning: {e}")

if __name__ == "__main__":
    test_neo4j_direct()