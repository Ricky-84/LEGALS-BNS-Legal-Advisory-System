#!/usr/bin/env python3
"""Quick API Test"""
import requests

def quick_test():
    print("Quick API Test")
    print("=" * 30)

    # Test health check
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: {data['status']}")
    except Exception as e:
        print(f"Health Check Error: {e}")

    # Test simple query
    try:
        payload = {"query": "Someone stole my phone", "language": "en"}
        response = requests.post("http://localhost:8000/api/v1/legal/query", json=payload, timeout=30)
        print(f"Legal Query: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Laws Found: {len(data['applicable_laws'])}")
            print(f"  Confidence: {data['confidence_score']}")
        elif response.status_code != 200:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"Legal Query Error: {e}")

if __name__ == "__main__":
    quick_test()