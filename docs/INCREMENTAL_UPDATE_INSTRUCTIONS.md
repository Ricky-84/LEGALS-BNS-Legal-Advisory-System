# Incremental Graph Update Instructions

**Goal:** Add 22 new BNS sections to your existing 10-section graph

**Method:** Incremental update (keeps existing data, adds new sections)

---

## Files Created

1. ✅ `bns_22_new_sections.csv` - Only the 22 new sections
2. ✅ `neo4j_import_22_new_sections.cypher` - Import script for new sections
3. ✅ `bns_32_sections_enhanced.csv` - Complete 32 sections (for future reference)

---

## Steps to Update Graph

### Step 1: Place CSV in Neo4j Import Folder

Copy the CSV file to your Neo4j import directory:

```bash
# Copy to Neo4j import folder
# Default location: C:\Users\<YourUser>\.Neo4jDesktop\relate-data\dbmss\<db-id>\import\

# Or find it via Neo4j Desktop:
# - Open your database
# - Click the three dots (...)
# - Select "Open folder"
# - Navigate to "import" folder
# - Copy bns_22_new_sections.csv here
```

**File to copy:**
```
bns_22_new_sections.csv
```

### Step 2: Open Neo4j Browser

1. Start your Neo4j database
2. Open Neo4j Browser: http://localhost:7474
3. Login with your credentials

### Step 3: Run the Import Script

Open the file `neo4j_import_22_new_sections.cypher` and copy-paste the queries into Neo4j Browser.

**OR** run it in sections:

#### Section 1: Import Sections (STEP 1-4)
```cypher
// Paste STEP 1-4 from neo4j_import_22_new_sections.cypher
```

Wait for completion, then check:
```cypher
MATCH (s:Section)
RETURN count(s) as total_sections;
// Should show: 32 sections (10 old + 22 new)
```

#### Section 2: Import Legal Elements (STEP 5-8)
```cypher
// Paste STEP 5-8 from neo4j_import_22_new_sections.cypher
```

#### Section 3: Create Relationships (STEP 9)
```cypher
// Paste STEP 9 from neo4j_import_22_new_sections.cypher
```

#### Section 4: Verify (VERIFICATION QUERIES)
```cypher
// Run verification queries to confirm all data imported correctly
```

---

## Expected Results

### Before Update:
- Sections: 10 (303, 304, 305, 306, 308, 309, 316, 318, 324, 329)
- Nodes: ~159
- Relationships: ~176

### After Update:
- Sections: 32 (303-334, complete Chapter XVII)
- Nodes: ~350+ (estimated)
- Relationships: ~400+ (estimated)

---

## Verification

Run these queries to verify the update:

### 1. Count Total Sections
```cypher
MATCH (s:Section)
RETURN count(s) as total_sections;
```
**Expected:** 32

### 2. List All Sections
```cypher
MATCH (s:Section)
RETURN s.section_id, s.section_number, s.title
ORDER BY s.section_number;
```
**Expected:** Sections 303-334 listed

### 3. Check New Sections Have Elements
```cypher
MATCH (s:Section)
WHERE s.section_number IN [307, 310, 311, 315, 317, 319, 320, 330, 333]
OPTIONAL MATCH (s)-[:DEFINES]->(o:Offence)
OPTIONAL MATCH (o)-[:REQUIRES_MENS_REA]->(mr)
OPTIONAL MATCH (o)-[:REQUIRES_ACTUS_REUS]->(ar)
OPTIONAL MATCH (ap:ActionPattern)-[:MATCHES]->(o)
RETURN s.section_id, s.title,
       count(DISTINCT mr) as mens_rea,
       count(DISTINCT ar) as actus_reus,
       count(DISTINCT ap) as action_patterns;
```
**Expected:** Each section should have mens_rea, actus_reus, and action_patterns > 0

### 4. Test with Sample Query
```cypher
// Test: Find sections for "dacoity"
MATCH (ap:ActionPattern)
WHERE toLower(ap.text) CONTAINS 'dacoity'
MATCH (ap)-[:MATCHES]->(o:Offence)
MATCH (s:Section)-[:DEFINES]->(o)
RETURN s.section_id, s.title;
```
**Expected:** Should return BNS-313 (Dacoity)

---

## Rollback (If Needed)

If something goes wrong, you can remove only the new sections:

```cypher
// Delete new sections and their connections
MATCH (s:Section)
WHERE s.section_number IN [307, 310, 311, 312, 313, 314, 315, 317, 319, 320, 321, 322, 323, 325, 326, 327, 328, 330, 331, 332, 333, 334]
DETACH DELETE s;

// Clean up orphaned nodes
MATCH (n)
WHERE NOT (n)--()
DELETE n;
```

Then you're back to your original 10 sections.

---

## Alternative: Full Recreate (If Preferred)

If you prefer to delete everything and start fresh:

### Step 1: Backup Query Results
```cypher
// Export your current graph structure if needed
MATCH (n)
OPTIONAL MATCH (n)-[r]->()
RETURN n, r;
```

### Step 2: Delete All
```cypher
// Delete everything
MATCH (n)
DETACH DELETE n;
```

### Step 3: Import All 32 Sections
Use `neo4j_import_enhanced.cypher` (from Phase 1) but with the new CSV:
- Replace CSV filename in script: `bns_10_sections_enhanced.csv` → `bns_32_sections_enhanced.csv`
- Run the complete import script

---

## Troubleshooting

### Issue: "Couldn't load the external resource"
**Solution:**
- Make sure CSV is in Neo4j import folder
- File name matches exactly: `bns_22_new_sections.csv`
- No typos in path

### Issue: "Neo4j.ClientError.Statement.SyntaxError"
**Solution:**
- Copy-paste queries carefully
- Run in sections (STEP 1-4, then STEP 5-8, etc.)
- Check for missing semicolons

### Issue: Duplicate nodes created
**Solution:**
- Script uses MERGE (not CREATE), so duplicates shouldn't happen
- If duplicates appear, check `section_id` format (should be 'BNS-XXX')

---

## Recommendation

✅ **Use Incremental Update** - Safer, keeps existing data

❌ **Avoid Full Delete** - Unless you have issues with existing graph

---

**Status:** Ready to execute
**Risk:** Low (incremental, can rollback)
**Time:** 2-3 minutes to run all imports
