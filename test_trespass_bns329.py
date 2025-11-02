#!/usr/bin/env python3
"""
Test BNS-329 (Criminal Trespass) Detection
Testing with varying complexity scenarios
"""
import requests
import json

def test_trespass_scenarios():
    """Test BNS-329 detection with different scenarios"""
    base_url = "http://localhost:8000"

    test_cases = [
        {
            "name": "Simple House Trespass",
            "query": "Someone entered my house without permission",
            "expected": ["BNS-329"]
        },
        {
            "name": "Breaking Into Property",
            "query": "A person broke into my property illegally last night",
            "expected": ["BNS-329"]
        },
        {
            "name": "Climbing Over Fence",
            "query": "Two men climbed over my compound fence and trespassed on my land",
            "expected": ["BNS-329"]
        },
        {
            "name": "Unauthorized Building Entry",
            "query": "Someone unlawfully entered my office building premises",
            "expected": ["BNS-329"]
        },
        {
            "name": "Garden Intrusion",
            "query": "A person trespassed into my garden and damaged my plants",
            "expected": ["BNS-329"]
        },
        {
            "name": "Roof Access Trespass",
            "query": "Someone invaded my roof area by scaling the boundary wall",
            "expected": ["BNS-329"]
        },
        {
            "name": "Edge Case - Public Road",
            "query": "Someone stole my phone on the public road",
            "expected": ["BNS-303"]  # Should NOT detect trespass
        }
    ]

    print("Testing BNS-329 (Criminal Trespass) Detection")
    print("=" * 50)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Query: {test_case['query']}")

        try:
            response = requests.post(
                f"{base_url}/api/v1/legal/query",
                json={"query": test_case["query"], "language": "en"},
                timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                detected_laws = [law["section"] for law in result.get("applicable_laws", [])]

                print(f"Detected: {detected_laws}")
                print(f"Expected: {test_case['expected']}")

                # Check if BNS-329 is correctly detected/not detected
                if "BNS-329" in test_case["expected"]:
                    if "BNS-329" in detected_laws:
                        print("PASS - Criminal trespass correctly detected")
                        # Print confidence and reasoning
                        for law in result["applicable_laws"]:
                            if law["section"] == "BNS-329":
                                print(f"   Confidence: {law['confidence']:.0%}")
                                print(f"   Reasoning: {law['reasoning']}")
                    else:
                        print("FAIL - Criminal trespass not detected")
                else:
                    if "BNS-329" not in detected_laws:
                        print("PASS - Criminal trespass correctly NOT detected")
                    else:
                        print("FAIL - False positive: Criminal trespass incorrectly detected")

            else:
                print(f"API Error: {response.status_code}")

        except Exception as e:
            print(f"Test failed: {e}")

    print("\n" + "=" * 50)
    print("BNS-329 Criminal Trespass Test Complete!")

if __name__ == "__main__":
    test_trespass_scenarios()