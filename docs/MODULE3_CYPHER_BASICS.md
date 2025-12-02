# Cypher Query Language - Quick Guide

## Basic Patterns

### 1. MATCH - Find nodes
```cypher
// Find all sections
MATCH (s:Section)
RETURN s
LIMIT 5

// Find a specific section
MATCH (s:Section {section_number: 303})
RETURN s.title, s.text
```

### 2. MATCH with Relationships
```cypher
// Find all offences defined by sections
MATCH (s:Section)-[:DEFINES]->(o:Offence)
RETURN s.section_id, o.type
LIMIT 10

// Find punishment for theft
MATCH (s:Section)-[:DEFINES]->(o:Offence {type: 'theft'})
MATCH (p:Punishment {section_id: s.section_id})
RETURN s.section_id, s.title, p.description
```

### 3. WHERE - Filter results
```cypher
// Find all theft-related offences
MATCH (o:Offence)
WHERE o.type CONTAINS 'theft'
RETURN o.section_id, o.type

// Find sections with number > 310
MATCH (s:Section)
WHERE s.section_number > 310
RETURN s.section_number, s.title
ORDER BY s.section_number
```

### 4. CREATE vs MERGE
```cypher
// CREATE - Always creates new (can create duplicates)
CREATE (s:Section {section_id: "BNS-999"})

// MERGE - Create only if doesn't exist (prevents duplicates)
MERGE (s:Section {section_id: "BNS-999"})
```

### 5. Count and Aggregate
```cypher
// Count total sections
MATCH (s:Section)
RETURN count(s) as total_sections

// Count offences by type
MATCH (o:Offence)
RETURN o.type, count(o) as count
ORDER BY count DESC
```

---

## Real Queries from Your Project

### Query 1: Find all property-related laws
```cypher
MATCH (c:Chapter {number: "XVII"})-[:CONTAINS]->(s:Section)
RETURN s.section_number, s.title
ORDER BY s.section_number
```

### Query 2: Get theft details with punishment
```cypher
MATCH (s:Section {section_number: 303})-[:DEFINES]->(o:Offence)
MATCH (p:Punishment {section_id: s.section_id})
RETURN s.title, o.type, p.description
```

### Query 3: Find all robbery-type offences
```cypher
MATCH (o:Offence)
WHERE o.type CONTAINS 'robbery'
RETURN o.section_id, o.type
```

---

## Practice Exercises

Try these queries in Neo4j Browser (http://localhost:7474):

1. **Easy**: Find all sections in Chapter XVII
```cypher
MATCH (c:Chapter)-[:CONTAINS]->(s:Section)
RETURN s.section_number, s.title
LIMIT 10
```

2. **Medium**: Find all offences and their punishments
```cypher
MATCH (s:Section)-[:DEFINES]->(o:Offence)
MATCH (p:Punishment {section_id: s.section_id})
RETURN s.section_number, o.type, p.description
LIMIT 5
```

3. **Hard**: Find sections related to "employee" or "dwelling"
```cypher
MATCH (o:Offence)
WHERE o.type CONTAINS 'employee' OR o.type CONTAINS 'dwelling'
MATCH (s:Section)-[:DEFINES]->(o)
RETURN s.section_number, s.title, o.type
```

---

## Cypher Cheat Sheet

| Operation | Syntax | Example |
|-----------|--------|---------|
| Find nodes | `MATCH (n:Label)` | `MATCH (s:Section)` |
| Filter | `WHERE` | `WHERE s.number > 300` |
| Return results | `RETURN` | `RETURN s.title` |
| Create node | `CREATE (n:Label {prop: value})` | `CREATE (s:Section {id: 1})` |
| Create if not exists | `MERGE` | `MERGE (s:Section {id: 1})` |
| Create relationship | `MERGE (a)-[:REL]->(b)` | `MERGE (c)-[:CONTAINS]->(s)` |
| Limit results | `LIMIT n` | `LIMIT 10` |
| Sort | `ORDER BY` | `ORDER BY s.number` |
| Count | `count()` | `RETURN count(s)` |

---

## Common Patterns

### Pattern 1: Two-hop relationship
```cypher
// Chapter → Section → Offence
MATCH (c:Chapter)-[:CONTAINS]->(s:Section)-[:DEFINES]->(o:Offence)
RETURN c.number, s.section_number, o.type
```

### Pattern 2: Multiple conditions
```cypher
MATCH (s:Section)
WHERE s.section_number >= 303 AND s.section_number <= 310
RETURN s.section_number, s.title
```

### Pattern 3: Optional match (like LEFT JOIN)
```cypher
MATCH (s:Section)
OPTIONAL MATCH (s)-[:DEFINES]->(o:Offence)
RETURN s.section_id, o.type
```

---

## Next Steps

1. Open Neo4j Browser: http://localhost:7474
2. Switch to database: `:use legalknowledge`
3. Try the practice queries above
4. Experiment with your own queries!

**Remember:**
- `MATCH` = Find/Search
- `WHERE` = Filter
- `RETURN` = Show results
- `MERGE` = Create if not exists
- `CREATE` = Always create new
