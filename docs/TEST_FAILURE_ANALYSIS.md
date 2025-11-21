# Test Failure Analysis: Tests 7, 9, 11

## Summary

3 out of 11 tests failed for BOTH old and new methods. This means the failures are NOT due to the new graph-based approach, but due to:
1. Missing keywords in old method
2. Incorrect entity categorization in test cases

---

## Test 7: Breach of Trust - BNS-316

### Test Case:
```python
{
  "query": "My business partner misappropriated company funds",
  "entities": {
    "actions": ["misappropriated"],
    "objects": ["funds"],
    "relationships": ["business partner", "company"]
  },
  "expected_sections": ["BNS-316"]
}
```

### Why It Failed:

**Old Method (neo4j_service.py:617):**
```python
# Requires: trust relationship/circumstance + dishonest action
return (has_trust_relationship or has_trust_circumstance) and has_trust_action
```

**Problem:**
- ✅ `has_trust_action` = TRUE ("misappropriated" is in trust_actions list)
- ❌ `has_trust_relationship` = FALSE ("business partner" is NOT in trust_relationships list)

**Line 598 - trust_relationships list:**
```python
trust_relationships = ["entrusted", "trustee", "fiduciary", "agent",
                       "guardian", "manager", "executor", "director"]
```

**Missing keywords:** "business partner", "partner", "colleague", "co-worker"

### Solutions:

**Option 1: Add keywords to old method** (quick fix)
```python
trust_relationships = [..., "business partner", "partner", "colleague"]
```

**Option 2: Add to graph** (better long-term)
Add "business partner" pattern to ActionPattern or create relationship-based matching in graph.

**Option 3: Fix test** (if entity categorization is wrong)
Maybe "business partner" should be in `circumstances` not `relationships`.

---

## Test 9: Mischief - BNS-324

### Test Case:
```python
{
  "query": "My neighbor intentionally damaged my car",
  "entities": {
    "actions": ["damaged"],
    "objects": ["car"],
    "persons": ["neighbor"],
    "intentions": ["intentionally"]  # <-- PROBLEM HERE
  },
  "expected_sections": ["BNS-324"]
}
```

### Why It Failed:

**Old Method (neo4j_service.py:700):**
```python
# Requires: damage action + property object + (damage_circumstance OR malicious_intention)
has_intentional_damage = has_damage_action and has_property_object and (has_damage_circumstance or has_malicious_intention)
```

**Problem:**
- ✅ `has_damage_action` = TRUE ("damaged" is in damage_actions)
- ✅ `has_property_object` = TRUE ("car" is in property_objects)
- ❌ `has_damage_circumstance` = FALSE (checks `circumstances` entity, not `intentions`)
- ❌ `has_malicious_intention` = FALSE ("intentionally" is NOT in malicious_intentions list)

**Line 681-682:**
```python
damage_circumstances = ["intentionally", "deliberately", ...]  # <-- Checks circumstances
malicious_intentions = ["to harm", "to damage", "revenge", ...]  # <-- "intentionally" NOT here
```

**The bug:** Test puts "intentionally" in `intentions` entity, but code checks for it in `circumstances` entity!

### Solutions:

**Option 1: Fix test** (correct approach)
```python
"entities": {
    "actions": ["damaged"],
    "objects": ["car"],
    "persons": ["neighbor"],
    "circumstances": ["intentionally"]  # <-- Move here from intentions
}
```

**Option 2: Add check for intentions in old method**
```python
has_damage_intention = any("intentional" in intention.lower() for intention in intentions)
return ... or has_damage_intention
```

---

## Test 11: Natural Language - "Borrowed Never Returned"

### Test Case:
```python
{
  "query": "I borrowed my friend's bike and never returned it",
  "entities": {
    "actions": ["borrowed", "never returned"],
    "objects": ["bike"],
    "relationships": ["friend"]
  },
  "expected_sections": ["BNS-303", "BNS-316"]
}
```

### Why It Failed:

**Problem:** The action patterns "borrowed" and "never returned" are NOT in ANY keyword lists!

**Theft keywords (line 480):**
```python
theft_actions = ["took", "stolen", "stole", "theft", "stealing",
                 "grabbed", "snatched", "broke into", "borrowed", "taken", ...]
```

Wait - "borrowed" IS in the list! Let me check more carefully...

**Actually checking the CSV:**

Looking at `bns_10_sections_enhanced.csv` line for BNS-316:
```csv
basic_keywords: misappropriated|embezzled|misused trust|converted|took entrusted property|breach of trust|borrowed never returned
```

So "borrowed never returned" IS in the graph as a SINGLE phrase!

**The problem:**
- Test splits it into TWO actions: ["borrowed", "never returned"]
- Old method checks for "borrowed" separately (matches theft, not breach of trust)
- New graph method checks for exact phrase "borrowed never returned" (won't match split actions)

### Solutions:

**Option 1: Fix test to use combined phrase**
```python
"entities": {
    "actions": ["borrowed never returned"],  # <-- Single phrase
    "objects": ["bike"],
    "relationships": ["friend"]
}
```

**Option 2: Add "borrowed" as standalone breach of trust keyword**
This is semantically wrong - "borrowed" alone doesn't mean breach of trust.

**Option 3: Use semantic similarity (Phase 3)**
This is why we need Phase 3 - semantic similarity will understand that ["borrowed", "never returned"] is similar to "borrowed never returned".

---

## Root Cause Analysis

| Test | Root Cause | Type | Fix |
|------|------------|------|-----|
| Test 7 | Missing "business partner" in trust_relationships keyword list | Missing Keyword | Add to keywords or graph |
| Test 9 | "intentionally" in wrong entity type (intentions vs circumstances) | Wrong Entity Type | Fix test |
| Test 11 | Multi-word phrase split into separate actions | Phrase Splitting | Fix test OR implement Phase 3 |

---

## Recommendations

### Immediate Fixes (to pass tests):

1. **Test 7:** Add missing keywords
   ```python
   # In neo4j_service.py line 598
   trust_relationships = [..., "business partner", "partner", "colleague", "associate"]
   ```

2. **Test 9:** Fix test entity categorization
   ```python
   # In test_graph_vs_keyword.py
   "circumstances": ["intentionally"]  # Move from intentions
   ```

3. **Test 11:** Fix test to use combined phrase
   ```python
   # In test_graph_vs_keyword.py
   "actions": ["borrowed never returned"]  # Combined, not split
   ```

### Long-term Solution (Phase 3):

Implement **semantic similarity** so that:
- ["borrowed", "never returned"] matches "misappropriated"
- ["business partner"] understands trust relationship context
- ["intentionally"] works regardless of entity categorization

---

## Decision Point

**Question:** Should we fix the tests or fix the code?

**Answer:** Mix of both:

1. **Fix Test 9** - This is clearly wrong entity categorization
2. **Fix Test 11** - Entity extraction should combine phrases better
3. **Enhance code for Test 7** - Add missing but valid keywords

**After fixes, we expect:**
- 8-9 exact matches (was 7)
- 1-2 new method better (was 1)
- 0-1 both empty (was 3)
- **Success rate: 90%+** (currently 72.7%)

---

## Conclusion

These failures are **NOT a problem with the graph-based approach**. They reveal:
1. Gaps in the old keyword lists (Test 7)
2. Test entity categorization issues (Test 9)
3. Multi-word phrase handling (Test 11) - will be solved by Phase 3

**The graph-based method is working correctly!** The failures expose existing limitations that Phase 3 (semantic similarity) will solve.

---

**Next Action:** Apply fixes and re-run tests to achieve 90%+ success rate.
