// AutoScroll Pro — Background Service Worker

// ─── Helper: inject content script into a tab if not already there ──────────
async function ensureContentScript(tabId) {
  try {
    // Try a ping first
    await chrome.tabs.sendMessage(tabId, { type: 'PING' });
    return true; // already injected
  } catch {
    // Not injected — try to inject
    try {
      await chrome.scripting.insertCSS({
        target: { tabId },
        files: ['content/content.css']
      });
      await chrome.scripting.executeScript({
        target: { tabId },
        files: ['content/content.js']
      });
      // Small delay for script init
      await new Promise(r => setTimeout(r, 120));
      return true;
    } catch (err) {
      // Protected pages (chrome://, extensions store, etc.) — silently skip
      console.warn('AutoScroll Pro: cannot inject into this page:', err.message);
      return false;
    }
  }
}

// ─── Relay messages from popup → content script ──────────────────────────────
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'PING') {
    sendResponse({ ok: true });
    return;
  }

  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const tab = tabs?.[0];
    if (!tab?.id) { sendResponse({ error: 'no active tab' }); return; }

    const injected = await ensureContentScript(tab.id);
    if (!injected) {
      sendResponse({ error: 'protected page' });
      return;
    }

    try {
      chrome.tabs.sendMessage(tab.id, message, (response) => {
        if (chrome.runtime.lastError) {
          sendResponse({ error: chrome.runtime.lastError.message });
        } else {
          sendResponse(response);
        }
      });
    } catch (err) {
      sendResponse({ error: err.message });
    }
  });

  return true; // keep channel open
});

// ─── On install: set defaults ────────────────────────────────────────────────
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['scrollSpeed', 'scrollDirection', 'threshold'], (data) => {
    const defaults = {};
    if (!data.scrollSpeed)    defaults.scrollSpeed    = 3;
    if (!data.scrollDirection) defaults.scrollDirection = 'down';
    if (!data.threshold)      defaults.threshold      = 60;
    if (Object.keys(defaults).length) chrome.storage.local.set(defaults);
  });
});
