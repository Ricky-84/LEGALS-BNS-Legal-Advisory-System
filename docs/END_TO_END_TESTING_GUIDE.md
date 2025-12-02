# End-to-End Testing Guide
**Branch**: phase2-cypher-rules
**Date**: 2025-12-02

## Overview

This guide will help you test the complete integration from frontend to backend, including Vaishnav's semantic transformer enhancement.

---

## Prerequisites

### 1. Check Dependencies Installed ✅

The semantic transformer dependencies should already be installed. Verify:

```bash
python -c "from sentence_transformers import SentenceTransformer; print('OK')"
```

If you get an error, run:
```bash
pip install -r requirements-semantic-fixed.txt
```

### 2. Verify Model Downloaded ✅

The sentence transformer model should be downloaded. Test:

```bash
python test_semantic_simple.py
```

Expected output: "ALL TESTS PASSED!"

---

## Testing Levels

### Level 1: Unit Tests (Backend Only)

Test individual components without frontend.

#### Test 1: Semantic Service
```bash
python test_semantic_simple.py
```

**Expected**: All 5 tests pass
- ✅ Module imports
- ✅ Service initialization
- ✅ Semantic matching
- ✅ Action enhancement
- ✅ Full integration

#### Test 2: OllamaService Integration
```bash
python test_ollama_integration.py
```

**Expected**:
- OllamaService has semantic_enhancer
- Test queries return semantic confidence scores
- Crime categories detected correctly

---

### Level 2: Backend API Tests

Test the FastAPI backend endpoints.

#### Step 1: Start Neo4j Database

Make sure Neo4j is running with your BNS data loaded.

```bash
# Check if Neo4j is running
# Usually accessible at http://localhost:7474
```

#### Step 2: Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

#### Step 3: Test Health Endpoint

Open browser or use curl:
```bash
curl http://localhost:8000/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "timestamp": "..."
}
```

#### Step 4: Test Query Endpoint with Semantic Enhancement

Use curl or Postman:

```bash
curl -X POST http://localhost:8000/api/legal-query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"He borrowed my laptop and never returned it\", \"language\": \"en\"}"
```

**What to look for in response**:
1. ✅ `entities_analyzed` - Contains extracted entities
2. ✅ `semantic_enhancements` - Vaishnav's semantic matching results
3. ✅ `semantic_confidence` - Confidence score (should be high for this query)
4. ✅ `applicable_laws` - BNS sections detected
5. ✅ Response time < 2 seconds

**Example successful response**:
```json
{
  "query": "He borrowed my laptop and never returned it",
  "entities_analyzed": {
    "actions": ["borrowed"],
    "objects": ["laptop"],
    "semantic_enhancements": {
      "categories_detected": ["theft_return"],
      "confidence_scores": {"theft_return": 1.0}
    },
    "semantic_confidence": 1.0
  },
  "applicable_laws": [
    {
      "section": "BNS Section 303",
      "title": "Theft",
      "confidence": 0.95
    }
  ]
}
```

#### Step 5: Test Multiple Query Types

Test these queries to verify semantic enhancement:

**Query 1: Theft (borrowing)**
```json
{"query": "He borrowed my laptop and never returned it", "language": "en"}
```
Expected: `theft_return` category, high confidence

**Query 2: Theft (taking)**
```json
{"query": "Someone took my phone without permission", "language": "en"}
```
Expected: `theft` category, high confidence

**Query 3: Fraud**
```json
{"query": "He scammed me out of 5000 rupees", "language": "en"}
```
Expected: `fraud` category, high confidence

**Query 4: Traditional keyword (should still work)**
```json
{"query": "He stole my wallet", "language": "en"}
```
Expected: Works with or without semantic enhancement

---

### Level 3: Frontend to Backend Integration

Test the complete user flow.

#### Step 1: Start Frontend Development Server

```bash
cd frontend
npm install  # If not already done
npm run dev
```

**Expected output**:
```
> legals-frontend@0.1.0 dev
> next dev

ready - started server on 0.0.0.0:3000
```

#### Step 2: Open Browser

Navigate to: `http://localhost:3000`

#### Step 3: Test User Flow

**Scenario 1: Simple Theft Query**

1. Enter query: "He borrowed my laptop and never returned it"
2. Click "Analyze Query" or submit
3. **Check**:
   - ✅ Loading indicator appears
   - ✅ Response appears within 2-3 seconds
   - ✅ Shows detected crime type (theft)
   - ✅ Shows applicable BNS sections
   - ✅ Shows legal advice

**Scenario 2: Fraud Query**

1. Enter query: "Someone scammed me online"
2. Submit query
3. **Check**:
   - ✅ Detects fraud category
   - ✅ Shows relevant sections
   - ✅ Provides appropriate advice

**Scenario 3: Hindi Query** (if supported)

1. Enter query in Hindi
2. Submit
3. **Check**:
   - ✅ Hindi response returned
   - ✅ Semantic enhancement works with Hindi

---

## What to Verify for Semantic Enhancement

### In Browser Developer Console (F12)

Look at the API response in Network tab:

**Before Semantic Enhancement**:
```json
{
  "entities": {
    "actions": ["borrowed"]
  }
}
```

