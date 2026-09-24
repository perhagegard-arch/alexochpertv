export function renderQuoteCard(content, mode = "hero") {
  const company = content.company
    ? `<span class="quote-company"> · ${esc(content.company)}</span>`
    : "";
  const compactClass = mode === "compact" ? " compact" : "";
  return `
    <div class="quote-card${compactClass}">
      <div class="quote-body">
        <div class="quote-mark" aria-hidden="true">“</div>
        <p class="quote-text">${esc(content.quote)}</p>
        <div class="quote-divider"></div>
        <p class="quote-author">${esc(content.author)}${company}</p>
      </div>
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
