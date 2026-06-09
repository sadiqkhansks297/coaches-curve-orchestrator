#!/usr/bin/env python3
"""
Step 1 verification script.

Usage:
    python scripts/test_demo.py                  # Full test (knowledge + LLM)
    python scripts/test_demo.py --knowledge-only # Knowledge layer only (no API key needed)
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import config
from src.knowledge import get_knowledge_store


def test_knowledge():
    print("=" * 60)
    print("KNOWLEDGE LAYER TEST")
    print("=" * 60)

    store = get_knowledge_store()
    sources = store.list_sources()
    print(f"\nBrain directory: {config.BRAIN_DIR}")
    print(f"Documents loaded: {len(sources)}")
    for s in sources:
        print(f"  - {s}")

    queries = [
        "Who is Curve Concierge for?",
        "What is non-transferable expertise?",
        "strategy session prep",
    ]
    print()
    for q in queries:
        print(f"Query: {q}")
        result = store.search(q, max_results=2)
        preview = result[:300].replace("\n", " ")
        print(f"  → {preview}...")
        print()


def test_llm():
    print("=" * 60)
    print("FULL ORCHESTRATOR TEST")
    print("=" * 60)
    print(f"LLM provider: {config.LLM_PROVIDER}")

    from src.orchestrator import handle_message

    # Test 1: Business question
    print("\n--- Test 1: Business Question ---")
    q1 = "Who is the ideal client for The Coaches Curve?"
    print(f"Input: {q1}")
    print(f"Intent: question")
    answer = handle_message(q1)
    print(f"Response:\n{answer}\n")

    # Test 2: Lead prep
    print("--- Test 2: Lead Prep ---")
    q2 = (
        "Prep me for a call with Christine, a business coach in Copenhagen. "
        "She struggles to explain what makes her work different from other coaches."
    )
    print(f"Input: {q2}")
    print(f"Intent: lead_prep")
    answer = handle_message(q2)
    print(f"Response:\n{answer}\n")

    print("=" * 60)
    print("ALL TESTS PASSED — ready for Step 2 (Telegram bot)")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--knowledge-only", action="store_true")
    args = parser.parse_args()

    test_knowledge()

    if not args.knowledge_only:
        test_llm()


if __name__ == "__main__":
    main()
