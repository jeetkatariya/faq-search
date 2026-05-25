import json
from pathlib import Path
from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SCORE_THRESHOLD = 0.3
MAX_RESULTS = 3
VALID_CATEGORIES = {"Billing", "Technical", "Account"}


class FAQSearch:
    def __init__(self, faq_path: Path):
        with open(faq_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

        self._documents = [
            f"{faq['question']} {faq['answer']}" for faq in self.faqs
        ]
        self._vectorizer = TfidfVectorizer(
            stop_words="english",
            lowercase=True,
        )
        self._doc_matrix = self._vectorizer.fit_transform(self._documents)

    def search(self, query: str, category: Optional[str] = None) -> list[dict]:
        if not query or not query.strip():
            return []

        if category is not None and category not in VALID_CATEGORIES:
            return []

        query_vec = self._vectorizer.transform([query.strip()])
        scores = cosine_similarity(query_vec, self._doc_matrix)[0]

        candidates = []
        for idx, score in enumerate(scores):
            faq = self.faqs[idx]
            if category is not None and faq["category"] != category:
                continue
            if score < SCORE_THRESHOLD:
                continue
            candidates.append({
                "id": faq["id"],
                "question": faq["question"],
                "answer": faq["answer"],
                "category": faq["category"],
                "score": round(float(score), 4),
            })

        candidates.sort(key=lambda r: r["score"], reverse=True)
        return candidates[:MAX_RESULTS]
