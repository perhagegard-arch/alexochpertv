export function renderBirthdayCard(content, mode = "hero") {
  const compactClass = mode === "compact" ? " compact" : "";

  if (content.people.length === 0) {
    return `
      <div class="birthday-card${compactClass}">
        <p class="birthday-title">🎂 Födelsedagar</p>
        <p class="birthday-fallback">Inga födelsedagar inom kort</p>
      </div>
    `;
  }

  const peopleHTML = content.people.map((p) => `
    <li class="birthday-person">
      <span class="birthday-name">${esc(p.name)}</span>
      <span class="birthday-label">${esc(p.label)}</span>
    </li>
  `).join("");

  return `
    <div class="birthday-card${compactClass}">
      <p class="birthday-title">🎂 Födelsedagar</p>
      <ul class="birthday-list">${peopleHTML}</ul>
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
