from pathlib import Path

import pytest

from search import MAX_RESULTS, FAQSearch

FAQ_PATH = Path(__file__).resolve().parent.parent / "faq.json"


@pytest.fixture(scope="module")
def faq_search():
    return FAQSearch(FAQ_PATH)


def test_matching_query_returns_relevant_result(faq_search):
    results = faq_search.search("reset my password")

    assert len(results) >= 1
    top = results[0]
    assert "password" in top["question"].lower()
    assert top["category"] == "Account"


def test_empty_and_whitespace_query_returns_no_results(faq_search):
    assert faq_search.search("") == []
    assert faq_search.search("   ") == []
    assert faq_search.search("\n\t ") == []


def test_results_capped_at_max(faq_search):
    results = faq_search.search("how do I")
    assert len(results) <= MAX_RESULTS


def test_irrelevant_query_returns_no_results(faq_search):
    results = faq_search.search("quantum chromodynamics lattice")
    assert results == []


def test_category_filter_restricts_corpus(faq_search):
    results = faq_search.search("refund", category="Billing")
    assert len(results) >= 1
    assert all(r["category"] == "Billing" for r in results)


def test_results_sorted_by_score_descending(faq_search):
    results = faq_search.search("payment invoice billing")
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)
