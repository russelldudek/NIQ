(() => {
  const scenes = [...document.querySelectorAll('.scene')];
  const navButtons = [...document.querySelectorAll('[data-jump]')];
  const root = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = window.matchMedia('(max-width: 760px)');
  const SNAP_IDLE_MS = 180;
  const SNAP_DURATION_MS = 820;
  const FINAL_SNAP_DURATION_MS = 1050;
  let currentScene = 0;
  let raf = 0;
  let snapTimer = 0;
  let snapRaf = 0;
  let snapToken = 0;
  let isSnapping = false;

  const scenarioData = {
    balanced: {
      mix: { field: 58, retailer: 52, ecommerce: 46, partner: 44, consumer: 36, ai: 42 },
      title: 'Augment before replacing',
      human: 'Local validation remains explicit',
      value: 'Cycle time + first-time-right',
      guard: 'Quality threshold before scale',
      next: 'Pilot one repeatable source class'
    },
    digital: {
      mix: { field: 24, retailer: 84, ecommerce: 78, partner: 54, consumer: 38, ai: 72 },
      title: 'Shift direct capture toward digital feeds',
      human: 'Humans govern exceptions and source quality',
      value: 'Latency + recurring acquisition cost',
      guard: 'Feed completeness and schema drift',
      next: 'Scale APIs where coverage is durable'
    },
    fragmented: {
      mix: { field: 76, retailer: 26, ecommerce: 31, partner: 70, consumer: 45, ai: 58 },
      title: 'Partner + augment the field network',
      human: 'Local market knowledge remains a core asset',
      value: 'Coverage + route productivity',
      guard: 'Partner quality and retailer relationship risk',
      next: 'Segment markets by source accessibility'
    },
    restricted: {
      mix: { field: 63, retailer: 44, ecommerce: 30, partner: 36, consumer: 22, ai: 34 },
      title: 'Keep collection explainable and bounded',
      human: 'Named authority for privacy-sensitive decisions',
      value: 'Trust + compliant coverage',
      guard: 'Privacy, consent and data minimization',
      next: 'Design market-specific privacy controls'
    }
  };

  function setScenario(key) {
    const data = scenarioData[key];
    if (!data) return;
    document.querySelectorAll('.scenario').forEach(btn => {
      const active = btn.dataset.scenario === key;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    Object.entries(data.mix).forEach(([mixKey, value]) => {
      const layer = document.querySelector(`.mix-layer[data-key="${mixKey}"]`);
      if (layer) layer.style.setProperty('--mix', `${value}%`);
    });
    document.getElementById('postureTitle').textContent = data.title;
    document.getElementById('humanAuthority').textContent = data.human;
    document.getElementById('valuePool').textContent = data.value;
    document.getElementById('guardrail').textContent = data.guard;
    document.getElementById('nextMove').textContent = data.next;
  }

  document.querySelectorAll('.scenario').forEach(btn => {
    btn.addEventListener('click', () => setScenario(btn.dataset.scenario));
  });
  setScenario('balanced');

  function maxScroll() {
    return Math.max(1, document.documentElement.scrollHeight - innerHeight);
  }

  function sceneTarget(index) {
    return (index / (scenes.length - 1)) * maxScroll();
  }

  function easeInOutCubic(t) {
    return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

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
      const eased = easeInOutCubic(progress);
      window.scrollTo(0, start + delta * eased);
      requestRender();

      if (progress < 1) {
        snapRaf = requestAnimationFrame(step);
      } else {
        snapRaf = 0;
        isSnapping = false;
        requestRender();
      }
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
    const duration = index === scenes.length - 1 ? FINAL_SNAP_DURATION_MS : SNAP_DURATION_MS;
    animateScrollTo(sceneTarget(index), duration);
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
    if (mobile.matches || reduceMotion.matches) {
      scenes[index]?.scrollIntoView({ behavior: reduceMotion.matches ? 'auto' : 'smooth', block: 'start' });
      return;
    }
    cancelSnapAnimation();
    const duration = index === scenes.length - 1 ? FINAL_SNAP_DURATION_MS : SNAP_DURATION_MS;
    animateScrollTo(sceneTarget(index), duration);
  }

  navButtons.forEach(btn => btn.addEventListener('click', () => scrollToScene(Number(btn.dataset.jump))));

  function updateNavigation(index) {
    if (index === currentScene && document.querySelector('.scene-nav button[aria-current="true"]')) return;
    currentScene = index;
    document.querySelectorAll('.scene-nav [data-jump]').forEach(btn => {
      btn.setAttribute('aria-current', Number(btn.dataset.jump) === index ? 'true' : 'false');
    });
  }

  function renderDepth() {
    raf = 0;
    if (mobile.matches || reduceMotion.matches) return;
    const max = maxScroll();
    const normalized = Math.min(1, Math.max(0, scrollY / max));
    const camera = normalized * (scenes.length - 1) * 1120;
    let nearest = 0;
    let nearestDistance = Infinity;

    scenes.forEach((scene, index) => {
      const z = index * 1120 - camera;
      const distance = Math.abs(z);
      if (distance < nearestDistance) { nearestDistance = distance; nearest = index; }
      const opacity = Math.max(0, 1 - distance / 700);
      const y = Math.max(-80, Math.min(80, z * .035));
      const rotate = Math.max(-3.5, Math.min(3.5, z / 320));
      scene.style.transform = `translate3d(0, ${y}px, ${z}px) rotateX(${rotate}deg)`;
      scene.style.opacity = String(opacity);
      scene.classList.toggle('is-active', distance < 420);
      scene.setAttribute('aria-hidden', distance < 520 ? 'false' : 'true');
    });

    updateNavigation(nearest);
    root.style.setProperty('--depth-progress', normalized.toFixed(4));
  }

  function requestRender() {
    if (!raf) raf = requestAnimationFrame(renderDepth);
  }

  window.addEventListener('scroll', () => {
    requestRender();
    scheduleSnap();
  }, { passive: true });
  window.addEventListener('resize', requestRender);
  window.addEventListener('wheel', cancelForUserIntent, { passive: true });
  window.addEventListener('touchstart', cancelForUserIntent, { passive: true });
  window.addEventListener('pointerdown', cancelForUserIntent, { passive: true });
  window.addEventListener('keydown', event => {
    if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' ', 'Spacebar'].includes(event.key)) {
      cancelForUserIntent();
    }
  });
  reduceMotion.addEventListener?.('change', () => location.reload());
  mobile.addEventListener?.('change', () => location.reload());

  if (!mobile.matches && !reduceMotion.matches) {
    scenes.forEach(scene => scene.setAttribute('aria-hidden', 'true'));
    renderDepth();
  }
})();
