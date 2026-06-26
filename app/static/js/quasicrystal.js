// Subtle animated quasicrystal background, recolored to blend into the
// light-grey (#fafafa) theme. Fixed behind all content, viewport-sized,
// ~30fps, and disabled for users who prefer reduced motion.
(function () {
  const canvas = document.getElementById("bg-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  const pixel = 16;     // grid cell size (bigger = cheaper)
  const AMP = 0.8;      // pattern strength — keep low so it stays faint

  const baseFill = [200, 201, 209];   // soft grey, barely off the bg
  const hoverFill = [226, 206, 174];  // soft warm — a nod to the amber accent

  let fill = baseFill.slice();
  let angles = 7;
  let offset = 0;
  let speed = 1;
  let modifier = 0;

  const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  function getOpacity(x, y, angle, bonus) {
    const angledX = Math.cos(angle - 2 * (modifier * bonus)) * x;
    const angledY = Math.sin(angle + 2 * (modifier * bonus)) * y;
    return Math.cos(angledX + angledY + offset) * AMP;
  }

  function getColor(x, y) {
    let opacity = 0;
    let angle = 2 * Math.PI;
    const delta = angle / angles;
    for (let i = 0; i < angles; i++) {
      opacity += getOpacity(x, y, angle, (Math.PI / angles) * i);
      angle -= delta;
    }
    return `rgba(${fill[0]}, ${fill[1]}, ${fill[2]}, ${opacity / angles})`;
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

  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);

  if (reduceMotion) {
    draw();
  } else {
    requestAnimationFrame(animate);
  }

  // Gentle reaction when hovering any link.
  document.querySelectorAll("a").forEach((url) => {
    url.addEventListener("mouseenter", () => {
      fill = hoverFill;
      angles = 3 + Math.floor(Math.random() * 4);
      speed = 1.5;
      modifier = 0.3 + Math.random() * 0.5;
    });
    url.addEventListener("mouseleave", () => {
      fill = baseFill;
      angles = 7;
      speed = 1;
      modifier = 0;
    });
  });
})();
