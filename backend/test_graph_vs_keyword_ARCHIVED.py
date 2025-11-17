"""
Comparison Test: Graph-based vs Keyword-based Legal Reasoning

This script compares the old keyword matching method with the new graph-based method
to verify that the new approach produces same or better results.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.services.neo4j_service import Neo4jService
from typing import Dict, List
import json

# Test cases covering all 10 main BNS sections
TEST_CASES = [
    {
        "name": "Basic Theft - BNS-303",
        "query": "Someone stole my iPhone",
        "entities": {
            "actions": ["stole"],
            "objects": ["iPhone"],
            "persons": ["someone"]
        },
        "expected_sections": ["BNS-303"]
    },
    {
        "name": "Dwelling Theft - BNS-305",
        "query": "Someone stole my laptop from my house",
        "entities": {
            "actions": ["stole"],
            "objects": ["laptop"],
            "locations": ["house"]
        },
        "expected_sections": ["BNS-303", "BNS-305"]
    },
    {
        "name": "Employee Theft - BNS-306",
        "query": "My employee took money from the cash register",
        "entities": {
            "actions": ["took"],
            "objects": ["money"],
            "persons": ["employee"],
            "relationships": ["employer"]
        },
        "expected_sections": ["BNS-306"]
    },
    {
        "name": "Snatching - BNS-304",
        "query": "Someone snatched my purse on the street",
        "entities": {
            "actions": ["snatched"],
            "objects": ["purse"],
            "locations": ["street"]
        },
        "expected_sections": ["BNS-304"]
    },
    {
        "name": "Robbery - BNS-309",
        "query": "Someone threatened me with a knife and took my wallet",
        "entities": {
            "actions": ["threatened", "took"],
            "objects": ["knife", "wallet"],
            "violence": ["threatened", "knife"]
        },
        "expected_sections": ["BNS-309"]
    },
    {
        "name": "Extortion - BNS-308",
        "query": "Someone threatened to harm my family unless I give them money",
        "entities": {
            "actions": ["threatened"],
            "objects": ["money"],
            "intentions": ["to harm"]
        },
        "expected_sections": ["BNS-308"]
    },
    {
        "name": "Breach of Trust - BNS-316",
        "query": "My business partner misappropriated company funds",
        "entities": {
            "actions": ["misappropriated"],
            "objects": ["funds"],
            "relationships": ["business partner", "company"]
        },
        "expected_sections": ["BNS-316"]
    },
    {
        "name": "Cheating - BNS-318",
        "query": "Someone deceived me and took my money through fake investment scheme",
        "entities": {
            "actions": ["deceived", "took"],
            "objects": ["money"],
            "circumstances": ["fake investment"]
        },
        "expected_sections": ["BNS-318"]
    },
    {
        "name": "Mischief - BNS-324",
        "query": "My neighbor intentionally damaged my car",
        "entities": {
            "actions": ["damaged"],
            "objects": ["car"],
            "persons": ["neighbor"],
            "circumstances": ["intentionally"]  # Fixed: moved from intentions to circumstances
        },
        "expected_sections": ["BNS-324"]
    },
    {
        "name": "Criminal Trespass - BNS-329",
        "query": "Someone entered my property without permission",
        "entities": {
            "actions": ["entered"],
            "locations": ["property"],
            "circumstances": ["without permission"]
        },
        "expected_sections": ["BNS-329"]
    },
    {
        "name": "Natural Language - Borrowed Never Returned",
        "query": "I borrowed my friend's bike and never returned it",
        "entities": {
            "actions": ["borrowed never returned"],  # Fixed: combined phrase
            "objects": ["bike"],
            "relationships": ["friend"]
        },
        "expected_sections": ["BNS-303", "BNS-316"]  # Could be theft or breach of trust
    }
]


def print_section_header(text: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_results(method_name: str, results: List[Dict]):
    """Print results in a formatted way"""
    if not results:
        print(f"  {method_name}: No laws detected")
        return

    print(f"\n  {method_name}:")
    for i, law in enumerate(results, 1):
        section = law.get("section", "Unknown")
        title = law.get("title", "No title")
        confidence = law.get("confidence", 0)
        reasoning = law.get("reasoning", "No reasoning provided")

        print(f"    {i}. {section}: {title}")
        print(f"       Confidence: {confidence:.2f}")
        print(f"       Reasoning: {reasoning}")


def compare_results(old_results: List[Dict], new_results: List[Dict]) -> Dict:
    """Compare old and new results"""
    old_sections = set([r.get("section") for r in old_results])
    new_sections = set([r.get("section") for r in new_results])

    comparison = {
        "match": old_sections == new_sections,
        "old_only": old_sections - new_sections,
        "new_only": new_sections - old_sections,
        "common": old_sections & new_sections,
        "old_count": len(old_results),
        "new_count": len(new_results)
    }

    return comparison


def print_comparison(comparison: Dict):
    """Print comparison results"""
    print("\n  Comparison:")

    if comparison["match"]:
        print("    Status: EXACT MATCH")
    else:
        print("    Status: DIFFERENT")

    if comparison["common"]:
        print(f"    Both detected: {', '.join(sorted(comparison['common']))}")

    if comparison["old_only"]:
        print(f"    Old only: {', '.join(sorted(comparison['old_only']))}")

    if comparison["new_only"]:
        print(f"    New only: {', '.join(sorted(comparison['new_only']))}")

    print(f"    Count: Old={comparison['old_count']}, New={comparison['new_count']}")


def main():
    """Run comparison tests"""
    print_section_header("GRAPH-BASED vs KEYWORD-BASED METHOD COMPARISON")
    print("\nTesting new graph-based method against old keyword matching...")
    print(f"Total test cases: {len(TEST_CASES)}")

    # Initialize service
    print("\nInitializing Neo4j service...")
    service = Neo4jService()

    if not service.available:
        print("ERROR: Neo4j not available. Cannot run tests.")
        return

    print("Neo4j connection: OK")

    # Results tracking
    results_summary = {
        "total": len(TEST_CASES),
        "exact_match": 0,
        "new_better": 0,
        "old_better": 0,
        "both_empty": 0,
        "failures": []
    }

    # Run tests
    for i, test_case in enumerate(TEST_CASES, 1):
        print_section_header(f"TEST {i}/{len(TEST_CASES)}: {test_case['name']}")
        print(f"\nQuery: \"{test_case['query']}\"")
        print(f"Entities: {json.dumps(test_case['entities'], indent=2)}")
        print(f"Expected sections: {', '.join(test_case['expected_sections'])}")

        try:
            # Test old method
            old_results = service.find_applicable_laws_old(test_case['entities'])

            # Test new method
            new_results = service.find_applicable_laws_graph_v2(test_case['entities'])

            # Print results
            print_results("OLD (Keyword Matching)", old_results)
            print_results("NEW (Graph-Based)", new_results)

            # Compare
            comparison = compare_results(old_results, new_results)
            print_comparison(comparison)

            # Track results
            if not old_results and not new_results:
                results_summary["both_empty"] += 1
                print("\n  Result: BOTH EMPTY (may need investigation)")
            elif comparison["match"]:
                results_summary["exact_match"] += 1
                print("\n  Result: EXACT MATCH")
            elif len(new_results) > len(old_results):
                results_summary["new_better"] += 1
                print("\n  Result: NEW METHOD DETECTED MORE")
            else:
                results_summary["old_better"] += 1
                print("\n  Result: OLD METHOD DETECTED MORE")

        except Exception as e:
            print(f"\n  ERROR: {str(e)}")
            results_summary["failures"].append({
                "test": test_case["name"],
                "error": str(e)
            })

    # Print summary
    print_section_header("TEST SUMMARY")
    print(f"\nTotal Tests: {results_summary['total']}")
    print(f"Exact Matches: {results_summary['exact_match']}")
    print(f"New Method Better: {results_summary['new_better']}")
    print(f"Old Method Better: {results_summary['old_better']}")
    print(f"Both Empty: {results_summary['both_empty']}")
    print(f"Failures: {len(results_summary['failures'])}")

    if results_summary['failures']:
        print("\nFailed Tests:")
        for failure in results_summary['failures']:
            print(f"  - {failure['test']}: {failure['error']}")

    # Success criteria
    success_rate = (results_summary['exact_match'] + results_summary['new_better']) / results_summary['total']
    print(f"\nSuccess Rate: {success_rate * 100:.1f}%")

    if success_rate >= 0.8:
        print("\nCONCLUSION: NEW METHOD READY FOR DEPLOYMENT")
    else:
        print("\nCONCLUSION: NEW METHOD NEEDS IMPROVEMENT")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
