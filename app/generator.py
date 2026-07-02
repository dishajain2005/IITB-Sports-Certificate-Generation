from PIL import Image, ImageDraw, ImageFont
import os
import shutil

# ─── PATHS ─────────────────────────────────────────────────────────────
TEMPLATE_PATH = "templates/certificate_base.png"
OUTPUT_DIR    = "output"

# ─── FONT ──────────────────────────────────────────────────────────────
FONT_PATH1 = "templates/GreatVibes-Regular.ttf"
#FONT_PATH1 = "templates/GreatVibes-Regular.ttf"  # ← change this
FONT_PATH2 = "templates/GreatVibes-Regular.ttf"  # ← change this
# ─── ZONES (Figma → Pixel converted, scaled ×1.5) ──────────────────────
ZONES = {
    "name":        (144, 741, 305, 44, 18),
    "position":    (255, 309, 342, 24, 10),
    "event":       (421, 740, 342, 26, 10),
    "start_date":  (314, 516, 369, 22, 10),
    "end_date":    (538, 740, 369, 22, 10),
}

INK = (25, 15, 5)


# ─── HELPERS ───────────────────────────────────────────────────────────

def clear_output_directory():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    return {"status": "success", "message": "Output directory cleared"}


def _fit_font(draw, text, font_path, max_width, size_max, size_min):
    for size in range(size_max, size_min - 1, -1):
        font = ImageFont.truetype(font_path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
    return ImageFont.truetype(font_path, size_min)


def _draw_field(draw, text, zone_key):
    x1, x2, y_baseline, size_max, size_min = ZONES[zone_key]

    # 👇 choose font based on field
    if zone_key == "name":
        font_path = FONT_PATH1
    else:
        font_path = FONT_PATH2

    font = _fit_font(draw, text, font_path, x2 - x1, size_max, size_min)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]

    # Horizontal centering
    x = x1 + (x2 - x1 - text_w) // 2

    # Baseline alignment + tweak
    ascent, descent = font.getmetrics()
    y = y_baseline - ascent - 10

    draw.text((x, y), text, fill=INK, font=font)


# ─── MAIN ──────────────────────────────────────────────────────────────

def generate_certificate(data):
    img = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(img)

    _draw_field(draw, data["name"], "name")
    _draw_field(draw, data["position"], "position")
    _draw_field(draw, data["event"], "event")
    _draw_field(draw, data["start_date"], "start_date")
    _draw_field(draw, data["end_date"], "end_date")

    safe = lambda s: s.replace(" ", "_")

    sport_dir = os.path.join(OUTPUT_DIR, safe(data["event"]))
    os.makedirs(sport_dir, exist_ok=True)

    filename = f"{safe(data['name'])}_{safe(data['event'])}_{safe(data['position'])}.pdf"
    output_path = os.path.join(sport_dir, filename)

    img.save(output_path, "PDF")
    return output_path