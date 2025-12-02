"""
Download sentence transformer model
This will download the all-MiniLM-L6-v2 model (~22MB) from HuggingFace
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

print("Downloading sentence transformer model...")
print("Model: all-MiniLM-L6-v2 (~22MB)")
print("Source: HuggingFace")
print("-" * 60)

try:
    from sentence_transformers import SentenceTransformer

    print("\nInitializing model (this will download if not cached)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("\n✓ Model downloaded and loaded successfully!")
    print(f"Model max sequence length: {model.max_seq_length}")

    # Test encoding
    print("\nTesting model with sample text...")
    test_text = "stole my phone"
    embedding = model.encode(test_text)
    print(f"✓ Model working! Generated {len(embedding)}-dimensional embedding")

    print("\n" + "="*60)
    print("SUCCESS: Sentence transformer model is ready to use!")
    print("="*60)

except ImportError as e:
    print(f"\n✗ Error: sentence-transformers not installed")
    print("\nPlease install dependencies first:")
    print("  pip install -r requirements-semantic-fixed.txt")
    sys.exit(1)

except Exception as e:
    print(f"\n✗ Error downloading model: {e}")
    sys.exit(1)
