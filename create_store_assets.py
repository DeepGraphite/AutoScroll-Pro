#!/usr/bin/env python3
"""
Generate official Chrome Web Store assets:
1. Store Icon (128x128 PNG)
2. Promotional Screenshots (1280x800, 24-bit RGB PNG, NO alpha)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

# ── 1. Store Icon (128x128) ──────────────────────────────────────────────────
def make_store_icon():
    scale = 4
    size = 128 * scale
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Rounded background with smooth orange border
    pad = size * 0.06
    draw.ellipse([pad, pad, size - pad, size - pad], fill=(255, 255, 255, 255), outline=(255, 107, 53, 255), width=int(size * 0.08))

    # Center divider
    my = size / 2
    dhw = size * 0.28
    draw.line([(size/2 - dhw, my), (size/2 + dhw, my)], fill=(255, 107, 53, 90), width=int(size * 0.025))

    orange = (255, 107, 53, 255)
    cx = size / 2
    # Up arrow
    draw.polygon([
        (cx, size * 0.18),
        (cx - size * 0.15, size * 0.36),
        (cx - size * 0.065, size * 0.36),
        (cx - size * 0.065, size * 0.44),
        (cx + size * 0.065, size * 0.44),
        (cx + size * 0.065, size * 0.36),
        (cx + size * 0.15, size * 0.36),
    ], fill=orange)

    # Down arrow
    draw.polygon([
        (cx, size * 0.82),
        (cx - size * 0.15, size * 0.64),
        (cx - size * 0.065, size * 0.64),
        (cx - size * 0.065, size * 0.56),
        (cx + size * 0.065, size * 0.56),
        (cx + size * 0.065, size * 0.64),
        (cx + size * 0.15, size * 0.64),
    ], fill=orange)

    out = img.resize((128, 128), Image.Resampling.LANCZOS)
    path = os.path.join(assets_dir, "store_icon_128.png")
    out.save(path, "PNG", optimize=True)
    print(f"✓ Created {path}")

# ── 2. Helper to draw rounded rectangle ──────────────────────────────────────
def draw_rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

# ── 3. Screenshot 1: Overview & Hands-Free Scrolling ────────────────────────
def make_screenshot_1():
    W, H = 1280, 800
    img = Image.new("RGB", (W, H), (248, 249, 252)) # Clean modern background
    draw = ImageDraw.Draw(img)

    # Top brand banner
    for y in range(80):
        # subtle top gradient
        r = int(255 - (y/80)*5)
        g = int(247 - (y/80)*3)
        b = int(242 - (y/80)*2)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Badge
    f_badge = get_font(FONT_BOLD, 13)
    draw_rounded_rect(draw, (80, 48, 230, 78), 15, fill=(255, 107, 53), outline=None)
    draw.text((102, 54), "AUTOSCROLL PRO", fill=(255, 255, 255), font=f_badge)

    # Main Headline
    f_title = get_font(FONT_BOLD, 46)
    f_sub   = get_font(FONT_REG, 21)
    draw.text((80, 100), "Effortless Hands-Free Scrolling", fill=(17, 24, 39), font=f_title)
    draw.text((80, 160), "Read long articles, code, and feeds without lifting a finger.", fill=(107, 114, 128), font=f_sub)

    # Feature pills
    f_pill = get_font(FONT_BOLD, 15)
    pills = [
        ("✨ Instant Hover & Tap", (254, 243, 199), (180, 83, 9)),
        ("⚡ 1–30 Custom Speed", (255, 237, 213), (194, 65, 12)),
        ("🖱️ Horizontal Mouse Release", (238, 242, 255), (67, 56, 202)),
    ]
    px = 80
    for label, bg, col in pills:
        pw = len(label) * 11 + 24
        draw_rounded_rect(draw, (px, 208, px + pw, 244), 18, fill=bg)
        draw.text((px + 14, 217), label, fill=col, font=f_pill)
        px += pw + 14

    # ── Mockup: Browser Window ───────────────────────────────────────────────
    bx, by, bw, bh = 80, 275, 1120, 475
    # Window shadow
    draw_rounded_rect(draw, (bx+6, by+8, bx+bw+6, by+bh+8), 16, fill=(226, 232, 240))
    # Window body
    draw_rounded_rect(draw, (bx, by, bx+bw, by+bh), 16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    # Browser toolbar
    draw_rounded_rect(draw, (bx, by, bx+bw, by+52), 16, fill=(241, 245, 249))
    draw.rectangle([bx, by+36, bx+bw, by+52], fill=(241, 245, 249))
    draw.line([(bx, by+52), (bx+bw, by+52)], fill=(226, 232, 240), width=1)

    # Browser buttons
    draw.ellipse([bx+20, by+20, bx+32, by+32], fill=(239, 68, 68))
    draw.ellipse([bx+38, by+20, bx+50, by+32], fill=(245, 158, 11))
    draw.ellipse([bx+56, by+20, bx+68, by+32], fill=(16, 185, 129))

    # Address bar
    draw_rounded_rect(draw, (bx+90, by+12, bx+600, by+40), 8, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    f_url = get_font(FONT_REG, 13)
    draw.text((bx+105, by+19), "🔒 https://wikipedia.org/wiki/Artificial_Intelligence", fill=(100, 116, 139), font=f_url)

    # Page content simulation
    # Article title
    f_art_h = get_font(FONT_BOLD, 22)
    draw.text((bx+50, by+85), "Deep Learning & Neural Architectures", fill=(30, 41, 59), font=f_art_h)
    f_art_p = get_font(FONT_REG, 14)
    lines = [
        "Artificial intelligence systems have undergone rapid transformation with modern deep architectures.",
        "Through autonomous representations, multi-layer networks discover feature hierarchies directly from raw inputs.",
        "Applications span from continuous natural language synthesis to automated cognitive workflows.",
        "As computational efficiency expands, real-time contextual interactions unlock unprecedented scalability."
    ]
    py = by + 125
    for l in lines:
        draw.text((bx+50, py), l, fill=(71, 85, 105), font=f_art_p)
        py += 24

    # Another paragraph
    py += 15
    draw.text((bx+50, py), "Evolution of Continuous User Interfaces", fill=(51, 65, 85), font=get_font(FONT_BOLD, 17))
    py += 30
    lines2 = [
        "Human-computer interfaces thrive when friction is eliminated. Automated viewport navigation empowers readers",
        "to maintain deep focus without physical strain from continuous manual wheel scrolling.",
        "Smart threshold calibration ensures intentional interaction while preserving natural stop gestures."
    ]
    for l in lines2:
        draw.text((bx+50, py), l, fill=(100, 116, 139), font=f_art_p)
        py += 24

    # ── Mockup of Floating Widget in Bottom-Center ───────────────────────────
    wx = bx + (bw // 2) - 30
    wy = by + bh - 90
    ws = 60
    # Widget shadow
    draw.ellipse([wx-2, wy+2, wx+ws+2, wy+ws+6], fill=(203, 213, 225))
    # Widget circle
    draw.ellipse([wx, wy, wx+ws, wy+ws], fill=(255, 255, 255), outline=(255, 107, 53), width=4)
    # Divider
    draw.line([(wx+14, wy+ws//2), (wx+ws-14, wy+ws//2)], fill=(255, 107, 53), width=2)
    # Up arrow
    draw.polygon([(wx+ws//2, wy+12), (wx+ws//2-8, wy+22), (wx+ws//2+8, wy+22)], fill=(255, 107, 53))
    # Down arrow
    draw.polygon([(wx+ws//2, wy+ws-12), (wx+ws//2-8, wy+ws-22), (wx+ws//2+8, wy+ws-22)], fill=(255, 107, 53))

    # Widget tooltip banner
    draw_rounded_rect(draw, (wx-80, wy-38, wx+ws+80, wy-10), 8, fill=(30, 41, 59))
    draw.text((wx-55, wy-30), "Hover ↑ / ↓ to Auto-Scroll", fill=(255, 255, 255), font=get_font(FONT_BOLD, 12))

    # ── Mockup of Popup on the Right ─────────────────────────────────────────
    px0 = bx + bw - 330
    py0 = by + 68
    pw0 = 300
    ph0 = 360
    draw_rounded_rect(draw, (px0+4, py0+6, px0+pw0+4, py0+ph0+6), 14, fill=(203, 213, 225))
    draw_rounded_rect(draw, (px0, py0, px0+pw0, py0+ph0), 14, fill=(255, 255, 255), outline=(255, 107, 53), width=2)

    # Popup header gradient simulation
    draw_rounded_rect(draw, (px0, py0, px0+pw0, py0+58), 14, fill=(255, 107, 53))
    draw.rectangle([px0, py0+44, px0+pw0, py0+58], fill=(255, 107, 53))
    draw.text((px0+18, py0+15), "AutoScroll Pro", fill=(255, 255, 255), font=get_font(FONT_BOLD, 17))
    draw.text((px0+18, py0+36), "Active · Free v1.0", fill=(255, 237, 213), font=get_font(FONT_REG, 11))

    # Speed control mockup
    draw.text((px0+18, py0+76), "SCROLL SPEED", fill=(75, 85, 99), font=get_font(FONT_BOLD, 11))
    draw_rounded_rect(draw, (px0+pw0-65, py0+72, px0+pw0-18, py0+94), 6, fill=(255, 245, 240), outline=(255, 107, 53), width=1)
    draw.text((px0+pw0-48, py0+76), "5", fill=(255, 107, 53), font=get_font(FONT_BOLD, 13))

    # Slider bar
    draw_rounded_rect(draw, (px0+18, py0+106, px0+pw0-18, py0+112), 3, fill=(229, 231, 235))
    draw_rounded_rect(draw, (px0+18, py0+106, px0+110, py0+112), 3, fill=(255, 107, 53))
    draw.ellipse([px0+104, py0+102, px0+118, py0+116], fill=(255, 107, 53))

    # Preset buttons
    speeds = ["Slow·2", "Normal·5", "Fast·12", "Turbo·25"]
    btn_w = (pw0 - 36 - 18) // 4
    for i, s in enumerate(speeds):
        bx_p = px0 + 18 + i * (btn_w + 6)
        active = (i == 1)
        bg_col = (255, 107, 53) if active else (249, 250, 251)
        txt_col = (255, 255, 255) if active else (75, 85, 99)
        draw_rounded_rect(draw, (bx_p, py0+128, bx_p + btn_w, py0+156), 6, fill=bg_col, outline=(255, 107, 53) if active else (229, 231, 235), width=1)
        draw.text((bx_p + 5, py0+137), s, fill=txt_col, font=get_font(FONT_BOLD, 9))

    # Quick Controls buttons
    draw_rounded_rect(draw, (px0+18, py0+174, px0+pw0//2-6, py0+214), 8, fill=(240, 253, 244), outline=(34, 197, 94), width=1)
    draw.text((px0+42, py0+188), "▶ Start", fill=(22, 101, 52), font=get_font(FONT_BOLD, 13))

    draw_rounded_rect(draw, (px0+pw0//2+6, py0+174, px0+pw0-18, py0+214), 8, fill=(249, 250, 251), outline=(229, 231, 235), width=1)
    draw.text((px0+pw0//2+25, py0+188), "↓ Downward", fill=(55, 65, 81), font=get_font(FONT_BOLD, 12))

    # Info banner in popup
    draw_rounded_rect(draw, (px0+18, py0+230, px0+pw0-18, py0+280), 8, fill=(254, 243, 199), outline=(245, 158, 11), width=1)
    draw.text((px0+28, py0+238), "💡 Quick Release:", fill=(146, 64, 14), font=get_font(FONT_BOLD, 11))
    draw.text((px0+28, py0+256), "Move mouse left or right to stop scrolling", fill=(146, 64, 14), font=get_font(FONT_REG, 10))

    # Developer tag
    draw.text((px0+95, py0+320), "Developed by DeepGraphite", fill=(156, 163, 175), font=get_font(FONT_REG, 11))

    path = os.path.join(assets_dir, "screenshot1_1280x800.png")
    # Save as 24-bit RGB (NO ALPHA)
    img.save(path, "PNG")
    print(f"✓ Created {path}")

# ── 4. Screenshot 2: Speed Customization & Smart Controls ───────────────────
def make_screenshot_2():
    W, H = 1280, 800
    img = Image.new("RGB", (W, H), (248, 249, 252))
    draw = ImageDraw.Draw(img)

    # Top brand badge
    f_badge = get_font(FONT_BOLD, 13)
    draw_rounded_rect(draw, (80, 48, 230, 78), 15, fill=(255, 107, 53), outline=None)
    draw.text((102, 54), "SMART SPEED CONTROL", fill=(255, 255, 255), font=f_badge)

    # Headline
    draw.text((80, 100), "Tailored For Every Reading Pace", fill=(17, 24, 39), font=get_font(FONT_BOLD, 46))
    draw.text((80, 160), "From relaxed reading to rapid scanning: precise 1 to 30 px/frame speeds.", fill=(107, 114, 128), font=get_font(FONT_REG, 21))

    # 3 Feature Cards
    cards = [
        ("🐌 Slow·2 (Reading)", "Perfect for books, academic papers, and detailed articles.", (255, 247, 237), (255, 107, 53)),
        ("⚡ Normal·5 (Browsing)", "Ideal for blogs, news feeds, and social media timelines.", (238, 242, 255), (79, 70, 229)),
        ("🚀 Turbo·25 (Scanning)", "Fast scanning through voluminous documentation & code.", (240, 253, 244), (22, 163, 74)),
    ]

    cx0 = 80
    for title, desc, bg, acc in cards:
        draw_rounded_rect(draw, (cx0, 225, cx0 + 350, 420), 16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
        # Accent top bar
        draw_rounded_rect(draw, (cx0, 225, cx0 + 350, 235), 16, fill=acc)
        draw.rectangle([cx0, 230, cx0 + 350, 235], fill=acc)
        # Icon circle
        draw.ellipse([cx0 + 24, 255, cx0 + 64, 295], fill=bg)
        # Title
        draw.text((cx0 + 24, 315), title, fill=(17, 24, 39), font=get_font(FONT_BOLD, 19))
        # Desc
        draw.text((cx0 + 24, 355), desc[:35], fill=(107, 114, 128), font=get_font(FONT_REG, 14))
        draw.text((cx0 + 24, 380), desc[35:], fill=(107, 114, 128), font=get_font(FONT_REG, 14))
        cx0 += 385

    # Bottom Banner: How mouse horizontal release works
    bx0, by0, bw0, bh0 = 80, 460, 1120, 280
    draw_rounded_rect(draw, (bx0, by0, bx0 + bw0, by0 + bh0), 16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

    draw.text((bx0 + 40, by0 + 35), "Intuitive Interaction Philosophy", fill=(17, 24, 39), font=get_font(FONT_BOLD, 26))
    draw.text((bx0 + 40, by0 + 75), "Designed specifically to never get in your way.", fill=(107, 114, 128), font=get_font(FONT_REG, 16))

    steps = [
        ("1. Hover or Click", "Simply place your mouse over the top or bottom arrow to glide in that direction."),
        ("2. Read Seamlessly", "Vertical mouse movements will not interrupt your reading flow."),
        ("3. Move Horizontally to Stop", "Gently move your mouse left or right to immediately release the scroll."),
    ]
    sx0 = bx0 + 40
    for stitle, sdesc in steps:
        draw_rounded_rect(draw, (sx0, by0 + 120, sx0 + 325, by0 + 240), 12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((sx0 + 16, by0 + 138), stitle, fill=(255, 107, 53), font=get_font(FONT_BOLD, 16))
        # Wrap sdesc
        words = sdesc.split()
        l1 = " ".join(words[:5])
        l2 = " ".join(words[5:10])
        l3 = " ".join(words[10:])
        draw.text((sx0 + 16, by0 + 168), l1, fill=(71, 85, 105), font=get_font(FONT_REG, 13))
        draw.text((sx0 + 16, by0 + 190), l2, fill=(71, 85, 105), font=get_font(FONT_REG, 13))
        if l3:
            draw.text((sx0 + 16, by0 + 212), l3, fill=(71, 85, 105), font=get_font(FONT_REG, 13))
        sx0 += 355

    path = os.path.join(assets_dir, "screenshot2_1280x800.png")
    img.save(path, "PNG")
    print(f"✓ Created {path}")

make_store_icon()
make_screenshot_1()
make_screenshot_2()
print("\n🎉 All store assets created successfully!")
