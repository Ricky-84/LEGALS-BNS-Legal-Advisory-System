# Semantic Similarity Enhancement Plan

## Problem Statement
Current system only handles explicitly mentioned phrases in prompts. Fails on new/unseen natural language expressions that users would commonly use.

**Current Success Rate**: 50% for natural language queries
**Target Success Rate**: 80%+ for natural language queries

## Proposed Solution: Semantic Similarity Matching

### Architecture Overview
```
User Query → [Entity Extraction] → [Semantic Similarity Layer] → [Crime Detection] → Result

Current Flow:
User: "borrowed laptop never returned" → Phi-3 SLM → "borrowed" → No detection

Enhanced Flow:
User: "borrowed laptop never returned" → Phi-3 SLM → "borrowed" → Semantic Layer → "stole" (0.85 similarity) → Theft detection
```

## Implementation Plan

### Phase 1: Research & Setup (1-2 days)
1. **Model Selection**
   - Primary: `sentence-transformers/all-MiniLM-L6-v2` (22MB, fast)
   - Alternative: `sentence-transformers/all-mpnet-base-v2` (438MB, more accurate)
   - Benchmark both for speed vs accuracy tradeoff

2. **Infrastructure Requirements**
   - Add `sentence-transformers` dependency to requirements.txt
   - Create new `semantic_service.py` module
   - Add semantic similarity cache for performance

### Phase 2: Core Implementation (2-3 days)
1. **Semantic Mapping Service**
   ```python
   class SemanticMappingService:
       def __init__(self):
           self.model = SentenceTransformer('all-MiniLM-L6-v2')
           self.legal_terms_embeddings = self._precompute_legal_embeddings()

       def find_semantic_matches(self, user_actions: List[str]) -> Dict[str, float]:
           # Return similarity scores for legal terms
           pass
   ```

2. **Legal Terms Database**
   - Create comprehensive list of legal action terms
   - Pre-compute embeddings for all legal terms
   - Store in cache for fast lookup

3. **Integration Points**
   - Modify `ollama_service.py` to use semantic enhancement
   - Update `neo4j_service.py` detection methods
   - Add semantic scoring to entity extraction

### Phase 3: Enhanced Detection Logic (1-2 days)
1. **Multi-Layer Detection**
   ```python
   def enhanced_entity_extraction(self, user_query: str):
       # Layer 1: Current SLM extraction
       entities = self.phi3_extract_entities(user_query)

       # Layer 2: Semantic similarity enhancement
       enhanced_actions = self.semantic_service.enhance_actions(entities['actions'])
       entities['actions'].extend(enhanced_actions)

       # Layer 3: Existing detection logic
       return entities
   ```

2. **Confidence Scoring**
   - Original keywords: confidence = 1.0
   - Semantic matches: confidence = similarity_score
   - Adjust final detection confidence accordingly

### Phase 4: Testing & Optimization (1-2 days)
1. **Comprehensive Testing**
   - Test with 100+ natural language variations
   - Benchmark against current approach
   - Measure latency impact

2. **Performance Optimization**
   - Cache embeddings for common phrases
   - Batch processing for multiple queries
   - Asynchronous semantic processing if needed

## Technical Specifications

### New Dependencies
```python
# requirements.txt additions
sentence-transformers==2.2.2
torch>=1.9.0  # Required by sentence-transformers
numpy>=1.21.0
scikit-learn>=1.0.0  # For cosine similarity
```

### New Files Structure
```
backend/app/services/
├── semantic_service.py          # New: Semantic similarity service
├── semantic_mappings.py         # New: Legal terms database
└── semantic_cache.py           # New: Caching for performance

backend/data/
├── legal_terms_embeddings.pkl  # New: Pre-computed embeddings
└── semantic_mappings.json      # New: Term mappings database
```

### Configuration Changes
```python
# config.py additions
SEMANTIC_SIMILARITY_THRESHOLD = 0.75
SEMANTIC_CACHE_SIZE = 1000
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

## Architecture Diagram Updates Required

### Current Architecture
```
Frontend → FastAPI → [Ollama/Phi-3] → [Neo4j Service] → Response
```

### Enhanced Architecture
```
Frontend → FastAPI → [Ollama/Phi-3] → [Semantic Service] → [Neo4j Service] → Response
                                              ↓
                                    [Embeddings Cache]
```

## Demo/PPT Updates Required

1. **New Component Slide**: Semantic Understanding Layer
2. **Architecture Diagram**: Add semantic service component
3. **Demo Enhancement**: Show natural language understanding
4. **Performance Metrics**: Before/after accuracy comparison

## Performance Expectations

### Accuracy Improvements
- Natural language queries: 50% → 80%+
- Overall system accuracy: +15-20%
- False positives: Potentially reduced due to better understanding

### Latency Impact
- Additional processing time: ~50-100ms per query
- Mitigated by caching and pre-computed embeddings
- Acceptable tradeoff for significantly better accuracy

## Implementation Priority
- **Priority**: Medium-High (significant UX improvement)
- **Effort**: ~1 week development + testing
- **Impact**: Major improvement in natural language handling
- **Risk**: Low (fallback to current system if issues)

## Fallback Strategy
If semantic similarity has issues:
1. Graceful degradation to current keyword-based approach
2. Feature flag to enable/disable semantic enhancement
3. Performance monitoring and automatic fallback

## Success Metrics
- [ ] Natural language query success rate > 80%
- [ ] Latency increase < 100ms per query
- [ ] No reduction in current keyword-based accuracy
- [ ] User satisfaction improvement in demo feedback

## Next Steps (When Ready to Implement)
1. Research and select optimal embedding model
2. Design detailed API for semantic service integration
3. Create development branch for semantic enhancement
4. Implement core semantic mapping functionality
5. Comprehensive testing with diverse natural language inputs
6. Update documentation and architecture diagrams
7. Demo preparation with enhanced natural language examples

---
**Note**: This enhancement addresses the core limitation of the current approach and would significantly improve user experience for natural language legal queries.