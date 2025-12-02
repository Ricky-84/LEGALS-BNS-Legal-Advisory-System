# METHODOLOGY - LEGALS: Legal Empowerment and Awareness System

## 3. METHODOLOGY

### 3.1 System Architecture Overview

The LEGALS (Legal Empowerment and Awareness System) is designed as a modular, deterministic legal advisory system that processes natural language queries and maps them to relevant sections of the Bharatiya Nyaya Sanhita (BNS). The system employs a multi-tier architecture with eight interconnected modules, each responsible for specific functionalities in the legal query processing pipeline.

The architectural design follows a service-oriented approach with clear separation of concerns, enabling independent development, testing, and scaling of individual components. Figure 1 illustrates the high-level system architecture with the sequential processing pipeline.

```
┌───────────────────────────────────────────────────────────────────────┐
│                      LEGALS System Architecture                        │
│                   (Planned with Semantic Enhancement)                  │
├───────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │          Module 1: User Interface (React.js)               │        │
│  │               - Query Input Component                       │        │
│  │               - Response Display Component                  │        │
│  └────────────────────────┬──────────────────────────────────┘        │
│                           │ HTTP POST                                  │
│                           ▼                                             │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │          Module 2: API Gateway (FastAPI)                   │        │
│  │               - Request Validation & Routing                │        │
│  │               - CORS & Middleware                           │        │
│  └────────────────────────┬──────────────────────────────────┘        │
│                           │                                             │
│                           ▼                                             │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │          Module 8: Orchestration Service                   │        │
│  │               - Pipeline Coordination                       │        │
│  │               - Sequential Processing Flow                  │        │
│  │               - Error Handling & Logging                    │        │
│  └────────────────────────┬──────────────────────────────────┘        │
│                           │                                             │
│                           ▼                                             │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │  STAGE 1: Module 3 - Entity Extraction (Phi-3 SLM)        │        │
│  │   Input: User's natural language query                     │        │
│  │   Output: Structured entities (persons, objects, actions)  │        │
│  └────────────────────────┬──────────────────────────────────┘        │
│                           │                                             │
│                           ▼                                             │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │  STAGE 2: Module 4 - Semantic Enhancement                 │        │
│  │           (Sentence Transformers)                          │        │
│  │   Input: Extracted actions/entities                        │        │
│  │   Process: Maps natural language → Legal terminology       │        │
│  │   Output: Enhanced entities with semantic similarity       │        │
│  │   Example: "borrowed never returned" → "stole", "theft"    │        │
│  └────────────────────────┬──────────────────────────────────┘        │
│                           │                                             │
│                           ▼                                             │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │  STAGE 3: Module 5 - Legal Reasoning (Neo4j Graph)        │        │
│  │   Input: Enhanced entities from semantic layer             │        │
│  │   Process: Cypher queries match patterns in graph          │        │
│  │   Uses: Module 7 - Knowledge Graph (BNS sections)          │        │
│  │   Output: Applicable BNS sections with confidence          │        │
│  │                                                             │        │
│  │   ┌─────────────────────────────────────┐                 │        │
│  │   │   Module 7: Knowledge Graph         │                 │        │
│  │   │   - BNS Legal Sections              │                 │        │
│  │   │   - Offence Definitions             │                 │        │
│  │   │   - Action Patterns                 │                 │        │
│  │   │   - Legal Elements                  │                 │        │
│  │   └─────────────────────────────────────┘                 │        │
│  │                                                             │        │
│  └────────────────────────┬──────────────────────────────────┘        │
│                           │                                             │
│                           ▼                                             │
│  ┌───────────────────────────────────────────────────────────┐        │
│  │  STAGE 4: Module 6 - Response Generation                  │        │
│  │           (Template-based Formatting)                      │        │
│  │   Input: Legal analysis from Neo4j                         │        │
│  │   Process: Structures advice with disclaimers              │        │
│  │   Output: Citizen-friendly legal response                  │        │
│  └────────────────────────┬──────────────────────────────────┘        │
│                           │                                             │
│                           ▼                                             │
│                 Final Legal Advisory Response                          │
│                 (Returned to User via API Gateway)                     │
│                                                                         │
└───────────────────────────────────────────────────────────────────────┘

PROCESSING FLOW (Sequential Pipeline):
User Query → Entity Extraction → Semantic Enhancement → Neo4j Legal
Processing → Response Formatting → User Response
```

**Figure 1**: High-level architecture of LEGALS system showing the sequential processing pipeline with eight interconnected modules. The diagram illustrates the planned architecture including the Semantic Enhancement module for improved natural language understanding.

### 3.2 Module Descriptions

#### 3.2.1 Module 1: User Interface Module

**Purpose**: The User Interface Module provides the frontend interface for citizen interaction with the legal advisory system.

**Technology Stack**:
- Framework: React 18.x
- UI Library: Material-UI (MUI) 5.x
- State Management: React Hooks (useState, useEffect)
- HTTP Client: Axios
- Build Tool: Create React App with Webpack

**Implementation Details**:

The User Interface Module consists of four primary components:

1. **Query Input Component** (`QueryInput.js`):
   - Provides a text area for natural language query input
   - Supports multilingual input (English and Hindi)
   - Implements input validation (minimum 10 characters, maximum 1000 characters)
   - Features voice input capability (optional, when configured)
   - Language selection toggle

2. **Response Display Component** (`ResponseDisplay.js`):
   - Renders structured legal analysis results
   - Displays extracted entities in categorized sections
   - Shows applicable BNS sections with confidence scores
   - Presents legal advice in citizen-friendly language
   - Highlights legal disclaimers prominently

3. **Header Component** (`Header.js`):
   - Application branding and navigation
   - System status indicators
   - Language preference settings

4. **Footer Component** (`Footer.js`):
   - Legal disclaimers
   - Contact information
   - Version information

**Data Flow**:
```
User Input → Query Validation → API Request (POST /api/v1/legal/query)
API Response → State Update → Component Re-render → Display Results
```

**Key Features**:
- Responsive design for mobile and desktop devices
- Real-time query processing status updates
- Error handling with user-friendly messages
- Accessibility compliance (WCAG 2.1 Level AA)

---

#### 3.2.2 Module 2: API Gateway Module

