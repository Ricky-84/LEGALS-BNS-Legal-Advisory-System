// ============================================
// Neo4j Incremental Import - 22 New BNS Sections (FIXED)
// ============================================
// This script adds 22 new sections to existing graph
// Does NOT delete existing 10 sections
// File: bns_22_new_sections.csv
// ============================================

// STEP 1: Import new Section nodes (22 sections)
LOAD CSV WITH HEADERS FROM 'file:///bns_22_new_sections.csv' AS row
WITH row, 'BNS-' + row.s_section_number AS section_id
MERGE (s:Section {section_id: section_id})
SET s.section_number = toInteger(row.s_section_number),
    s.title = row.s_section_title,
    s.text = row.s_section_text,
    s.chapter = row.c_number;

// STEP 2: Connect Sections to Chapter (if not already connected)
LOAD CSV WITH HEADERS FROM 'file:///bns_22_new_sections.csv' AS row
WITH row, 'BNS-' + row.s_section_number AS section_id
MATCH (s:Section {section_id: section_id})
MERGE (c:Chapter {number: row.c_number})
ON CREATE SET c.title = row.c_title
MERGE (c)-[:CONTAINS]->(s);

// STEP 3: Create Offence nodes for new sections
LOAD CSV WITH HEADERS FROM 'file:///bns_22_new_sections.csv' AS row
WITH row, 'BNS-' + row.s_section_number AS section_id
MATCH (s:Section {section_id: section_id})
MERGE (o:Offence {offence_id: row.offence_type})
ON CREATE SET
    o.name = row.s_section_title,
    o.type = row.offence_type,
    o.category = row.category
MERGE (s)-[:DEFINES]->(o);

// STEP 4: Create Punishment nodes for new sections
LOAD CSV WITH HEADERS FROM 'file:///bns_22_new_sections.csv' AS row
WITH row, 'BNS-' + row.s_section_number AS section_id
MATCH (s:Section {section_id: section_id})
MERGE (p:Punishment {section_id: section_id})
SET p.description = row.punishment
MERGE (s)-[:PRESCRIBES]->(p);

// STEP 5: Create MensRea elements for new sections
LOAD CSV WITH HEADERS FROM 'file:///bns_22_new_sections.csv' AS row
WITH row
WHERE row.mens_rea IS NOT NULL AND row.mens_rea <> ''
MATCH (o:Offence {offence_id: row.offence_type})
WITH o, row, split(row.mens_rea, '|') AS mens_rea_list
UNWIND mens_rea_list AS mens_rea_item
WITH o, row, trim(mens_rea_item) AS mens_rea_name
WHERE mens_rea_name <> ''
MERGE (mr:MensRea:LegalElement {name: mens_rea_name})
ON CREATE SET mr.type = 'mens_rea'
MERGE (o)-[:REQUIRES_MENS_REA]->(mr);

// STEP 6: Create ActusReus elements for new sections
LOAD CSV WITH HEADERS FROM 'file:///bns_22_new_sections.csv' AS row
WITH row
WHERE row.actus_reus IS NOT NULL AND row.actus_reus <> ''
MATCH (o:Offence {offence_id: row.offence_type})
WITH o, row, split(row.actus_reus, '|') AS actus_reus_list
UNWIND actus_reus_list AS actus_reus_item
WITH o, row, trim(actus_reus_item) AS actus_reus_name
WHERE actus_reus_name <> ''
MERGE (ar:ActusReus:LegalElement {name: actus_reus_name})
ON CREATE SET ar.type = 'actus_reus'
MERGE (o)-[:REQUIRES_ACTUS_REUS]->(ar);

// STEP 7: Create Circumstance elements for new sections
LOAD CSV WITH HEADERS FROM 'file:///bns_22_new_sections.csv' AS row
WITH row
WHERE row.circumstances IS NOT NULL AND row.circumstances <> ''
MATCH (o:Offence {offence_id: row.offence_type})
WITH o, row, split(row.circumstances, '|') AS circumstances_list
UNWIND circumstances_list AS circumstance_item
WITH o, row, trim(circumstance_item) AS circumstance_name
WHERE circumstance_name <> ''
MERGE (circ:Circumstance:LegalElement {name: circumstance_name})
ON CREATE SET circ.type = 'circumstance'
MERGE (o)-[:REQUIRES_CIRCUMSTANCE]->(circ);

