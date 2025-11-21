# Phase 2: Replace Python Keyword Matching with Cypher Graph Queries

## 📋 Pre-Execution Review (Complete)

### ✅ Phase 1 Verification

**Neo4j Graph Status:**
- ✅ Database: `legalknowledge`
- ✅ Nodes: 159 total
  - Chapter: 1
  - Section: 10
  - Offence: 10
  - ActionPattern: 73
  - LegalElement: 55 (ActusReus: 20, Circumstance: 26, MensRea: 9)
  - Punishment: 10
- ✅ Relationships: 176 total
- ✅ CSV imported successfully
- ✅ Graph visualized and verified

**Current Code Status:**
- ✅ File: `backend/app/services/neo4j_service.py` (707 lines)
- ✅ Contains 10 hardcoded `_has_*_elements()` methods
- ✅ Each method has keyword lists (150+ lines of Python logic)
- ✅ Git commit: `9decfdd` (Phase 1 checkpoint created)

---

## 🎯 Phase 2 Objective

**Replace this:**
```python
# 200+ lines of hardcoded Python
def _has_theft_elements(self, entities):
    theft_actions = ["took", "stolen", "stole", ...]  # Hardcoded
    if any(action in theft_actions for action in actions):
        return True
```

**With this:**
```python
# Single Cypher query using graph
def find_applicable_laws_v2(self, entities):
    result = session.run("""
        MATCH (pattern:ActionPattern)
        WHERE pattern.text IN $user_actions
        MATCH (pattern)-[:MATCHES]->(offence:Offence)
        MATCH (section:Section)-[:DEFINES]->(offence)
        RETURN section, offence
    """, user_actions=entities['actions'])
```

**Benefits:**
- ❌ Remove 200+ lines of hardcoded Python
- ✅ Add new patterns by editing graph, not code
- ✅ Graph explains WHY a law applies
- ✅ Faster and more maintainable

---

## 📊 Current System Analysis

### Current Keyword Matching Methods (10 total):

1. `_has_theft_elements()` - Line 309
2. `_has_dwelling_theft_elements()` - Line 326
3. `_has_employee_theft_elements()` - Line 339
4. `_has_robbery_elements()` - Line 355
5. `_has_snatching_elements()` - Line 373
6. `_has_cheating_elements()` - Line 394
7. `_has_breach_of_trust_elements()` - Line 424
8. `_has_extortion_elements()` - Line 454
9. `_has_trespass_elements()` - Line 480
10. `_has_mischief_elements()` - Line 506

### Example Current Implementation:

```python
def _has_theft_elements(self, entities: Dict[str, List[str]]) -> bool:
    actions = entities.get("actions", [])
    objects = entities.get("objects", [])

    # PROBLEM: Hardcoded lists
    theft_actions = ["took", "stolen", "stole", "theft", "stealing",
                     "grabbed", "snatched", "broke into", "borrowed",
                     "taken", "kept", "appropriated"]
    property_objects = ["phone", "mobile", "iphone", "smartphone",
                        "wallet", "money", "cash", "bag", "purse",
                        "jewelry", "laptop", "computer"]

    # PROBLEM: Python loops for matching
    has_theft_action = any(
        theft_action.lower() in action.lower()
        for action in actions
        for theft_action in theft_actions
    )
    has_property = any(
        prop.lower() in obj.lower()
        for obj in objects
        for prop in property_objects
    )

    return has_theft_action and has_property
```

**Problems:**
- To add "misappropriated" → Must edit Python code
- To add "embezzled" → Must edit Python code and redeploy
- No explanation of WHY it matched
- Duplicate keyword lists across methods

---

## 🔧 Phase 2 Implementation Plan

### Step 1: Create New Graph-Based Method (No Deletion Yet!)

**Strategy:** Add NEW method alongside old ones, test it, THEN delete old methods.

**File:** `backend/app/services/neo4j_service.py`

