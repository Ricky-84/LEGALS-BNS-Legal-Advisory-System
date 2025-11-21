#!/usr/bin/env python3
"""
Test BNS-304 (Snatching) Detection
Testing with varying complexity scenarios
"""
import requests
import json

def test_snatching_scenarios():
    """Test BNS-304 detection with different scenarios"""
    base_url = "http://localhost:8000"

    test_cases = [
        {
            "name": "Simple Snatching",
            "query": "Someone snatched my chain on the street",
            "expected": ["BNS-304"]
        },
        {
            "name": "Motorcycle Snatching",
            "query": "Two men on a motorcycle snatched my purse while I was walking",
            "expected": ["BNS-304"]
        },
        {
            "name": "Chain Snatching with Force",
            "query": "A person suddenly grabbed my gold chain and yanked it off my neck at the bus stop",
            "expected": ["BNS-304"]
        },
        {
            "name": "Phone Snatching",
            "query": "Someone quickly grabbed my phone from my hand and ran away on the road",
            "expected": ["BNS-304"]
        },
        {
            "name": "Complex Snatching",
            "query": "While walking on the footpath, two men on a speeding bike snatched my bag and earrings",
            "expected": ["BNS-304"]
        },
        {
            "name": "Edge Case - Not Snatching",
            "query": "Someone stole my laptop from my office desk",
            "expected": ["BNS-303", "BNS-306"]  # Should NOT detect snatching
        }
    ]

    print("Testing BNS-304 (Snatching) Detection")
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

                # Check if BNS-304 is correctly detected/not detected
                if "BNS-304" in test_case["expected"]:
                    if "BNS-304" in detected_laws:
                        print("PASS - Snatching correctly detected")
                        # Print confidence and reasoning
                        for law in result["applicable_laws"]:
                            if law["section"] == "BNS-304":
                                print(f"   Confidence: {law['confidence']:.0%}")
                                print(f"   Reasoning: {law['reasoning']}")
                    else:
                        print("FAIL - Snatching not detected")
                else:
                    if "BNS-304" not in detected_laws:
                        print("PASS - Snatching correctly NOT detected")
                    else:
                        print("FAIL - False positive: Snatching incorrectly detected")

            else:
                print(f"API Error: {response.status_code}")

        except Exception as e:
            print(f"Test failed: {e}")

    print("\n" + "=" * 50)
    print("BNS-304 Snatching Test Complete!")

if __name__ == "__main__":
    test_snatching_scenarios()