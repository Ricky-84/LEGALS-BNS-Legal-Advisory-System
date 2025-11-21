// ==================================================================
// LEGALS Neo4j Knowledge Graph Import Script
// ==================================================================
// This script imports BNS (Bharatiya Nyaya Sanhita) Chapter XVII
// legal data into Neo4j knowledge graph
//
// Prerequisites:
// 1. Neo4j database 'legalknowledge' must be created
// 2. CSV file 'bns_ch17_final_cleaned.csv' must be in Neo4j import folder
// 3. Switch to legalknowledge database: :use legalknowledge
// ==================================================================

// ------------------------------------------------------------------
// STEP 1: Import Legal Data from CSV
// ------------------------------------------------------------------
// This creates Chapter, Section, Offence, and Punishment nodes
// with proper relationships

LOAD CSV WITH HEADERS FROM 'file:///bns_ch17_final_cleaned.csv' AS row
WITH row
WHERE row.s_section_number IS NOT NULL AND trim(row.s_section_number) <> ""

// Create Chapter node
MERGE (c:Chapter {
    number: "XVII",
    title: "Of Offences Against Property"
})

// Create Section nodes
MERGE (s:Section {
    section_id: "BNS-" + row.s_section_number,
    section_number: toInteger(row.s_section_number),
    title: row.s_section_title,
    text: row.s_section_text
})

// Create Offence nodes with proper type mapping
MERGE (o:Offence {
    section_id: "BNS-" + row.s_section_number,
    type: CASE toInteger(row.s_section_number)
        WHEN 303 THEN 'theft'
        WHEN 304 THEN 'snatching'
        WHEN 305 THEN 'dwelling_theft'
        WHEN 306 THEN 'employee_theft'
        WHEN 307 THEN 'prepared_theft'
        WHEN 308 THEN 'extortion'
        WHEN 309 THEN 'robbery'
        WHEN 310 THEN 'dacoity'
        WHEN 311 THEN 'armed_robbery'
        WHEN 316 THEN 'breach_of_trust'
        WHEN 318 THEN 'cheating'
        WHEN 324 THEN 'mischief'
        WHEN 329 THEN 'criminal_trespass'
        ELSE 'other'
    END,
    section_number: toInteger(row.s_section_number)
})

// Create Punishment nodes
MERGE (p:Punishment {
    punishment_id: 'PUN_' + row.s_section_number,
    section_id: "BNS-" + row.s_section_number,
    description: row.punishment,
    punishment_type: 'imprisonment_and_fine'
})

// Create relationships
MERGE (c)-[:CONTAINS]->(s)
MERGE (s)-[:DEFINES]->(o)

RETURN
    count(DISTINCT c) as chapters_created,
    count(DISTINCT s) as sections_created,
    count(DISTINCT o) as offences_created,
    count(DISTINCT p) as punishments_created;

// Expected Results:
// - chapters_created: 1
// - sections_created: 32
// - offences_created: 32
// - punishments_created: 32


// ------------------------------------------------------------------
// STEP 2: Verify Import - Check Specific Section
// ------------------------------------------------------------------
// Verify Section 303 (Theft) was imported correctly

MATCH (s:Section)-[:DEFINES]->(o:Offence)
MATCH (p:Punishment)
WHERE s.section_number = 303 AND p.section_id = s.section_id
RETURN
    s.section_id as section_id,
    s.title as section_title,
    o.type as offence_type,
    p.description as punishment
LIMIT 1;

// Expected: Should return data for BNS-303 (Theft)


// ------------------------------------------------------------------
// STEP 3: Count All Nodes (Verification)
// ------------------------------------------------------------------
// Check total counts of each node type

MATCH (c:Chapter) RETURN 'Chapters' as type, count(c) as count
UNION
MATCH (s:Section) RETURN 'Sections' as type, count(s) as count
UNION
MATCH (o:Offence) RETURN 'Offences' as type, count(o) as count
UNION
MATCH (p:Punishment) RETURN 'Punishments' as type, count(p) as count;


// ------------------------------------------------------------------
// STEP 4: View Sample Graph Structure
// ------------------------------------------------------------------
// Visualize a sample of the knowledge graph

MATCH path = (c:Chapter)-[:CONTAINS]->(s:Section)-[:DEFINES]->(o:Offence)
MATCH (p:Punishment)
WHERE s.section_number = 303 AND p.section_id = s.section_id
RETURN path, p
LIMIT 1;


// ------------------------------------------------------------------
// STEP 5: List All Sections (Optional)
// ------------------------------------------------------------------
// View all imported BNS sections

MATCH (s:Section)
RETURN s.section_number, s.title
ORDER BY s.section_number;


// ------------------------------------------------------------------
// STEP 6: Clear Database (Use with caution!)
// ------------------------------------------------------------------
// UNCOMMENT ONLY IF YOU WANT TO DELETE ALL DATA AND START OVER

// MATCH (n) DETACH DELETE n;


// ==================================================================
// Troubleshooting
// ==================================================================
//
// If import fails:
// 1. Ensure you're in 'legalknowledge' database: :use legalknowledge
// 2. Check CSV file is in Neo4j import folder
// 3. Verify CSV filename matches: bns_ch17_final_cleaned.csv
// 4. Check Neo4j Desktop → Database → Three dots → Open Folder → Import
//
// If nodes are created but properties are missing:
// 1. Delete all and re-run: MATCH (n) DETACH DELETE n;
// 2. Check CSV column headers match: s_section_number, s_section_title, etc.
//
// ==================================================================