**After Semantic Enhancement** (should now have):
```json
{
  "entities": {
    "actions": ["borrowed"],
    "semantic_enhancements": {
      "categories_detected": ["theft_return"],
      "semantic_matches": {
        "theft_return": [
          ["borrowed", 1.0],
          ["never gave back", 0.72]
        ]
      }
    },
    "semantic_confidence": 1.0,
    "detected_crimes": [
      {
        "type": "theft_return",
        "source": "semantic_enhancement",
        "confidence": 1.0
      }
    ]
  }
}
```

---

## Performance Benchmarks

### Expected Performance Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Backend response time | < 2 seconds | First query might be slower (model load) |
| Semantic enhancement overhead | < 100ms | After model loaded |
| Frontend render time | < 500ms | After receiving response |
| Total user experience | < 3 seconds | Query to result |

### How to Measure

**Backend timing**:
- Check FastAPI logs for request duration
- Look for "Semantic enhancement applied" log entries

**Frontend timing**:
- Use browser DevTools Network tab
- Check "Time" column for API request

---

## Common Issues & Solutions

### Issue 1: "Module not found: sentence_transformers"
**Solution**: Install dependencies
```bash
pip install -r requirements-semantic-fixed.txt
```

### Issue 2: Semantic enhancement not working
**Check**:
1. Is `ENABLE_SEMANTIC_ENHANCEMENT = True` in `backend/app/services/semantic_config.py`?
2. Check backend logs for semantic initialization errors
3. Run `python test_semantic_simple.py` to verify setup

**Solution**:
```bash
cd backend
python download_model.py
```

### Issue 3: Backend connection error
**Check**:
1. Is backend running on port 8000?
2. Is Neo4j running?
3. Check backend/.env configuration

**Solution**:
```bash
# Check port
netstat -ano | findstr :8000

# Restart backend
cd backend
python -m uvicorn app.main:app --reload
```

### Issue 4: Frontend can't connect to backend
**Check**:
1. CORS settings in backend
2. API URL in frontend configuration
3. Both services running

**Solution**: Check `frontend/.env` or config file for correct backend URL

### Issue 5: Neo4j connection failed
**Check**:
1. Neo4j service running
2. Credentials correct in backend/.env
3. Database has data loaded

**Solution**:
```bash
# Restart Neo4j
# Re-import data if needed
```

---

## Verification Checklist

Use this checklist to ensure everything is working:

### Backend Tests
- [ ] `test_semantic_simple.py` passes
- [ ] `test_ollama_integration.py` passes
- [ ] Backend starts without errors
- [ ] Health endpoint returns 200
- [ ] Query endpoint returns valid responses
- [ ] Semantic enhancement fields present in responses
- [ ] Logs show "Semantic enhancement applied"

### Frontend Tests
- [ ] Frontend starts without errors
- [ ] Can access UI at localhost:3000
- [ ] Query submission works
- [ ] Loading state displays correctly
- [ ] Results display correctly
- [ ] Multiple queries work
- [ ] No console errors in browser

### Integration Tests
- [ ] Frontend can reach backend
- [ ] Natural language queries work better than before
- [ ] "Borrowed and never returned" → detects theft
- [ ] "Scammed" → detects fraud
- [ ] Response times acceptable
- [ ] No errors in any logs

---

## Success Criteria

Your integration is successful if:

1. ✅ All unit tests pass
2. ✅ Backend starts and responds to queries
3. ✅ Frontend connects to backend
4. ✅ Natural language queries return correct results
5. ✅ Semantic confidence scores appear in responses
6. ✅ Performance is acceptable (< 3 seconds total)
7. ✅ No errors in browser console
8. ✅ No errors in backend logs

---

## Next Steps After Testing

### If All Tests Pass ✅

1. **Document any issues found**
2. **Test with more complex queries**
3. **Consider deploying to staging**
4. **Prepare demo scenarios**

### If Tests Fail ❌

1. **Check logs** (backend console + browser console)
2. **Verify all dependencies installed**
3. **Confirm Neo4j has data**
4. **Check configuration files**
5. **Review error messages carefully**
6. **Consult troubleshooting section above**

---

## Quick Test Commands

Run these in order for fast verification:

```bash
# 1. Test semantic service
python test_semantic_simple.py

# 2. Test integration
python test_ollama_integration.py

# 3. Start backend (in one terminal)
cd backend && python -m uvicorn app.main:app --reload

# 4. Start frontend (in another terminal)
cd frontend && npm run dev

# 5. Open browser
# Navigate to http://localhost:3000
# Enter query: "He borrowed my laptop and never returned it"
# Verify results appear
```

---

## Support & Documentation

- **Semantic Implementation Review**: `docs/SEMANTIC_TRANSFORMER_REVIEW.md`
- **Test Results**: `docs/SEMANTIC_TEST_RESULTS.md`
- **Original Plan**: `docs/SEMANTIC_ENHANCEMENT_PLAN.md`
- **Integration Tracking**: `tasks/todo.md`

---

## Credits

- **Semantic Transformer Implementation**: Vaishnav
- **Integration & Testing**: Claude
- **End-to-End Testing Guide**: Claude

---

**Last Updated**: 2025-12-02
**Branch**: phase2-cypher-rules
**Status**: Ready for Testing
