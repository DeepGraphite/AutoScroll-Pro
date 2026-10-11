# AutoScroll Pro - Chrome Extension

A smooth, feature-rich auto-scrolling Chrome extension with speed control, direction toggle, and a floating in-page widget.

## Features

- 🖱️ **Floating Widget**: A draggable scroll icon appears on any webpage
- ⬆️⬇️ **Bi-directional Scrolling**: Scroll up or down with one click
- 🎚️ **Speed Control**: 10 speed levels (1–10) with preset buttons
- 🛑 **Auto-stop on Mouse Move**: Moving the mouse left or right stops scrolling
- 📌 **Always Show Mode**: Widget appears on all pages automatically
- 🖱️ **Drag to Reposition**: Move the widget anywhere on the page
- 🔄 **Right-click to Flip Direction**: Instantly reverse scroll direction
- 🌙 **Dark Mode UI**: Beautiful dark popup with Arabic support

## Installation (Developer Mode)

1. Open Chrome and navigate to: `chrome://extensions/`
2. Enable **Developer Mode** (top right toggle)
3. Click **"Load unpacked"**
4. Select this folder: `/Users/muaz/Documents/Chrome Extensions/autoscroll`
5. The ✅ AutoScroll Pro icon will appear in your Chrome toolbar!

## How to Use

### Basic Usage
- Click the **extension icon** in the toolbar → popup opens
- Click **"إظهار الأداة في الصفحة"** to show the floating widget on the current page
- Click the floating widget to **start/stop** scrolling
- The **green glow** = scrolling down, **amber glow** = scrolling up

### Speed Control
- Use the **slider** in the popup to set speed (1–10)
- Or click quick presets: 🐢 بطيء / 🏃 متوسط / 🚀 سريع
- **Scroll wheel** on the floating widget also changes speed

### Stop Scrolling
- **Click** the widget again
- **Move mouse horizontally** (left/right) past the threshold
- Use the **Stop** button in popup

### Direction
- **Right-click** the floating widget to flip direction instantly
- Click **"للأسفل / للأعلى"** button in the popup

## Publishing to Chrome Web Store

### Requirements
- A Google Developer account ($5 one-time fee)
- Store listing assets (screenshots, description)

### Steps
1. **Zip the extension**:
   ```
   cd "/Users/muaz/Documents/Chrome Extensions"
   zip -r autoscroll-pro.zip autoscroll/ --exclude "*.py" --exclude "*.md"
   ```

2. **Go to**: https://chrome.google.com/webstore/devconsole

3. **Click**: "Add new item" → Upload the zip file

4. **Fill in**:
   - Name: `AutoScroll Pro`
   - Category: `Productivity`
   - Language: Arabic + English
   - Description (see below)
   - Screenshots (1280×800 or 640×400)
   - Privacy policy URL (required)

5. **Set Price**: Free ✅

6. **Submit for Review** (usually 1–3 business days)

### Store Description (English)
```
AutoScroll Pro lets you automatically scroll any webpage up or down with a single click. 

Features:
• Floating draggable scroll widget on every page
• 10-level speed control
• Auto-stops when you move your mouse horizontally
• Right-click to flip scroll direction
• Always-show mode for quick access
• Beautiful dark UI with full speed customization
```

### Store Description (Arabic)
```
AutoScroll Pro يتيح لك التمرير التلقائي لأي صفحة ويب لأعلى أو لأسفل بنقرة واحدة.

المميزات:
• أداة تمرير عائمة وقابلة للسحب في كل صفحة
• تحكم بالسرعة من 1 إلى 10 مستويات
• يتوقف تلقائياً عند تحريك الماوس أفقياً
• انقر بزر الماوس الأيمن لعكس اتجاه التمرير
• وضع الإظهار الدائم للوصول السريع
• واجهة مظلمة جميلة مع تخصيص كامل
```

## File Structure

```
autoscroll/
├── manifest.json          # Extension config (Manifest V3)
├── background/
│   └── background.js      # Service worker
├── content/
│   ├── content.js         # In-page widget logic
│   └── content.css        # Widget styles
├── popup/
│   ├── popup.html         # Extension popup
│   ├── popup.css          # Popup styles
│   └── popup.js           # Popup logic
└── icons/
    ├── icon16.png
    ├── icon32.png
    ├── icon48.png
    └── icon128.png
```

## Privacy Policy (Required for Store)

> AutoScroll Pro does not collect, store, or transmit any personal data. All settings (speed, direction, widget position) are stored locally using Chrome's storage API and never leave your device.

Host a simple privacy policy page (GitHub Pages is free) before submitting.
