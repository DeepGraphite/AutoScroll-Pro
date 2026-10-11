// AutoScroll Pro — Content Script

(function () {
  'use strict';

  if (window.__autoscrollProLoaded) return;
  window.__autoscrollProLoaded = true;

  // ─── State ─────────────────────────────────────────────────────────────────
  let scrollDirection     = 'down';
  let scrollSpeed         = 3;
  let isScrolling         = false;
  let animFrameId         = null;
  let widgetVisible       = false;
  let isDragging          = false;
  let dragOffsetX         = 0, dragOffsetY = 0;
  let widgetX             = 0, widgetY = 0;
  let lastMouseX          = 0;
  let mouseMoveThreshold  = 60;
  let mouseXAtScrollStart = 0;
  let alwaysShow          = false;

  // ─── Arrow SVGs — orange, bold, always visible ───────────────────────────
  const SVG_UP = `<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <polygon points="10,3 4,10 8,10 8,16 12,16 12,10 16,10" fill="#FF6B35"/>
  </svg>`;

  const SVG_DOWN = `<svg viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
    <polygon points="10,17 16,10 12,10 12,4 8,4 8,10 4,10" fill="#FF6B35"/>
  </svg>`;

  // ─── Wait for body ──────────────────────────────────────────────────────────
  function waitForBody(cb) {
    if (document.body) { cb(); return; }
    const obs = new MutationObserver(() => {
      if (document.body) { obs.disconnect(); cb(); }
    });
    obs.observe(document.documentElement, { childList: true });
  }

  // ─── Create Widget ──────────────────────────────────────────────────────────
  function createWidget() {
    if (document.getElementById('autoscroll-widget')) return;

    const widget = document.createElement('div');
    widget.id = 'autoscroll-widget';
    widget.className = 'hidden';

    widgetX = Math.round(window.innerWidth / 2 - 25);
    widgetY = window.innerHeight - 75;
    widget.style.cssText = `
      position: fixed !important;
      left: ${widgetX}px !important;
      top:  ${widgetY}px !important;
      z-index: 2147483647 !important;
    `;

    widget.innerHTML = `
      <div id="autoscroll-handle">
        <div id="asc-top">
          <div id="asc-arrow-up">${SVG_UP}</div>
        </div>
        <div id="asc-divider"></div>
        <div id="asc-bottom">
          <div id="asc-arrow-down">${SVG_DOWN}</div>
        </div>
      </div>
      <div id="autoscroll-tooltip">
        Hover ↑↓ to scroll<br>
        <small style="color:rgba(255,255,255,0.5)">Move mouse ← → to stop</small>
      </div>
    `;

    const target = document.body || document.documentElement;
    target.appendChild(widget);
    attachEvents(widget);
  }

  // ─── Attach Events ──────────────────────────────────────────────────────────
  function attachEvents(widget) {
    const handle  = widget.querySelector('#autoscroll-handle');
    const topHalf = widget.querySelector('#asc-top');
    const botHalf = widget.querySelector('#asc-bottom');
    if (!handle) return;

    // ── Top half: scroll UP instantly on hover or click ──────────────
    topHalf.addEventListener('mouseenter', (e) => {
      if (isDragging) return;
      scrollDirection = 'up';
      if (!isScrolling) startScroll();
      else updateScrollingState();
    });

    topHalf.addEventListener('click', (e) => {
      e.stopPropagation();
      if (isDragging) return;
      scrollDirection = 'up';
      if (!isScrolling) startScroll();
      else updateScrollingState();
    });

    // ── Bottom half: scroll DOWN instantly on hover or click ──────────
    botHalf.addEventListener('mouseenter', (e) => {
      if (isDragging) return;
      scrollDirection = 'down';
      if (!isScrolling) startScroll();
      else updateScrollingState();
    });

    botHalf.addEventListener('click', (e) => {
      e.stopPropagation();
      if (isDragging) return;
      scrollDirection = 'down';
      if (!isScrolling) startScroll();
      else updateScrollingState();
    });

    // ── Only left/right mouse movement stops scrolling ──────────────────────

    // ── Drag to reposition widget ─────────────────────────────────────────
    handle.addEventListener('mousedown', (e) => {
      if (e.button !== 0) return;
      isDragging = false;
      const startX = e.clientX, startY = e.clientY;
      dragOffsetX = e.clientX - widgetX;
      dragOffsetY = e.clientY - widgetY;

      const onMove = (ev) => {
        if (Math.abs(ev.clientX - startX) > 5 || Math.abs(ev.clientY - startY) > 5) {
          isDragging = true;
        }
        if (!isDragging) return;
        widgetX = Math.max(4, Math.min(window.innerWidth  - 58, ev.clientX - dragOffsetX));
        widgetY = Math.max(4, Math.min(window.innerHeight - 58, ev.clientY - dragOffsetY));
        widget.style.setProperty('left', widgetX + 'px', 'important');
        widget.style.setProperty('top',  widgetY + 'px', 'important');
        savePosition(widgetX, widgetY);
      };
      const onUp = () => {
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
        setTimeout(() => { isDragging = false; }, 60);
      };
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    });

    // ── Scroll wheel → adjust speed ───────────────────────────────────────
    handle.addEventListener('wheel', (e) => {
      e.preventDefault(); e.stopPropagation();
      scrollSpeed = e.deltaY < 0
        ? Math.min(10, scrollSpeed + 1)
        : Math.max(1,  scrollSpeed - 1);
      saveSettings();
      updateTooltip();
    }, { passive: false });

    // ── Right-click → stop ────────────────────────────────────────────────
    handle.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      if (isScrolling) stopScroll();
    });
  }

  // ─── Scroll Logic ───────────────────────────────────────────────────────────
  function startScroll() {
    isScrolling = true;
    mouseXAtScrollStart = lastMouseX;
    updateScrollingState();
    animFrameId = requestAnimationFrame(doScroll);
  }

  function stopScroll() {
    isScrolling = false;
    if (animFrameId) { cancelAnimationFrame(animFrameId); animFrameId = null; }
    updateScrollingState();
  }

  function doScroll() {
    if (!isScrolling) return;
    const el  = document.scrollingElement || document.documentElement;
    const dir = scrollDirection === 'down' ? 1 : -1;
    el.scrollTop += dir * scrollSpeed;

    // Auto-stop at edge
    const max = el.scrollHeight - el.clientHeight;
    if (max > 0) {
      if (scrollDirection === 'down' && el.scrollTop >= max) { stopScroll(); return; }
      if (scrollDirection === 'up'   && el.scrollTop <= 0)   { stopScroll(); return; }
    }
    animFrameId = requestAnimationFrame(doScroll);
  }

  function updateScrollingState() {
    const handle = document.getElementById('autoscroll-handle');
    if (!handle) return;
    handle.classList.remove('scrolling-up', 'scrolling-down');
    if (isScrolling) {
      handle.classList.add(scrollDirection === 'up' ? 'scrolling-up' : 'scrolling-down');
    }
    updateTooltip();
  }

  function updateTooltip() {
    const tip = document.getElementById('autoscroll-tooltip');
    if (!tip) return;
    if (isScrolling) {
      const sym = scrollDirection === 'up' ? '↑' : '↓';
      tip.innerHTML = `Scrolling ${scrollDirection} ${sym}<br><small style="color:rgba(255,255,255,0.5)">Move mouse ← → to stop</small>`;
    } else {
      tip.innerHTML = `↑ tap top &nbsp;·&nbsp; ↓ tap bottom<br><small style="color:rgba(255,255,255,0.5)">Move mouse ← → to stop</small>`;
    }
  }

  // ─── Mouse horizontal → stop ────────────────────────────────────────────────
  document.addEventListener('mousemove', (e) => {
    lastMouseX = e.clientX;
    if (isScrolling && Math.abs(e.clientX - mouseXAtScrollStart) > mouseMoveThreshold) {
      stopScroll();
    }
  }, true);

  // ─── Show / Hide ────────────────────────────────────────────────────────────
  function showWidget() {
    const widget = document.getElementById('autoscroll-widget');
    if (!widget) { createWidget(); setTimeout(showWidget, 60); return; }

    chrome.storage.local.get(['widgetX','widgetY','scrollSpeed','scrollDirection'], (data) => {
      if (data.widgetX !== undefined) {
        widgetX = Math.min(data.widgetX, window.innerWidth  - 58);
        widgetY = Math.min(data.widgetY, window.innerHeight - 58);
        widget.style.setProperty('left', widgetX + 'px', 'important');
        widget.style.setProperty('top',  widgetY + 'px', 'important');
      }
      if (data.scrollSpeed)     scrollSpeed     = data.scrollSpeed;
      if (data.scrollDirection) scrollDirection  = data.scrollDirection;
      updateTooltip();
    });

    widget.classList.remove('hidden');
    widget.classList.add('visible');
    widgetVisible = true;
  }

  function hideWidget() {
    stopScroll();
    const widget = document.getElementById('autoscroll-widget');
    if (!widget) return;
    widget.classList.remove('visible');
    widget.classList.add('hidden');
    widgetVisible = false;
  }

  // ─── Storage ────────────────────────────────────────────────────────────────
  function savePosition(x, y) { chrome.storage.local.set({ widgetX: x, widgetY: y }); }
  function saveSettings()      { chrome.storage.local.set({ scrollSpeed, scrollDirection }); }

  // ─── Messages ────────────────────────────────────────────────────────────────
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    switch (msg.type) {
      case 'PING':
        sendResponse({ ok: true }); break;

      case 'TOGGLE_WIDGET':
        waitForBody(() => {
          if (!document.getElementById('autoscroll-widget')) createWidget();
          if (widgetVisible) hideWidget(); else showWidget();
          sendResponse({ visible: widgetVisible });
        });
        break;

      case 'GET_STATE':
        sendResponse({ isScrolling, scrollDirection, scrollSpeed, widgetVisible }); break;

      case 'SET_SPEED':
        scrollSpeed = msg.speed;
        saveSettings();
        sendResponse({ ok: true }); break;

      case 'SET_DIRECTION':
        scrollDirection = msg.direction;
        if (isScrolling) updateScrollingState();
        saveSettings();
        sendResponse({ ok: true }); break;

      case 'TOGGLE_SCROLL':
        isScrolling ? stopScroll() : startScroll();
        sendResponse({ isScrolling }); break;

      case 'STOP_SCROLL':
        stopScroll(); sendResponse({ ok: true }); break;

      case 'SET_ALWAYS_SHOW':
        alwaysShow = msg.value;
        waitForBody(() => {
          if (alwaysShow) { createWidget(); showWidget(); }
          else hideWidget();
        });
        sendResponse({ ok: true }); break;

      case 'SET_THRESHOLD':
        mouseMoveThreshold = msg.threshold;
        sendResponse({ ok: true }); break;
    }
    return true;
  });

  // ─── Auto-show ───────────────────────────────────────────────────────────────
  chrome.storage.local.get(['alwaysShow','scrollSpeed','scrollDirection'], (data) => {
    if (data.scrollSpeed)     scrollSpeed     = data.scrollSpeed;
    if (data.scrollDirection) scrollDirection  = data.scrollDirection;
    if (data.alwaysShow) {
      alwaysShow = true;
      waitForBody(() => { createWidget(); showWidget(); });
    }
  });

})();
