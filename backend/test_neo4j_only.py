#!/usr/bin/env python3
"""
LEGALS Neo4j Backend Test (No SLM Required)
Test only the Neo4j knowledge graph integration with sample JSON entities
"""
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.neo4j_service import neo4j_service
from app.services.property_value_estimator import PropertyValueEstimator

def test_neo4j_connection():
    """Test basic Neo4j connection"""
    print("Testing Neo4j Connection...")

    if not neo4j_service.available:
        print("FAIL: Neo4j not available")
        return False

    try:
        with neo4j_service.driver.session(database="legalknowledge") as session:
            result = session.run("MATCH (c:Chapter) RETURN c.title as title")
            chapters = [record["title"] for record in result]
            print(f"SUCCESS: Connected! Chapters: {chapters}")
            return True
    except Exception as e:
        print(f"FAIL: Connection failed: {e}")
        return False

def test_sample_scenarios():
    """Test various legal scenarios with sample JSON entities"""
    print("\nTesting Sample Legal Scenarios...")

    # Sample scenarios with pre-defined entities (no SLM needed)
    scenarios = [
        {
            "name": "Basic Theft Case",
            "description": "Simple theft of iPhone from someone's house",
            "entities": {
                "persons": ["thief", "victim"],
                "objects": ["iPhone"],
                "locations": ["house"],
                "actions": ["took", "stolen"],
                "intentions": ["dishonestly", "without permission"],
                "circumstances": ["at night"],
                "relationships": []
            }
        },
        {
            "name": "Dwelling House Theft",
            "description": "Theft committed in someone's dwelling",
            "entities": {
                "persons": ["burglar", "homeowner"],
                "objects": ["laptop", "jewelry"],
                "locations": ["house", "bedroom", "dwelling"],
                "actions": ["broke in", "stolen"],
                "intentions": ["theft"],
                "circumstances": ["while family sleeping"],
                "relationships": []
            }
        },
        {
            "name": "Employee Theft",
            "description": "Employee stealing from employer",
            "entities": {
                "persons": ["employee", "clerk"],
                "objects": ["cash", "laptop"],
                "locations": ["office", "workplace"],
                "actions": ["took", "theft"],
                "intentions": ["dishonestly"],
                "circumstances": ["during work hours"],
                "relationships": ["employer", "company"]
            }
        },
        {
            "name": "Robbery with Violence",
            "description": "Theft with force and violence",
            "entities": {
                "persons": ["robber", "victim"],
                "objects": ["wallet", "phone", "jewelry"],
                "locations": ["street", "road"],
                "actions": ["snatched", "threatened", "pushed"],
                "intentions": ["theft"],
                "circumstances": ["used force"],
                "violence": ["threatened", "pushed", "hurt"],
                "relationships": []
            }
        },
        {
            "name": "High-Value Theft",
            "description": "Theft of expensive items",
            "entities": {
                "persons": ["thief"],
                "objects": ["diamond ring", "gold necklace", "expensive watch"],
                "locations": ["jewelry store"],
                "actions": ["stolen"],
                "intentions": ["theft"],
                "circumstances": [],
                "relationships": []
            }
        },
        {
            "name": "Low-Value Theft (Community Service Eligible)",
            "description": "Theft of low-value items",
            "entities": {
                "persons": ["first-time offender"],
                "objects": ["old phone", "small wallet"],
                "locations": ["park"],
                "actions": ["took"],
                "intentions": ["theft"],
                "circumstances": ["first time"],
                "relationships": []
            }
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['name']} ---")
        print(f"Description: {scenario['description']}")

        # Test basic legal reasoning
        applicable_laws = neo4j_service.find_applicable_laws(scenario['entities'])

        # Test enhanced reasoning with property analysis
        enhanced_laws = neo4j_service.enhance_with_property_analysis(applicable_laws, scenario['entities'])

        # Calculate confidence
        confidence = neo4j_service.get_legal_confidence_score(enhanced_laws)

        print(f"RESULTS:")
        print(f"   Found {len(enhanced_laws)} applicable laws")
        print(f"   Overall confidence: {confidence:.2f}")

        for law in enhanced_laws:
            print(f"\n   SECTION: {law['section']}: {law['title']}")
            print(f"      Confidence: {law['confidence']}")
            print(f"      Reasoning: {law['reasoning']}")
            print(f"      Offence Type: {law.get('offence_type', 'N/A')}")

            # Property analysis details
            if law.get('property_analysis'):
                print(f"      PROPERTY ANALYSIS:")
                for prop in law['property_analysis']:
                    value_status = "LOW" if prop['estimated_value'] < 5000 else "HIGH"
                    print(f"         [{value_status}] {prop['item']}: Rs.{prop['estimated_value']:,}")
                    print(f"            Reasoning: {prop.get('reasoning', prop.get('basis', 'N/A'))}")

            # Punishment modifications
            if law.get('punishment_modification'):
                mod = law['punishment_modification']
                print(f"      PUNISHMENT MODIFICATION:")
                print(f"         Threshold: {mod['threshold_applied']}")
                print(f"         Modified: {mod['modified']}")
                print(f"         Reason: {mod['reasoning']}")

        print("-" * 60)

    return True

def test_property_value_scenarios():
    """Test property value estimation with various items"""
    print("\nTesting Property Value Estimation...")

    estimator = PropertyValueEstimator()

    test_cases = [
        ["iPhone", "wallet"],  # Mixed values
        ["diamond ring", "gold necklace"],  # High values
        ["old phone", "small purse"],  # Low values
        ["laptop", "camera", "jewelry"],  # Multiple items
        ["cash", "documents"],  # Special cases
    ]

    for i, objects in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {objects}")
        analysis = estimator.estimate_value(objects)

        total_value = analysis['total_estimated_value']
        threshold_status = "Below Rs.5,000 (Community Service Eligible)" if total_value < 5000 else "Above Rs.5,000 (Standard Punishment)"

        print(f"   Total Value: Rs.{total_value:,}")
        print(f"   Confidence: {analysis['confidence']}")
        print(f"   Threshold Status: {threshold_status}")

        for item in analysis['breakdown']:
            print(f"   - {item['item']}: Rs.{item['estimated_value']:,} (confidence: {item['confidence']})")

    return True

def export_test_results():
    """Export test results to JSON for further analysis"""
    print("\nExporting Test Results...")

    test_scenario = {
        "entities": {
            "persons": ["thief"],
            "objects": ["iPhone", "wallet"],
            "locations": ["house"],
            "actions": ["stolen"],
            "intentions": ["theft"],
            "circumstances": [],
            "relationships": []
        }
    }

    # Get legal analysis
    applicable_laws = neo4j_service.find_applicable_laws(test_scenario['entities'])
    enhanced_laws = neo4j_service.enhance_with_property_analysis(applicable_laws, test_scenario['entities'])

    result = {
        "test_scenario": test_scenario,
        "legal_analysis": {
            "applicable_laws": enhanced_laws,
            "confidence_score": neo4j_service.get_legal_confidence_score(enhanced_laws),
            "reasoning_method": "neo4j_graph_enhanced",
            "property_value_analysis": any(law.get("property_analysis") for law in enhanced_laws)
        }
    }

    # Save to file
    output_file = "test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: Results exported to {output_file}")
    return True

def main():
    """Run Neo4j-only tests"""
    print("LEGALS Neo4j Backend Test (No SLM)")
    print("=" * 50)

    tests = [
        ("Neo4j Connection", test_neo4j_connection),
        ("Sample Legal Scenarios", test_sample_scenarios),
        ("Property Value Scenarios", test_property_value_scenarios),
        ("Export Test Results", export_test_results)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            print(f"\nRunning: {test_name}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"FAIL: {test_name} failed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} {test_name}")

    print(f"\nResults: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("SUCCESS: All Neo4j tests passed!")
        print("INFO: The knowledge graph integration is working correctly!")
    else:
        print("WARNING: Some tests failed. Check Neo4j connection and data.")

if __name__ == "__main__":
    main()