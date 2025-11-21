#!/usr/bin/env python3
"""
Convert JSON files to CSV format for Neo4j import
Converts both BNS legal data and entity extraction training data
"""

import json
import csv
import pandas as pd
from pathlib import Path

def convert_bns_data_to_csv():
    """Convert BNS Chapter XVII JSON to CSV files for Neo4j import"""

    # Read the BNS JSON file
    with open('data/bns_data/bns_ch17.json', 'r', encoding='utf-8-sig') as f:
        bns_data = json.load(f)

    # Create output directory
    Path('data/csv_exports').mkdir(exist_ok=True)

    # 1. Create Chapters CSV
    chapters_data = [{
        'chapter_id': f"CH_{bns_data['chapter_number']}",
        'chapter_number': bns_data['chapter_number'],
        'chapter_title': bns_data['chapter_title'],
        'full_title': f"Chapter {bns_data['chapter_number']}: {bns_data['chapter_title']}"
    }]

    chapters_df = pd.DataFrame(chapters_data)
    chapters_df.to_csv('data/csv_exports/chapters.csv', index=False)
    print("Created chapters.csv")

    # 2. Create Sections CSV
    sections_data = []
    for section in bns_data['sections']:
        # Clean text by removing newlines and excessive whitespace
        section_text = section['section_text'].replace('\n', ' ').replace('\r', ' ')
        section_text = ' '.join(section_text.split())  # Remove extra whitespace

        # Truncate very long text if needed (Neo4j string limit)
        if len(section_text) > 10000:
            section_text = section_text[:10000] + "..."

        sections_data.append({
            'section_id': f"BNS_{section['section_number']}",
            'section_number': section['section_number'],
            'section_title': section['section_title'],
            'section_text': section_text,
            'chapter_id': f"CH_{bns_data['chapter_number']}"
        })

    sections_df = pd.DataFrame(sections_data)
    sections_df.to_csv('data/csv_exports/sections.csv', index=False)
    print(f"Created sections.csv with {len(sections_data)} sections")

    # 3. Extract Legal Concepts
    legal_concepts = []
    concept_id = 1

    # Key legal terms to extract
    key_terms = [
        'theft', 'snatching', 'extortion', 'robbery', 'dacoity',
        'misappropriation', 'breach', 'trust', 'cheating', 'mischief',
        'trespass', 'property', 'dwelling', 'movable', 'dishonest',
        'possession', 'consent', 'force', 'violence', 'criminal'
    ]

    for term in key_terms:
        legal_concepts.append({
            'concept_id': f"CONCEPT_{concept_id:03d}",
            'concept_name': term,
            'concept_type': 'legal_term',
            'description': f"Legal concept: {term}"
        })
        concept_id += 1

    concepts_df = pd.DataFrame(legal_concepts)
    concepts_df.to_csv('data/csv_exports/legal_concepts.csv', index=False)
    print(f"Created legal_concepts.csv with {len(legal_concepts)} concepts")

    # 4. Create Section-Concept relationships
    section_concepts = []
    for section in bns_data['sections']:
        section_text_lower = section['section_text'].lower()
        section_title_lower = section['section_title'].lower()

        for concept in legal_concepts:
            term = concept['concept_name']
            if term in section_text_lower or term in section_title_lower:
                section_concepts.append({
                    'section_id': f"BNS_{section['section_number']}",
                    'concept_id': concept['concept_id'],
                    'relationship_type': 'APPLIES_TO',
                    'relevance_score': 1.0
                })

    section_concepts_df = pd.DataFrame(section_concepts)
    section_concepts_df.to_csv('data/csv_exports/section_concepts.csv', index=False)
    print(f"Created section_concepts.csv with {len(section_concepts)} relationships")

def convert_entity_training_to_csv():
    """Convert entity extraction training JSON to CSV"""

    # Read entity extraction training data (first 100 entries for manageability)
    with open('data/training_data/entity_extraction_training.json', 'r', encoding='utf-8') as f:
        training_data = json.load(f)

    # Limit to first 100 entries for initial import
    training_data = training_data[:100]

    # 1. Create Queries CSV
    queries_data = []
    for i, entry in enumerate(training_data):
        queries_data.append({
            'query_id': f"QUERY_{i+1:03d}",
            'user_query': entry['user_query'],
            'language': entry.get('language', 'en'),
            'task': entry.get('task', 'entity_extraction')
        })

    queries_df = pd.DataFrame(queries_data)
    queries_df.to_csv('data/csv_exports/user_queries.csv', index=False)
    print(f"Created user_queries.csv with {len(queries_data)} queries")

    # 2. Create Entities CSV
    entities_data = []
    entity_id = 1

    for i, entry in enumerate(training_data):
        query_id = f"QUERY_{i+1:03d}"
        extracted = entry.get('extracted_entities', {})

        # Process each entity type
        for entity_type, entity_list in extracted.items():
            if isinstance(entity_list, list):
                for entity_value in entity_list:
                    entities_data.append({
                        'entity_id': f"ENTITY_{entity_id:04d}",
                        'entity_type': entity_type,
                        'entity_value': entity_value,
                        'query_id': query_id
                    })
                    entity_id += 1

    entities_df = pd.DataFrame(entities_data)
    entities_df.to_csv('data/csv_exports/entities.csv', index=False)
    print(f"Created entities.csv with {len(entities_data)} entities")

    # 3. Create Entity Types CSV
    entity_types = [
        {'type_id': 'TYPE_001', 'type_name': 'objects', 'description': 'Physical objects that can be stolen or damaged'},
        {'type_id': 'TYPE_002', 'type_name': 'locations', 'description': 'Places where offenses occur'},
        {'type_id': 'TYPE_003', 'type_name': 'actions', 'description': 'Criminal actions or behaviors'},
        {'type_id': 'TYPE_004', 'type_name': 'intentions', 'description': 'Criminal intent or motivation'},
        {'type_id': 'TYPE_005', 'type_name': 'persons', 'description': 'People involved in the offense'},
        {'type_id': 'TYPE_006', 'type_name': 'circumstances', 'description': 'Situational factors'}
    ]

    entity_types_df = pd.DataFrame(entity_types)
    entity_types_df.to_csv('data/csv_exports/entity_types.csv', index=False)
    print(f"Created entity_types.csv with {len(entity_types)} entity types")

def main():
    """Convert both JSON files to CSV format"""
    print("Converting JSON files to CSV for Neo4j import...")
    print("=" * 50)

    try:
        convert_bns_data_to_csv()
        print()
        convert_entity_training_to_csv()
        print()
        print("=" * 50)
        print("All CSV files created successfully!")
        print("\nFiles created in data/csv_exports/:")
        print("- chapters.csv")
        print("- sections.csv")
        print("- legal_concepts.csv")
        print("- section_concepts.csv")
        print("- user_queries.csv")
        print("- entities.csv")
        print("- entity_types.csv")
        print("\nReady for Neo4j Data Importer!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()