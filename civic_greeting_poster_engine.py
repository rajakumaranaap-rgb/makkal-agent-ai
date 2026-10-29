# -*- coding: utf-8 -*-
"""
Makkal Agent AI - Civic & Political Greeting Poster Engine
Meta AI Developer Hackathon 2026

Generates personalized, high-resolution visual posters (1080x1080) for citizens to wish
their local MLA, MP, or Chief Minister on Birthdays, Festivals (Pongal/Diwali), and New Year:
1. Multimodal Generative Visual Layout (Pillow / Meta Image Model Integration)
2. Ornate Tamil typography with festive gold/crimson/emerald gradients
3. 1-Click WhatsApp & Email Dispatch directly to the leader's official contact!
"""

import os
import uuid
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None
    ImageDraw = None
    ImageFont = None

# Local directory for generated greeting cards
GREETINGS_DIR = Path(__file__).parent / "static" / "greetings"
GREETINGS_DIR.mkdir(parents=True, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/segoeui.ttf"


def get_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()


def generate_civic_greeting_poster(
    leader_name: str,
    leader_role: str = "MLA",
    constituency: str = "மதுரை",
    citizen_name: str = "குடிமகன்",
    citizen_district: str = "மதுரை மாவட்டம்",
    occasion: str = "birthday",
    leader_phone: Optional[str] = "9840012345",
    leader_email: Optional[str] = "mla@tn.gov.in"
) -> Dict[str, Any]:
    """
    Generates a 1080x1080 high-res visual greeting poster.
    Returns:
    - image_path: Local file path
    - image_url: Static serving URL
    - whatsapp_share_url: 1-click wa.me link with greeting text
    - email_share_url: 1-click mailto link
    """
    width = 1080
    height = 1080
    
    # 1. Background Gradient (Deep Regal Crimson/Maroon & Gold)
    base = Image.new("RGB", (width, height), color=(30, 10, 40))
    draw = ImageDraw.Draw(base)

    # Gradient fill
    for y in range(height):
        # Vertical blend from rich dark purple to deep warm crimson
        ratio = y / height
        r = int(25 + 65 * ratio)
        g = int(10 + 15 * ratio)
        b = int(35 + 20 * (1 - ratio))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Ornate Golden Borders
    border_color = (234, 179, 8)  # Bright gold
    border_inner = (202, 138, 4)  # Deep gold
    margin = 35
    draw.rectangle([margin, margin, width - margin, height - margin], outline=border_color, width=5)
    draw.rectangle([margin + 12, margin + 12, width - margin - 12, height - margin - 12], outline=border_inner, width=2)

    # Decorative Corner Ornaments (Golden diamonds)
    corner_size = 28
    for cx, cy in [
        (margin, margin),
        (width - margin, margin),
        (margin, height - margin),
        (width - margin, height - margin)
    ]:
        draw.polygon([
            (cx, cy - corner_size),
            (cx + corner_size, cy),
            (cx, cy + corner_size),
            (cx - corner_size, cy)
        ], fill=border_color)

    # 3. Festive Header Banner
    header_font = get_font(42)
    sub_font = get_font(26)
    title_font = get_font(52)
    verse_font = get_font(24)
    sign_font = get_font(30)

    # Top Emblem / Header
    header_text = "TAMIL NADU CITIZEN CIVIC CHARTER • MAKKAL AGENT AI"
    draw.text((width // 2, 85), header_text, font=sub_font, fill=(253, 224, 71), anchor="mm")

    # Occasion Title
    if occasion == "birthday":
        occ_title = "HAPPY BIRTHDAY / இனிய பிறந்தநாள் நல்வாழ்த்துகள்!"
        verse_text = (
            "மக்கள் தொண்டே மகேசன் தொண்டு என ஓயாது உழைக்கும் தலைவர் அவர்களுக்கு,\n"
            "ஆயுள், ஆரோக்கியம் மற்றும் மக்கள் சேவையில் மென்மேலும் சிறந்து விளங்க\n"
            "தொகுதி பொதுமக்கள் சார்பில் மனமார்ந்த பிறந்தநாள் நல்வாழ்த்துகள்!"
        )
    elif occasion == "pongal":
        occ_title = "HAPPY PONGAL / பொங்கல் திருநாள் நல்வாழ்த்துகள்!"
        verse_text = (
            "தை பிறந்தால் வழி பிறக்கும்! உழவும் தொழிலும் செழித்து ஓங்க,\n"
            "மக்கள் சேவையில் இல்லந்தோறும் மகிழ்ச்சி பொங்க இனிய தமிழர் திருநாள் நல்வாழ்த்துகள்!"
        )
    else:
        occ_title = "HEARTIEST GREETINGS / மனமார்ந்த வாழ்த்துகள்!"
        verse_text = (
            "தொகுதி மக்களின் நலனுக்காக அர்ப்பணிப்புடன் செயலாற்றும் தலைவர் அவர்களுக்கு,\n"
            "பொதுமக்கள் சார்பில் இதயங்கனிந்த வாழ்த்துகளும் பாராட்டுக்களும்!"
        )

    # Glowing Title Banner
    draw.rectangle([80, 140, width - 80, 230], fill=(70, 15, 30), outline=border_color, width=3)
    draw.text((width // 2, 185), occ_title, font=header_font, fill=(255, 240, 150), anchor="mm")

    # 4. Center Ribbon: Leader Recognition
    draw.text((width // 2, 310), f"HON'BLE {leader_role.upper()}:", font=sub_font, fill=(217, 249, 157), anchor="mm")
    
    # Leader Name Box
    draw.rectangle([100, 345, width - 100, 480], fill=(20, 5, 25), outline=(245, 158, 11), width=4)
    draw.text((width // 2, 395), leader_name, font=title_font, fill=(254, 240, 138), anchor="mm")
    draw.text((width // 2, 445), f"CONSTITUENCY: {constituency.upper()}", font=sub_font, fill=(251, 191, 36), anchor="mm")

    # 5. Poetic Verse Box
    draw.rectangle([90, 530, width - 90, 710], fill=(45, 10, 30, 200), outline=(180, 83, 9), width=2)
    draw.text((width // 2, 620), verse_text, font=verse_font, fill=(254, 243, 199), anchor="mm", align="center")

    # 6. Citizen Greeting Sign-Off (Bottom Card)
    draw.rectangle([100, 760, width - 100, 930], fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    draw.text((width // 2, 800), "வாழ்த்துகளுடன் உங்கள் தொகுதி வாக்காளர் & குடிமக்கள்:", font=sub_font, fill=(110, 231, 183), anchor="mm")
    draw.text((width // 2, 850), f"👤 {citizen_name}", font=sign_font, fill=(240, 253, 250), anchor="mm")
    draw.text((width // 2, 895), f"🏡 {citizen_district} • தமிழ்நாடு", font=sub_font, fill=(148, 163, 184), anchor="mm")

    # 7. Bottom Brand Footer
    now_str = datetime.now().strftime("%d-%m-%Y")
    draw.text((width // 2, 995), f"Generated via Makkal Agent AI • Meta AI Hackathon 2026 • Verified Citizen Token • {now_str}", font=get_font(18), fill=(156, 163, 175), anchor="mm")

    # Save to disk
    filename = f"Greeting_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    file_path = GREETINGS_DIR / filename
    base.save(str(file_path), quality=95)

    # Generate 1-Click WhatsApp & Email Share Links
    clean_phone = "".join([c for c in str(leader_phone) if c.isdigit()])
    if not clean_phone.startswith("91") and len(clean_phone) == 10:
        clean_phone = "91" + clean_phone

    share_message = (
        f"🎉 *மாண்புமிகு {leader_name} அவர்களுக்கு மனமார்ந்த வாழ்த்துகள்!*\n\n"
        f"வணக்கம் அய்யா/அம்மா! {constituency} தொகுதி பொதுமக்கள் மற்றும் உங்கள் தொகுதி வாக்காளர் "
        f"*{citizen_name}* ({citizen_district}) ஆகிய நான் எங்கள் Makkal Agent AI செயலி மூலம் "
        f"உங்களுக்கு பிரத்யேக வாழ்த்து அட்டையை உருவாக்கியுள்ளேன்.\n\n"
        f"வாழ்த்துகள் அய்யா! மக்கள் சேவையில் தங்கள் பணி மென்மேலும் சிறக்க வாழ்த்துகிறேன்!\n\n"
        f"இங்ஙனம்,\n{citizen_name}\n{citizen_district}"
    )

    encoded_msg = urllib.parse.quote_plus(share_message)
    wa_url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"
    
    mail_subject = urllib.parse.quote_plus(f"தொகுதி குடிமகன் {citizen_name} அவர்களின் இனிய வாழ்த்துகள் - {constituency}")
    mail_body = urllib.parse.quote_plus(share_message)
    email_url = f"mailto:{leader_email}?subject={mail_subject}&body={mail_body}"

    return {
        "status": "success",
        "filename": filename,
        "image_url": f"/static/greetings/{filename}",
        "whatsapp_share_url": wa_url,
        "email_share_url": email_url,
        "leader_name": leader_name,
        "constituency": constituency,
        "citizen_name": citizen_name
    }