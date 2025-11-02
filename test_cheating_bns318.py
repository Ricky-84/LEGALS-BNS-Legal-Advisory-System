#!/usr/bin/env python3
"""
Test BNS-318 (Cheating) Detection
Testing with varying complexity scenarios
"""
import requests
import json

def test_cheating_scenarios():
    """Test BNS-318 detection with different scenarios"""
    base_url = "http://localhost:8000"

    test_cases = [
        {
            "name": "Simple Online Fraud",
            "query": "Someone promised me high returns on investment online but cheated me",
            "expected": ["BNS-318"]
        },
        {
            "name": "Fake Lottery Scam",
            "query": "I received a phone call saying I won a lottery prize but they asked for money and deceived me",
            "expected": ["BNS-318"]
        },
        {
            "name": "Credit Card Fraud",
            "query": "A person tricked me into sharing my credit card details through a fake website",
            "expected": ["BNS-318"]
        },
        {
            "name": "OTP Fraud",
            "query": "Someone called pretending to be from the bank and fraudulently got my OTP and money",
            "expected": ["BNS-318"]
        },
        {
            "name": "Investment Scam",
            "query": "A company promised guaranteed returns on cryptocurrency investment but it was all fraudulent",
            "expected": ["BNS-318"]
        },
        {
            "name": "Job Fraud",
            "query": "They promised me a job but asked for money upfront and then disappeared - I was scammed",
            "expected": ["BNS-318"]
        },
        {
            "name": "Edge Case - Not Cheating",
            "query": "Someone stole my wallet from my pocket on the bus",
            "expected": ["BNS-303"]  # Should NOT detect cheating
        }
    ]

    print("Testing BNS-318 (Cheating) Detection")
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

                # Check if BNS-318 is correctly detected/not detected
                if "BNS-318" in test_case["expected"]:
                    if "BNS-318" in detected_laws:
                        print("PASS - Cheating correctly detected")
                        # Print confidence and reasoning
                        for law in result["applicable_laws"]:
                            if law["section"] == "BNS-318":
                                print(f"   Confidence: {law['confidence']:.0%}")
                                print(f"   Reasoning: {law['reasoning']}")
                    else:
                        print("FAIL - Cheating not detected")
                else:
                    if "BNS-318" not in detected_laws:
                        print("PASS - Cheating correctly NOT detected")
                    else:
                        print("FAIL - False positive: Cheating incorrectly detected")

            else:
                print(f"API Error: {response.status_code}")

        except Exception as e:
            print(f"Test failed: {e}")

    print("\n" + "=" * 50)
    print("BNS-318 Cheating Test Complete!")

if __name__ == "__main__":
    test_cheating_scenarios()