#!/usr/bin/env python3
"""
LEGALS Simple Pipeline Test
Quick test of SLM + Neo4j integration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ollama_service import ollama_service
from app.services.neo4j_service import neo4j_service

def test_simple_case():
    """Test one simple case end-to-end"""
    print("LEGALS Simple Pipeline Test")
    print("=" * 40)

    query = "Someone stole my iPhone from my house"
    print(f"Query: {query}")

    # Step 1: Entity Extraction
    print("\n[STEP 1] Entity Extraction...")
    entities = ollama_service.extract_entities(query)

    print("Extracted:")
    for category, items in entities.items():
        if items and category != "property_value_analysis":
            print(f"  {category}: {items}")

    if "property_value_analysis" in entities:
        analysis = entities["property_value_analysis"]
        print(f"  Property Value: Rs.{analysis.get('total_estimated_value', 0):,}")

    # Step 2: Legal Reasoning
    print("\n[STEP 2] Legal Reasoning...")
    applicable_laws = neo4j_service.find_applicable_laws(entities)
    enhanced_laws = neo4j_service.enhance_with_property_analysis(applicable_laws, entities)

    print(f"Found {len(enhanced_laws)} laws:")
    for law in enhanced_laws:
        print(f"  {law['section']}: {law['title']} (confidence: {law['confidence']})")

    # Result
    if len(enhanced_laws) > 0:
        print("\nSUCCESS: Complete pipeline working!")
        return True
    else:
        print("\nFAIL: No laws found")
        return False

if __name__ == "__main__":
    test_simple_case()