// AutoScroll Pro — Popup Script

document.addEventListener('DOMContentLoaded', () => {

  // ── Elements ──────────────────────────────────────────────────────────────
  const toggleWidgetBtn  = document.getElementById('toggle-widget-btn');
  const widgetBtnText    = document.getElementById('widget-btn-text');
  const scrollToggleBtn  = document.getElementById('scroll-toggle-btn');
  const scrollToggleText = document.getElementById('scroll-toggle-text');
  const toggleIcon       = document.getElementById('toggle-icon');
  const directionBtn     = document.getElementById('direction-btn');
  const directionText    = document.getElementById('direction-text');
  const directionIcon    = document.getElementById('direction-icon');
  const speedSlider      = document.getElementById('speed-slider');
  const speedNumber      = document.getElementById('speed-number');   // ← new
  const thresholdSlider  = document.getElementById('threshold-slider');
  const thresholdDisplay = document.getElementById('threshold-display');
  const alwaysShowToggle = document.getElementById('always-show-toggle');
  const statusBadge      = document.getElementById('status-badge');
  const statusDot        = document.getElementById('status-dot');
  const statusText       = document.getElementById('status-text');
  const presetBtns       = document.querySelectorAll('.preset-btn');

  // ── SVG strings ───────────────────────────────────────────────────────────
  const ICON_PLAY = `<svg viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/>
    <polygon points="10,8 17,12 10,16" fill="currentColor"/>
  </svg>`;
  const ICON_PAUSE = `<svg viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/>
    <rect x="9" y="8" width="2" height="8" rx="1" fill="currentColor"/>
    <rect x="13" y="8" width="2" height="8" rx="1" fill="currentColor"/>
  </svg>`;
  const ICON_DOWN_DIR = `<svg viewBox="0 0 24 24" fill="none">
    <path d="M12 19V5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <path d="M8 15l4 4 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;
  const ICON_UP_DIR = `<svg viewBox="0 0 24 24" fill="none">
    <path d="M12 5v14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <path d="M8 9l4-4 4 4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;

  // ── Local state ───────────────────────────────────────────────────────────
  let isScrolling      = false;
  let currentDirection = 'down';
  let widgetVisible    = false;
  let currentSpeed     = 3;

  // ── Init: load state from content script ─────────────────────────────────
  sendMsg({ type: 'GET_STATE' }, (res) => {
    if (!res) return;
    isScrolling      = !!res.isScrolling;
    currentDirection = res.scrollDirection || 'down';
    widgetVisible    = !!res.widgetVisible;
    currentSpeed     = res.scrollSpeed || 3;

    syncSpeedUI(currentSpeed);
    updateAllUI();
  });

  chrome.storage.local.get(['alwaysShow', 'threshold', 'scrollSpeed'], (data) => {
    if (data.alwaysShow) alwaysShowToggle.checked = true;
    if (data.threshold) {
      thresholdSlider.value = data.threshold;
      updateThresholdUI(data.threshold);
    }
    if (data.scrollSpeed) {
      currentSpeed = data.scrollSpeed;
      syncSpeedUI(currentSpeed);
    }
  });

  // ── Toggle Widget ─────────────────────────────────────────────────────────
  toggleWidgetBtn.addEventListener('click', () => {
    sendMsg({ type: 'TOGGLE_WIDGET' }, (res) => {
      widgetVisible = res?.visible ?? !widgetVisible;
      updateWidgetBtn();
    });
  });

  // ── Start / Stop Scroll ───────────────────────────────────────────────────
  scrollToggleBtn.addEventListener('click', () => {
    sendMsg({ type: 'TOGGLE_SCROLL' }, (res) => {
      isScrolling = res?.isScrolling ?? !isScrolling;
      updateScrollBtn();
      updateStatus();
    });
  });

  // ── Direction ─────────────────────────────────────────────────────────────
  directionBtn.addEventListener('click', () => {
    currentDirection = currentDirection === 'down' ? 'up' : 'down';
    sendMsg({ type: 'SET_DIRECTION', direction: currentDirection });
    updateDirectionBtn();
  });

  // ── Speed Slider ─────────────────────────────────────────────────────────
  speedSlider.addEventListener('input', () => {
    currentSpeed = parseInt(speedSlider.value);
    syncSpeedUI(currentSpeed);
    applySpeed(currentSpeed);
  });

  // ── Speed Number Input ────────────────────────────────────────────────────
  speedNumber.addEventListener('input', () => {
    let val = parseInt(speedNumber.value);
    if (isNaN(val)) return;
    val = Math.max(1, Math.min(30, val));
    currentSpeed = val;
    speedSlider.value = val;
    updateSpeedUI(val);
    updatePresetBtns(val);
    applySpeed(val);
  });

  speedNumber.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') speedNumber.blur();
  });

  speedNumber.addEventListener('blur', () => {
    let val = parseInt(speedNumber.value);
    if (isNaN(val) || val < 1) val = 1;
    if (val > 30) val = 30;
    currentSpeed = val;
    speedNumber.value = val;
    speedSlider.value = val;
    updateSpeedUI(val);
    updatePresetBtns(val);
    applySpeed(val);
  });

  // ── Preset Buttons ────────────────────────────────────────────────────────
  presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      currentSpeed = parseInt(btn.dataset.speed);
      syncSpeedUI(currentSpeed);
      applySpeed(currentSpeed);
    });
  });

  // ── Threshold Slider ──────────────────────────────────────────────────────
  thresholdSlider.addEventListener('input', () => {
    const t = parseInt(thresholdSlider.value);
    updateThresholdUI(t);
    sendMsg({ type: 'SET_THRESHOLD', threshold: t });
    chrome.storage.local.set({ threshold: t });
  });

  // ── Always Show ───────────────────────────────────────────────────────────
  alwaysShowToggle.addEventListener('change', () => {
    const val = alwaysShowToggle.checked;
    chrome.storage.local.set({ alwaysShow: val });
    sendMsg({ type: 'SET_ALWAYS_SHOW', value: val });
    if (val) { widgetVisible = true; updateWidgetBtn(); }
  });

  // ── UI helpers ────────────────────────────────────────────────────────────
  function updateAllUI() {
    updateScrollBtn();
    updateDirectionBtn();
    updateWidgetBtn();
    updateStatus();
  }

  function updateScrollBtn() {
    if (isScrolling) {
      toggleIcon.innerHTML = ICON_PAUSE;
      scrollToggleText.textContent = 'Pause';
      scrollToggleBtn.classList.add('playing');
    } else {
      toggleIcon.innerHTML = ICON_PLAY;
      scrollToggleText.textContent = 'Start';
      scrollToggleBtn.classList.remove('playing');
    }
  }

  function updateDirectionBtn() {
    if (currentDirection === 'down') {
      directionIcon.innerHTML = ICON_DOWN_DIR;
      directionText.textContent = 'Downward';
      directionBtn.classList.remove('dir-up');
    } else {
      directionIcon.innerHTML = ICON_UP_DIR;
      directionText.textContent = 'Upward';
      directionBtn.classList.add('dir-up');
    }
  }

  function updateWidgetBtn() {
    if (widgetVisible) {
      toggleWidgetBtn.classList.add('active');
      widgetBtnText.textContent = 'Hide widget from page';
    } else {
      toggleWidgetBtn.classList.remove('active');
      widgetBtnText.textContent = 'Show widget on page';
    }
  }

  function updateStatus() {
    if (isScrolling) {
      statusBadge.classList.add('active');
      statusDot.classList.add('active');
      statusText.textContent = currentDirection === 'down' ? 'Scrolling ↓' : 'Scrolling ↑';
    } else {
      statusBadge.classList.remove('active');
      statusDot.classList.remove('active');
      statusText.textContent = 'Stopped';
    }
  }

  function syncSpeedUI(speed) {
    speedSlider.value = speed;
    if (speedNumber) speedNumber.value = speed;
    updatePresetBtns(speed);
    const pct = ((speed - 1) / 29) * 100;
    speedSlider.style.setProperty('--val', pct + '%');
  }

  function applySpeed(speed) {
    sendMsg({ type: 'SET_SPEED', speed });
    chrome.storage.local.set({ scrollSpeed: speed });
  }

  function updateSpeedUI(speed) {
    if (speedNumber) speedNumber.value = speed;
    const pct = ((speed - 1) / 29) * 100;
    speedSlider.style.setProperty('--val', pct + '%');
  }

  function updateThresholdUI(val) {
    thresholdDisplay.textContent = val + 'px';
    const pct = ((val - 20) / 180) * 100;
    thresholdSlider.style.setProperty('--val', pct + '%');
  }

  function updatePresetBtns(speed) {
    presetBtns.forEach(btn => {
      btn.classList.toggle('active', parseInt(btn.dataset.speed) === speed);
    });
  }

  // ── Messaging ─────────────────────────────────────────────────────────────
  function sendMsg(message, callback) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tab = tabs?.[0];
      if (!tab?.id) return;

      // Check if we can inject (not a chrome:// page)
      const url = tab.url || '';
      if (url.startsWith('chrome://') || url.startsWith('chrome-extension://') || url.startsWith('edge://') || url === '') {
        if (callback) callback(null);
        return;
      }

      chrome.tabs.sendMessage(tab.id, message, (response) => {
        if (chrome.runtime.lastError) {
          // Inject content script first
          chrome.scripting.insertCSS({ target: { tabId: tab.id }, files: ['content/content.css'] })
            .then(() => chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ['content/content.js'] }))
            .then(() => {
              setTimeout(() => {
                chrome.tabs.sendMessage(tab.id, message, (r) => {
                  if (callback) callback(chrome.runtime.lastError ? null : r);
                });
              }, 150);
            })
            .catch(() => { if (callback) callback(null); });
        } else {
          if (callback) callback(response);
        }
      });
    });
  }
});
