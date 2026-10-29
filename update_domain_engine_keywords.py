"""
Update domain_keywords in domain_training_engine.py
"""

import sys

FILE_PATH = r"D:\api\makkal-agent-ai\domain_training_engine.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

target = """            "redtaxi_travel": ["redtaxi", "uber", "டாக்ஸி", "வாடகைக்கார்", "ஆட்டோ", "முன்பதிவு", "நம்மா ஆட்டோ", "இன்னோவா", "செடான்", "டெம்போ", "கட்டணம்", "otp", "surge", "சர்ஜ்"],
            "education": ["நியூட்டன்", "ஒளியியல்", "physics", "maths", "science", "tnpsc", "சமச்சீர்", "தேர்வு", "quiz", "course"]
        }"""

replacement = """            "redtaxi_travel": ["redtaxi", "uber", "டாக்ஸி", "வாடகைக்கார்", "ஆட்டோ", "முன்பதிவு", "நம்மா ஆட்டோ", "இன்னோவா", "செடான்", "டெம்போ", "கட்டணம்", "otp", "surge", "சர்ஜ்"],
            "spoken_english": ["english", "spoken english", "self-introduction", "tanglish", "grammar", "interview", "ptm", "ஹலோ", "உச்சரிப்பு", "fluency", "பேச்சு ஆங்கிலம்"],
            "mental_health": ["stress", "anxiety", "mental health", "மன நலம்", "மன அழுத்தம்", "பயம்", "தேர்வு பயம்", "14416", "counseling", "helpline", "burnout", "சுவாசப் பயிற்சி", "pomodoro"],
            "tuition_curriculum": ["cbse", "ncert", "tuition", "டியூஷன்", "வகுப்பு 10", "வகுப்பு 12", "இரட்டை இரத்த ஓட்டம்", "ஓம் விதி", "sn1", "sn2", "பின்னங்கள்", "multiplication", "science", "maths"],
            "education": ["நியூட்டன்", "ஒளியியல்", "physics", "maths", "science", "tnpsc", "சமச்சீர்", "தேர்வு", "quiz", "course"]
        }"""

if target in content and "spoken_english" not in content:
    content = content.replace(target, replacement, 1)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Updated domain_training_engine.py keywords successfully!")
else:
    print("Keywords already present or target not found.")
