#!/usr/bin/env python3
"""
Debug Neo4j data structure
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.neo4j_service import neo4j_service

def debug_neo4j_structure():
    """Debug what's actually in Neo4j"""
    print("Debugging Neo4j Data Structure...")

    if not neo4j_service.available:
        print("FAIL: Neo4j not available")
        return

    try:
        # Try connecting to specific database
        with neo4j_service.driver.session(database="legalknowledge") as session:
            # Check what labels exist
            print("\n=== LABELS ===")
            result = session.run("CALL db.labels() YIELD label RETURN label")
            for record in result:
                print(f"Label: {record['label']}")

            # Check Section properties
            print("\n=== SECTION PROPERTIES ===")
            result = session.run("MATCH (s:Section) RETURN properties(s) LIMIT 3")
            for i, record in enumerate(result, 1):
                print(f"Section {i} properties: {record['properties(s)']}")

            # Check relationships
            print("\n=== RELATIONSHIPS ===")
            result = session.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")
            for record in result:
                print(f"Relationship: {record['relationshipType']}")

            # Check specific Section data
            print("\n=== SAMPLE SECTION DATA ===")
            result = session.run("MATCH (s:Section) WHERE s.section_number = 303 RETURN s LIMIT 1")
            for record in result:
                section = record['s']
                print(f"Section 303 found:")
                for key, value in section.items():
                    print(f"  {key}: {value}")

            # Check Section-Punishment relationship
            print("\n=== SECTION-PUNISHMENT RELATIONSHIPS ===")
            result = session.run("""
                MATCH (s:Section)-[r]-(p:Punishment)
                WHERE s.section_number = 303
                RETURN type(r) as relationship_type, s.section_number as section, properties(p) as punishment_props
                LIMIT 3
            """)
            for record in result:
                print(f"Section {record['section']} --[{record['relationship_type']}]--> Punishment properties: {record['punishment_props']}")

            # Check the full path structure
            print("\n=== FULL PATH STRUCTURE ===")
            result = session.run("""
                MATCH (c:Chapter)-[r1]-(s:Section)-[r2]-(o:Offence)
                WHERE s.section_number = 303
                RETURN type(r1) as chapter_section_rel, type(r2) as section_offence_rel, s.section_number as section
                LIMIT 3
            """)
            for record in result:
                print(f"Chapter --[{record['chapter_section_rel']}]--> Section {record['section']} --[{record['section_offence_rel']}]--> Offence")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_neo4j_structure()