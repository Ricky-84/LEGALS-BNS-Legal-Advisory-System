#!/usr/bin/env python3
"""
Debug entity matching logic
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.neo4j_service import neo4j_service

def test_entity_matching():
    """Test the entity matching logic"""
    print("Testing Entity Matching Logic...")

    # Test entities from the first scenario
    test_entities = {
        "persons": ["thief", "victim"],
        "objects": ["iPhone"],
        "locations": ["house"],
        "actions": ["took", "stolen"],
        "intentions": ["dishonestly", "without permission"],
        "circumstances": ["at night"],
        "relationships": []
    }

    print(f"Test entities: {test_entities}")

    # Test each detection method
    print(f"\n=== THEFT DETECTION ===")

    # Debug the theft detection logic
    actions = test_entities.get("actions", [])
    objects = test_entities.get("objects", [])
    intentions = test_entities.get("intentions", [])

    theft_actions = ["took", "stolen", "theft", "stealing", "grabbed", "snatched"]
    property_objects = ["phone", "mobile", "wallet", "money", "bag", "purse", "jewelry"]
    dishonest_intentions = ["without permission", "dishonest", "wrongfully"]

    print(f"Actions: {actions}")
    print(f"Objects: {objects}")
    print(f"Intentions: {intentions}")

    has_theft_action = any(action.lower() in theft_actions for action in actions)
    has_property = any(obj.lower() in property_objects for obj in objects)
    has_dishonest_intent = any(intent.lower() in dishonest_intentions for intent in intentions)

    print(f"Has theft action: {has_theft_action} (looking for: {theft_actions})")
    print(f"Has property: {has_property} (looking for: {property_objects})")
    print(f"Has dishonest intent: {has_dishonest_intent} (looking for: {dishonest_intentions})")

    has_theft = neo4j_service._has_theft_elements(test_entities)
    print(f"Overall has theft elements: {has_theft}")

    print(f"\n=== DWELLING THEFT DETECTION ===")
    has_dwelling = neo4j_service._has_dwelling_theft_elements(test_entities)
    print(f"Has dwelling theft elements: {has_dwelling}")

    print(f"\n=== EMPLOYEE THEFT DETECTION ===")
    has_employee = neo4j_service._has_employee_theft_elements(test_entities)
    print(f"Has employee theft elements: {has_employee}")

    print(f"\n=== ROBBERY DETECTION ===")
    has_robbery = neo4j_service._has_robbery_elements(test_entities)
    print(f"Has robbery elements: {has_robbery}")

    # Test the actual query
    if has_theft:
        print(f"\n=== TESTING ACTUAL NEO4J QUERY ===")
        try:
            with neo4j_service.driver.session(database="legalknowledge") as session:
                # First, check what relationships Section 303 actually has
                print("Checking Section 303 relationships...")
                result = session.run("""
                    MATCH (s:Section)-[r]-(n)
                    WHERE s.section_number = 303
                    RETURN labels(n) as connected_to, type(r) as relationship_type, properties(n) as props
                """)

                for record in result:
                    print(f"Section 303 --[{record['relationship_type']}]--> {record['connected_to']}")
                    if 'description' in record['props']:
                        print(f"  Description: {record['props']['description'][:50]}...")

                # Check punishment nodes and their relationships to Section 303
                print("\nChecking Section 303 to Punishment relationship...")
                result = session.run("""
                    MATCH (s:Section)-[r]-(p:Punishment)
                    WHERE s.section_number = 303
                    RETURN type(r) as relationship_type, startNode(r) = s as section_is_start, properties(p) as punishment_props
                """)

                records = list(result)
                print(f"Found {len(records)} Section-Punishment relationships for section 303")
                for i, record in enumerate(records):
                    direction = "Section --[{}]--> Punishment" if record['section_is_start'] else "Punishment --[{}]--> Section"
                    print(f"Relationship {i+1}: {direction.format(record['relationship_type'])}")
                    print(f"  Punishment: {record['punishment_props']['description'][:50]}...")

                # Check punishment nodes
                print("\nChecking Punishment nodes for section 303...")
                result = session.run("""
                    MATCH (p:Punishment)
                    WHERE p.section_id = 'BNS-303'
                    RETURN properties(p) as punishment_props
                """)

                records = list(result)
                print(f"Found {len(records)} Punishment records for section 303")
                for i, record in enumerate(records):
                    print(f"Punishment {i+1}: {record['punishment_props']}")

                # Check all relationships in the graph
                print("\nChecking all relationship types...")
                result = session.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")
                rels = [record['relationshipType'] for record in result]
                print(f"Available relationships: {rels}")

                # Test the new fixed query structure
                print("\nTesting fixed query structure...")
                result = session.run("""
                    MATCH (s:Section)-[:DEFINES]->(o:Offence)
                    MATCH (p:Punishment)
                    WHERE s.section_number = 303 AND p.section_id = s.section_id
                    RETURN s.section_id as section, s.title as title,
                           s.text as description, p.description as punishment,
                           p.punishment_type as severity, o.type as offence_type
                """)

                records = list(result)
                print(f"Fixed query returned {len(records)} records")
                for i, record in enumerate(records):
                    print(f"Record {i+1}:")
                    for key, value in record.items():
                        print(f"  {key}: {value[:100] if isinstance(value, str) and len(value) > 100 else value}")

                # Test simpler query first
                print("\nTesting simpler query...")
                result = session.run("""
                    MATCH (s:Section)
                    WHERE s.section_number = 303
                    RETURN s.section_id as section, s.title as title, s.text as description
                """)

                records = list(result)
                print(f"Simple query returned {len(records)} records")
                for i, record in enumerate(records):
                    print(f"Record {i+1}:")
                    for key, value in record.items():
                        print(f"  {key}: {value}")

        except Exception as e:
            print(f"Query failed: {e}")

if __name__ == "__main__":
    test_entity_matching()