#!/usr/bin/env python3
"""
Generate compliant PNG icons for AutoScroll Pro using Pillow (PIL).
Complies 100% with Chrome Web Store libpng and RGBA specifications.
"""
import os
from PIL import Image, ImageDraw

base_dir = os.path.dirname(os.path.abspath(__file__))
icons_dir = os.path.join(base_dir, "icons")
os.makedirs(icons_dir, exist_ok=True)

SIZES = [16, 32, 48, 128]

def create_icon(size):
    # Render at 4x resolution for smooth anti-aliased downsampling
    scale = 4
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pad = canvas_size * 0.05
    box = [pad, pad, canvas_size - pad, canvas_size - pad]

    # White circular background with crisp orange border (#FF6B35)
    border_width = max(2, int(canvas_size * 0.075))
    draw.ellipse(box, fill=(255, 255, 255, 255), outline=(255, 107, 53, 255), width=border_width)

    # Center horizontal divider line
    mid_y = canvas_size / 2
    divider_half_w = canvas_size * 0.28
    draw.line(
        [(canvas_size/2 - divider_half_w, mid_y), (canvas_size/2 + divider_half_w, mid_y)],
        fill=(255, 107, 53, 90),
        width=max(1, int(canvas_size * 0.025))
    )

    # Orange color for arrows (#FF6B35)
    orange = (255, 107, 53, 255)

    # Top Arrow (Up)
    # Point at top, stem at bottom
    top_tip_y = canvas_size * 0.18
    top_base_y = canvas_size * 0.36
    top_stem_bottom_y = canvas_size * 0.44
    arrow_half_w = canvas_size * 0.15
    stem_half_w = canvas_size * 0.065
    cx = canvas_size / 2

    # Up polygon: 7 vertices
    up_points = [
        (cx, top_tip_y),                              # tip
        (cx - arrow_half_w, top_base_y),             # left wing
        (cx - stem_half_w, top_base_y),              # inner left
        (cx - stem_half_w, top_stem_bottom_y),       # bottom left stem
        (cx + stem_half_w, top_stem_bottom_y),       # bottom right stem
        (cx + stem_half_w, top_base_y),              # inner right
        (cx + arrow_half_w, top_base_y),             # right wing
    ]
    draw.polygon(up_points, fill=orange)

    # Bottom Arrow (Down)
    bot_tip_y = canvas_size * 0.82
    bot_base_y = canvas_size * 0.64
    bot_stem_top_y = canvas_size * 0.56

    down_points = [
        (cx, bot_tip_y),                              # tip
        (cx - arrow_half_w, bot_base_y),             # left wing
        (cx - stem_half_w, bot_base_y),              # inner left
        (cx - stem_half_w, bot_stem_top_y),          # top left stem
        (cx + stem_half_w, bot_stem_top_y),          # top right stem
        (cx + stem_half_w, bot_base_y),              # inner right
        (cx + arrow_half_w, bot_base_y),             # right wing
    ]
    draw.polygon(down_points, fill=orange)

    # High-quality Lanczos downsampling to target size
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

for s in SIZES:
    icon = create_icon(s)
    path = os.path.join(icons_dir, f"icon{s}.png")
    # Save standard PNG with standard headers
    icon.save(path, format="PNG", optimize=True)
    print(f"Generated {path}: {icon.size}, mode={icon.mode}")

print("All icons successfully generated!")
