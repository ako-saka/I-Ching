const LINE_COUNT = 6;
const ANIMATION_MS = 1350;

const landingPage = document.getElementById("landing-page");
const readingPage = document.getElementById("reading-page");
const questionInput = document.getElementById("question-input");
const questionDisplay = document.getElementById("question-display");
const beginButton = document.getElementById("begin-button");
const resetButton = document.getElementById("reset-button");
const backButton = document.getElementById("back-button");
const lineGuides = document.getElementById("line-guides");
const hexagramLines = document.getElementById("hexagram-lines");
const castOverlay = document.getElementById("cast-overlay");
const castCoins = Array.from(document.querySelectorAll(".cast-coin"));
const castResult = document.getElementById("cast-result");
const starsContainer = document.getElementById("stars");
const orbsContainer = document.getElementById("orbs");

const state = {
  question: "",
  lineData: [],
  revealed: Array(LINE_COUNT).fill(false),
  animatingIndex: -1,
};

function randomBool() {
  return Math.random() >= 0.5;
}

function createHexagram() {
  state.lineData = Array.from({ length: LINE_COUNT }, () => {
    const cast = [randomBool(), randomBool(), randomBool()];
    const heads = cast.filter(Boolean).length;
    return {
      cast,
      isSolid: heads >= 2,
    };
  });
  state.revealed = Array(LINE_COUNT).fill(false);
  state.animatingIndex = -1;
}

function buildAtmosphere() {
  const starMarkup = Array.from({ length: 44 }, () => {
    const size = (Math.random() * 2 + 1).toFixed(2);
    const top = (Math.random() * 62).toFixed(2);
    const left = (Math.random() * 100).toFixed(2);
    const delay = `${(Math.random() * 4).toFixed(2)}s`;
    const duration = `${(Math.random() * 2 + 2.4).toFixed(2)}s`;
    return `<span style="top:${top}%;left:${left}%;width:${size}px;height:${size}px;--delay:${delay};--duration:${duration};"></span>`;
  }).join("");

  const orbMarkup = Array.from({ length: 10 }, () => {
    const size = (Math.random() * 34 + 20).toFixed(0);
    const top = (Math.random() * 62 + 8).toFixed(2);
    const left = (Math.random() * 100).toFixed(2);
    const delay = `${(Math.random() * 5).toFixed(2)}s`;
    const duration = `${(Math.random() * 8 + 8).toFixed(2)}s`;
    return `<span style="top:${top}%;left:${left}%;width:${size}px;height:${size}px;--delay:${delay};--duration:${duration};"></span>`;
  }).join("");

  starsContainer.innerHTML = starMarkup;
  orbsContainer.innerHTML = orbMarkup;
}

function lineTop(index) {
  return 360 - index * 72;
}

function renderGuides() {
  lineGuides.innerHTML = Array.from({ length: LINE_COUNT }, (_, index) => {
    const top = lineTop(index);
    return `
      <div class="line-slot" style="top:${top}px;">
        <span class="guide-label">${index + 1}</span>
        <span class="guide-line left"></span>
        <span class="guide-line right"></span>
      </div>
    `;
  }).join("");
}

function renderLines() {
  hexagramLines.innerHTML = state.lineData.map((line, index) => {
    const top = lineTop(index);
    const content = state.revealed[index]
      ? `<div class="line-reveal ${line.isSolid ? "solid" : "broken"}" aria-label="${line.isSolid ? "Yang" : "Yin"} line"></div>`
      : `<button class="seal-button" type="button" data-line-index="${index}" aria-label="Cast line ${index + 1}" ${state.animatingIndex !== -1 ? "disabled" : ""}></button>`;

    return `<div class="line-slot" style="top:${top}px;">${content}</div>`;
  }).join("");
}

function renderAll() {
  renderGuides();
  renderLines();
}

function showReadingPage() {
  landingPage.classList.remove("active");
  landingPage.setAttribute("aria-hidden", "true");
  readingPage.classList.add("active");
  readingPage.setAttribute("aria-hidden", "false");
}

function showLandingPage() {
  readingPage.classList.remove("active");
  readingPage.setAttribute("aria-hidden", "true");
  landingPage.classList.add("active");
  landingPage.setAttribute("aria-hidden", "false");
  questionInput.focus();
}

function returnToLanding() {
  questionInput.value = "";
  state.question = "";
  castOverlay.classList.add("hidden");
  state.animatingIndex = -1;
  showLandingPage();
}

function castLabel(cast) {
  const heads = cast.filter(Boolean).length;
  return `${heads} heads -> ${heads >= 2 ? "yang line" : "yin line"}`;
}

function setCoinFace(coin, isHeads) {
  coin.classList.toggle("heads", isHeads);
  coin.classList.toggle("tails", !isHeads);
  coin.dataset.face = isHeads ? "H" : "T";
}

function playCastAnimation(index) {
  state.animatingIndex = index;
  renderLines();
  castOverlay.classList.remove("hidden");
  castResult.textContent = "";

  const cast = state.lineData[index].cast;
  castCoins.forEach((coin, coinIndex) => {
    coin.classList.remove("animate", "heads", "tails");
    coin.style.animationDelay = `${coinIndex * 110}ms`;
    setCoinFace(coin, cast[coinIndex]);
    void coin.offsetWidth;
    coin.classList.add("animate");
  });

  window.setTimeout(() => {
    castResult.textContent = castLabel(cast);
  }, 900);

  window.setTimeout(() => {
    state.revealed[index] = true;
    state.animatingIndex = -1;
    castOverlay.classList.add("hidden");
    renderLines();
  }, ANIMATION_MS);
}

function beginCasting() {
  const question = questionInput.value.trim();
  if (!question) {
    questionInput.focus();
    return;
  }

  state.question = question;
  questionDisplay.textContent = question;
  createHexagram();
  renderAll();
  showReadingPage();
}

function resetHexagram() {
  createHexagram();
  castOverlay.classList.add("hidden");
  renderAll();
}

beginButton.addEventListener("click", beginCasting);
questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    beginCasting();
  }
});

hexagramLines.addEventListener("click", (event) => {
  const button = event.target.closest(".seal-button");
  if (!button || state.animatingIndex !== -1) {
    return;
  }

  const index = Number(button.dataset.lineIndex);
  if (Number.isNaN(index) || state.revealed[index]) {
    return;
  }

  playCastAnimation(index);
});

resetButton.addEventListener("click", resetHexagram);
backButton.addEventListener("click", returnToLanding);

document.addEventListener("keydown", (event) => {
  if (event.key.toLowerCase() === "r" && readingPage.classList.contains("active")) {
    returnToLanding();
  }
});

buildAtmosphere();
createHexagram();
renderAll();
questionInput.focus();
