#!/usr/bin/env python3
"""
Test BNS-316 (Criminal Breach of Trust) Detection
Testing with varying complexity scenarios
"""
import requests
import json

def test_breach_of_trust_scenarios():
    """Test BNS-316 detection with different scenarios"""
    base_url = "http://localhost:8000"

    test_cases = [
        {
            "name": "Employee Trust Breach",
            "query": "I entrusted my manager with company funds but he misappropriated the money for personal use",
            "expected": ["BNS-316"]
        },
        {
            "name": "Business Partner Fraud",
            "query": "My business partner was handling our joint account but dishonestly misused the funds",
            "expected": ["BNS-316"]
        },
        {
            "name": "Agent Betrayal",
            "query": "I gave my agent responsibility for property sales but he betrayed my trust and kept the money",
            "expected": ["BNS-316"]
        },
        {
            "name": "Trustee Misconduct",
            "query": "The trustee was in charge of managing the estate but embezzled the funds",
            "expected": ["BNS-316"]
        },
        {
            "name": "Employee Embezzlement",
            "query": "My employee was responsible for handling cash but misappropriated company money",
            "expected": ["BNS-316"]
        },
        {
            "name": "Director Misappropriation",
            "query": "The director was entrusted with investor funds but used them for unauthorized personal expenses",
            "expected": ["BNS-316"]
        },
        {
            "name": "Edge Case - Simple Theft",
            "query": "Someone stole money from my wallet",
            "expected": ["BNS-303"]  # Should NOT detect breach of trust
        }
    ]

    print("Testing BNS-316 (Criminal Breach of Trust) Detection")
    print("=" * 60)

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

                # Check if BNS-316 is correctly detected/not detected
                if "BNS-316" in test_case["expected"]:
                    if "BNS-316" in detected_laws:
                        print("PASS - Breach of trust correctly detected")
                        # Print confidence and reasoning
                        for law in result["applicable_laws"]:
                            if law["section"] == "BNS-316":
                                print(f"   Confidence: {law['confidence']:.0%}")
                                print(f"   Reasoning: {law['reasoning']}")
                    else:
                        print("FAIL - Breach of trust not detected")
                else:
                    if "BNS-316" not in detected_laws:
                        print("PASS - Breach of trust correctly NOT detected")
                    else:
                        print("FAIL - False positive: Breach of trust incorrectly detected")

            else:
                print(f"API Error: {response.status_code}")

        except Exception as e:
            print(f"Test failed: {e}")

    print("\n" + "=" * 60)
    print("BNS-316 Criminal Breach of Trust Test Complete!")

if __name__ == "__main__":
    test_breach_of_trust_scenarios()