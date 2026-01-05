from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def add_overlay(base_url: str, hook: str, subtitle: str = "") -> str:
    response = requests.get(base_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    
    draw = ImageDraw.Draw(img)
    try:
        font_large = ImageFont.truetype("fonts/impact.ttf", 80)  # Add fonts later
        font_small = ImageFont.truetype("fonts/arial.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Dark overlay
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 180))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Text
    w = img.width // 2
    draw.text((w, img.height//3), hook.upper(), font=font_large, fill="white", anchor="mm", stroke_width=4, stroke_fill="black")
    if subtitle:
        draw.text((w, img.height//2), subtitle, font=font_small, fill="white", anchor="mm")
    
    # Save to bytes (for Streamlit display)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
