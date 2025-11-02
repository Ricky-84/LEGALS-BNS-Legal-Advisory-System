#!/usr/bin/env python3
"""
Test BNS-308 (Extortion) Detection
Testing with varying complexity scenarios
"""
import requests
import json

def test_extortion_scenarios():
    """Test BNS-308 detection with different scenarios"""
    base_url = "http://localhost:8000"

    test_cases = [
        {
            "name": "Simple Threat for Money",
            "query": "Someone threatened to harm me if I don't pay them money",
            "expected": ["BNS-308"]
        },
        {
            "name": "Blackmail with Photos",
            "query": "A person blackmailed me with compromising photos and demanded cash",
            "expected": ["BNS-308"]
        },
        {
            "name": "Business Intimidation",
            "query": "Local goons intimidated me and forced me to pay protection money for my shop",
            "expected": ["BNS-308"]
        },
        {
            "name": "Online Extortion",
            "query": "Someone threatened to expose my personal information unless I transfer money to their account",
            "expected": ["BNS-308"]
        },
        {
            "name": "Violence Threat",
            "query": "He threatened to beat me up if I don't give him my property",
            "expected": ["BNS-308"]
        },
        {
            "name": "Reputation Damage Threat",
            "query": "They coerced me into paying money by threatening to damage my business reputation",
            "expected": ["BNS-308"]
        },
        {
            "name": "Edge Case - Simple Theft",
            "query": "Someone stole my wallet from my pocket",
            "expected": ["BNS-303"]  # Should NOT detect extortion
        }
    ]

    print("Testing BNS-308 (Extortion) Detection")
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

                # Check if BNS-308 is correctly detected/not detected
                if "BNS-308" in test_case["expected"]:
                    if "BNS-308" in detected_laws:
                        print("PASS - Extortion correctly detected")
                        # Print confidence and reasoning
                        for law in result["applicable_laws"]:
                            if law["section"] == "BNS-308":
                                print(f"   Confidence: {law['confidence']:.0%}")
                                print(f"   Reasoning: {law['reasoning']}")
                    else:
                        print("FAIL - Extortion not detected")
                else:
                    if "BNS-308" not in detected_laws:
                        print("PASS - Extortion correctly NOT detected")
                    else:
                        print("FAIL - False positive: Extortion incorrectly detected")

            else:
                print(f"API Error: {response.status_code}")

        except Exception as e:
            print(f"Test failed: {e}")

    print("\n" + "=" * 50)
    print("BNS-308 Extortion Test Complete!")

if __name__ == "__main__":
    test_extortion_scenarios()