#!/usr/bin/env python3
"""
Test API Endpoints for Frontend Integration
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"PASS Health Check: {data['status']}")
            print(f"   Ollama: {data['services']['ollama']}")
            return True
        else:
            print(f"FAIL Health Check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL Health Check error: {e}")
        return False

def test_system_status():
    """Test system status endpoint"""
    print("\nTesting System Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/legal/system-status")
        if response.status_code == 200:
            data = response.json()
            print(f"PASS System Status: {data['status']}")
            print(f"   Services: {data['services']}")
            return True
        else:
            print(f"FAIL System Status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL System Status error: {e}")
        return False

def test_legal_query_api():
    """Test the main legal query API"""
    print("\nTesting Legal Query API...")

    test_query = "Someone stole my iPhone from my house"

    payload = {
        "query": test_query,
        "language": "en"
    }

    try:
        print(f"Sending query: {test_query}")
        start_time = time.time()

        response = requests.post(
            f"{BASE_URL}/api/v1/legal/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        processing_time = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            print(f"PASS Legal Query API: Success")
            print(f"   Query ID: {data['query_id']}")
            print(f"   Processing Time: {processing_time:.2f}s")
            print(f"   Laws Found: {len(data['applicable_laws'])}")
            print(f"   Confidence: {data['confidence_score']:.2f}")

            for law in data['applicable_laws']:
                print(f"     - {law['section']}: {law['title']}")

            print(f"   Response Preview: {data['legal_advice'][:100]}...")
            return True
        else:
            print(f"FAIL Legal Query failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"FAIL Legal Query error: {e}")
        return False

def test_entity_extraction_api():
    """Test entity extraction endpoint"""
    print("\nTesting Entity Extraction API...")

    payload = {
        "query": "Employee took laptop from office",
        "language": "en"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/legal/extract-entities",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print(f"PASS Entity Extraction: Success")
            print(f"   Entities: {list(data['entities'].keys())}")

            for category, entities in data['entities'].items():
                if entities and category != "property_value_analysis":
                    print(f"     {category}: {entities}")

            return True
        else:
            print(f"FAIL Entity Extraction failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"FAIL Entity Extraction error: {e}")
        return False

def test_supported_laws_api():
    """Test supported laws endpoint"""
    print("\nTesting Supported Laws API...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/legal/supported-laws")
        if response.status_code == 200:
            data = response.json()
            print(f"PASS Supported Laws: {data['total_sections']} sections")
            for law in data['supported_laws'][:3]:
                print(f"     - {law}")
            print("     ...")
            return True
        else:
            print(f"FAIL Supported Laws failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL Supported Laws error: {e}")
        return False

def main():
    """Run all API tests"""
    print("LEGALS API Endpoint Tests")
    print("=" * 50)

    tests = [
        ("Health Check", test_health_check),
        ("System Status", test_system_status),
        ("Legal Query API", test_legal_query_api),
        ("Entity Extraction API", test_entity_extraction_api),
        ("Supported Laws API", test_supported_laws_api)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"FAIL {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("API TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status} {test_name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\nSUCCESS: All API endpoints working!")
        print("Backend API ready for frontend integration")
    else:
        print(f"\nWARNING: {total - passed} API tests failed")

if __name__ == "__main__":
    main()