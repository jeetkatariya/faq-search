const form = document.getElementById("search-form");
const queryInput = document.getElementById("query");
const categorySelect = document.getElementById("category");
const messageEl = document.getElementById("message");
const resultsEl = document.getElementById("results");

function setMessage(text, isError = false) {
  messageEl.textContent = text;
  messageEl.classList.toggle("error", isError);
}

function clearResults() {
  resultsEl.innerHTML = "";
}

function badgeClass(category) {
  return `badge badge-${category.toLowerCase()}`;
}

function renderResults(results) {
  clearResults();
  for (const r of results) {
    const li = document.createElement("li");
    li.className = "result-card";
    li.innerHTML = `
      <div class="result-header">
        <h2 class="result-question"></h2>
        <span class="${badgeClass(r.category)}"></span>
      </div>
      <p class="result-answer"></p>
      <div class="result-score">Relevance score: ${r.score}</div>
    `;
    li.querySelector(".result-question").textContent = r.question;
    li.querySelector(".badge").textContent = r.category;
    li.querySelector(".result-answer").textContent = r.answer;
    resultsEl.appendChild(li);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = queryInput.value.trim();
  const category = categorySelect.value;

  if (!query) {
    setMessage("Please enter a search query.", true);
    clearResults();
    return;
  }

  setMessage("Searching...");

  const body = { query };
  if (category) body.category = category;

  try {
    const response = await fetch("/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.error || "Something went wrong.", true);
      clearResults();
      return;
    }

    if (!data.results || data.results.length === 0) {
      const where = category ? ` in "${category}"` : "";
      setMessage(`No results found${where}. Try different keywords${category ? ' or "All categories"' : ""}.`);
      clearResults();
      return;
    }

    const scope = category ? ` in "${category}"` : "";
    setMessage(`Showing top ${data.results.length} result${data.results.length === 1 ? "" : "s"} for "${data.query}"${scope}.`);
    renderResults(data.results);
  } catch (err) {
    setMessage("Network error. Please try again.", true);
    clearResults();
  }
});
