(() => {
  const scenes = [...document.querySelectorAll('.scene')];
  const navButtons = [...document.querySelectorAll('[data-jump]')];
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = window.matchMedia('(max-width: 760px)');
  const SNAP_IDLE_MS = 180;
  const SNAP_DURATION_MS = 820;
  const FINAL_SNAP_DURATION_MS = 1050;
  const SCENE_DEPTH = 1120;
  let currentScene = 0;
  let depthRaf = 0;
  let snapTimer = 0;
  let snapRaf = 0;
  let snapToken = 0;
  let isSnapping = false;

  const sourceLabels = {
    field: 'Field / audit', retailer: 'Retailer feeds', ecommerce: 'eCommerce',
    partner: 'Partner data', consumer: 'Consumer capture', ai: 'CV / voice / passive'
  };

  const layouts = {
    balanced: {
      title: 'Augment before replacing', human: 'Exceptions + local judgment', automate: 'Repeatable capture + QA', proof: 'Quality + unit economics',
      sources: {
        field: ['supporting', -48, -128, 32], retailer: ['primary', 48, -128, 105], ecommerce: ['supporting', -150, -25, 5],
        partner: ['supporting', 54, -15, 58], consumer: ['exception', -92, 90, -28], ai: ['supporting', 92, 82, 80]
      }
    },
    digital: {
      title: 'Shift repeatable capture toward digital access', human: 'Exceptions + source governance', automate: 'Feeds + recurring QA + classification', proof: 'Completeness + latency + economics',
      sources: {
        field: ['exception', -145, 88, -35], retailer: ['primary', -55, -125, 112], ecommerce: ['primary', 72, -125, 104],
        partner: ['supporting', -95, -18, 15], consumer: ['supporting', 88, -15, 40], ai: ['primary', 15, 82, 118]
      }
    },
    fragmented: {
      title: 'Partner + augment the field network', human: 'Local knowledge + retailer exceptions', automate: 'Routing + capture assistance + QA', proof: 'Coverage + partner quality + route economics',
      sources: {
        field: ['primary', -68, -126, 118], retailer: ['exception', 112, 86, -25], ecommerce: ['exception', -132, 82, -35],
        partner: ['primary', 64, -126, 105], consumer: ['supporting', -45, -18, 28], ai: ['supporting', 78, -14, 65]
      }
    },
    restricted: {
      title: 'Keep collection explainable and bounded', human: 'Privacy-sensitive decisions + local validation', automate: 'Low-risk capture + controlled QA', proof: 'Trust + consent + compliant coverage',
      sources: {
        field: ['primary', -65, -126, 108], retailer: ['supporting', 66, -126, 55], ecommerce: ['exception', 110, 82, -32],
        partner: ['supporting', -108, -18, 22], consumer: ['exception', -115, 88, -36], ai: ['supporting', 68, -14, 48]
      }
    }
  };

  function applyScenario(key) {
    const layout = layouts[key];
    if (!layout) return;
    document.querySelectorAll('.scenario').forEach(btn => {
      const active = btn.dataset.scenario === key;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    Object.entries(layout.sources).forEach(([source, [role, x, y, z]]) => {
      const el = document.querySelector(`.portfolio-source[data-source="${source}"]`);
      if (!el) return;
      el.dataset.role = role;
      el.style.transform = `translate3d(calc(-50% + ${x}px), calc(-50% + ${y}px), ${z}px) rotateX(4deg) rotateY(${x / 85}deg)`;
      el.querySelector('em').textContent = role.toUpperCase();
      el.setAttribute('aria-label', `${sourceLabels[source]}, ${role}`);
    });
    document.getElementById('postureTitle').textContent = layout.title;
    document.getElementById('humanAuthority').textContent = layout.human;
    document.getElementById('automateFocus').textContent = layout.automate;
    document.getElementById('proofFocus').textContent = layout.proof;
  }

  document.querySelectorAll('.scenario').forEach(btn => btn.addEventListener('click', () => applyScenario(btn.dataset.scenario)));
  document.getElementById('scenarioReset')?.addEventListener('click', () => applyScenario('balanced'));
  applyScenario('balanced');

  function maxScroll() { return Math.max(1, document.documentElement.scrollHeight - innerHeight); }
  function sceneTarget(index) { return (index / (scenes.length - 1)) * maxScroll(); }
  function easeInOutCubic(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  function cancelSnapAnimation() {
    if (snapTimer) clearTimeout(snapTimer);
    snapTimer = 0;
    if (snapRaf) cancelAnimationFrame(snapRaf);
    snapRaf = 0;
    snapToken += 1;
    isSnapping = false;
  }

  function animateScrollTo(target, duration = SNAP_DURATION_MS) {
    const start = scrollY;
    const delta = target - start;
    if (Math.abs(delta) < 2) return;
    if (snapRaf) cancelAnimationFrame(snapRaf);
    const token = ++snapToken;
    isSnapping = true;
    let startedAt = 0;
    function step(timestamp) {
      if (token !== snapToken) return;
      if (!startedAt) startedAt = timestamp;
      const progress = Math.min(1, (timestamp - startedAt) / duration);
      window.scrollTo(0, start + delta * easeInOutCubic(progress));
      requestDepthRender();
      if (progress < 1) snapRaf = requestAnimationFrame(step);
      else { snapRaf = 0; isSnapping = false; requestDepthRender(); }
    }
    snapRaf = requestAnimationFrame(step);
  }

  function nearestSceneIndex() {
    const normalized = Math.min(1, Math.max(0, scrollY / maxScroll()));
    return Math.round(normalized * (scenes.length - 1));
  }

  function snapToNearestScene() {
    snapTimer = 0;
    if (mobile.matches || reduceMotion.matches || isSnapping) return;
    const index = nearestSceneIndex();
    animateScrollTo(sceneTarget(index), index === scenes.length - 1 ? FINAL_SNAP_DURATION_MS : SNAP_DURATION_MS);
  }

  function scheduleSnap() {
    if (mobile.matches || reduceMotion.matches || isSnapping) return;
    if (snapTimer) clearTimeout(snapTimer);
    snapTimer = window.setTimeout(snapToNearestScene, SNAP_IDLE_MS);
  }

  function cancelForUserIntent() {
    if (mobile.matches || reduceMotion.matches) return;
    if (snapTimer || isSnapping || snapRaf) cancelSnapAnimation();
  }

  function scrollToScene(index) {
    if (!Number.isInteger(index) || index < 0 || index >= scenes.length) return;
    if (mobile.matches || reduceMotion.matches) {
      scenes[index]?.scrollIntoView({ behavior: reduceMotion.matches ? 'auto' : 'smooth', block: 'start' });
      return;
    }
    cancelSnapAnimation();
    animateScrollTo(sceneTarget(index), index === scenes.length - 1 ? FINAL_SNAP_DURATION_MS : SNAP_DURATION_MS);
  }

  navButtons.forEach(btn => btn.addEventListener('click', event => {
    const index = Number(event.currentTarget.dataset.jump);
    scrollToScene(index);
  }));

  function updateNavigation(index) {
    currentScene = index;
    document.querySelectorAll('.scene-nav [data-jump]').forEach(btn => btn.setAttribute('aria-current', Number(btn.dataset.jump) === index ? 'true' : 'false'));
    const topNumber = document.getElementById('topSceneNumber');
    if (topNumber) topNumber.textContent = String(index + 1).padStart(2, '0');
    document.body.dataset.scene = String(index);
  }

  function renderDepth() {
    depthRaf = 0;
    if (mobile.matches || reduceMotion.matches) return;
    const normalized = Math.min(1, Math.max(0, scrollY / maxScroll()));
    const camera = normalized * (scenes.length - 1) * SCENE_DEPTH;
    let nearest = 0;
    let nearestDistance = Infinity;
    scenes.forEach((scene, index) => {
      const z = index * SCENE_DEPTH - camera;
      const distance = Math.abs(z);
      if (distance < nearestDistance) { nearestDistance = distance; nearest = index; }
      const opacity = Math.max(0, 1 - distance / 735);
      const focusDistance = Math.max(0, Math.min(1, (distance - 80) / 620));
      const blur = 8 * Math.pow(focusDistance, 1.65);
      const y = Math.max(-86, Math.min(86, z * .035));
      const rotate = Math.max(-3.8, Math.min(3.8, z / 315));
      scene.style.transform = `translate3d(0, ${y}px, ${z}px) rotateX(${rotate}deg)`;
      scene.style.opacity = String(opacity);
      scene.style.filter = `blur(${blur.toFixed(2)}px)`;
      scene.classList.toggle('is-active', distance < 420);
      scene.setAttribute('aria-hidden', distance < 520 ? 'false' : 'true');
    });
    updateNavigation(nearest);
    root.style.setProperty('--depth-progress', normalized.toFixed(4));
  }

  function requestDepthRender() { if (!depthRaf) depthRaf = requestAnimationFrame(renderDepth); }

  /* Signal field — deliberately sparse. It reads as data in motion, not a space theme. */
  const canvas = document.getElementById('signalField');
  const ctx = canvas?.getContext('2d', { alpha: true });
  let stars = [];
  let fieldRaf = 0;
  let warp = 0;
  let targetWarp = 0;
  let lastY = scrollY;
  let lastScrollAt = performance.now();

  function deterministicNoise(n) {
    const x = Math.sin(n * 12.9898 + 78.233) * 43758.5453;
    return x - Math.floor(x);
  }

  function resizeField() {
    if (!canvas || !ctx) return;
    const dpr = Math.min(2, devicePixelRatio || 1);
    canvas.width = Math.round(innerWidth * dpr);
    canvas.height = Math.round(innerHeight * dpr);
    canvas.style.width = `${innerWidth}px`;
    canvas.style.height = `${innerHeight}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = mobile.matches ? 58 : Math.min(128, Math.max(84, Math.round(innerWidth / 12)));
    stars = Array.from({ length: count }, (_, i) => ({
      x: deterministicNoise(i + 1) * innerWidth,
      y: deterministicNoise(i + 101) * innerHeight,
      depth: .2 + deterministicNoise(i + 211) * .8,
      size: .35 + deterministicNoise(i + 307) * 1.05,
      phase: deterministicNoise(i + 401) * Math.PI * 2,
      speed: .00018 + deterministicNoise(i + 503) * .00032,
      base: .07 + deterministicNoise(i + 601) * .13
    }));
    drawField(performance.now(), true);
  }

  function drawField(time, staticOnly = false) {
    if (!canvas || !ctx) return;
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    const cx = innerWidth * .5;
    const cy = innerHeight * .46;
    const finalScene = document.body.dataset.scene === String(scenes.length - 1);
    const finalFade = finalScene ? .38 : 1;
    stars.forEach(star => {
      const dx = star.x - cx;
      const dy = star.y - cy;
      const expansion = 1 + warp * .055 * star.depth;
      const x = cx + dx * expansion;
      const y = cy + dy * expansion;
      const twinkle = staticOnly || mobile.matches || reduceMotion.matches ? 0 : Math.sin(time * star.speed + star.phase) * .045;
      const alpha = Math.max(.025, (star.base + twinkle) * finalFade);
      const streak = warp * star.depth * 11;
      if (streak > .55) {
        const len = Math.hypot(dx, dy) || 1;
        const ux = dx / len;
        const uy = dy / len;
        const grad = ctx.createLinearGradient(x - ux * streak, y - uy * streak, x, y);
        grad.addColorStop(0, `rgba(49,209,255,0)`);
        grad.addColorStop(1, `rgba(163,169,245,${Math.min(.32, alpha * 1.8)})`);
        ctx.strokeStyle = grad;
        ctx.lineWidth = Math.max(.45, star.size * .55);
        ctx.beginPath();
        ctx.moveTo(x - ux * streak, y - uy * streak);
        ctx.lineTo(x, y);
        ctx.stroke();
      }
      ctx.fillStyle = `rgba(226,235,255,${alpha})`;
      ctx.beginPath();
      ctx.arc(x, y, star.size * (1 + star.depth * .2), 0, Math.PI * 2);
      ctx.fill();
    });
  }

  function animateField(time) {
    warp += (targetWarp - warp) * .08;
    targetWarp *= .92;
    if (Math.abs(targetWarp) < .002) targetWarp = 0;
    drawField(time, false);
    fieldRaf = requestAnimationFrame(animateField);
  }

  function noteScrollVelocity() {
    const now = performance.now();
    const dt = Math.max(16, now - lastScrollAt);
    const velocity = Math.abs(scrollY - lastY) / dt;
    targetWarp = Math.min(1, Math.max(targetWarp, velocity * 1.8));
    lastY = scrollY;
    lastScrollAt = now;
  }

  window.addEventListener('scroll', () => {
    requestDepthRender();
    scheduleSnap();
    if (!reduceMotion.matches && !mobile.matches) noteScrollVelocity();
  }, { passive: true });
  window.addEventListener('resize', () => { requestDepthRender(); resizeField(); });
  window.addEventListener('wheel', cancelForUserIntent, { passive: true });
  window.addEventListener('touchstart', cancelForUserIntent, { passive: true });
  window.addEventListener('pointerdown', cancelForUserIntent, { passive: true });
  window.addEventListener('keydown', event => {
    if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' ', 'Spacebar'].includes(event.key)) cancelForUserIntent();
  });
  reduceMotion.addEventListener?.('change', () => location.reload());
  mobile.addEventListener?.('change', () => location.reload());

  resizeField();
  if (!reduceMotion.matches && !mobile.matches) fieldRaf = requestAnimationFrame(animateField);

  if (!mobile.matches && !reduceMotion.matches) {
    scenes.forEach(scene => scene.setAttribute('aria-hidden', 'true'));
    renderDepth();
  } else {
    updateNavigation(0);
  }

  window.addEventListener('beforeunload', () => {
    if (fieldRaf) cancelAnimationFrame(fieldRaf);
  });
})();
