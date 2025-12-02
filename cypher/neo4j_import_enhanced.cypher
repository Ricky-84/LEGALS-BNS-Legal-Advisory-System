// ====================================================================
// Neo4j Import Script for Enhanced BNS Knowledge Graph
// ====================================================================
// File: neo4j_import_enhanced.cypher
// Purpose: Import enhanced CSV with legal elements, action patterns
// CSV File: bns_10_sections_enhanced.csv
// Database: legalknowledge
// ====================================================================

// ====================================================================
// STEP 0: CLEAR OLD DATA (OPTIONAL - COMMENT OUT IF YOU WANT TO KEEP)
// ====================================================================
// WARNING: This will delete ALL data in the graph!
// Uncomment the lines below only if you want to start fresh

MATCH (n) DETACH DELETE n;


// ====================================================================
// STEP 1: CREATE CONSTRAINTS AND INDEXES (Performance Optimization)
// ====================================================================

// Constraints ensure uniqueness
CREATE CONSTRAINT section_id_unique IF NOT EXISTS
FOR (s:Section) REQUIRE s.section_id IS UNIQUE;

CREATE CONSTRAINT offence_id_unique IF NOT EXISTS
FOR (o:Offence) REQUIRE o.offence_id IS UNIQUE;

CREATE CONSTRAINT element_id_unique IF NOT EXISTS
FOR (e:LegalElement) REQUIRE e.element_id IS UNIQUE;

CREATE CONSTRAINT pattern_id_unique IF NOT EXISTS
FOR (ap:ActionPattern) REQUIRE ap.pattern_id IS UNIQUE;

CREATE CONSTRAINT punishment_id_unique IF NOT EXISTS
FOR (p:Punishment) REQUIRE p.punishment_id IS UNIQUE;

// Indexes for faster lookups
CREATE INDEX section_number_idx IF NOT EXISTS
FOR (s:Section) ON (s.section_number);

CREATE INDEX offence_type_idx IF NOT EXISTS
FOR (o:Offence) ON (o.offence_type);

CREATE INDEX element_type_idx IF NOT EXISTS
FOR (e:LegalElement) ON (e.element_type);


// ====================================================================
// STEP 2: LOAD CSV AND CREATE CHAPTER NODES
// ====================================================================

LOAD CSV WITH HEADERS FROM 'file:///bns_10_sections_enhanced.csv' AS row
WITH row
MERGE (chapter:Chapter {chapter_number: row.c_number})
ON CREATE SET
    chapter.title = row.c_title;


// ====================================================================
// STEP 3: CREATE SECTION NODES
// ====================================================================

LOAD CSV WITH HEADERS FROM 'file:///bns_10_sections_enhanced.csv' AS row
WITH row
MERGE (section:Section {section_id: 'BNS-' + row.s_section_number})
ON CREATE SET
    section.section_number = toInteger(row.s_section_number),
    section.title = row.s_section_title,
    section.text = row.s_section_text,
    section.explanation = row.explain,
    section.illustration = row.illustration,
    section.chapter = row.c_number,
    section.category = row.category
WITH section, row
MATCH (chapter:Chapter {chapter_number: row.c_number})
MERGE (chapter)-[:CONTAINS]->(section);


// ====================================================================
// STEP 4: CREATE OFFENCE NODES AND LINK TO SECTIONS
// ====================================================================

LOAD CSV WITH HEADERS FROM 'file:///bns_10_sections_enhanced.csv' AS row
WITH row
MATCH (section:Section {section_id: 'BNS-' + row.s_section_number})
MERGE (offence:Offence {offence_id: row.offence_type})
ON CREATE SET
    offence.name = row.s_section_title,
    offence.type = row.offence_type,
    offence.category = row.category,
    offence.section_number = toInteger(row.s_section_number)
MERGE (section)-[:DEFINES]->(offence);


// ====================================================================
// STEP 5: CREATE PUNISHMENT NODES AND LINK TO SECTIONS
// ====================================================================

LOAD CSV WITH HEADERS FROM 'file:///bns_10_sections_enhanced.csv' AS row
WITH row
MATCH (section:Section {section_id: 'BNS-' + row.s_section_number})
MERGE (punishment:Punishment {punishment_id: 'p_' + row.s_section_number})
ON CREATE SET
    punishment.section_id = 'BNS-' + row.s_section_number,
    punishment.description = row.punishment
MERGE (section)-[:PRESCRIBES]->(punishment);


// ====================================================================
// STEP 6: CREATE LEGAL ELEMENT NODES (MENS REA)
// ====================================================================

LOAD CSV WITH HEADERS FROM 'file:///bns_10_sections_enhanced.csv' AS row
WITH row
MATCH (offence:Offence {offence_id: row.offence_type})
WITH offence, row, split(row.mens_rea, '|') AS mens_rea_list
UNWIND mens_rea_list AS mens_rea_item
WITH offence, mens_rea_item
WHERE mens_rea_item IS NOT NULL AND trim(mens_rea_item) <> ''
MERGE (element:LegalElement:MensRea {element_id: 'mens_rea_' + trim(mens_rea_item)})
ON CREATE SET
    element.name = trim(mens_rea_item),
    element.element_type = 'mens_rea',
    element.description = 'Mental element: ' + trim(mens_rea_item)
MERGE (offence)-[:REQUIRES_MENS_REA {mandatory: true, weight: 1.0}]->(element);


// ====================================================================
// STEP 7: CREATE LEGAL ELEMENT NODES (ACTUS REUS)
// ====================================================================

