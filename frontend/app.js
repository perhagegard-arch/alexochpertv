import { renderQuoteCard } from "./widgets/QuoteWidget.js";

const POLL_BUFFER_MS = 500;

const layers = [
  document.getElementById("card-a"),
  document.getElementById("card-b"),
];
let active = 0;
let lastId = null;

const renderers = {
  quote: renderQuoteCard,
};

async function fetchCard() {
  const url = lastId !== null ? `/api/card?ignore=${lastId}` : "/api/card";
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  return resp.json();
}

function applyCard(layer, card) {
  layer.style.backgroundImage = card.background ? `url('${card.background}')` : "";
  const render = renderers[card.type];
  layer.innerHTML = render ? render(card.content) : "";
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

  const next = 1 - active;
  applyCard(layers[next], card);

  layers[next].classList.add("visible");
  layers[active].classList.remove("visible");
  active = next;

  setTimeout(showNext, card.display_seconds * 1000 + POLL_BUFFER_MS);
}

showNext();
