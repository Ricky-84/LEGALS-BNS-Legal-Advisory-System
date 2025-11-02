#!/usr/bin/env python3
"""
LEGALS Complete Pipeline Test
Test the full end-to-end integration: SLM Entity Extraction + Neo4j Legal Reasoning
"""
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ollama_service import ollama_service
from app.services.neo4j_service import neo4j_service

def test_complete_end_to_end_pipeline():
    """Test the complete LEGALS pipeline: User Query -> SLM -> Neo4j -> Legal Response"""
    print("Testing Complete End-to-End LEGALS Pipeline")
    print("=" * 60)

    test_cases = [
        {
            "name": "Basic Theft Case",
            "query": "Someone stole my iPhone from my house last night",
            "expected_sections": ["BNS-303", "BNS-305"],
            "expected_elements": ["iPhone", "house", "stolen"]
        },
        {
            "name": "Employee Theft Case",
            "query": "My employee took cash and laptop from my office drawer",
            "expected_sections": ["BNS-303", "BNS-306"],
            "expected_elements": ["employee", "cash", "laptop", "office"]
        },
        {
            "name": "Robbery Case",
            "query": "A robber threatened me with a knife and snatched my wallet on the street",
            "expected_sections": ["BNS-303", "BNS-309"],
            "expected_elements": ["robber", "threatened", "knife", "wallet"]
        },
        {
            "name": "High-Value Theft",
            "query": "Thief broke into my house and stole my diamond jewelry worth 50000 rupees",
            "expected_sections": ["BNS-303", "BNS-305"],
            "expected_elements": ["jewelry", "house", "broke"]
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {test_case['name']} ---")
        print(f"Query: {test_case['query']}")

        try:
            # Step 1: SLM Entity Extraction
            print("\n[STEP 1] Entity Extraction (SLM)")
            entities = ollama_service.extract_entities(test_case['query'])

            print("Extracted Entities:")
            for category, items in entities.items():
                if items and category != "property_value_analysis":
                    print(f"  {category}: {items}")

            # Show property value analysis
            if "property_value_analysis" in entities:
                analysis = entities["property_value_analysis"]
                total_value = analysis.get('total_estimated_value', 0)
                threshold_status = "Above Rs.5,000" if total_value >= 5000 else "Below Rs.5,000"
                print(f"  Property Value: Rs.{total_value:,} ({threshold_status})")

            # Step 2: Neo4j Legal Reasoning
            print("\n[STEP 2] Legal Reasoning (Neo4j)")
            applicable_laws = neo4j_service.find_applicable_laws(entities)
            enhanced_laws = neo4j_service.enhance_with_property_analysis(applicable_laws, entities)
            confidence = neo4j_service.get_legal_confidence_score(enhanced_laws)

            print(f"Found {len(enhanced_laws)} applicable laws (confidence: {confidence:.2f})")

            for law in enhanced_laws:
                print(f"\n  SECTION {law['section']}: {law['title']}")
                print(f"     Confidence: {law['confidence']:.2f}")
                print(f"     Reasoning: {law['reasoning']}")

                # Show property analysis for BNS-303
                if law.get('property_analysis'):
                    print(f"     Property Analysis:")
                    for prop in law['property_analysis']:
                        value_status = "HIGH" if prop['estimated_value'] >= 5000 else "LOW"
                        print(f"       [{value_status}] {prop['item']}: Rs.{prop['estimated_value']:,}")

                # Show punishment modifications
                if law.get('punishment_modification'):
                    mod = law['punishment_modification']
                    print(f"     Punishment: {mod.get('modified', 'Standard punishment')}")

            # Step 3: Validation
            print("\n[STEP 3] Validation")
            found_sections = [law['section'] for law in enhanced_laws]
            expected_found = any(section in found_sections for section in test_case.get('expected_sections', []))

            if expected_found:
                print(f"     SUCCESS: Found expected legal sections")
                results.append((test_case['name'], True))
            else:
                print(f"     WARNING: Expected sections {test_case.get('expected_sections', [])} not found")
                print(f"     Found: {found_sections}")
                results.append((test_case['name'], False))

        except Exception as e:
            print(f"FAIL: Test case failed: {e}")
            results.append((test_case['name'], False))

        print("-" * 60)

    return results

def test_property_value_thresholds():
    """Test property value threshold logic with different scenarios"""
    print("\n\nTesting Property Value Threshold Logic")
    print("=" * 50)

    threshold_cases = [
        {
            "name": "Low-Value Theft (Community Service)",
            "query": "Someone took my old phone and small purse from bus",
            "expected_threshold": "below"
        },
        {
            "name": "High-Value Theft (Standard Punishment)",
            "query": "Thief stole my iPhone and MacBook from office",
            "expected_threshold": "above"
        },
        {
            "name": "Mixed-Value Items",
            "query": "Robber took my wallet with cash and expensive watch",
            "expected_threshold": "above"
        }
    ]

    for case in threshold_cases:
        print(f"\n--- {case['name']} ---")
        print(f"Query: {case['query']}")

        try:
            # Extract entities and get property analysis
            entities = ollama_service.extract_entities(case['query'])

            if "property_value_analysis" in entities:
                analysis = entities["property_value_analysis"]
                total_value = analysis.get('total_estimated_value', 0)
                threshold_status = "above" if total_value >= 5000 else "below"

                print(f"Total Value: Rs.{total_value:,}")
                print(f"Threshold Status: {threshold_status} Rs.5,000")
                print(f"Expected: {case['expected_threshold']}")

                if threshold_status == case['expected_threshold']:
                    print("PASS: Threshold analysis correct")
                else:
                    print("WARNING: Threshold analysis unexpected")

        except Exception as e:
            print(f"FAIL: {e}")

def test_legal_response_generation():
    """Test legal response generation with SLM"""
    print("\n\nTesting Legal Response Generation")
    print("=" * 40)

    test_query = "Someone stole my iPhone from my house"

    try:
        # Get complete legal analysis
        entities = ollama_service.extract_entities(test_query)
        applicable_laws = neo4j_service.find_applicable_laws(entities)
        enhanced_laws = neo4j_service.enhance_with_property_analysis(applicable_laws, entities)

        legal_analysis = {
            "applicable_laws": enhanced_laws,
            "confidence_score": neo4j_service.get_legal_confidence_score(enhanced_laws),
            "reasoning_method": "ollama_neo4j_integrated"
        }

        print(f"Legal Analysis Summary:")
        print(f"  Laws Found: {len(enhanced_laws)}")
        print(f"  Confidence: {legal_analysis['confidence_score']:.2f}")

        # Generate citizen-friendly response
        print(f"\nGenerating Citizen-Friendly Response...")
        response = ollama_service.format_legal_response(legal_analysis, language="en")

        print(f"\nGenerated Response:")
        print("-" * 30)
        print(response)
        print("-" * 30)

        if len(response) > 50:
            print("PASS: Response generated successfully")
            return True
        else:
            print("WARNING: Response seems too short")
            return False

    except Exception as e:
        print(f"FAIL: Response generation failed: {e}")
        return False

def main():
    """Run complete pipeline tests"""
    print("LEGALS COMPLETE PIPELINE TEST SUITE")
    print("=" * 70)

    # Check prerequisites
    print("Checking Prerequisites...")
    if not ollama_service.is_available():
        print("FAIL: Ollama service not available")
        return

    if not neo4j_service.available:
        print("FAIL: Neo4j service not available")
        return

    print("All services available")

    # Run tests
    test_results = []

    # Test 1: Complete End-to-End Pipeline
    pipeline_results = test_complete_end_to_end_pipeline()
    test_results.extend(pipeline_results)

    # Test 2: Property Value Thresholds
    test_property_value_thresholds()

    # Test 3: Legal Response Generation
    response_success = test_legal_response_generation()
    test_results.append(("Legal Response Generation", response_success))

    # Summary
    print("\n" + "=" * 70)
    print("COMPLETE PIPELINE TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)

    for test_name, result in test_results:
        status = "PASS" if result else "FAIL"
        print(f"{status} {test_name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\nSUCCESS: Complete LEGALS pipeline is working!")
        print("SLM Entity Extraction: Working")
        print("Neo4j Legal Reasoning: Working")
        print("Property Value Analysis: Working")
        print("Legal Response Generation: Working")
        print("\nREADY FOR PRODUCTION!")
    else:
        print(f"\nWARNING: {total - passed} tests failed")
        print("Some components need attention before production")

if __name__ == "__main__":
    main()