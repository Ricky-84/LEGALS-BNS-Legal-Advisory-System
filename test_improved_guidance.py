#!/usr/bin/env python3
"""Test the improved legal guidance"""
import requests
import json

def test_improved_guidance():
    print("Testing Improved Legal Guidance")
    print("=" * 50)

    test_cases = [
        {
            "name": "iPhone Theft at College",
            "query": "Someone stole my iPhone from my bag in college library"
        },
        {
            "name": "Employee Laptop Theft",
            "query": "My employee took the company laptop from office"
        },
        {
            "name": "Robbery with Threat",
            "query": "A robber threatened me with knife and took my wallet on street"
        }
    ]

    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Query: {test_case['query']}")
        print()

        try:
            payload = {
                "query": test_case['query'],
                "language": "en"
            }

            response = requests.post(
                "http://localhost:8000/api/v1/legal/query",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()

                print("LEGAL GUIDANCE:")
                print("-" * 30)
                print(data.get('legal_advice', 'No guidance available'))
                print("-" * 30)

                print(f"\nConfidence: {data.get('confidence_score', 0):.0%}")
                print(f"Laws Found: {len(data.get('applicable_laws', []))}")

                for law in data.get('applicable_laws', []):
                    print(f"  • {law['section']}: {law['title']}")

            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.Timeout:
            print("Request timed out (SLM processing...)")
        except Exception as e:
            print(f"Error: {e}")

        print("\n" + "=" * 80)

if __name__ == "__main__":
    test_improved_guidance()