**Add new method:**
```python
def find_applicable_laws_graph_v2(self, entities: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """
    NEW: Use graph-based reasoning instead of Python keyword matching
    This will REPLACE find_applicable_laws() after testing
    """

    if not self.available or not self.driver:
        return self._fallback_legal_reasoning(entities)

    applicable_laws = []
    user_actions = entities.get("actions", [])
    user_objects = entities.get("objects", [])
    user_locations = entities.get("locations", [])

    try:
        with self.driver.session(database="legalknowledge") as session:
            # Query 1: Match user actions to ActionPatterns
            result = session.run("""
                // Step 1: Find action patterns that match user's actions
                UNWIND $user_actions AS user_action
                MATCH (ap:ActionPattern)
                WHERE toLower(ap.text) CONTAINS toLower(user_action)
                   OR toLower(user_action) CONTAINS toLower(ap.text)

                // Step 2: Find which offences these patterns match
                MATCH (ap)-[:MATCHES]->(offence:Offence)

                // Step 3: Find the section that defines this offence
                MATCH (section:Section)-[:DEFINES]->(offence)

                // Step 4: Get punishment details
                MATCH (section)-[:PRESCRIBES]->(punishment:Punishment)

                // Step 5: Get legal elements required
                OPTIONAL MATCH (offence)-[req:REQUIRES_MENS_REA|REQUIRES_ACTUS_REUS|REQUIRES_CIRCUMSTANCE]->(element:LegalElement)

                // Step 6: Calculate confidence based on matches
                WITH section, offence, punishment,
                     collect(DISTINCT element.element_id) as matched_elements,
                     collect(DISTINCT ap.text) as matched_patterns,
                     count(DISTINCT ap) as pattern_matches

                // Step 7: Return results with reasoning
                RETURN DISTINCT
                    section.section_id as section,
                    section.title as title,
                    section.text as description,
                    punishment.description as punishment,
                    offence.offence_type as offence_type,
                    matched_patterns as patterns_matched,
                    matched_elements as legal_elements,
                    pattern_matches as confidence_score

                ORDER BY confidence_score DESC
                LIMIT 10
            """,
                user_actions=user_actions
            )

            for record in result:
                # Calculate confidence (0.0 to 1.0)
                base_confidence = min(0.5 + (record["confidence_score"] * 0.1), 1.0)

                applicable_laws.append({
                    "section": record["section"],
                    "title": record["title"],
                    "description": record["description"],
                    "punishment": record["punishment"],
                    "offence_type": record["offence_type"],
                    "confidence": base_confidence,
                    "reasoning": f"Matched patterns: {', '.join(record['patterns_matched'][:3])}",
                    "matched_patterns": record["patterns_matched"],
                    "legal_elements": record["legal_elements"],
                    "graph_based": True  # Mark as graph-based result
                })

    except Exception as e:
        logger.error(f"Graph query failed: {e}")
        # Fallback to old method if graph query fails
        return self._fallback_legal_reasoning(entities)

    return applicable_laws
```

---

### Step 2: Add Enhanced Query with Location/Object Context

**Add another query for location-based offences:**

```python
def _query_location_based_offences(self, session, locations: List[str]) -> List[Dict]:
    """Query for location-specific offences (dwelling, trespass)"""

    result = session.run("""
        UNWIND $locations AS user_location

        // Find circumstances that match locations
        MATCH (circ:Circumstance)
        WHERE toLower(circ.name) CONTAINS 'dwelling'
           OR toLower(circ.name) CONTAINS 'house'
           OR toLower(user_location) CONTAINS 'house'
           OR toLower(user_location) CONTAINS 'home'

        // Find offences requiring this circumstance
        MATCH (offence:Offence)-[:REQUIRES_CIRCUMSTANCE]->(circ)
        MATCH (section:Section)-[:DEFINES]->(offence)
        MATCH (section)-[:PRESCRIBES]->(punishment:Punishment)

        RETURN DISTINCT
            section.section_id as section,
            section.title as title,
            section.text as description,
            punishment.description as punishment,
            offence.offence_type as offence_type,
            circ.name as circumstance_matched

        LIMIT 5
    """,
        locations=locations
    )

    return [dict(record) for record in result]
```

---

### Step 3: Combine Multiple Query Results

```python
def find_applicable_laws_graph_v2(self, entities: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """Combined graph-based legal reasoning"""

    if not self.available or not self.driver:
        return self._fallback_legal_reasoning(entities)

    all_laws = []

    try:
        with self.driver.session(database="legalknowledge") as session:
            # Query 1: Action-based matching
            if entities.get("actions"):
                action_laws = self._query_action_patterns(session, entities["actions"])
                all_laws.extend(action_laws)

            # Query 2: Location-based matching
            if entities.get("locations"):
                location_laws = self._query_location_based_offences(session, entities["locations"])
                all_laws.extend(location_laws)

            # Query 3: Property value consideration
            if entities.get("objects"):
                property_value = self.property_estimator.estimate_total_value(entities["objects"])
                # Add value to each law for punishment adjustment
                for law in all_laws:
                    law["estimated_property_value"] = property_value

    except Exception as e:
        logger.error(f"Graph query failed: {e}")
        return self._fallback_legal_reasoning(entities)

    # Deduplicate and sort by confidence
    seen_sections = set()
    unique_laws = []
    for law in sorted(all_laws, key=lambda x: x.get("confidence", 0), reverse=True):
        if law["section"] not in seen_sections:
            seen_sections.add(law["section"])
            unique_laws.append(law)

    return unique_laws
```

---

### Step 4: Testing Strategy (CRITICAL!)

