# AutoScroll Pro - Chrome Extension

A smooth, high-performance automated scrolling Chrome extension with granular speed controls, direction toggling, and an intuitive floating in-page widget. Developed by DeepGraphite.

## Key Features

- 🖱️ **Floating Split Widget**: A minimal, elegant floating widget on any page. Hover or click the top half to scroll up, or bottom half to scroll down.
- ⬆️⬇️ **Bi-Directional Scrolling**: Smooth scrolling powered by `requestAnimationFrame`.
- 🎚️ **Customizable Speed**: Choose any speed between 1 and 30 px/frame, or pick instant presets (Slow, Normal, Fast, Turbo).
- 🛑 **Smart Mouse-Release**: Move your mouse horizontally (left or right) to immediately release scrolling.
- 📌 **Always-Show Mode**: Option to show the widget automatically across all browsing tabs.
- 🖱️ **Draggable Placement**: Drag and position the widget anywhere on your viewport.
- 🔒 **100% Private**: Runs entirely locally on your device with zero data collection.

## Installation (Developer Mode)

1. Open Chrome and navigate to: `chrome://extensions/`
2. Enable **Developer Mode** (top-right toggle).
3. Click **"Load unpacked"**.
4. Select this folder: `/Users/muaz/Documents/Chrome Extensions/autoscroll`.
5. The AutoScroll Pro icon will appear in your Chrome toolbar.

## Usage

### Basic Controls
- Click the **extension icon** in your toolbar to open the control popup.
- Click **"Show widget on page"** to display the floating widget.
- Hover or tap either half of the widget to begin scrolling in that direction.

### Speed Customization
- Adjust the **Scroll Speed slider** or type your desired speed into the number input (1–30 px/frame).
- Use quick preset buttons: `Slow·2`, `Normal·5`, `Fast·12`, or `Turbo·25`.

### Stopping Auto-Scroll
- **Move your mouse horizontally** (left or right) to release the scroll immediately.
- Or click **Pause** in the extension popup.

## Architecture

- `manifest.json`: Manifest V3 configuration.
- `background/background.js`: Lightweight service worker for active tab injection and messaging.
- `content/content.js`: Core scrolling engine, event listeners, and draggable widget mechanics.
- `content/content.css`: Modern glassmorphic styles and animations.
- `popup/`: User settings popup with speed sliders and quick controls.
- `icons/`: High-resolution RGBA icons (16px, 32px, 48px, 128px).

## Privacy Policy

AutoScroll Pro operates completely offline and respects user privacy. See [PRIVACY_POLICY.md](PRIVACY_POLICY.md) for full details.