LOAD CSV WITH HEADERS FROM 'file:///bns_10_sections_enhanced.csv' AS row
WITH row
MATCH (offence:Offence {offence_id: row.offence_type})
WITH offence, row, split(row.actus_reus, '|') AS actus_reus_list
UNWIND actus_reus_list AS actus_reus_item
WITH offence, actus_reus_item
WHERE actus_reus_item IS NOT NULL AND trim(actus_reus_item) <> ''
MERGE (element:LegalElement:ActusReus {element_id: 'actus_reus_' + trim(actus_reus_item)})
ON CREATE SET
    element.name = trim(actus_reus_item),
    element.element_type = 'actus_reus',
    element.description = 'Physical act: ' + trim(actus_reus_item)
MERGE (offence)-[:REQUIRES_ACTUS_REUS {mandatory: true, weight: 1.0}]->(element);


// ====================================================================
// STEP 8: CREATE LEGAL ELEMENT NODES (CIRCUMSTANCES)
// ====================================================================

LOAD CSV WITH HEADERS FROM 'file:///bns_10_sections_enhanced.csv' AS row
WITH row
MATCH (offence:Offence {offence_id: row.offence_type})
WITH offence, row, split(row.circumstances, '|') AS circumstances_list
UNWIND circumstances_list AS circumstance_item
WITH offence, circumstance_item
WHERE circumstance_item IS NOT NULL AND trim(circumstance_item) <> ''
MERGE (element:LegalElement:Circumstance {element_id: 'circumstance_' + trim(circumstance_item)})
ON CREATE SET
    element.name = trim(circumstance_item),
    element.element_type = 'circumstance',
    element.description = 'Circumstantial requirement: ' + trim(circumstance_item)
MERGE (offence)-[:REQUIRES_CIRCUMSTANCE {mandatory: true, weight: 1.0}]->(element);


// ====================================================================
// STEP 9: CREATE ACTION PATTERN NODES FROM BASIC KEYWORDS
// ====================================================================

LOAD CSV WITH HEADERS FROM 'file:///bns_10_sections_enhanced.csv' AS row
WITH row
MATCH (offence:Offence {offence_id: row.offence_type})
WITH offence, row, split(row.basic_keywords, '|') AS keyword_list
UNWIND keyword_list AS keyword
WITH offence, keyword, row.s_section_number AS section_num, row.offence_type AS offence_type
WHERE keyword IS NOT NULL AND trim(keyword) <> ''
MERGE (pattern:ActionPattern {pattern_id: trim(keyword) + '_' + section_num})
ON CREATE SET
    pattern.text = trim(keyword),
    pattern.canonical = offence_type,
    pattern.confidence = 0.9
MERGE (pattern)-[:MATCHES]->(offence);


// ====================================================================
// STEP 10: CREATE SECTION RELATIONSHIPS (AGGRAVATED FORMS)
// ====================================================================

// BNS-305 (Dwelling Theft) is aggravated form of BNS-303 (Theft)
MATCH (aggravated:Section {section_id: 'BNS-305'})
MATCH (base:Section {section_id: 'BNS-303'})
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(base);

// BNS-306 (Employee Theft) is aggravated form of BNS-303 (Theft)
MATCH (aggravated:Section {section_id: 'BNS-306'})
MATCH (base:Section {section_id: 'BNS-303'})
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(base);

// BNS-309 (Robbery) is aggravated form of BNS-303 (Theft)
MATCH (aggravated:Section {section_id: 'BNS-309'})
MATCH (base:Section {section_id: 'BNS-303'})
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(base);


// ====================================================================
// STEP 11: VERIFICATION QUERIES
// ====================================================================

// Count all nodes by type
MATCH (n)
RETURN labels(n)[0] as NodeType, count(n) as Count
ORDER BY Count DESC;

// Show sample of each node type
MATCH (s:Section)
RETURN 'Section' as Type, s.section_id as ID, s.title as Title
LIMIT 3
UNION
MATCH (o:Offence)
RETURN 'Offence' as Type, o.offence_id as ID, o.name as Title
LIMIT 3
UNION
MATCH (e:LegalElement)
RETURN 'LegalElement' as Type, e.element_id as ID, e.element_type as Title
LIMIT 3
UNION
MATCH (ap:ActionPattern)
RETURN 'ActionPattern' as Type, ap.pattern_id as ID, ap.text as Title
LIMIT 3;

// Show full graph structure for one section (BNS-303 Theft)
MATCH path = (chapter:Chapter)-[:CONTAINS]->(section:Section {section_id: 'BNS-303'})
              -[:DEFINES]->(offence:Offence)
              -[:REQUIRES_MENS_REA|REQUIRES_ACTUS_REUS|REQUIRES_CIRCUMSTANCE]->(element:LegalElement)
RETURN path
LIMIT 50;

// Count relationships by type
MATCH ()-[r]->()
RETURN type(r) as RelationshipType, count(r) as Count
ORDER BY Count DESC;


// ====================================================================
// SUCCESS MESSAGE
// ====================================================================
// If you see results from verification queries above, import succeeded!
//
// Expected node counts:
// - Chapter: 1
// - Section: 10
// - Offence: 10
// - LegalElement: 30-40 (mens rea + actus reus + circumstances)
// - ActionPattern: 60-80 (from basic_keywords)
// - Punishment: 10
//
// Expected relationship counts:
// - CONTAINS: 10
// - DEFINES: 10
// - PRESCRIBES: 10
// - REQUIRES_MENS_REA: 10-15
// - REQUIRES_ACTUS_REUS: 15-25
// - REQUIRES_CIRCUMSTANCE: 20-30
// - MATCHES: 60-80
// - AGGRAVATED_FORM_OF: 3
// ====================================================================
