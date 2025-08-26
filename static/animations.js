// animations.js

document.addEventListener("DOMContentLoaded", () => {
  // Intro overlay fade-out
  const overlay = document.getElementById("introOverlay");
  if (overlay) {
    overlay.style.transition = "opacity 1s ease";
    overlay.style.opacity = 1;

    setTimeout(() => {
      overlay.style.opacity = 0;
      setTimeout(() => {
        overlay.style.display = "none";
      }, 1000);
    }, 1500);
  }

  // Create floating particle background
  createParticles();
});

// Floating particles
function createParticles() {
  const container = document.createElement("div");
  container.className = "particle-container";
  document.body.appendChild(container);

  for (let i = 0; i < 50; i++) {
    const particle = document.createElement("div");
    particle.className = "particle";

    const size = Math.random() * 6 + 2;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    particle.style.left = `${Math.random() * 100}vw`;
    particle.style.top = `${Math.random() * 100}vh`;

    const duration = Math.random() * 20 + 10;
    const delay = Math.random() * 10;
    particle.style.animation = `float ${duration}s linear infinite`;
    particle.style.animationDelay = `${delay}s`;

    container.appendChild(particle);
  }
}
