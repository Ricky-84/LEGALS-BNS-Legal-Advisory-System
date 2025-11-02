#!/usr/bin/env python3
"""
LEGALS Backend Integration Test
Test the complete pipeline: Entity Extraction → Neo4j Knowledge Graph → Property Value Analysis
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.neo4j_service import neo4j_service
from app.services.property_value_estimator import PropertyValueEstimator
from app.services.legal_processing_service import LegalProcessingService

def test_neo4j_connection():
    """Test Neo4j connection and basic graph query"""
    print(" Testing Neo4j Connection...")

    if not neo4j_service.available:
        print(" Neo4j not available - using fallback reasoning")
        return False

    try:
        with neo4j_service.driver.session() as session:
            result = session.run("MATCH (c:Chapter) RETURN c.title as title")
            chapters = [record["title"] for record in result]
            print(f" Neo4j connected! Found chapters: {chapters}")
            return True
    except Exception as e:
        print(f" Neo4j connection failed: {e}")
        return False

def test_knowledge_graph_queries():
    """Test knowledge graph structure and queries"""
    print("\n Testing Knowledge Graph Queries...")

    try:
        with neo4j_service.driver.session() as session:
            # Test 1: Count all nodes
            result = session.run("""
                MATCH (c:Chapter) WITH count(c) as chapters
                MATCH (s:Section) WITH chapters, count(s) as sections
                MATCH (o:Offence) WITH chapters, sections, count(o) as offences
                MATCH (p:Punishment) WITH chapters, sections, offences, count(p) as punishments
                RETURN chapters, sections, offences, punishments
            """)

            for record in result:
                print(f" Chapters: {record['chapters']}, Sections: {record['sections']}")
                print(f"   Offences: {record['offences']}, Punishments: {record['punishments']}")

            # Test 2: Test Section 303 (Theft) query
            result = session.run("""
                MATCH (c:Chapter)-[:CONTAINS]->(s:Section)-[:DEFINES]->(o:Offence)-[:PUNISHABLE_BY]->(p:Punishment)
                WHERE s.section_number = 303
                RETURN s.title as section_title, o.name as offence_name, p.description as punishment
            """)

            for record in result:
                print(f" Section 303: {record['section_title']}")
                print(f"   Offence: {record['offence_name']}")
                print(f"   Punishment: {record['punishment'][:100]}...")

        return True
    except Exception as e:
        print(f" Knowledge graph queries failed: {e}")
        return False

def test_property_value_estimation():
    """Test property value estimation"""
    print("\n Testing Property Value Estimation...")

    estimator = PropertyValueEstimator()

    test_objects = ["iPhone", "laptop", "wallet", "gold chain"]
    analysis = estimator.analyze_property_values(test_objects)

    print(" Property Value Analysis:")
    for item in analysis:
        print(f"   {item['item']}: ₹{item['estimated_value']:,} ({item['reasoning']})")

    return True

def test_entity_extraction_integration():
    """Test entity extraction with Neo4j integration"""
    print("\n Testing Entity Extraction → Neo4j Integration...")

    # Simulate extracted entities (as if from Ollama)
    test_entities = {
        "persons": ["John", "victim"],
        "objects": ["iPhone", "wallet"],
        "locations": ["house", "bedroom"],
        "actions": ["took", "stolen"],
        "intentions": ["without permission"],
        "circumstances": ["at night"],
        "relationships": []
    }

    # Test Neo4j legal reasoning
    applicable_laws = neo4j_service.find_applicable_laws(test_entities)
    enhanced_laws = neo4j_service.enhance_with_property_analysis(applicable_laws, test_entities)

    print(f" Found {len(enhanced_laws)} applicable laws:")
    for law in enhanced_laws:
        print(f"   {law['section']}: {law['title']} (confidence: {law['confidence']})")
        print(f"   Reasoning: {law['reasoning']}")

        if law.get('property_analysis'):
            print(f"   Property Analysis: {law['property_analysis']}")

        if law.get('punishment_modification'):
            print(f"   Punishment Modification: {law['punishment_modification']['modified']}")

    return True

def test_full_pipeline():
    """Test the complete legal processing pipeline"""
    print("\n Testing Complete Legal Processing Pipeline...")

    try:
        legal_service = LegalProcessingService()

        # Test query with theft scenario
        test_query = "Someone broke into my house and stole my iPhone and wallet while I was sleeping"

        print(f"Query: {test_query}")

        # Note: This would normally go through Ollama for entity extraction
        # For testing, we simulate the entities
        simulated_entities = {
            "persons": ["someone"],
            "objects": ["iPhone", "wallet"],
            "locations": ["house"],
            "actions": ["broke", "stole"],
            "intentions": ["theft"],
            "circumstances": ["while sleeping"],
            "relationships": []
        }

        # Test legal reasoning step directly
        legal_analysis = legal_service._legal_reasoning_step(simulated_entities)

        print(" Legal Analysis Results:")
        print(f"   Confidence Score: {legal_analysis['confidence_score']}")
        print(f"   Reasoning Method: {legal_analysis['reasoning_method']}")
        print(f"   Property Value Analysis: {legal_analysis.get('property_value_analysis', False)}")
        print(f"   Applicable Laws: {len(legal_analysis['applicable_laws'])}")

        for law in legal_analysis['applicable_laws']:
            print(f"\n    {law['section']}: {law['title']}")
            print(f"      Confidence: {law['confidence']}")
            print(f"      Reasoning: {law['reasoning']}")

            if law.get('property_analysis'):
                print(f"      Property Analysis: Yes")
                for prop in law['property_analysis']:
                    print(f"        - {prop['item']}: ₹{prop['estimated_value']:,}")

            if law.get('punishment_modification'):
                print(f"      Punishment Modification: {law['punishment_modification']['threshold_applied']}")

        return True

    except Exception as e:
        print(f" Full pipeline test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    print(" LEGALS Backend Integration Test Suite")
    print("=" * 50)

    tests = [
        ("Neo4j Connection", test_neo4j_connection),
        ("Knowledge Graph Queries", test_knowledge_graph_queries),
        ("Property Value Estimation", test_property_value_estimation),
        ("Entity → Neo4j Integration", test_entity_extraction_integration),
        ("Full Pipeline", test_full_pipeline)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f" {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print(" TEST SUMMARY")
    print("=" * 50)

    passed = 0
    for test_name, result in results:
        status = " PASS" if result else " FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\nResults: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print(" All tests passed! LEGALS backend integration is working!")
    else:
        print("  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()