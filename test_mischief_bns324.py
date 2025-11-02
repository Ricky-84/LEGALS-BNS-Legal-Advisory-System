#!/usr/bin/env python3
"""
Test BNS-324 (Mischief) Detection
Testing with varying complexity scenarios
"""
import requests
import json

def test_mischief_scenarios():
    """Test BNS-324 detection with different scenarios"""
    base_url = "http://localhost:8000"

    test_cases = [
        {
            "name": "Car Vandalism",
            "query": "Someone intentionally damaged my car by scratching it with a key",
            "expected": ["BNS-324"]
        },
        {
            "name": "Window Breaking",
            "query": "A person deliberately broke my house window with a stone",
            "expected": ["BNS-324"]
        },
        {
            "name": "Property Destruction",
            "query": "Vandals destroyed my fence and gate maliciously",
            "expected": ["BNS-324"]
        },
        {
            "name": "Equipment Damage",
            "query": "Someone smashed my computer equipment on purpose out of anger",
            "expected": ["BNS-324"]
        },
        {
            "name": "Furniture Damage",
            "query": "They ruined my furniture willfully to take revenge",
            "expected": ["BNS-324"]
        },
        {
            "name": "Wall Defacement",
            "query": "Someone defaced my building wall by painting graffiti on it",
            "expected": ["BNS-324"]
        },
        {
            "name": "Edge Case - Accidental Damage",
            "query": "My phone got damaged accidentally when it fell",
            "expected": []  # Should NOT detect mischief (no intent)
        }
    ]

    print("Testing BNS-324 (Mischief) Detection")
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

                # Check if BNS-324 is correctly detected/not detected
                if "BNS-324" in test_case["expected"]:
                    if "BNS-324" in detected_laws:
                        print("PASS - Mischief correctly detected")
                        # Print confidence and reasoning
                        for law in result["applicable_laws"]:
                            if law["section"] == "BNS-324":
                                print(f"   Confidence: {law['confidence']:.0%}")
                                print(f"   Reasoning: {law['reasoning']}")
                    else:
                        print("FAIL - Mischief not detected")
                else:
                    if "BNS-324" not in detected_laws:
                        print("PASS - Mischief correctly NOT detected")
                    else:
                        print("FAIL - False positive: Mischief incorrectly detected")

            else:
                print(f"API Error: {response.status_code}")

        except Exception as e:
            print(f"Test failed: {e}")

    print("\n" + "=" * 50)
    print("BNS-324 Mischief Test Complete!")

if __name__ == "__main__":
    test_mischief_scenarios()