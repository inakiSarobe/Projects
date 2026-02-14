const envelopeButton = document.getElementById("loveEnvelope");
const hintText = document.getElementById("hintText");
const floatingHeartsContainer = document.querySelector(".floating-hearts");

const floatingHeartCount = 24;
let isOpen = false;

createFloatingHearts(floatingHeartCount);

envelopeButton.addEventListener("click", () => {
  isOpen = !isOpen;
  envelopeButton.classList.toggle("open", isOpen);
  envelopeButton.setAttribute("aria-pressed", String(isOpen));
  hintText.textContent = isOpen
    ? "Cada latido es por ti <3"
    : "Haz clic para abrir";

  if (isOpen) {
    launchHeartBurst(envelopeButton.getBoundingClientRect());
  }
});

function createFloatingHearts(count) {
  for (let i = 0; i < count; i += 1) {
    const heart = document.createElement("span");
    const size = randomNumber(0.85, 1.7);
    const duration = randomNumber(8, 16);
    const delay = randomNumber(0, 10);
    const left = randomNumber(2, 98);

    heart.textContent = "\u2764";
    heart.style.setProperty("--size", `${size}rem`);
    heart.style.setProperty("--duration", `${duration}s`);
    heart.style.setProperty("--delay", `${delay}s`);
    heart.style.setProperty("--left", `${left}%`);

    floatingHeartsContainer.appendChild(heart);
  }
}

function launchHeartBurst(rect) {
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  const total = 22;

  for (let i = 0; i < total; i += 1) {
    const heart = document.createElement("span");
    const angle = (Math.PI * 2 * i) / total + randomNumber(-0.2, 0.2);
    const distance = randomNumber(80, 170);
    const x = Math.cos(angle) * distance;
    const y = Math.sin(angle) * distance - randomNumber(8, 36);

    heart.className = "burst-heart";
    heart.textContent = "\u2764";
    heart.style.left = `${centerX}px`;
    heart.style.top = `${centerY}px`;
    heart.style.setProperty("--x", `${x}px`);
    heart.style.setProperty("--y", `${y}px`);
    heart.style.color = randomHeartColor();

    document.body.appendChild(heart);

    heart.addEventListener("animationend", () => {
      heart.remove();
    });
  }
}

function randomHeartColor() {
  const colors = ["#ffd0e0", "#ff9fbf", "#ffb3cd", "#ffe0ec", "#ff7ca9"];
  return colors[Math.floor(Math.random() * colors.length)];
}

function randomNumber(min, max) {
  return Math.random() * (max - min) + min;
}
