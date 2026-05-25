from pathlib import Path

from flask import Flask, jsonify, render_template, request

from search import VALID_CATEGORIES, FAQSearch

app = Flask(__name__)
faq_search = FAQSearch(Path(__file__).parent / "faq.json")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")
    category = data.get("category")

    if not isinstance(query, str) or not query.strip():
        return jsonify({
            "error": "Please enter a search query.",
            "results": [],
        }), 400

    if category is not None and category != "" and category not in VALID_CATEGORIES:
        return jsonify({
            "error": f"Invalid category. Must be one of: {', '.join(sorted(VALID_CATEGORIES))}.",
            "results": [],
        }), 400

    results = faq_search.search(query, category=category or None)
    return jsonify({
        "query": query,
        "category": category or None,
        "results": results,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
