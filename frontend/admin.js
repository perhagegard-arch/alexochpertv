const loginView = document.getElementById("login-view");
const panelView = document.getElementById("panel-view");
const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");
const logoutButton = document.getElementById("logout-button");
const widgetsList = document.getElementById("widgets-list");
const zonesList = document.getElementById("zones-list");
const birthdaySection = document.getElementById("birthday-section");
const birthdayTextarea = document.getElementById("birthday-textarea");
const saveBirthdaysButton = document.getElementById("save-birthdays-button");
const birthdayPreview = document.getElementById("birthday-preview");

function esc(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function checkSession() {
  const resp = await fetch("/admin/api/session");
  const data = await resp.json();
  if (data.logged_in) {
    showPanel();
  } else {
    showLogin();
  }
}

function showLogin() {
  loginView.hidden = false;
  panelView.hidden = true;
}

function showPanel() {
  loginView.hidden = true;
  panelView.hidden = false;
  loadWidgets();
}

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  loginError.hidden = true;
  const password = document.getElementById("password").value;
  const resp = await fetch("/admin/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });
  if (resp.ok) {
    loginForm.reset();
    showPanel();
  } else {
    loginError.textContent = "Fel lösenord";
    loginError.hidden = false;
  }
});

logoutButton.addEventListener("click", async () => {
  await fetch("/admin/api/logout", { method: "POST" });
  showLogin();
});

async function loadWidgets() {
  const resp = await fetch("/admin/api/widgets");
  if (!resp.ok) return showLogin();
  const widgets = await resp.json();

  widgetsList.innerHTML = widgets.map((w) => `
    <li>
      <label>
        <input type="checkbox" data-widget-id="${esc(w.id)}" ${w.enabled ? "checked" : ""}>
        ${esc(w.label)}
      </label>
    </li>
  `).join("");

  widgetsList.querySelectorAll("input[type=checkbox]").forEach((checkbox) => {
    checkbox.addEventListener("change", () => toggleWidget(checkbox.dataset.widgetId, checkbox.checked));
  });

  const birthdayWidget = widgets.find((w) => w.id === "birthday" && w.editable);
  birthdaySection.hidden = !birthdayWidget;
  if (birthdayWidget) {
    loadBirthdays();
  }

  loadZones(widgets);
}

async function toggleWidget(id, enabled) {
  await fetch(`/admin/api/widgets/${encodeURIComponent(id)}/toggle`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enabled }),
  });
}

async function loadZones(widgets) {
  const resp = await fetch("/admin/api/zones");
  if (!resp.ok) return;
  const zones = await resp.json();

  const optionsHTML = (selectedId) => `
    <option value="">Ingen</option>
    ${widgets.map((w) => `
      <option value="${esc(w.id)}" ${w.id === selectedId ? "selected" : ""}>${esc(w.label)}</option>
    `).join("")}
  `;

  zonesList.innerHTML = zones.map((z) => `
    <li>
      <label>
        ${esc(z.label)}
        <select data-zone-id="${esc(z.id)}">${optionsHTML(z.widget)}</select>
      </label>
    </li>
  `).join("");

  zonesList.querySelectorAll("select").forEach((select) => {
    select.addEventListener("change", () => setZone(select.dataset.zoneId, select.value || null));
  });
}

async function setZone(zoneId, widget) {
  await fetch(`/admin/api/zones/${encodeURIComponent(zoneId)}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ widget }),
  });
}

async function loadBirthdays() {
  const resp = await fetch("/admin/api/birthdays");
  if (!resp.ok) return;
  const data = await resp.json();
  birthdayTextarea.value = data.raw;
}

saveBirthdaysButton.addEventListener("click", async () => {
  const resp = await fetch("/admin/api/birthdays", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ raw: birthdayTextarea.value }),
  });
  if (!resp.ok) return;
  const data = await resp.json();
  renderBirthdayPreview(data);
});

function renderBirthdayPreview({ count, today, invalid }) {
  const todayText = today.length
    ? `Firar idag: ${today.map(esc).join(", ")}.`
    : "Ingen firar idag.";

  const invalidHTML = invalid.length
    ? `<p>${invalid.length} rad${invalid.length === 1 ? "" : "er"} kunde inte tolkas:</p>
       <ul>${invalid.map((line) => `<li class="invalid-line">${esc(line)}</li>`).join("")}</ul>`
    : "";

  birthdayPreview.innerHTML = `
    <p>${count} person${count === 1 ? "" : "er"} tolkade. ${todayText}</p>
    ${invalidHTML}
  `;
}

checkSession();
