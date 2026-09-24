import { renderQuoteCard } from "./widgets/QuoteWidget.js";
import { renderWeatherCard } from "./widgets/WeatherWidget.js";
import { renderBirthdayCard } from "./widgets/BirthdayWidget.js";

const POLL_BUFFER_MS = 500;

// --- Bakgrundslager (cross-fade) ---
const bgLayers = [
  document.getElementById("bg-a"),
  document.getElementById("bg-b"),
];
let activeBg = 0;
let currentBgUrl = null;

async function refreshBackground() {
  try {
    const resp = await fetch("/api/background");
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    if (data.url && data.url !== currentBgUrl) {
      currentBgUrl = data.url;
      const next = 1 - activeBg;
      bgLayers[next].style.backgroundImage = `url('${data.url}')`;
      bgLayers[next].classList.add("visible");
      bgLayers[activeBg].classList.remove("visible");
      activeBg = next;
    }
  } catch (err) {
    console.error("Kunde inte hämta bakgrund:", err);
  }
}

// --- Mittrotation ---
const layers = [
  document.getElementById("card-a"),
  document.getElementById("card-b"),
];
let active = 0;
let lastId = null;

const renderers = {
  quote: renderQuoteCard,
  weather: renderWeatherCard,
  birthday: renderBirthdayCard,
};

async function fetchCard() {
  const url = lastId !== null ? `/api/card?ignore=${lastId}` : "/api/card";
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  return resp.json();
}

function applyCard(layer, card) {
  const render = renderers[card.type];
  layer.innerHTML = render ? render(card.content, "hero") : "";
  if (card.type === "quote") fitQuoteText(layer);
}

function fitQuoteText(layer) {
  const text = layer.querySelector(".quote-text");
  const card = layer.querySelector(".quote-card");
  const body = layer.querySelector(".quote-body");
  if (!text || !card || !body) return;
  // Kortet fyller alltid panelen, så vi mäter innehållet mot ytan innanför paddingen
  const style = getComputedStyle(card);
  const available =
    card.clientHeight - parseFloat(style.paddingTop) - parseFloat(style.paddingBottom);
  let size = 56;
  text.style.fontSize = `${size}px`;
  while (body.offsetHeight > available && size > 16) {
    size -= 1;
    text.style.fontSize = `${size}px`;
  }
}

async function showNext() {
  let card;
  try {
    card = await fetchCard();
  } catch (err) {
    console.error("Kunde inte hämta kort:", err);
    setTimeout(showNext, 10_000);
    return;
  }

  if (card.content?.id != null) lastId = card.content.id;

  refreshBackground();

  const next = 1 - active;
  applyCard(layers[next], card);

  layers[next].classList.add("visible");
  layers[active].classList.remove("visible");
  active = next;

  setTimeout(showNext, card.display_seconds * 1000 + POLL_BUFFER_MS);
}

showNext();

const ZONE_IDS = ["left-top", "left-bottom"];
const zoneLastId = {};

async function showZone(zoneId) {
  const el = document.getElementById(`zone-${zoneId}`);
  let card;
  try {
    const url = zoneLastId[zoneId] != null
      ? `/api/zone/${zoneId}?ignore=${zoneLastId[zoneId]}`
      : `/api/zone/${zoneId}`;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    card = await resp.json();
  } catch (err) {
    console.error(`Kunde inte hämta zon ${zoneId}:`, err);
    setTimeout(() => showZone(zoneId), 10_000);
    return;
  }

  if (card.content?.id != null) zoneLastId[zoneId] = card.content.id;

  const render = renderers[card.type];
  el.innerHTML = render ? render(card.content, "compact") : "";

  setTimeout(() => showZone(zoneId), card.display_seconds * 1000 + POLL_BUFFER_MS);
}

ZONE_IDS.forEach(showZone);
