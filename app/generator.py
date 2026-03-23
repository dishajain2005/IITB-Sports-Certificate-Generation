from PIL import Image, ImageDraw, ImageFont
import os

TEMPLATE_PATH = "templates/certificate_base.png"
OUTPUT_DIR = "output"


# 🔹 Helper function for name formatting
def format_name(name, max_length=20):
    name = name.strip()

    if len(name) <= max_length:
        return name

    # take only first name if too long
    parts = name.split()
    return parts[0] if parts else name


def generate_certificate(data):
    img = Image.open(TEMPLATE_PATH)
    draw = ImageDraw.Draw(img)

    # Load font
    font_path = "templates/GreatVibes-Regular.ttf"
    font_large = ImageFont.truetype(font_path, 50)
    font_medium = ImageFont.truetype(font_path, 35)
    font_small = ImageFont.truetype(font_path, 25)

    # 🔹 APPLY NAME TRUNCATION LOGIC
    display_name = format_name(data["name"], max_length=20)

    # Draw text (your original positions preserved)
    draw.text((355, 260), display_name, fill="black", font=font_medium)
    draw.text((80, 290), data["position"], fill="black", font=font_medium)
    draw.text((420, 290), data["sport"], fill="black", font=font_medium)
    draw.text((240, 320), data["date"], fill="black", font=font_medium)

    # 🔹 Keep original full name for filename (important)
    filename = data["name"].replace(" ", "_")
    output_path = f"{OUTPUT_DIR}/{filename}.pdf"

    img.save(output_path, "PDF")

    return output_path