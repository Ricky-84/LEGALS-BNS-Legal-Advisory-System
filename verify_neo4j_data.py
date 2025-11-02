#!/usr/bin/env python3
"""Verify Neo4j data is correctly imported"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv('backend/.env')

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

print(f"Connecting to Neo4j at {NEO4J_URI}...")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

with driver.session(database="legalknowledge") as session:
    # Check what nodes exist
    print("\n=== NODE COUNTS ===")
    result = session.run("MATCH (c:Chapter) RETURN count(c) as count")
    print(f"Chapters: {result.single()['count']}")

    result = session.run("MATCH (s:Section) RETURN count(s) as count")
    print(f"Sections: {result.single()['count']}")

    result = session.run("MATCH (o:Offence) RETURN count(o) as count")
    print(f"Offences: {result.single()['count']}")

    result = session.run("MATCH (p:Punishment) RETURN count(p) as count")
    print(f"Punishments: {result.single()['count']}")

    # Check section 303 specifically
    print("\n=== SECTION 303 (Theft) ===")
    result = session.run("""
        MATCH (s:Section)
        WHERE s.section_number = 303
        RETURN s.section_id, s.section_number, s.title
    """)

    for record in result:
        print(f"Section found: {record['s.section_id']}, {record['s.section_number']}, {record['s.title']}")

    # Check if offence exists
    print("\n=== OFFENCE FOR SECTION 303 ===")
    result = session.run("""
        MATCH (s:Section)-[:DEFINES]->(o:Offence)
        WHERE s.section_number = 303
        RETURN s.section_id, o.type, o.section_number
    """)

    for record in result:
        print(f"Offence found: {record['s.section_id']} -> {record['o.type']}")

    # Check punishment
    print("\n=== PUNISHMENT FOR SECTION 303 ===")
    result = session.run("""
        MATCH (s:Section)
        MATCH (p:Punishment)
        WHERE s.section_number = 303 AND p.section_id = s.section_id
        RETURN s.section_id, p.section_id, p.description
    """)

    for record in result:
        print(f"Punishment found: section={record['s.section_id']}, punishment.section_id={record['p.section_id']}")
        print(f"Description: {record['p.description'][:100]}...")

    # Test the EXACT query from neo4j_service.py
    print("\n=== TESTING EXACT QUERY FROM CODE ===")
    result = session.run("""
        MATCH (s:Section)-[:DEFINES]->(o:Offence)
        MATCH (p:Punishment)
        WHERE s.section_number = 303 AND p.section_id = s.section_id
        RETURN s.section_id as section, s.title as title,
               s.text as description, p.description as punishment,
               p.punishment_type as severity, o.type as offence_type
    """)

    count = 0
    for record in result:
        count += 1
        print(f"✓ Query returned: {record['section']}, {record['title']}, {record['offence_type']}")

    if count == 0:
        print("✗ Query returned NO RESULTS - this is the problem!")

    # Check all section numbers
    print("\n=== ALL SECTION NUMBERS IN DATABASE ===")
    result = session.run("""
        MATCH (s:Section)
        RETURN s.section_number
        ORDER BY s.section_number
    """)

    sections = [record['s.section_number'] for record in result]
    print(f"Sections: {sections}")

driver.close()
print("\n✓ Verification complete")
