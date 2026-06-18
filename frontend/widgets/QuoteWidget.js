export function renderQuoteCard(content, mode = "hero") {
  const company = content.company
    ? `<p class="quote-company">${esc(content.company)}</p>`
    : "";
  const compactClass = mode === "compact" ? " compact" : "";
  return `
    <div class="quote-card${compactClass}">
      <p class="quote-text">${esc(content.quote)}</p>
      <p class="quote-author">${esc(content.author)}</p>
      ${company}
    </div>
  `;
}

function esc(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
