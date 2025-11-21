#!/usr/bin/env python3
"""
Test Complex Multi-Section BNS Detection
Testing realistic scenarios that involve multiple applicable laws
"""
import requests
import json

def test_complex_scenarios():
    """Test complex scenarios with multiple applicable BNS sections"""
    base_url = "http://localhost:8000"

    test_cases = [
        {
            "name": "Home Invasion with Multiple Crimes",
            "query": "Last night someone broke into my house without permission, threatened me with a knife, stole my laptop and jewelry, and then demanded Rs. 50,000 or they would hurt my family. They also smashed my television before leaving.",
            "expected_sections": ["BNS-329", "BNS-308", "BNS-303", "BNS-324"],
            "description": "Trespass + Extortion + Theft + Mischief"
        },
        {
            "name": "Employee Fraud and Trust Violation",
            "query": "My company accountant was entrusted with managing our financial accounts. Over six months, he misappropriated Rs. 5 lakh from company funds for his personal expenses. When confronted, he threatened to destroy important company documents unless we let him go quietly. He also cheated us by creating fake invoices to cover his tracks.",
            "expected_sections": ["BNS-316", "BNS-308", "BNS-318"],
            "description": "Breach of Trust + Extortion + Cheating"
        },
        {
            "name": "Chain Snatching with Extortion Follow-up",
            "query": "Two men on a motorcycle snatched my gold chain worth Rs. 80,000 near the market. Later, they called me and threatened to harm my daughter unless I transfer another Rs. 1 lakh to their account. They said they know where I live and work.",
            "expected_sections": ["BNS-304", "BNS-308"],
            "description": "Snatching + Extortion"
        },
        {
            "name": "Business Partner Comprehensive Fraud",
            "query": "My business partner, who I entrusted with our joint venture funds of Rs. 10 lakh, deceived me by creating fake investment documents and misappropriated the entire amount for his personal use. When I discovered this, he threatened to defame my reputation in the industry unless I stayed quiet. He also vandalized my office by breaking windows and destroying equipment out of spite.",
            "expected_sections": ["BNS-316", "BNS-318", "BNS-308", "BNS-324"],
            "description": "Breach of Trust + Cheating + Extortion + Mischief"
        },
        {
            "name": "Online Fraud with Multiple Deceptions",
            "query": "I was approached online by someone claiming to be an investment advisor. They promised guaranteed returns of 30% and cheated me into investing Rs. 3 lakh in a fake cryptocurrency scheme. When I asked for my money back, they threatened to expose my personal photos unless I invest another Rs. 2 lakh. The entire investment platform was fraudulent.",
            "expected_sections": ["BNS-318", "BNS-308"],
            "description": "Cheating + Extortion"
        },
        {
            "name": "Property Dispute with Violence and Damage",
            "query": "My neighbor illegally entered my property by climbing over the boundary wall. He then threatened me with physical violence, demanding I sell my land to him at a low price. When I refused, he deliberately damaged my garden, destroyed my plants, and broke my water pipes. He also stole some gardening tools.",
            "expected_sections": ["BNS-329", "BNS-308", "BNS-324", "BNS-303"],
            "description": "Trespass + Extortion + Mischief + Theft"
        },
        {
            "name": "Corporate Executive Embezzlement Case",
            "query": "Our company director, who was entrusted with investor funds worth Rs. 50 lakh, misused the money for unauthorized personal expenses including buying luxury cars and property. When the board started investigating, he threatened to leak confidential company information and destroy financial records. He also created fake documents to deceive auditors about the missing funds.",
            "expected_sections": ["BNS-316", "BNS-308", "BNS-318"],
            "description": "Breach of Trust + Extortion + Cheating"
        },
        {
            "name": "Domestic Helper Betrayal",
            "query": "I entrusted my domestic helper with house keys and access to my safe. She betrayed my trust by stealing cash, jewelry worth Rs. 2 lakh, and important documents. When I confronted her, she threatened to file false cases against me unless I let her go without police involvement. She also intentionally broke my expensive vase out of anger.",
            "expected_sections": ["BNS-316", "BNS-303", "BNS-308", "BNS-324"],
            "description": "Breach of Trust + Theft + Extortion + Mischief"
        }
    ]

    print("Testing Complex Multi-Section BNS Detection")
    print("=" * 60)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        print(f"Expected Sections: {test_case['expected_sections']}")

        try:
            response = requests.post(
                f"{base_url}/api/v1/legal/query",
                json={"query": test_case["query"], "language": "en"},
                timeout=20
            )

            if response.status_code == 200:
                result = response.json()
                detected_laws = [law["section"] for law in result.get("applicable_laws", [])]

                print(f"Detected Sections: {detected_laws}")

                # Calculate detection accuracy
                expected_set = set(test_case["expected_sections"])
                detected_set = set(detected_laws)

                correctly_detected = expected_set.intersection(detected_set)
                missed = expected_set - detected_set
                false_positives = detected_set - expected_set

                accuracy = len(correctly_detected) / len(expected_set) * 100 if expected_set else 100

                print(f"Accuracy: {accuracy:.1f}% ({len(correctly_detected)}/{len(expected_set)} sections)")

                if correctly_detected:
                    print(f"Correctly Detected: {list(correctly_detected)}")
                if missed:
                    print(f"Missed: {list(missed)}")
                if false_positives:
                    print(f"False Positives: {list(false_positives)}")

                # Show details for each detected law
                print("Detection Details:")
                for law in result["applicable_laws"]:
                    print(f"  {law['section']}: {law['title']} (Confidence: {law['confidence']:.0%})")
                    print(f"    Reasoning: {law['reasoning']}")

            else:
                print(f"API Error: {response.status_code}")

        except Exception as e:
            print(f"Test failed: {e}")

        print("-" * 60)

    print("Complex Multi-Section Test Complete!")

if __name__ == "__main__":
    test_complex_scenarios()