// STEP 8: Create ActionPattern nodes for new sections
LOAD CSV WITH HEADERS FROM 'file:///bns_22_new_sections.csv' AS row
WITH row
WHERE row.basic_keywords IS NOT NULL AND row.basic_keywords <> ''
MATCH (o:Offence {offence_id: row.offence_type})
WITH o, row, split(row.basic_keywords, '|') AS keyword_list
UNWIND keyword_list AS keyword
WITH o, trim(keyword) AS keyword_text, row.s_section_number AS section_num, row.offence_type AS offence_type
WHERE keyword_text <> ''
MERGE (ap:ActionPattern {text: keyword_text})
ON CREATE SET
    ap.canonical = offence_type,
    ap.created = datetime()
MERGE (ap)-[:MATCHES]->(o);

// STEP 9: Create AGGRAVATED_FORM_OF relationships for new sections
// BNS-305 (dwelling theft) is aggravated form of BNS-303 (basic theft)
MATCH (basic:Section {section_id: 'BNS-303'})
MATCH (aggravated:Section {section_id: 'BNS-305'})
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(basic);

// BNS-307 (theft with preparation for violence) is aggravated form of BNS-303
MATCH (basic:Section {section_id: 'BNS-303'})
MATCH (aggravated:Section {section_id: 'BNS-307'})
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(basic);

// BNS-309 (robbery) is aggravated form of BNS-303 (theft)
MATCH (basic:Section {section_id: 'BNS-303'})
MATCH (aggravated:Section {section_id: 'BNS-309'})
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(basic);

// BNS-310-314 (robbery variants) are aggravated forms of BNS-309 (basic robbery)
MATCH (basic:Section {section_id: 'BNS-309'})
MATCH (aggravated:Section)
WHERE aggravated.section_id IN ['BNS-310', 'BNS-311', 'BNS-312', 'BNS-313', 'BNS-314']
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(basic);

// BNS-317 (breach of trust by public servant) is aggravated form of BNS-316 (basic breach of trust)
MATCH (basic:Section {section_id: 'BNS-316'})
MATCH (aggravated:Section {section_id: 'BNS-317'})
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(basic);

// BNS-330-334 (trespass variants) are aggravated forms of BNS-329 (basic criminal trespass)
MATCH (basic:Section {section_id: 'BNS-329'})
MATCH (aggravated:Section)
WHERE aggravated.section_id IN ['BNS-330', 'BNS-331', 'BNS-332', 'BNS-333', 'BNS-334']
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(basic);

// BNS-325-328 (mischief variants) are aggravated forms of BNS-324 (basic mischief)
MATCH (basic:Section {section_id: 'BNS-324'})
MATCH (aggravated:Section)
WHERE aggravated.section_id IN ['BNS-325', 'BNS-326', 'BNS-327', 'BNS-328']
MERGE (aggravated)-[:AGGRAVATED_FORM_OF]->(basic);

// ============================================
// VERIFICATION QUERIES
// ============================================

// Count total sections (should be 32 now)
MATCH (s:Section)
RETURN count(s) as total_sections;

// Count by section number range
MATCH (s:Section)
WHERE s.section_number >= 303 AND s.section_number <= 334
RETURN count(s) as sections_in_range;

// List all sections
MATCH (s:Section)
RETURN s.section_id, s.section_number, s.title
ORDER BY s.section_number;

// Count relationships
MATCH ()-[r]->()
RETURN type(r) as relationship_type, count(r) as count
ORDER BY count DESC;

// Verify new sections have all elements
MATCH (s:Section)
WHERE s.section_number IN [307, 310, 311, 312, 313, 314, 315, 317, 319, 320, 321, 322, 323, 325, 326, 327, 328, 330, 331, 332, 333, 334]
OPTIONAL MATCH (s)-[:DEFINES]->(o:Offence)
OPTIONAL MATCH (o)-[:REQUIRES_MENS_REA]->(mr:MensRea)
OPTIONAL MATCH (o)-[:REQUIRES_ACTUS_REUS]->(ar:ActusReus)
OPTIONAL MATCH (ap:ActionPattern)-[:MATCHES]->(o)
RETURN s.section_id, s.section_number, s.title,
       count(DISTINCT mr) as mens_rea_count,
       count(DISTINCT ar) as actus_reus_count,
       count(DISTINCT ap) as action_pattern_count
ORDER BY s.section_number;
