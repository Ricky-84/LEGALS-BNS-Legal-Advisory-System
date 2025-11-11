// ====================================================================
// VERIFICATION QUERIES FOR ENHANCED BNS KNOWLEDGE GRAPH
// ====================================================================

// ====================================================================
// QUERY 1: VIEW ENTIRE GRAPH (ALL NODES AND RELATIONSHIPS)
// ====================================================================
// WARNING: This might be large with 100+ nodes
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 300;


// ====================================================================
// QUERY 2: VIEW COMPLETE STRUCTURE FOR ONE SECTION (BNS-303 THEFT)
// ====================================================================
// This shows everything related to Theft section
MATCH path = (chapter:Chapter)-[:CONTAINS]->(section:Section {section_id: 'BNS-303'})
OPTIONAL MATCH path2 = (section)-[:DEFINES]->(offence:Offence)
OPTIONAL MATCH path3 = (offence)-[:REQUIRES_MENS_REA|REQUIRES_ACTUS_REUS|REQUIRES_CIRCUMSTANCE]->(element:LegalElement)
OPTIONAL MATCH path4 = (pattern:ActionPattern)-[:MATCHES]->(offence)
OPTIONAL MATCH path5 = (section)-[:PRESCRIBES]->(punishment:Punishment)
RETURN chapter, section, offence, element, pattern, punishment;


// ====================================================================
// QUERY 3: VIEW ALL SECTIONS WITH THEIR OFFENCES
// ====================================================================
MATCH (section:Section)-[:DEFINES]->(offence:Offence)
RETURN section, offence
LIMIT 50;


// ====================================================================
// QUERY 4: VIEW ALL LEGAL ELEMENTS GROUPED BY TYPE
// ====================================================================
MATCH (offence:Offence)-[r:REQUIRES_MENS_REA|REQUIRES_ACTUS_REUS|REQUIRES_CIRCUMSTANCE]->(element:LegalElement)
RETURN offence, r, element
LIMIT 100;


// ====================================================================
// QUERY 5: VIEW ALL ACTION PATTERNS AND THEIR OFFENCES
// ====================================================================
MATCH (pattern:ActionPattern)-[:MATCHES]->(offence:Offence)
RETURN pattern, offence
LIMIT 100;


// ====================================================================
// QUERY 6: VIEW HIERARCHICAL RELATIONSHIPS (AGGRAVATED FORMS)
// ====================================================================
MATCH (aggravated:Section)-[:AGGRAVATED_FORM_OF]->(base:Section)
RETURN aggravated, base;


// ====================================================================
// QUERY 7: COUNT ALL NODES BY TYPE
// ====================================================================
MATCH (n)
RETURN labels(n)[0] as NodeType, count(n) as Count
ORDER BY Count DESC;


// ====================================================================
// QUERY 8: COUNT ALL RELATIONSHIPS BY TYPE
// ====================================================================
MATCH ()-[r]->()
RETURN type(r) as RelationshipType, count(r) as Count
ORDER BY Count DESC;


// ====================================================================
// QUERY 9: VIEW SPECIFIC ACTION PATTERNS (NATURAL LANGUAGE)
// ====================================================================
// See what patterns exist for "borrowed never returned"
MATCH (pattern:ActionPattern)
WHERE pattern.text CONTAINS 'borrowed'
RETURN pattern;

// See all "stole" variations
MATCH (pattern:ActionPattern)
WHERE pattern.text CONTAINS 'stole' OR pattern.text CONTAINS 'stolen'
RETURN pattern;


// ====================================================================
// QUERY 10: VIEW COMPLETE PATH FOR A SPECIFIC KEYWORD
// ====================================================================
// Example: Show how "borrowed never returned" maps to a BNS section
MATCH (pattern:ActionPattern {text: 'borrowed never returned'})
      -[:MATCHES]->(offence:Offence)
      <-[:DEFINES]-(section:Section)
RETURN pattern, offence, section;


// ====================================================================
// QUERY 11: VIEW ALL MENS REA ELEMENTS
// ====================================================================
MATCH (element:MensRea)
RETURN element.element_id as MensRea, element.description as Description
ORDER BY element.element_id;


// ====================================================================
// QUERY 12: VIEW ALL ACTUS REUS ELEMENTS
// ====================================================================
MATCH (element:ActusReus)
RETURN element.element_id as ActusReus, element.description as Description
ORDER BY element.element_id;


// ====================================================================
// QUERY 13: VIEW ALL CIRCUMSTANCE ELEMENTS
// ====================================================================
MATCH (element:Circumstance)
RETURN element.element_id as Circumstance, element.description as Description
ORDER BY element.element_id;


// ====================================================================
// QUERY 14: SHOW THEFT-RELATED SECTIONS (BASE + AGGRAVATED)
// ====================================================================
MATCH path = (base:Section {section_id: 'BNS-303'})
             <-[:AGGRAVATED_FORM_OF*0..]-(related:Section)
RETURN path;


// ====================================================================
// QUERY 15: VIEW GRAPH SCHEMA (NODE TYPES AND RELATIONSHIPS)
// ====================================================================
CALL db.schema.visualization();


// ====================================================================
// RECOMMENDED: USE THIS FOR FULL VISUALIZATION
// ====================================================================
// This query shows a balanced view of the entire graph structure
MATCH (chapter:Chapter)-[:CONTAINS]->(section:Section)-[:DEFINES]->(offence:Offence)
OPTIONAL MATCH (offence)-[r:REQUIRES_MENS_REA|REQUIRES_ACTUS_REUS|REQUIRES_CIRCUMSTANCE]->(element:LegalElement)
OPTIONAL MATCH (section)-[:PRESCRIBES]->(punishment:Punishment)
OPTIONAL MATCH (pattern:ActionPattern)-[:MATCHES]->(offence)
WHERE section.section_number IN [303, 304, 305, 316, 318, 329]
RETURN chapter, section, offence, element, pattern, punishment, r
LIMIT 200;
