// Subtle animated quasicrystal background, recolored to blend into the
// light-grey (#fafafa) theme. Fixed behind all content, viewport-sized,
// ~30fps, and disabled for users who prefer reduced motion.
// A small control panel (top-left) tweaks opacity / pixel / directions / seed live.
(function () {
  const canvas = document.getElementById("bg-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  const AMP = 10; // pattern amplitude (opacity slider scales the final alpha)

  const baseFill = [238, 238, 238]; // #eeeeee — barely-grey, near white
  const hoverFill = [226, 206, 174]; // soft warm — a nod to the amber accent

  // live-tunable params (driven by the control panel)
  let pixel = 16;
  let angles = 7;
  let alphaScale = 1; // "opacity"
  let seed = 0; // base warp

  // animation + hover state
  let fill = baseFill.slice();
  let offset = 0;
  let speed = 1;
  let modifier = seed;
  let hovering = false;

  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  function getOpacity(x, y, angle, bonus) {
    const angledX = Math.cos(angle - 2 * (modifier * bonus)) * x;
    const angledY = Math.sin(angle + 2 * (modifier * bonus)) * y;
    return Math.cos(angledX + angledY + offset) * AMP;
  }

  function getColor(x, y) {
    let sum = 0;
    let angle = 2 * Math.PI;
    const delta = angle / angles;
    for (let i = 0; i < angles; i++) {
      sum += getOpacity(x, y, angle, (Math.PI / angles) * i);
      angle -= delta;
    }
    return `rgba(${fill[0]}, ${fill[1]}, ${fill[2]}, ${(sum / angles) * alphaScale})`;
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const halfW = canvas.width / 2;
    const halfH = canvas.height / 2;
    for (let x = -halfW; x < halfW; x += pixel) {
      for (let y = -halfH; y < halfH; y += pixel) {
        ctx.fillStyle = getColor(x / pixel, y / pixel);
        ctx.fillRect(
          pixel * Math.round((x + halfW) / pixel),
          pixel * Math.round((y + halfH) / pixel),
          pixel,
          pixel
        );
      }
    }
  }

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    if (reduceMotion) draw();
  }

  let last = 0;
  function animate(now) {
    requestAnimationFrame(animate);
    if (now - last < 33) return; // ~30fps
    last = now;
    offset += speed / 16;
    draw();
  }

  // ---- control panel ----
  function buildControls() {
    const panel = document.createElement("div");
    panel.id = "bg-controls";
    panel.innerHTML = `
      <button type="button" class="bgc-head" aria-label="toggle background controls">bg ✦</button>
      <div class="bgc-body">
        <label>opacity <span data-v="opacity">1.00</span></label>
        <input type="range" data-k="opacity" min="0" max="1" step="0.01" value="1">
        <label>pixel <span data-v="pixel">16</span></label>
        <input type="range" data-k="pixel" min="4" max="48" step="2" value="16">
        <label>directions <span data-v="angles">7</span></label>
        <input type="range" data-k="angles" min="1" max="12" step="1" value="7">
        <label>seed <span data-v="seed">0.00</span></label>
        <input type="range" data-k="seed" min="0" max="1" step="0.01" value="0">
      </div>`;
    document.body.appendChild(panel);

    const show = (k, v) => {
      const el = panel.querySelector(`[data-v="${k}"]`);
      if (el) el.textContent = k === "pixel" || k === "angles" ? v : Number(v).toFixed(2);
    };

    panel.querySelectorAll("input[type=range]").forEach((input) => {
      input.addEventListener("input", () => {
        const k = input.dataset.k;
        const v = parseFloat(input.value);
        if (k === "opacity") alphaScale = v;
        else if (k === "pixel") pixel = v;
        else if (k === "angles") angles = v;
        else if (k === "seed") {
          seed = v;
          if (!hovering) modifier = seed;
        }
        show(k, v);
        if (reduceMotion) draw();
      });
    });

    panel
      .querySelector(".bgc-head")
      .addEventListener("click", () => panel.classList.toggle("collapsed"));
  }

  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);
  buildControls();

  if (reduceMotion) {
    draw();
  } else {
    requestAnimationFrame(animate);
  }

  // Gentle reaction when hovering any link (skips the control panel itself).
  document.querySelectorAll("a").forEach((url) => {
    url.addEventListener("mouseenter", () => {
      hovering = true;
      fill = hoverFill;
      speed = 1.5;
      modifier = 0.3 + Math.random() * 0.5;
    });
    url.addEventListener("mouseleave", () => {
      hovering = false;
      fill = baseFill;
      speed = 1;
      modifier = seed;
    });
  });
})();
