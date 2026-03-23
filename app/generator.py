from PIL import Image, ImageDraw, ImageFont
import os

TEMPLATE_PATH = "templates/certificate_base.png"
OUTPUT_DIR = "output"


# 🔹 Helper function for name formatting
def format_name(name, max_length=13):
    name = name.strip()
    parts = name.split()

    # If already short, keep as is
    if len(name) <= max_length:
        return name

    # Always keep first name
    first_name = parts[0]

    # If only one word
    if len(parts) == 1:
        return first_name

    # Build initials (S. K. ...)
    initials = ""
    for part in parts[1:]:
        initials += f" {part[0]}."

    short_name = first_name + initials

    # If still too long, reduce to just first + first initial
    if len(short_name) > max_length:
        short_name = f"{first_name} {parts[1][0]}."

    return short_name


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