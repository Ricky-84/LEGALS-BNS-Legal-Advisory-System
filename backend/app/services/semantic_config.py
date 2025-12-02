"""
Configuration for Semantic Enhancement
Implemented by: Vaishnav
"""

# Semantic Similarity Configuration
SEMANTIC_SIMILARITY_THRESHOLD = 0.75
SEMANTIC_CACHE_SIZE = 1000
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Lightweight model, 22MB

# Alternative model (more accurate but larger)
# EMBEDDING_MODEL = "all-mpnet-base-v2"  # 438MB, higher accuracy

# Cache settings
SEMANTIC_CACHE_FILE = "data/semantic_query_cache.pkl"
SEMANTIC_EMBEDDINGS_CACHE_FILE = "data/semantic_cache.pkl"

# Performance settings
BATCH_PROCESSING_SIZE = 32
ENABLE_SEMANTIC_ENHANCEMENT = True
SEMANTIC_CACHE_TTL = 3600  # 1 hour in seconds

# Logging
SEMANTIC_LOG_LEVEL = "INFO"

# Model download settings
SENTENCE_TRANSFORMERS_HOME = "./models"
