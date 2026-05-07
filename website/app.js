const LINE_COUNT = 6;
const ANIMATION_MS = 1350;

const landingPage = document.getElementById("landing-page");
const readingPage = document.getElementById("reading-page");
const questionInput = document.getElementById("question-input");
const questionDisplay = document.getElementById("question-display");
const beginButton = document.getElementById("begin-button");
const castAllButton = document.getElementById("cast-all-button");
const resetButton = document.getElementById("reset-button");
const backButton = document.getElementById("back-button");
const hexagramLines = document.getElementById("hexagram-lines");
const castOverlay = document.getElementById("cast-overlay");
const castCoins = Array.from(document.querySelectorAll(".cast-coin"));
const castResult = document.getElementById("cast-result");
const starsContainer = document.getElementById("stars");
const orbsContainer = document.getElementById("orbs");
const readingResult = document.getElementById("reading-result");
const readingTitle = document.getElementById("reading-title");
const readingCode = document.getElementById("reading-code");
const readingBody = document.getElementById("reading-body");
const scrollTip = document.getElementById("scroll-tip");

const state = {
  question: "",
  lineData: [],
  revealed: Array(LINE_COUNT).fill(false),
  revealedNow: Array(LINE_COUNT).fill(false),
  animatingIndex: -1,
  readingRequestId: 0,
  animationRequestId: 0,
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
  state.revealedNow = Array(LINE_COUNT).fill(false);
  state.animatingIndex = -1;
  state.readingRequestId += 1;
  state.animationRequestId += 1;
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

function renderLines() {
  hexagramLines.innerHTML = state.lineData.map((line, index) => {
    const top = lineTop(index);
    const slotClasses = [
      "line-slot",
      state.revealed[index] ? "is-revealed" : "",
      state.revealedNow[index] ? "just-revealed" : "",
      state.revealed.every(Boolean) ? "hexagram-complete" : "",
    ].filter(Boolean).join(" ");
    const content = state.revealed[index]
      ? `<div class="line-reveal ${line.isSolid ? "solid" : "broken"}" aria-label="${line.isSolid ? "Yang" : "Yin"} line"></div>`
      : `<button class="seal-button" type="button" data-line-index="${index}" aria-label="Cast line ${index + 1}" ${state.animatingIndex !== -1 ? "disabled" : ""}></button>`;

    return `
      <div class="${slotClasses}" style="top:${top}px;">
        <span class="guide-label">${index + 1}</span>
        <span class="guide-line"></span>
        ${content}
        <span class="guide-line"></span>
      </div>
    `;
  }).join("");
}

function renderAll() {
  renderLines();
  updateCastAllButton();
}

function updateCastAllButton() {
  const isBusy = state.animatingIndex !== -1;
  const isComplete = state.revealed.every(Boolean);
  castAllButton.disabled = isBusy || isComplete;
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
  castOverlay.classList.remove("casting-all");
  state.animatingIndex = -1;
  state.animationRequestId += 1;
  setReadingPlaceholder("Your reading will appear here after the casting is complete.");
  showLandingPage();
}

function castLabel(cast) {
  const heads = cast.filter(Boolean).length;
  return `${heads} heads -> ${heads >= 2 ? "yang line" : "yin line"}`;
}

function getHexagramCode() {
  return state.lineData.map((line) => (line.isSolid ? "1" : "0")).join("");
}

function setReadingPlaceholder(message) {
  readingResult.classList.add("hidden");
  scrollTip.classList.add("hidden");
  readingTitle.textContent = "Reveal all six lines to read the hexagram.";
  readingCode.textContent = "";
  readingBody.textContent = message;
}

function completeLine(index, requestId) {
  if (requestId !== state.animationRequestId) {
    return;
  }

  state.revealedNow = Array(LINE_COUNT).fill(false);
  state.revealed[index] = true;
  state.revealedNow[index] = true;
  state.animatingIndex = -1;
  castOverlay.classList.add("hidden");
  castOverlay.classList.remove("casting-all");
  renderAll();
  if (state.revealed.every(Boolean)) {
    loadReading();
  }

  window.setTimeout(() => {
    if (requestId !== state.animationRequestId) {
      return;
    }

    state.revealedNow[index] = false;
    renderAll();
  }, 900);
}

async function loadReading() {
  const code = getHexagramCode();
  const requestId = state.readingRequestId;

  readingResult.classList.remove("hidden");
  scrollTip.classList.remove("hidden");
  readingTitle.textContent = "Loading hexagram reading...";
  readingCode.textContent = `Code ${code}`;
  readingBody.textContent = "Opening the matched reading...";

  try {
    const text = window.ICHING_READINGS?.[code];
    if (!text) {
      throw new Error("Reading not found in bundled data");
    }
    if (requestId !== state.readingRequestId) {
      return;
    }

    const lines = text.trim().split("\n");
    const titleLine = lines[1]?.trim() || `Hexagram ${code}`;
    readingCode.textContent = `Code ${code}`;
    readingTitle.textContent = titleLine;
    readingBody.textContent = lines.slice(2).join("\n").trim() || "The reading file is empty.";
  } catch (error) {
    if (requestId !== state.readingRequestId) {
      return;
    }

    readingTitle.textContent = "Unable to load the reading";
    readingCode.textContent = `Code ${code}`;
    readingBody.textContent = "The bundled reading data did not include this hexagram code.";
  }
}

function setCoinFace(coin, isHeads) {
  coin.classList.toggle("heads", isHeads);
  coin.classList.toggle("tails", !isHeads);
  coin.dataset.face = isHeads ? "H" : "T";
}

function playCastAnimation(index) {
  const requestId = state.animationRequestId + 1;
  state.animationRequestId = requestId;
  state.animatingIndex = index;
  renderAll();
  castOverlay.classList.remove("hidden");
  castOverlay.classList.remove("casting-all");
  castOverlay.querySelector(".cast-title").textContent = "Coin casting in motion";
  castResult.textContent = "";

  const cast = state.lineData[index].cast;
  castCoins.forEach((coin, coinIndex) => {
    coin.parentElement.classList.remove("animate");
    coin.classList.remove("animate", "heads", "tails");
    coin.style.animationDelay = `${coinIndex * 110}ms`;
    setCoinFace(coin, cast[coinIndex]);
    void coin.offsetWidth;
    coin.parentElement.classList.add("animate");
    coin.classList.add("animate");
  });

  window.setTimeout(() => {
    if (requestId !== state.animationRequestId) {
      return;
    }

    castResult.textContent = castLabel(cast);
  }, 900);

  window.setTimeout(() => {
    completeLine(index, requestId);
  }, ANIMATION_MS);
}

function playCastAllAnimation() {
  if (state.animatingIndex !== -1 || state.revealed.every(Boolean)) {
    return;
  }

  const requestId = state.animationRequestId + 1;
  state.animationRequestId = requestId;
  state.animatingIndex = -2;
  renderAll();
  castOverlay.classList.remove("hidden");
  castOverlay.classList.add("casting-all");
  castOverlay.querySelector(".cast-title").textContent = "Throwing all coins";
  castResult.textContent = "";

  const previewLine = state.lineData.find((line, index) => !state.revealed[index]) || state.lineData[0];
  castCoins.forEach((coin, coinIndex) => {
    coin.parentElement.classList.remove("animate");
    coin.classList.remove("animate", "heads", "tails");
    coin.style.animationDelay = `${coinIndex * 110}ms`;
    setCoinFace(coin, previewLine.cast[coinIndex]);
    void coin.offsetWidth;
    coin.parentElement.classList.add("animate");
    coin.classList.add("animate");
  });

  window.setTimeout(() => {
    if (requestId !== state.animationRequestId) {
      return;
    }

    const remainingCount = state.revealed.filter((isRevealed) => !isRevealed).length;
    castResult.textContent = `${remainingCount} ${remainingCount === 1 ? "line" : "lines"} cast`;
  }, 900);

  window.setTimeout(() => {
    if (requestId !== state.animationRequestId) {
      return;
    }

    state.revealedNow = state.revealed.map((isRevealed) => !isRevealed);
    state.revealed = Array(LINE_COUNT).fill(true);
    state.animatingIndex = -1;
    castOverlay.classList.add("hidden");
    castOverlay.classList.remove("casting-all");
    renderAll();
    loadReading();

    window.setTimeout(() => {
      if (requestId !== state.animationRequestId) {
        return;
      }

      state.revealedNow = Array(LINE_COUNT).fill(false);
      renderAll();
    }, 1600);
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
  setReadingPlaceholder("Your reading will appear here after the casting is complete.");
  showReadingPage();
}

function resetHexagram() {
  createHexagram();
  castOverlay.classList.add("hidden");
  castOverlay.classList.remove("casting-all");
  renderAll();
  setReadingPlaceholder("Your reading will appear here after the casting is complete.");
}

beginButton.addEventListener("click", beginCasting);
castAllButton.addEventListener("click", playCastAllAnimation);
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
setReadingPlaceholder("Your reading will appear here after the casting is complete.");
questionInput.focus();