**Before deleting old methods:**

1. **Create test script** to compare old vs new:

```python
# backend/test_graph_vs_keyword.py

from app.services.neo4j_service import Neo4jService

service = Neo4jService()

test_queries = [
    {
        "query": "Someone stole my iPhone from my house",
        "entities": {
            "actions": ["stole"],
            "objects": ["iPhone"],
            "locations": ["house"]
        }
    },
    {
        "query": "Employee took company money",
        "entities": {
            "actions": ["took"],
            "objects": ["money"],
            "persons": ["employee"],
            "relationships": ["company"]
        }
    },
    # Add 10+ test cases
]

for test in test_queries:
    print(f"\nQuery: {test['query']}")

    # Old method
    old_results = service.find_applicable_laws(test['entities'])
    print(f"Old method: {[r['section'] for r in old_results]}")

    # New method
    new_results = service.find_applicable_laws_graph_v2(test['entities'])
    print(f"New method: {[r['section'] for r in new_results]}")

    # Compare
    if set([r['section'] for r in old_results]) == set([r['section'] for r in new_results]):
        print("✅ MATCH")
    else:
        print("❌ DIFFERENT - needs investigation")
```

2. **Run comparison** and verify accuracy is same or better

3. **Only then** replace old method with new one

---

### Step 5: Replace Old Method (After Testing!)

**Once testing confirms new method works:**

1. Rename `find_applicable_laws()` → `find_applicable_laws_old()`
2. Rename `find_applicable_laws_graph_v2()` → `find_applicable_laws()`
3. Delete all `_has_*_elements()` methods (10 methods, ~200 lines)
4. Test entire system end-to-end
5. Commit

---

## 📝 Implementation Checklist

### Pre-Implementation:
- [x] Phase 1 completed and committed
- [x] Neo4j graph verified (159 nodes, 176 relationships)
- [x] Current code analyzed (10 methods to replace)
- [ ] Create Phase 2 branch: `git checkout -b phase2-cypher-rules`

### Implementation:
- [ ] Add new `find_applicable_laws_graph_v2()` method
- [ ] Add helper query methods (`_query_action_patterns()`, etc.)
- [ ] Create comparison test script
- [ ] Run tests with 10+ scenarios
- [ ] Verify accuracy matches or improves
- [ ] Replace old method with new
- [ ] Delete old `_has_*_elements()` methods
- [ ] Update method documentation

### Testing:
- [ ] Test with existing test files (test_theft.py, test_robbery.py, etc.)
- [ ] Test with natural language variations
- [ ] Verify Neo4j fallback still works
- [ ] Check performance (should be faster)
- [ ] Verify reasoning explanation works

### Finalization:
- [ ] Run all existing tests: `pytest backend/tests/`
- [ ] Manual testing via frontend
- [ ] Code cleanup and comments
- [ ] Git commit with detailed message
- [ ] Merge to main if successful

---

## 🎯 Success Criteria

**Phase 2 is complete when:**

1. ✅ Graph-based method returns same or better results than keyword matching
2. ✅ All 10 `_has_*_elements()` methods deleted (~200 lines removed)
3. ✅ Single `find_applicable_laws()` method using Cypher queries
4. ✅ All existing tests still pass
5. ✅ Graph provides reasoning (shows which patterns matched)
6. ✅ Can add new patterns by editing graph, not code

---

## ⚠️ Risk Mitigation

**What if new method doesn't work well?**

1. We created Phase 1 Git checkpoint (`9decfdd`)
2. We're working on a branch (`phase2-cypher-rules`)
3. We keep old methods until testing passes
4. We can always revert: `git checkout main`

**Fallback Plan:**
- If graph queries fail → Fall back to old keyword matching
- If accuracy drops → Keep both methods, improve graph
- If performance issues → Optimize Cypher queries, add indexes

---

## 📊 Expected Improvements

**Lines of Code:**
- Before: 707 lines (200+ in keyword matching)
- After: ~500 lines (200+ lines deleted)

**Maintainability:**
- Before: Edit Python code to add patterns
- After: Edit Neo4j graph data

**Performance:**
- Before: Python loops through lists
- After: Neo4j indexed graph queries (faster)

**Explainability:**
- Before: No reasoning ("Theft detected")
- After: "Matched patterns: stole, took from house"

---

## 🚀 Ready to Execute?

**Current Status:**
- ✅ Phase 1 complete and committed
- ✅ Neo4j graph ready
- ✅ Plan reviewed and documented
- ⏳ Awaiting confirmation to proceed

**Next Action:** Create Phase 2 branch and begin implementation

---

**Last Updated:** 2025-01-09
**Checkpoint:** Commit `9decfdd` (Phase 1)
**Next:** Phase 2 Implementation
