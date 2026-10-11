#!/usr/bin/env python3
"""
Generate Promo Tiles for Chrome Web Store:
1. Small Promo Tile: 440x280 (24-bit RGB PNG, NO alpha)
2. Marquee / Featured Promo Tile: 1400x560 (24-bit RGB PNG, NO alpha)
"""
import os
from PIL import Image, ImageDraw, ImageFont

base_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_dir, "store_assets")
os.makedirs(assets_dir, exist_ok=True)

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG  = "/System/Library/Fonts/Supplemental/Arial.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# ── 1. Small Promo Tile (440x280) ───────────────────────────────────────────
def make_small_promo():
    W, H = 440, 280
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Clean gradient-like background top to bottom
    for y in range(H):
        r = int(255 - (y / H) * 12)
        g = int(250 - (y / H) * 18)
        b = int(245 - (y / H) * 22)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Decorative warm circular aura behind widget
    draw.ellipse([270, 40, 450, 220], fill=(255, 237, 213))

    # Mockup of the AutoScroll floating widget on the right
    wx, wy, ws = 305, 80, 105
    # Shadow
    draw.ellipse([wx+3, wy+5, wx+ws+3, wy+ws+5], fill=(226, 232, 240))
    # Widget circle
    draw.ellipse([wx, wy, wx+ws, wy+ws], fill=(255, 255, 255), outline=(255, 107, 53), width=6)
    # Divider
    draw.line([(wx+24, wy+ws//2), (wx+ws-24, wy+ws//2)], fill=(255, 107, 53), width=3)
    # Up arrow
    draw.polygon([(wx+ws//2, wy+22), (wx+ws//2-14, wy+40), (wx+ws//2+14, wy+40)], fill=(255, 107, 53))
    # Down arrow
    draw.polygon([(wx+ws//2, wy+ws-22), (wx+ws//2-14, wy+ws-40), (wx+ws//2+14, wy+ws-40)], fill=(255, 107, 53))

    # Left content: Brand and Title
    # Orange badge
    draw_rounded_rect(draw, (28, 42, 135, 66), 12, fill=(255, 107, 53))
    draw.text((40, 48), "CHROME EXTENSION", fill=(255, 255, 255), font=get_font(FONT_BOLD, 9))

    # Main Title
    draw.text((28, 80), "AutoScroll", fill=(17, 24, 39), font=get_font(FONT_BOLD, 28))
    draw.text((28, 114), "Pro", fill=(255, 107, 53), font=get_font(FONT_BOLD, 28))

    # Subtitle
    draw.text((28, 160), "Hands-free smart scrolling", fill=(75, 85, 99), font=get_font(FONT_BOLD, 13))
    draw.text((28, 180), "with instant speed controls.", fill=(107, 114, 128), font=get_font(FONT_REG, 12))

    # Feature tags
    draw_rounded_rect(draw, (28, 218, 132, 244), 6, fill=(255, 237, 213))
    draw.text((36, 224), "⚡ Speed 1–30", fill=(194, 65, 12), font=get_font(FONT_BOLD, 10))

    draw_rounded_rect(draw, (140, 218, 250, 244), 6, fill=(240, 253, 244))
    draw.text((148, 224), "🖱️ Smart Stop", fill=(22, 101, 52), font=get_font(FONT_BOLD, 10))

    path = os.path.join(assets_dir, "promo_small_440x280.png")
    img.save(path, "PNG")
    print(f"✓ Created {path}")

# ── 2. Marquee Promo Tile (1400x560) ────────────────────────────────────────
def make_marquee_promo():
    W, H = 1400, 560
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Soft subtle background
    for y in range(H):
        r = int(255 - (y / H) * 10)
        g = int(250 - (y / H) * 16)
        b = int(246 - (y / H) * 20)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Decorative soft circles
    draw.ellipse([880, 40, 1360, 520], fill=(255, 245, 235))
    draw.ellipse([980, 100, 1300, 420], fill=(255, 237, 213))

    # Floating Widget Mockup (large, centered in right side)
    wx, wy, ws = 1040, 170, 200
    # Shadow
    draw.ellipse([wx+6, wy+10, wx+ws+6, wy+ws+10], fill=(226, 232, 240))
    # Widget circle
    draw.ellipse([wx, wy, wx+ws, wy+ws], fill=(255, 255, 255), outline=(255, 107, 53), width=10)
    # Divider
    draw.line([(wx+45, wy+ws//2), (wx+ws-45, wy+ws//2)], fill=(255, 107, 53), width=5)
    # Up arrow
    draw.polygon([(wx+ws//2, wy+40), (wx+ws//2-25, wy+76), (wx+ws//2+25, wy+76)], fill=(255, 107, 53))
    # Down arrow
    draw.polygon([(wx+ws//2, wy+ws-40), (wx+ws//2-25, wy+ws-76), (wx+ws//2+25, wy+ws-76)], fill=(255, 107, 53))

    # Left content:
    # Pill badge
    draw_rounded_rect(draw, (90, 80, 260, 115), 17, fill=(255, 107, 53))
    draw.text((115, 91), "AUTOSCROLL PRO", fill=(255, 255, 255), font=get_font(FONT_BOLD, 13))

    # Big Headline
    draw.text((90, 140), "Effortless Hands-Free Scrolling", fill=(17, 24, 39), font=get_font(FONT_BOLD, 50))
    draw.text((90, 210), "For Chrome", fill=(255, 107, 53), font=get_font(FONT_BOLD, 50))

    # Subtitle
    draw.text((90, 290), "Glide through documents, feeds, and articles with zero finger strain.", fill=(75, 85, 99), font=get_font(FONT_REG, 23))
    draw.text((90, 325), "Instant hover-to-scroll, customizable speeds (1–30 px), and mouse release.", fill=(107, 114, 128), font=get_font(FONT_REG, 19))

    # Feature tags
    pills = [
        ("✨ Instant Hover & Tap", (254, 243, 199), (180, 83, 9)),
        ("⚡ 1–30 Custom Speed Slider", (255, 237, 213), (194, 65, 12)),
        ("🖱️ Left / Right Mouse Release", (238, 242, 255), (67, 56, 202)),
        ("🛡️ 100% Private — No Data Collected", (240, 253, 244), (22, 101, 52)),
    ]
    px = 90
    py = 405
    for label, bg, col in pills:
        pw = len(label) * 11 + 28
        draw_rounded_rect(draw, (px, py, px + pw, py + 42), 21, fill=bg)
        draw.text((px + 14, py + 12), label, fill=col, font=get_font(FONT_BOLD, 14))
        px += pw + 16

    # Bottom branding
    draw.text((90, 485), "Crafted with passion by DeepGraphite", fill=(156, 163, 175), font=get_font(FONT_REG, 14))

    path = os.path.join(assets_dir, "promo_marquee_1400x560.png")
    img.save(path, "PNG")
    print(f"✓ Created {path}")

make_small_promo()
make_marquee_promo()
print("🎉 All promotional tiles created successfully!")
