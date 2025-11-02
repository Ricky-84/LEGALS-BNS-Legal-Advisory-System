# LEGALS Neo4j Setup Guide

## 1. Install Neo4j Python Driver

```bash
pip install neo4j
```

## 2. Set Neo4j Connection Details

### Option A: Environment Variables
```bash
set NEO4J_URI=bolt://localhost:7687
set NEO4J_USER=neo4j
set NEO4J_PASSWORD=your_password
```

### Option B: Update config.py directly
Edit `app/core/config.py`:
```python
NEO4J_URI: str = "bolt://localhost:7687"
NEO4J_USER: str = "neo4j"
NEO4J_PASSWORD: str = "your_actual_password"
```

## 3. Verify Neo4j Desktop is Running

1. Open Neo4j Desktop
2. Start your database instance
3. Verify connection at `neo4j://127.0.0.1:7687`

## 4. Test the Integration

```bash
cd backend
python test_neo4j_only.py
```

## Expected Output

```
LEGALS Neo4j Backend Test (No SLM)
==================================================

Running: Neo4j Connection
Testing Neo4j Connection...
SUCCESS: Connected! Chapters: ['Of Offences Against Property']

Running: Sample Legal Scenarios
Testing Sample Legal Scenarios...

--- Scenario 1: Basic Theft Case ---
Description: Simple theft of iPhone from someone's house
RESULTS:
   Found 2 applicable laws
   Overall confidence: 0.90

   SECTION: BNS-303: Theft
      Confidence: 0.8
      Reasoning: Basic theft elements detected
      Offence Type: theft_related
      PROPERTY ANALYSIS:
         [HIGH] iPhone: Rs.50,000
      PUNISHMENT MODIFICATION:
         Threshold: Rs.5,000 BNS-303 threshold
         Modified: Community service (if first-time offender and property value < Rs.5,000)
```

## Troubleshooting

1. **"Neo4j not available"** - Install driver: `pip install neo4j`
2. **Connection failed** - Check Neo4j Desktop is running and credentials are correct
3. **No data found** - Make sure you imported the BNS knowledge graph using the import scripts