**Purpose**: The API Gateway Module serves as the entry point for all client requests, handling routing, authentication, request validation, and cross-origin resource sharing (CORS).

**Technology Stack**:
- Framework: FastAPI 0.104+
- ASGI Server: Uvicorn
- Schema Validation: Pydantic 2.0+
- Documentation: OpenAPI 3.0 (Swagger UI)

**Implementation Details**:

The API Gateway is implemented in `backend/main.py` and consists of the following components:

1. **FastAPI Application Instance**:
```python
app = FastAPI(
    title="LEGALS API",
    description="Legal Empowerment and Awareness System",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
```

2. **CORS Middleware Configuration**:
   - Allows cross-origin requests from frontend (http://localhost:3000)
   - Configurable origin whitelist for production deployment
   - Supports credentials, all HTTP methods, and headers

3. **Router Registration**:
   - `/api/v1/legal/*` - Legal query processing endpoints
   - `/api/v1/health` - System health check endpoint
   - `/ws` - WebSocket endpoint for real-time communication

4. **Request/Response Models** (defined in `legal_query.py`):

```python
class LegalQueryRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=1000)
    language: Optional[str] = Field("en", pattern="^(en|hi)$")
    user_id: Optional[str] = None

class LegalQueryResponse(BaseModel):
    query_id: str
    entities: Dict[str, List[str]]
    applicable_laws: List[Dict[str, Any]]
    legal_advice: str
    confidence_score: float
    processing_time: float
    disclaimers: List[str]
```

**Endpoints**:

1. `POST /api/v1/legal/query` - Main legal query processing endpoint
2. `GET /api/v1/legal/query/{query_id}` - Retrieve historical query results
3. `POST /api/v1/legal/extract-entities` - Entity extraction only endpoint
4. `GET /api/v1/legal/supported-laws` - List supported BNS sections
5. `GET /api/v1/legal/system-status` - System component health check
6. `GET /health` - Basic health check

**Security Features**:
- Input sanitization and validation using Pydantic
- Request size limits (max 1000 characters per query)
- Rate limiting capability (configurable)
- HTTPS support for production deployment

---

#### 3.2.3 Module 3: Entity Extraction Module

**Purpose**: The Entity Extraction Module is responsible for extracting factual entities from user queries using the Phi-3 Small Language Model (SLM). It identifies persons, objects, locations, actions, intentions, circumstances, and relationships without making legal classifications.

**Technology Stack**:
- AI Model: Microsoft Phi-3-mini (3.8B parameters)
- Model Runtime: Ollama
- HTTP Client: Python Requests library
- Fallback: Keyword-based extraction

**Implementation Details**:

The Entity Extraction Module is implemented in `backend/app/services/ollama_service.py` (class `OllamaService`).

**Entity Categories**:

The system extracts seven categories of entities:

1. **Persons**: Individuals involved (victim, accused, witness, employee, employer, etc.)
2. **Objects**: Physical items mentioned (phone, wallet, money, jewelry, documents, etc.)
3. **Locations**: Places where incidents occurred (house, office, street, dwelling, vehicle, etc.)
4. **Actions**: Verbs describing what happened (took, stole, grabbed, threatened, damaged, etc.)
5. **Intentions**: Mental states or motivations (dishonestly, forcefully, without permission, etc.)
6. **Circumstances**: Contextual factors (at night, during absence, with weapon, etc.)
7. **Relationships**: Connections between persons (employee-employer, friend, stranger, etc.)

**Extraction Process**:

1. **Primary Method - Phi-3 SLM Extraction**:

```python
def extract_entities(self, user_query: str, language: str = "en")
    -> Dict[str, List[str]]:
    """
    Extract factual entities using Phi-3 model via Ollama
    """
    prompt = self._create_entity_extraction_prompt(user_query, language)

    response = requests.post(
        f"{self.base_url}/api/generate",
        json={
            "model": self.model,  # phi3:latest
            "prompt": prompt,
            "stream": False,
            "temperature": 0.3    # Low temperature for consistency
        }
    )

    entities = self._parse_entity_response(response.json()["response"])
    return entities
```

**Prompt Engineering**:

The entity extraction prompt is carefully designed to:
- Instruct the model to extract only factual information
- Explicitly prohibit legal classification or interpretation
- Request structured JSON output with predefined categories
- Include few-shot examples for consistent formatting

Example prompt structure:
```
You are a factual entity extraction system. Extract ONLY factual elements
from the user's description. DO NOT determine which laws apply or make
legal classifications.

Extract the following categories:
1. PERSONS: [description]
2. OBJECTS: [description]
...

Return in JSON format:
{
    "persons": [...],
    "objects": [...],
    ...
}

User Query: [actual query]
```

2. **Fallback Method - Keyword-based Extraction**:

When Phi-3 is unavailable or produces invalid output, the system uses a deterministic keyword-based fallback:

```python
def _extract_entities_fallback(self, query_lower: str)
    -> Dict[str, List[str]]:
    """
    Fallback entity extraction using keyword matching
    """
    entities = {
        "persons": [],
        "objects": [],
        "locations": [],
        "actions": [],
        "intentions": [],
        "circumstances": [],
        "relationships": []
    }

    # Action keywords
    action_keywords = {
        "stole", "stolen", "took", "taken", "grabbed", "snatched",
        "threatened", "extorted", "damaged", "trespassed", "cheated"
    }

    # Object keywords
    object_keywords = {
        "phone", "mobile", "iphone", "samsung", "laptop", "money",
        "wallet", "purse", "jewelry", "gold", "cash", "documents"
    }

    # [Similar keyword sets for other categories]

    # Pattern matching logic
    for keyword in action_keywords:
        if keyword in query_lower:
            entities["actions"].append(keyword)

    # [Similar matching for other categories]

    return entities
```

**Output Format**:

```json
{
    "persons": ["victim", "accused"],
    "objects": ["mobile phone", "wallet"],
    "locations": ["bus", "market"],
    "actions": ["stole", "grabbed"],
    "intentions": ["dishonestly", "without permission"],
    "circumstances": ["in crowded place", "during daytime"],
    "relationships": ["stranger"]
}
```

**Quality Assurance**:
- JSON validation and schema verification
- Duplicate removal and normalization
- Empty category handling
- Logging of extraction confidence

---

#### 3.2.4 Module 4: Semantic Enhancement Module

**Purpose**: The Semantic Enhancement Module transforms natural language expressions into legal terminology using semantic similarity, enabling the system to understand queries like "borrowed and never returned" as equivalent to "stole" or "theft".

**Technology Stack**:
- NLP Library: sentence-transformers 2.2+
- Model: all-MiniLM-L6-v2 (22MB, optimized for speed)
- Vector Operations: NumPy
- Similarity Metric: Cosine similarity
- Caching: In-memory dictionary for performance

**Implementation Details**:

The Semantic Enhancement Module bridges the gap between colloquial language and legal terminology through embedding-based semantic similarity matching.

**Semantic Mapping Process**:

1. **Pre-computed Legal Term Embeddings**:

The system maintains a database of legal action terms with pre-computed embeddings:

```python
class SemanticEnhancementService:
    def __init__(self):
        # Load lightweight, fast model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Pre-compute embeddings for legal terms
        self.legal_action_embeddings = self._precompute_legal_actions()

    def _precompute_legal_actions(self) -> Dict[str, np.ndarray]:
        """
        Pre-compute embeddings for all legal action terms
        """
        legal_actions = {
            # Theft actions
            "stole": "took property without permission",
            "misappropriated": "used entrusted property dishonestly",
            "embezzled": "misused funds in trust",

            # Fraud actions
            "cheated": "deceived someone for gain",
            "defrauded": "obtained property by deception",

            # Violence actions
            "threatened": "put someone in fear",
            "extorted": "obtained property by threat",

            # Property damage
            "damaged": "destroyed or harmed property",
            "vandalized": "deliberately damaged property",

            # Trespass
            "trespassed": "entered property without permission"
        }

        embeddings = {}
        for action, description in legal_actions.items():
            embeddings[action] = self.model.encode(description)

        return embeddings
```

2. **Runtime Semantic Matching**:

When user actions are extracted, the semantic enhancement module computes similarities:

```python
def enhance_actions(self, user_actions: List[str]) -> List[Dict[str, Any]]:
    """
    Map user's natural language actions to legal terminology

    Example:
    Input: ["borrowed and never returned"]
    Output: [
        {
            "original": "borrowed and never returned",
            "legal_term": "stole",
            "confidence": 0.87
        },
        {
            "original": "borrowed and never returned",
            "legal_term": "misappropriated",
            "confidence": 0.82
        }
    ]
    """
    enhanced_actions = []

    for action in user_actions:
        # Get embedding for user's action
        action_embedding = self._get_embedding(action)

        # Find most similar legal actions
        similarities = {}
        for legal_action, legal_embedding in self.legal_action_embeddings.items():
            similarity = self._cosine_similarity(action_embedding, legal_embedding)
            if similarity > 0.75:  # Threshold
                similarities[legal_action] = similarity

        # Add top matches
        for legal_action, confidence in sorted(
            similarities.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]:
            enhanced_actions.append({
                "original": action,
                "legal_term": legal_action,
                "confidence": confidence
            })

    return enhanced_actions
```

3. **Cosine Similarity Calculation**:

```python
def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors
    Range: [-1, 1], where 1 = identical, 0 = orthogonal, -1 = opposite
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

**Integration with Pipeline**:

The semantic enhancement integrates between entity extraction and legal reasoning:

```python
# In legal_processing_service.py
def process_legal_query(self, query: str, language: str = "en"):
    # Stage 1: Entity Extraction
    entities = self.ollama.extract_entities(query, language)

    # Stage 2: Semantic Enhancement (NEW)
    if entities.get("actions"):
        enhanced_actions = self.semantic_service.enhance_actions(
            entities["actions"]
        )

        # Add semantically matched actions
        for enhanced in enhanced_actions:
            if enhanced["confidence"] > 0.8:
                entities["actions"].append(enhanced["legal_term"])

    # Stage 3: Legal Reasoning (receives enhanced entities)
    legal_analysis = self.neo4j.find_applicable_laws(entities)
```

**Example Transformations**:

| User Expression | Semantic Match | Confidence | Legal Term Used |
|----------------|----------------|------------|-----------------|
| "borrowed and never returned" | Theft pattern | 0.87 | stole, misappropriated |
| "convinced to give money for fake product" | Fraud pattern | 0.91 | cheated, defrauded |
| "said bad things would happen unless paid" | Extortion pattern | 0.89 | threatened, extorted |
| "took company money for vacation" | Breach of trust | 0.85 | embezzled, misappropriated |
| "came inside when no one home" | Trespass pattern | 0.83 | trespassed, entered unlawfully |

**Performance Optimization**:

1. **Embedding Caching**:
```python
def _get_embedding(self, text: str) -> np.ndarray:
    """Get embedding with caching for repeated queries"""
    if text not in self.embedding_cache:
        self.embedding_cache[text] = self.model.encode(text)
    return self.embedding_cache[text]
```

2. **Batch Processing**:
- Pre-compute all legal term embeddings at initialization
- Cache user action embeddings during session
- Use NumPy vectorized operations for similarity calculations

3. **Threshold Optimization**:
- Similarity threshold of 0.75 balances precision and recall
- Top-3 matches prevent overwhelming the legal reasoning stage
- Confidence scores propagate through pipeline for transparency

**Quality Metrics**:
- Natural language query success rate: 50% → 80%+ (target)
- Average processing time: 50-100ms additional latency
- False positive rate: < 10%
- Semantic match accuracy: > 85%

**Fallback Handling**:
- If sentence-transformers unavailable: Skip enhancement, use raw entities
- If similarity scores below threshold: No enhancement applied
- If model loading fails: Log warning, continue with original entities

---

#### 3.2.5 Module 5: Legal Reasoning Module

**Purpose**: The Legal Reasoning Module performs deterministic, graph-based legal classification by matching extracted entities to relevant BNS (Bharatiya Nyaya Sanhita) sections using Cypher queries on the Neo4j knowledge graph.

**Technology Stack**:
- Graph Database: Neo4j Community Edition 5.x
- Query Language: Cypher
- Python Driver: neo4j-driver 5.0+
- Fallback: Rule-based Python classification

**Implementation Details**:

The Legal Reasoning Module is implemented in `backend/app/services/neo4j_service.py` (class `Neo4jService`).

**Graph-Based Reasoning Approach**:

Unlike traditional keyword-matching approaches, this module uses graph traversal to determine applicable laws. The reasoning process involves:

1. **Connection to Neo4j Database**:
```python
def connect(self):
    self.driver = GraphDatabase.driver(
        settings.NEO4J_URI,          # bolt://localhost:7687
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )
```

2. **Primary Query Method - Graph Traversal**:

The core legal reasoning is performed using Cypher graph queries:

```python
def find_applicable_laws(self, entities: Dict[str, List[str]])
    -> List[Dict[str, Any]]:
    """
    Find applicable BNS laws using graph-based Cypher queries
    """
    user_actions = entities.get("actions", [])
    user_locations = entities.get("locations", [])
    user_objects = entities.get("objects", [])

    with self.driver.session(database="legalknowledge") as session:
        # Query 1: Action-based matching
        action_results = session.run("""
            // Step 1: Find action patterns matching user's actions
            UNWIND $user_actions AS user_action
            MATCH (ap:ActionPattern)
            WHERE toLower(ap.text) CONTAINS toLower(user_action)
               OR toLower(user_action) CONTAINS toLower(ap.text)

            // Step 2: Find offences matched by these patterns
            MATCH (ap)-[:MATCHES]->(offence:Offence)

            // Step 3: Find sections defining these offences
            MATCH (section:Section)-[:DEFINES]->(offence)

            // Step 4: Get punishment information
            MATCH (punishment:Punishment)
            WHERE punishment.section_id = section.section_id

            // Step 5: Count matched patterns for confidence
            WITH section, offence, punishment,
                 count(DISTINCT ap) as matched_patterns

            RETURN
                section.section_id as section,
                section.title as title,
                section.text as description,
                punishment.description as punishment,
                offence.type as offence_type,
                matched_patterns,
                "action_based" as match_type

            ORDER BY matched_patterns DESC
        """, user_actions=user_actions)
```

**Multi-Criteria Matching**:

The system performs multiple types of graph queries:

1. **Action-based Matching**: Matches user actions to ActionPattern nodes
2. **Location-based Matching**: Identifies aggravating circumstances (dwelling, vehicle)
3. **Object-based Matching**: Considers property type and value
4. **Relationship-based Matching**: Identifies special relationships (employee-employer)

**Confidence Scoring Algorithm**:

```python
def _calculate_confidence(self, law_dict: Dict[str, Any],
                          entities: Dict[str, List[str]]) -> float:
    """
    Calculate confidence score based on multiple factors
    """
    base_confidence = 0.5

    # Factor 1: Pattern matches
    matched_patterns = law_dict.get("matched_patterns", 0)
    pattern_score = min(matched_patterns * 0.15, 0.3)

    # Factor 2: Required elements present
    required_elements = ["actions", "objects"]
    element_score = sum(0.1 for elem in required_elements
                       if entities.get(elem)) / len(required_elements)

    # Factor 3: Circumstantial evidence
    circumstances = entities.get("circumstances", [])
    circumstance_score = min(len(circumstances) * 0.05, 0.15)

    # Factor 4: Match type priority
    match_type = law_dict.get("match_type", "")
    type_score = {
        "action_based": 0.05,
        "location_based": 0.03,
        "relationship_based": 0.02
    }.get(match_type, 0)

    confidence = base_confidence + pattern_score + element_score + \
                 circumstance_score + type_score

    return min(confidence, 1.0)  # Cap at 1.0
```

**Fallback Legal Reasoning**:

When Neo4j is unavailable, the system uses rule-based Python logic:

```python
def _fallback_legal_reasoning(self, entities: Dict[str, List[str]])
    -> List[Dict[str, Any]]:
    """
    Fallback rule-based legal reasoning when Neo4j unavailable
    """
    applicable_laws = []

    actions = entities.get("actions", [])
    locations = entities.get("locations", [])
    relationships = entities.get("relationships", [])

    # Rule 1: Theft detection
    if self._has_theft_elements(entities):
        applicable_laws.append({
            "section": "BNS-303",
            "title": "Theft",
            "confidence": 0.8,
            "reasoning": "Basic theft elements detected",
            "match_type": "fallback_rule"
        })

    # Rule 2: Dwelling house theft
    if self._has_theft_elements(entities) and \
       any(loc in ["house", "home", "dwelling"] for loc in locations):
        applicable_laws.append({
            "section": "BNS-305",
            "title": "Theft in dwelling house",
            "confidence": 0.85,
            "reasoning": "Theft in dwelling detected",
            "match_type": "fallback_rule"
        })

    # [Additional rules for other offences]

    return applicable_laws
```

**Supported Offence Types**:

The module currently supports 10 offence categories from BNS Chapter XVII:

1. BNS-303: Theft
2. BNS-304: Snatching
3. BNS-305: Theft in dwelling house
4. BNS-306: Theft by clerk or servant
5. BNS-308: Extortion
6. BNS-309: Robbery
7. BNS-316: Criminal breach of trust
8. BNS-318: Cheating and dishonestly inducing delivery of property
9. BNS-324: Mischief
10. BNS-329: Criminal trespass

**Output Format**:

```json
{
    "section": "BNS-303",
    "title": "Theft",
    "description": "Whoever intends to take dishonestly any movable property...",
    "punishment": "Imprisonment up to 3 years or fine or both",
    "confidence": 0.85,
    "reasoning": "Matched 3 action patterns, theft elements present",
    "match_type": "action_based",
    "matched_patterns": 3
}
```

---

#### 3.2.6 Module 6: Response Generation Module

**Purpose**: The Response Generation Module transforms structured legal analysis results into citizen-friendly, natural language responses with proper legal disclaimers and actionable guidance.

**Technology Stack**:
- Template Engine: Python string formatting
- AI Model (optional): Phi-3 via Ollama for natural language enhancement
- Language Support: English and Hindi

**Implementation Details**:

The Response Generation Module is implemented in `backend/app/services/ollama_service.py` (method `format_legal_response`).

**Response Generation Approach**:

The system uses a template-based approach with structured sections:

```python
def format_legal_response(self, legal_analysis: Dict[str, Any],
                          language: str = "en") -> str:
    """
    Generate citizen-friendly response from legal analysis
    """
    applicable_laws = legal_analysis.get("applicable_laws", [])
    entities = legal_analysis.get("entities", {})
    confidence = legal_analysis.get("confidence_score", 0.0)

    # Build response using template
    response = self._get_fallback_response(legal_analysis, language)

    return response
```

**Response Structure**:

Each response contains the following sections:

1. **Summary Section**:
   - Brief overview of the legal situation
   - Key entities identified
   - Overall confidence level

2. **Legal Classification Section**:
   - Applicable BNS sections with titles
   - Explanation of why each section applies
   - Confidence scores for each section

3. **Punishment Information Section**:
   - Prescribed punishments for each applicable section
   - Severity classification (minor, moderate, serious)
   - Aggravating and mitigating factors

4. **Immediate Actions Section**:
   - Step-by-step guidance for filing FIR
   - Evidence preservation recommendations
   - Timeline for legal actions

5. **Disclaimer Section**:
   - Legal limitations of the system
   - Requirement for professional legal counsel
   - Preliminary information only notice

**Template Example (English)**:

```python
def _get_fallback_response(self, legal_analysis: Dict, language: str) -> str:
    applicable_laws = legal_analysis.get("applicable_laws", [])
    entities = legal_analysis.get("entities", {})

    if language == "hi":
        return self._get_hindi_response(legal_analysis)

    # English response template
    response = "LEGAL ANALYSIS RESULT\n"
    response += "=" * 80 + "\n\n"

    # Section 1: Case Summary
    response += "1. CASE SUMMARY\n"
    response += "-" * 80 + "\n"
    response += f"Based on your description, we have identified:\n"
    response += f"- Actions: {', '.join(entities.get('actions', ['None']))}\n"
    response += f"- Objects: {', '.join(entities.get('objects', ['None']))}\n"
    response += f"- Locations: {', '.join(entities.get('locations', ['None']))}\n\n"

    # Section 2: Applicable Laws
    response += "2. APPLICABLE LEGAL PROVISIONS\n"
    response += "-" * 80 + "\n"

    if not applicable_laws:
        response += "No specific BNS sections could be determined...\n\n"
    else:
        for i, law in enumerate(applicable_laws, 1):
            response += f"\n{i}. {law['section']}: {law['title']}\n"
            response += f"   Confidence: {law['confidence']*100:.0f}%\n"
            response += f"   Reasoning: {law.get('reasoning', 'N/A')}\n"
            response += f"   Punishment: {law.get('punishment', 'N/A')}\n"

    # Section 3: Immediate Actions
    response += "\n3. RECOMMENDED IMMEDIATE ACTIONS\n"
    response += "-" * 80 + "\n"
    response += "a) File an FIR (First Information Report) at the nearest police station\n"
    response += "b) Preserve all evidence (photos, receipts, witness contacts)\n"
    response += "c) Prepare a detailed written account of the incident\n"
    response += "d) Consult a criminal lawyer for case-specific legal advice\n\n"

    # Section 4: Legal Disclaimers
    response += "4. IMPORTANT LEGAL DISCLAIMER\n"
    response += "-" * 80 + "\n"
    response += "This system provides PRELIMINARY legal information only.\n"
    response += "It is NOT a replacement for qualified legal counsel.\n"
    response += "You MUST consult a licensed criminal lawyer for:\n"
    response += "- Accurate legal advice specific to your case\n"
    response += "- Court proceedings and representation\n"
    response += "- Detailed analysis of case facts and circumstances\n\n"
    response += "=" * 80 + "\n"

    return response
```

**Multilingual Support**:

For Hindi language responses, the system provides translated templates:

```python
def _get_hindi_response(self, legal_analysis: Dict) -> str:
    response = "कानूनी विश्लेषण परिणाम\n"
    response += "=" * 80 + "\n\n"

    response += "1. मामले का सारांश\n"
    # [Hindi template sections]

    response += "\n4. महत्वपूर्ण कानूनी अस्वीकरण\n"
    response += "यह प्रणाली केवल प्रारंभिक कानूनी जानकारी प्रदान करती है।\n"
    response += "यह योग्य कानूनी परामर्श का विकल्प नहीं है।\n"
    # [Additional Hindi disclaimers]

    return response
```

**Response Quality Features**:

1. **Readability**:
   - Clear section headings
   - Bullet points for easy scanning
   - Consistent formatting
   - Appropriate use of whitespace

2. **Accuracy**:
   - Only includes information from legal analysis
   - No hallucination or invention of laws
   - Explicit confidence levels
   - Clear reasoning for classifications

3. **Actionability**:
   - Concrete next steps
   - Timeline guidance
   - Resource recommendations
   - Emergency contact information (when applicable)

4. **Legal Compliance**:
   - Prominent disclaimers
   - Clear limitations stated
   - Professional consultation emphasized
   - No guarantees or absolute statements

---

#### 3.2.7 Module 7: Knowledge Graph Module

**Purpose**: The Knowledge Graph Module stores and manages the structured legal knowledge base containing BNS sections, offence definitions, legal elements, action patterns, and their interconnections using a graph database.

**Technology Stack**:
- Database: Neo4j Community Edition 5.x
- Data Model: Property Graph Model
- Import Format: CSV with Cypher queries
- Query Language: Cypher

**Implementation Details**:

The Knowledge Graph is stored in Neo4j and consists of multiple node types and relationship types that represent legal concepts and their connections.

**Graph Schema**:

**Node Types**:

1. **Section Node**:
```cypher
(:Section {
    section_id: "BNS-303",           // Unique identifier
    section_number: 303,              // Numeric reference
    title: "Theft",                   // Section title
    text: "Full legal text...",       // Complete section text
    chapter: "XVII",                  // BNS chapter number
    category: "property_offences"     // Offence category
})
```

2. **Offence Node**:
```cypher
(:Offence {
    section_id: "BNS-303",
    type: "theft",                    // Canonical offence type
    section_number: 303
})
```

3. **Punishment Node**:
```cypher
(:Punishment {
    punishment_id: "PUN_303",
    section_id: "BNS-303",
    description: "Imprisonment up to 3 years or fine or both",
    punishment_type: "imprisonment_and_fine"
})
```

4. **LegalElement Node** (Enhanced Knowledge Graph):
```cypher
(:LegalElement {
    element_id: "dishonest_intent",
    type: "mens_rea",                 // Mental element
    name: "Dishonest Intent",
    description: "Intention to cause wrongful gain or loss",
    required: true
})

(:LegalElement {
    element_id: "taking_movable_property",
    type: "actus_reus",              // Physical act element
    name: "Taking Property",
    required: true
})
```

5. **ActionPattern Node** (Enhanced Knowledge Graph):
```cypher
(:ActionPattern {
    pattern_id: "theft_actions_001",
    text: "stole",
    variations: ["took", "stolen", "taking", "grabbed"],
    confidence: 1.0
})
```

6. **Chapter Node**:
```cypher
(:Chapter {
    number: "XVII",
    title: "Of Offences Against Property"
})
```

**Relationship Types**:

1. **CONTAINS**: Links Chapter to Section
```cypher
(:Chapter)-[:CONTAINS]->(:Section)
```

2. **DEFINES**: Links Section to Offence
```cypher
(:Section)-[:DEFINES]->(:Offence)
```

3. **PRESCRIBES**: Links Section to Punishment (implicit via section_id)

4. **MATCHES**: Links ActionPattern to Offence
```cypher
(:ActionPattern)-[:MATCHES {confidence: 0.95}]->(:Offence)
```

5. **REQUIRES**: Links Offence to LegalElement
```cypher
(:Offence)-[:REQUIRES_MENS_REA {weight: 1.0, mandatory: true}]->(:LegalElement)
(:Offence)-[:REQUIRES_ACTUS_REUS {weight: 1.0, mandatory: true}]->(:LegalElement)
(:Offence)-[:REQUIRES_CIRCUMSTANCE {weight: 0.8}]->(:LegalElement)
```

6. **AGGRAVATED_FORM_OF**: Links related offences
```cypher
(:Offence {type: "dwelling_theft"})-[:AGGRAVATED_FORM_OF]->(:Offence {type: "theft"})
(:Offence {type: "robbery"})-[:AGGRAVATED_FORM_OF]->(:Offence {type: "theft"})
```

**Graph Population**:

The knowledge graph is populated using Cypher import scripts located in the `cypher/` directory:

1. **Basic Import** (`neo4j_import.cypher`):
   - Creates Section, Offence, and Punishment nodes
   - Establishes basic relationships
   - Imports from CSV file: `bns_ch17_final_cleaned.csv`

```cypher
LOAD CSV WITH HEADERS FROM 'file:///bns_ch17_final_cleaned.csv' AS row
WITH row
WHERE row.s_section_number IS NOT NULL

// Create Section nodes
MERGE (s:Section {
    section_id: "BNS-" + row.s_section_number,
    section_number: toInteger(row.s_section_number),
    title: row.s_section_title,
    text: row.s_section_text
})

// Create Offence nodes with type mapping
MERGE (o:Offence {
    section_id: "BNS-" + row.s_section_number,
    type: CASE toInteger(row.s_section_number)
        WHEN 303 THEN 'theft'
        WHEN 304 THEN 'snatching'
        WHEN 305 THEN 'dwelling_theft'
        WHEN 306 THEN 'employee_theft'
        WHEN 308 THEN 'extortion'
        WHEN 309 THEN 'robbery'
        WHEN 316 THEN 'breach_of_trust'
        WHEN 318 THEN 'cheating'
        WHEN 324 THEN 'mischief'
        WHEN 329 THEN 'criminal_trespass'
        ELSE 'other'
    END
})

// Create Punishment nodes
MERGE (p:Punishment {
    punishment_id: 'PUN_' + row.s_section_number,
    section_id: "BNS-" + row.s_section_number,
    description: row.punishment
})

// Create relationships
MERGE (c)-[:CONTAINS]->(s)
MERGE (s)-[:DEFINES]->(o)
```

2. **Enhanced Import** (`neo4j_import_enhanced.cypher`):
   - Adds LegalElement nodes (mens rea, actus reus, circumstances)
   - Creates ActionPattern nodes with variations
   - Establishes REQUIRES and MATCHES relationships
   - Adds semantic connections between related offences

Example ActionPattern creation:
```cypher
// Theft action patterns
CREATE (ap1:ActionPattern {
    pattern_id: 'theft_action_001',
    text: 'stole',
    variations: ['took', 'stolen', 'taking', 'grabbed', 'snatched'],
    confidence: 1.0
})

CREATE (ap2:ActionPattern {
    pattern_id: 'theft_action_002',
    text: 'misappropriated',
    variations: ['kept for himself', 'used wrongfully'],
    confidence: 0.9
})

// Link patterns to theft offence
MATCH (ap:ActionPattern)
WHERE ap.pattern_id IN ['theft_action_001', 'theft_action_002']
MATCH (o:Offence {type: 'theft'})
MERGE (ap)-[:MATCHES {confidence: 0.95}]->(o)
```

**Query Patterns**:

The knowledge graph supports various query patterns:

1. **Find sections by action**:
```cypher
MATCH (ap:ActionPattern)-[:MATCHES]->(o:Offence)<-[:DEFINES]-(s:Section)
WHERE toLower(ap.text) CONTAINS toLower($action)
RETURN s.section_id, s.title
```

2. **Find legal requirements for offence**:
```cypher
MATCH (s:Section)-[:DEFINES]->(o:Offence)
MATCH (o)-[r:REQUIRES_MENS_REA|REQUIRES_ACTUS_REUS|REQUIRES_CIRCUMSTANCE]->(le:LegalElement)
WHERE s.section_id = $section_id
RETURN le.name, le.type, r.mandatory
```

3. **Find aggravated forms**:
```cypher
MATCH (base:Offence)<-[:AGGRAVATED_FORM_OF]-(aggravated:Offence)
WHERE base.type = $offence_type
RETURN aggravated.type, aggravated.section_id
```

**Graph Statistics**:

Current knowledge graph contains:
- 32 Section nodes (BNS Chapter XVII)
- 32 Offence nodes
- 32 Punishment nodes
- 150+ ActionPattern nodes (with variations)
- 80+ LegalElement nodes
- 300+ relationships

**Maintenance and Updates**:

The knowledge graph can be extended by:
1. Adding new CSV rows for additional BNS sections
2. Creating new ActionPattern nodes for improved matching
3. Adding LegalElement nodes for refined reasoning
4. Establishing new relationship types for complex legal concepts

---

#### 3.2.8 Module 8: Orchestration Module

**Purpose**: The Orchestration Module coordinates the entire legal query processing pipeline, managing the sequential flow of data through all modules, handling errors, implementing fallback mechanisms, and ensuring system reliability.

**Technology Stack**:
- Framework: Python 3.11+
- Async Support: Python asyncio (optional)
- Logging: Python logging module
- Error Handling: Try-except with graceful degradation

**Implementation Details**:

The Orchestration Module is implemented in `backend/app/services/legal_processing_service.py` (class `LegalProcessingService`).

**Pipeline Architecture**:

The orchestration follows a four-stage pipeline:

```python
class LegalProcessingService:
    def __init__(self):
        self.ollama = ollama_service       # Entity extraction
        self.neo4j = neo4j_service         # Legal reasoning

    def process_legal_query(
        self,
        query: str,
        language: str = "en",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete legal query processing pipeline

        Pipeline Flow:
        1. User Query → Entity Extraction (Phi-3)
        2. Entities → Legal Reasoning (Neo4j)
        3. Legal Analysis → Response Generation (Templates)
        4. Results → Verification & Storage
        """
        start_time = time.time()
        query_id = str(uuid.uuid4())

        # Stage 1: Entity Extraction
        extracted_entities = self._extract_entities_step(query, language)

        # Stage 2: Legal Reasoning
        legal_analysis = self._legal_reasoning_step(extracted_entities)

        # Stage 3: Response Generation
        formatted_response = self._response_generation_step(
            legal_analysis, language
        )

        # Stage 4: Verification and Storage
        verified_result = self._verification_and_storage_step(
            query_id, query, language, extracted_entities,
            legal_analysis, formatted_response, start_time, user_id
        )

        return verified_result
```

**Stage 1: Entity Extraction**

```python
def _extract_entities_step(
    self,
    query: str,
    language: str
) -> Dict[str, List[str]]:
    """
    Extract factual entities using trained SLM
    """
    try:
        entities = self.ollama.extract_entities(query, language)
        validated_entities = self._validate_extracted_entities(entities)
        logger.info(f"Extracted entities: {validated_entities}")
        return validated_entities

    except Exception as e:
        logger.error(f"Entity extraction failed: {e}")
        # Return empty but valid entity structure
        return {
            "persons": [], "objects": [], "locations": [],
            "actions": [], "intentions": [], "circumstances": [],
            "relationships": []
        }
```

**Entity Validation**:
```python
def _validate_extracted_entities(
    self,
    entities: Dict
) -> Dict[str, List[str]]:
    """
    Validate and normalize extracted entities
    """
    required_keys = [
        "persons", "objects", "locations", "actions",
        "intentions", "circumstances", "relationships"
    ]

    validated = {}
    for key in required_keys:
        if key in entities and isinstance(entities[key], list):
            # Remove duplicates, normalize, filter empty
            validated[key] = list(set([
                item.strip().lower()
                for item in entities[key]
                if item and item.strip()
            ]))
        else:
            validated[key] = []

    return validated
```

**Stage 2: Legal Reasoning**

```python
def _legal_reasoning_step(
    self,
    entities: Dict[str, List[str]]
) -> Dict[str, Any]:
    """
    Perform legal reasoning using Neo4j
    """
    try:
        applicable_laws = self.neo4j.find_applicable_laws(entities)

        # Calculate overall confidence
        if applicable_laws:
            confidence = max(law.get("confidence", 0.5)
                           for law in applicable_laws)
        else:
            confidence = 0.0

        return {
            "applicable_laws": applicable_laws,
            "confidence_score": confidence,
            "entities": entities,
            "reasoning_method": "neo4j_graph" if applicable_laws
                              else "no_match"
        }

    except Exception as e:
        logger.error(f"Legal reasoning failed: {e}")
        return {
            "applicable_laws": [],
            "confidence_score": 0.0,
            "entities": entities,
            "error": str(e)
        }
```

**Stage 3: Response Generation**

```python
def _response_generation_step(
    self,
    legal_analysis: Dict[str, Any],
    language: str
) -> str:
    """
    Generate citizen-friendly response
    """
    try:
        response = self.ollama.format_legal_response(
            legal_analysis,
            language
        )
        logger.info("Generated legal response")
        return response

    except Exception as e:
        logger.error(f"Response generation failed: {e}")
        return self._get_error_response_template(legal_analysis, language)
```

**Stage 4: Verification and Storage**

```python
def _verification_and_storage_step(
    self,
    query_id: str,
    query: str,
    language: str,
    entities: Dict,
    legal_analysis: Dict,
    response: str,
    start_time: float,
    user_id: Optional[str]
) -> Dict[str, Any]:
    """
    Verify results and prepare final response
    """
    processing_time = time.time() - start_time

    # Fact verification
    verified = self._verify_legal_facts(legal_analysis)

    # Build final result
    result = {
        "query_id": query_id,
        "query": query,
        "language": language,
        "entities": entities,
        "applicable_laws": legal_analysis.get("applicable_laws", []),
        "legal_advice": response,
        "confidence_score": legal_analysis.get("confidence_score", 0.0),
        "processing_time": round(processing_time, 2),
        "timestamp": datetime.utcnow().isoformat(),
        "verified": verified,
        "disclaimers": self._get_disclaimers(language),
        "system_info": {
            "version": "2.0.0",
            "model": "phi3-trained",
            "reasoning": "neo4j-graph-based"
        }
    }

    # Future: Store in database
    # self.database.store_query_result(result, user_id)

    return result
```

**Error Handling and Fallbacks**:

The orchestration module implements comprehensive error handling:

1. **Stage-level Fallbacks**:
```python
def _create_error_response(
    self,
    query_id: str,
    query: str,
    error: str,
    error_time: float
) -> Dict[str, Any]:
    """
    Create error response with diagnostic information
    """
    return {
        "query_id": query_id,
        "query": query,
        "error": error,
        "applicable_laws": [],
        "legal_advice": "Unable to process query due to system error.",
        "confidence_score": 0.0,
        "processing_time": error_time,
        "timestamp": datetime.utcnow().isoformat(),
        "disclaimers": ["System error occurred. Please try again."],
        "system_info": {"status": "error"}
    }
```

2. **Graceful Degradation**:
   - Entity extraction failure → Empty entities, continue processing
   - Neo4j unavailable → Fallback rule-based reasoning
   - Response generation failure → Template-based fallback
   - Complete system failure → Informative error response

3. **Logging and Monitoring**:
```python
logger.info(f"Processing legal query {query_id}")
logger.info(f"Step 1: Extracting entities")
logger.info(f"Step 2: Legal reasoning")
logger.info(f"Step 3: Response generation")
logger.info(f"Query processed in {processing_time:.2f}s")
logger.error(f"Query failed: {error}")
```

**Performance Monitoring**:

The orchestration module tracks:
- Total processing time
- Per-stage timing (future enhancement)
- Success/failure rates
- Confidence score distribution
- Entity extraction quality metrics

**Quality Assurance**:

```python
def _verify_legal_facts(self, legal_analysis: Dict) -> bool:
    """
    Verify legal analysis meets quality standards
    """
    laws = legal_analysis.get("applicable_laws", [])

    # Verification checks
    if not laws:
        return False

    # All laws must have required fields
    required_fields = ["section", "title", "confidence"]
    for law in laws:
        if not all(field in law for field in required_fields):
            return False

    # Confidence must be reasonable
    if any(law.get("confidence", 0) < 0.3 for law in laws):
        return False

    return True
```

**Future Enhancements**:
- Asynchronous processing for improved concurrency
- Distributed tracing for debugging
- Performance caching layer
- Database integration for query history
- Real-time progress updates via WebSocket

---

### 3.3 Data Flow and System Integration

**Complete Query Processing Flow**:

```
1. User submits query via React frontend
   ↓
2. POST request to /api/v1/legal/query (API Gateway)
   ↓
3. Request validation (Pydantic models)
   ↓
4. Orchestration Service initiates pipeline
   ↓
5. Entity Extraction Module (Phi-3)
   - Extracts 7 entity categories
   - Returns JSON structure
   ↓
6. Legal Reasoning Module (Neo4j)
   - Cypher graph queries
   - Pattern matching
   - Confidence scoring
   ↓
7. Response Generation Module (Templates)
   - Structures legal advice
   - Adds disclaimers
   - Formats for readability
   ↓
8. Verification & Response Assembly (Orchestration)
   - Quality checks
   - Final JSON construction
   ↓
9. HTTP response to frontend (API Gateway)
   ↓
10. Display results to user (React UI)
```

**Inter-Module Communication**:

All modules communicate via Python function calls with standardized data structures:

- **Entity Structure**: Dictionary with 7 keys (persons, objects, locations, actions, intentions, circumstances, relationships), each containing a list of strings

- **Legal Analysis Structure**: Dictionary containing applicable_laws (list), confidence_score (float), entities (dict), reasoning_method (string)

- **Final Response Structure**: Dictionary with 11 keys including query_id, entities, applicable_laws, legal_advice, confidence_score, processing_time, disclaimers, etc.

**Error Propagation**:

Errors are caught at each module level and propagated upward with context:
- Module-level exceptions are logged
- Fallback mechanisms activate automatically
- User receives informative error messages
- System continues operation (graceful degradation)

---

### 3.4 Technology Justification

**Choice of Technologies**:

1. **React.js for Frontend**:
   - Component-based architecture for modularity
   - Large ecosystem and community support
   - Excellent performance with virtual DOM
   - Material-UI provides accessible, professional UI components

2. **FastAPI for Backend**:
   - Modern Python framework with automatic API documentation
   - Native async support for scalability
   - Pydantic for robust data validation
   - High performance comparable to Node.js

3. **Neo4j for Knowledge Graph**:
   - Native graph database optimized for relationship queries
   - Cypher query language designed for graph traversal
   - Superior performance for complex legal reasoning patterns
   - Flexible schema for evolving legal knowledge

4. **Phi-3 (Microsoft) for SLM**:
   - Small model size (3.8B parameters) suitable for local deployment
   - Good balance of accuracy and performance
   - Specialized for instruction-following tasks
   - Can run on consumer hardware via Ollama

5. **Ollama for Model Runtime**:
   - Simple local LLM deployment
   - No cloud dependencies or API costs
   - Easy model management
   - REST API for integration

**Advantages of Architecture**:

1. **Determinism**: Graph-based reasoning ensures consistent results for identical inputs
2. **Explainability**: Graph paths show reasoning process
3. **Scalability**: Modular design allows independent scaling of components
4. **Maintainability**: Clear separation of concerns, well-documented modules
5. **Extensibility**: New BNS sections can be added via graph data, not code changes
6. **Reliability**: Multiple fallback mechanisms ensure system availability

---

### 3.5 Experimental Setup and Evaluation

**Development Environment**:
- Operating System: Windows 10/11, Linux (Ubuntu 20.04+)
- Python Version: 3.11+
- Node.js Version: 16+
- Neo4j Version: 5.x Community Edition
- Ollama Version: Latest stable

**Dataset**:
- Source: Bharatiya Nyaya Sanhita (BNS) Chapter XVII
- Sections: 32 legal sections (BNS-303 to BNS-334)
- Offence Categories: 10 property offense types
- Format: CSV with section number, title, full text, punishment details

**Performance Metrics**:

1. **Accuracy Metrics**:
   - Legal classification accuracy
   - Entity extraction precision and recall
   - Confidence score correlation with human judgment

2. **Performance Metrics**:
   - Average query processing time
   - Per-module latency
   - System throughput (queries per second)

3. **Quality Metrics**:
   - Response completeness
   - Disclaimer presence
   - Fact verification success rate

**Testing Methodology**:
- Unit tests for individual modules
- Integration tests for complete pipeline
- End-to-end tests with realistic user queries
- Performance benchmarking with load testing tools

---

This concludes the comprehensive methodology section for the LEGALS research paper, providing detailed technical descriptions of all eight system modules, their implementations, interactions, and the overall system architecture.
