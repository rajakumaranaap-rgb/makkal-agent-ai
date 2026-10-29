"""
==============================================================================
Makkal Agent AI - Student Mental Health & Emotional Wellbeing Coach (மன நலம்)
==============================================================================
Target: Meta AI Developer Hackathon 2026 ($150,000 Track)
Role:
1. Provides empathetic, confidential emotional support and stress counseling:
   - Board Exam (10th/12th), NEET & Competitive Exam Fear
   - Peer Pressure & Parental Expectations
   - Study Burnout, Sleeplessness & Concentration Issues
   - Emotional Resilience via Thirukkural & Positive Psychology
2. WhatsApp Interactive 1-Click Buttons & Quick Relief Toolkits.
3. Official Emergency Helplines (Tamil Nadu Student Helpline 14416, Tele-MANAS).
4. Real-time dual sync between WhatsApp chat and Web App Student Hub.
==============================================================================
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("makkal.mental_health")

# Official Government & NGO Crisis Helplines (Mandatory 24x7 Free)
STATUTORY_HELPLINES = [
    {
        "name_ta": "தமிழ்நாடு பள்ளிக் கல்வித்துறை மாணவர் மனநல உதவி எண்",
        "name_en": "Tamil Nadu Student Counseling Helpline",
        "number": "14416",
        "toll_free": True,
        "hours": "24 மணி நேரமும் இலவச சேவை (24x7 Toll-Free)",
        "scope": "பள்ளி மாணவர்கள் தேர்வு பயம், மன அழுத்தம், பெற்றோர் ஆலோசனை"
    },
    {
        "name_ta": "மத்திய அரசு டெலி-மானாஸ் (Tele-MANAS)",
        "name_en": "National Tele-Mental Health Assistance and Networking Across States",
        "number": "14416 / 1800-891-4416",
        "toll_free": True,
        "hours": "24x7 தமிழ் மற்றும் அனைத்து மொழிகளிலும்",
        "scope": "அனைத்து வயதினருக்குமான மனநல ஆலோசனை & மன அழுத்தம் தீர்வு"
    },
    {
        "name_ta": "சினேகா தற்கொலை தடுப்பு உதவி மையம் (Sneha Foundation)",
        "name_en": "Sneha Suicide Prevention Helpline",
        "number": "044-24640050",
        "toll_free": False,
        "hours": "24x7 Chennai Helpline",
        "scope": "தீவிர மன உளைச்சல், தனிமை, மற்றும் தற்கொலை எண்ணங்களை மாற்றும் ரகசிய ஆலோசனை"
    },
    {
        "name_ta": "சைல்டுலைன் குழந்தைகள் உதவி எண்",
        "name_en": "Childline India",
        "number": "1098",
        "toll_free": True,
        "hours": "24x7 Toll-Free",
        "scope": "18 வயதுக்குட்பட்ட குழந்தைகளின் பாதுகாப்பு மற்றும் உதவி"
    }
]

# Mental Health Topic Toolkits
WELLBEING_MODULES = [
    {
        "id": "exam_anxiety",
        "title_ta": "🎯 தேர்வு பயம் & பதட்டம் தணிக்கும் பயிற்சி (Exam Anxiety Relief)",
        "title_en": "Overcoming Board Exam & Competitive Pressure",
        "icon": "🎯",
        "description_ta": "10-ம் வகுப்பு, 12-ம் வகுப்பு மற்றும் நீட் தேர்வில் பதட்டத்தை குறைத்து நம்பிக்கையை வளர்த்தல்.",
        "calm_technique": {
            "name_ta": "4-7-8 சுவாசப் பயிற்சி (Box Breathing)",
            "steps_ta": [
                "1. மூச்சை 4 வினாடிகள் மூக்கு வழியே மெதுவாக உள்ளிழுங்கள்.",
                "2. மூச்சை 7 வினாடிகள் அமைதியாக உள்ளே அடக்கி வையுங்கள்.",
                "3. மூச்சை 8 வினாடிகள் வாய் வழியே 'ஹூஷ்' என்ற ஒலியுடன் மெதுவாக வெளியேற்றுங்கள்.",
                "4. இதை 4 முறை தொடர்ந்து செய்யுங்கள் - உங்கள் இதயத் துடிப்பு இயல்பு நிலைக்கு வரும்."
            ]
        },
        "affirmation_ta": "மதிப்பெண்கள் என் எதிர்காலத்தை மட்டுமே தீர்மானிப்பதில்லை; என் கடின உழைப்பும் விடாமுயற்சியுமே என்னை உயர்த்தும். என்னால் முடியும்!",
        "thirukkural": {
            "kural": "இடுக்கண் வருங்கால் நகுக அதனை\nஅடுத்தூர்வது அஃதொப்பது இல்.",
            "meaning_ta": "துன்பம் வரும்போது கலங்காமல் சிரித்து எதிர்கொள்ளுங்கள். துன்பத்தை வெல்லும் ஆற்றல் அதைவிட வேறு எதுவுமில்லை."
        }
    },
    {
        "id": "study_burnout",
        "title_ta": "🔋 படிப்பு சோர்வு & கவனச் சிதறல் (Beating Burnout & Regaining Focus)",
        "title_en": "Study Fatigue & Focus Restoration",
        "icon": "🔋",
        "description_ta": "நீண்ட நேரம் படிப்பதால் ஏற்படும் தலைவலி, சோர்வு, மற்றும் நினைவாற்றல் குறைபாட்டைப் போக்குதல்.",
        "calm_technique": {
            "name_ta": "பொமோடோரோ 25/5 உத்தி (Pomodoro Technique)",
            "steps_ta": [
                "1. மொபைல் நோட்டிபிகேஷன்களை அணைத்துவிட்டு 25 நிமிடங்கள் மட்டுமே ஒரே ஒரு பாடத்தை ஆழ்ந்து படியுங்கள்.",
                "2. 25 நிமிடம் முடிந்ததும் 5 நிமிடங்கள் எழுந்து நடந்து தண்ணீர் குடியுங்கள் அல்லது கண்களை மூடி ஓய்வெடுங்கள்.",
                "3. 4 சுற்றுகள் முடிந்ததும் 20 நிமிடங்கள் நீண்ட இடைவேளை எடுங்கள்.",
                "4. மூளை புத்துணர்ச்சியுடன் பாடங்களை அதிக நாட்கள் நினைவில் வைத்திருக்கும்."
            ]
        },
        "affirmation_ta": "ஒவ்வொரு சிறிய முன்னேற்றமும் என்னை என் லட்சியத்தை நோக்கி நகர்த்துகிறது. சோர்வு தற்காலிகமானது, என் வெற்றி நிரந்தரமானது!",
        "thirukkural": {
            "kural": "முயற்சி திருவினை ஆக்கும் முயற்றின்மை\nஇன்மை புகுத்தி விடும்.",
            "meaning_ta": "விடாமுயற்சி செல்வத்தையும் வெற்றிகளையும் உண்டாக்கும்; முயற்சியில்லாமை வறுமையையும் தோல்வியையும் தந்துவிடும்."
        }
    },
    {
        "id": "parent_peer_pressure",
        "title_ta": "🤝 பெற்றோர் எதிர்பார்ப்பு & நண்பர்களுடன் ஒப்பீடு (Peer & Parent Expectations)",
        "title_en": "Handling Comparison & Family Pressure",
        "icon": "🤝",
        "description_ta": "மற்ற மாணவர்களுடன் ஒப்பிடுவதால் ஏற்படும் தாழ்வு மனப்பான்மை மற்றும் குடும்ப அழுத்தத்தை சமாளித்தல்.",
        "calm_technique": {
            "name_ta": "5-4-3-2-1 உணர்வு அமைதிப் பயிற்சி (Sensory Grounding)",
            "steps_ta": [
                "1. கண்களால் 5 பொருட்களைப் பாருங்கள் (புத்தகம், சுவர், பேனா...).",
                "2. விரல்களால் தொடக்கூடிய 4 பொருட்களைத் தொடுங்கள் (மேஜை, ஆடை...).",
                "3. காதுகளால் கேட்கும் 3 ஒலிகளைக் கவனியுங்கள் (காற்று, பறவை...).",
                "4. 2 வாசனைகளை நுகருங்கள்.",
                "5. 1 நல்ல சுவையை உணருங்கள்.",
                "இது உங்கள் மனதை தேவையற்ற கவலைகளில் இருந்து நிகழ்காலத்திற்கு கொண்டு வரும்."
            ]
        },
        "affirmation_ta": "நான் தனித்துவமானவன். என் பாதை மற்றவர்களுடையது போன்றதல்ல. எனக்கென்று ஒரு தனி பலமும் தனித்துவமான திறமையும் உண்டு!",
        "thirukkural": {
            "kural": "வெள்ளத் தனைய மலர்நீட்டம் மாந்தர்தம்\nஉள்ளத் தனையது உயர்வு.",
            "meaning_ta": "தண்ணீரின் உயரத்திற்கு ஏற்ப அல்லி மலர் உயரும்; அதுபோல மனிதனின் ஊக்கத்தின் அளவுக்கு ஏற்ப அவனது வாழ்வு உயரும்."
        }
    },
    {
        "id": "emotional_listening",
        "title_ta": "👂 பாதுகாப்பான ரகசிய கேட்பு மையம் (Anonymous Safe Listening Space)",
        "title_en": "Confidential Empathetic Listening",
        "icon": "👂",
        "description_ta": "யாரிடமும் சொல்ல முடியாத மனக் கஷ்டங்கள், தனிமை, அழுகை அல்லது கவலைகளை எந்த தீர்ப்பும் இன்றி பகிரலாம்.",
        "calm_technique": {
            "name_ta": "மன அழுத்தம் விடுவிக்கும் சுய வழிகாட்டல்",
            "steps_ta": [
                "1. உங்கள் மனதில் உள்ள பாரத்தை வார்த்தைகளாக இந்த வாட்ஸ்அப் அரட்டையில் எழுதுங்கள் அல்லது ஆடியோவாகப் பேசுங்கள்.",
                "2. உங்கள் பெயர், ரகசியங்கள் 100% பாதுகாப்பாக இருக்கும்; எங்கும் பகிரப்படாது.",
                "3. உங்களை புரிந்துகொள்ளும் நண்பனாக SIA உங்களுக்கு துணை நிற்கும்."
            ]
        },
        "affirmation_ta": "இன்று கடினமான நாளாக இருக்கலாம், ஆனால் இது என் வாழ்வின் முடிவு அல்ல. என் வாழ்க்கை இனிமேல் தான் அழகாகத் தொடங்குகிறது!",
        "thirukkural": {
            "kural": "உள்ளுவ தெல்லாம் உயர்வுள்ளல் மற்றது\nதள்ளினும் தள்ளாமை நீர்த்து.",
            "meaning_ta": "எண்ணுவதெல்லாம் உயர்வானதாகவே இருக்க வேண்டும்; ஒருவேளை அது கைகூடாவிட்டாலும் அந்த எண்ணமே பெருமை தரும்."
        }
    }
]


def get_all_wellbeing_modules() -> List[Dict[str, Any]]:
    """Returns all mental health support modules."""
    return WELLBEING_MODULES


def get_statutory_helplines() -> List[Dict[str, Any]]:
    """Returns official crisis helplines."""
    return STATUTORY_HELPLINES


def format_whatsapp_mental_health_menu() -> Dict[str, Any]:
    """Generates interactive WhatsApp button menu for student mental health."""
    body_text = (
        "🧠 *SIA மாணவர் மன நலம் & ஊக்க அரங்கம் (Student Wellbeing Coach)* 🌸\n\n"
        "தேர்வு பயமா? அதிக மன அழுத்தமா? குடும்ப எதிர்பார்ப்புகளால் கவலையா?\n\n"
        "கவலைப்படாதீர்கள்! உங்களுடன் பேசவும், மனதை அமைதிப்படுத்தவும் SIA எப்போதும் துணை நிற்கிறது:\n\n"
        "🎯 *தேர்வு பயம் & பதட்டம் தணிக்க*\n"
        "🔋 *படிப்பு சோர்வு போக்க (Pomodoro 25/5)*\n"
        "🤝 *ஒப்பீடு & பெற்றோர் எதிர்பார்ப்பை வெல்ல*\n"
        "📞 *அரசு உதவி எண்: 14416 (24x7 இலவசம்)*\n\n"
        "கீழே உள்ள பொத்தானை அழுத்தி உடனடி மன அமைதிப் பயிற்சியைத் தொடங்குங்கள் 👇"
    )
    buttons = [
        {"id": "mh_exam", "title": "🎯 தேர்வு பயம்"},
        {"id": "mh_burnout", "title": "🔋 படிப்பு சோர்வு"},
        {"id": "mh_helpline", "title": "📞 உதவி எண் 14416"}
    ]
    return {
        "body_text": body_text,
        "buttons": buttons,
        "header_text": "🧠 SIA மன நலம் & ஆறுதல்",
        "footer_text": "Confidential & Empathetic Student Care"
    }


def format_wellbeing_module_message(module_id: str) -> str:
    """Formats full advice, breathing exercise, affirmation and Thirukkural."""
    mod = next((m for m in WELLBEING_MODULES if m["id"] == module_id), WELLBEING_MODULES[0])

    lines = [
        f"{mod['icon']} *{mod['title_ta']}*",
        "-----------------------------------------",
        f"📝 *விளக்கம்:* {mod['description_ta']}\n",
        f"🧘 *உடனடி மன அமைதிப் பயிற்சி: {mod['calm_technique']['name_ta']}*"
    ]
    for s in mod["calm_technique"]["steps_ta"]:
        lines.append(f"  {s}")

    lines.append("\n✨ *உங்களுக்கான ஊக்க வாக்குறுதி (Affirmation):*")
    lines.append(f"\"{mod['affirmation_ta']}\"\n")

    lines.append("📜 *திருக்குறள் மன வலிமை:*")
    lines.append(f"_{mod['thirukkural']['kural']}_")
    lines.append(f"📌 *பொருள்:* {mod['thirukkural']['meaning_ta']}\n")

    lines.append("-----------------------------------------")
    lines.append("📞 *அவசர உதவி தேவைப்பட்டால்:* தமிழ்நாடு அரசு மாணவர் மனநல உதவி எண் *14416* (24 மணி நேரமும் இலவசம்).")
    lines.append("💬 உங்கள் கவலையை இந்த அரட்டையிலேயே தட்டச்சு செய்யலாம்; SIA உங்களுக்கு தோழனாக வழிகாட்டும்.")

    return "\n".join(lines)


def format_emergency_helpline_message() -> str:
    """Formats official crisis counseling helplines message."""
    lines = [
        "🆘 *அவசர மாணவர் & இளைஞர் மனநல உதவி எண்கள் (Emergency Helplines)* 📞",
        "-----------------------------------------",
        "மன உளைச்சல், தீவிர பயம், அல்லது தனிமை ஏற்படும் போது தயங்காமல் உடனடியாக அழையுங்கள்:\n"
    ]
    for h in STATUTORY_HELPLINES:
        lines.append(f"🏛️ *{h['name_ta']}*")
        lines.append(f"   📞 *தொலைபேசி எண்:* *{h['number']}*")
        lines.append(f"   ⏱️ *இயங்கும் நேரம்:* {h['hours']}")
        lines.append(f"   🎯 *பயன்:* {h['scope']}\n")

    lines.append("-----------------------------------------")
    lines.append("🛡️ *நினைவில் கொள்ளுங்கள்:* நீங்கள் தனியாக இல்லை. உங்களை நேசிக்கவும், உதவவும் ஒரு உலகம் காத்திருக்கிறது. உதவி கோருவது உங்கள் பலவீனம் அல்ல; உங்கள் தைரியம்!")
    return "\n".join(lines)


def handle_empathetic_counseling_query(user_query: str) -> Dict[str, Any]:
    """
    Generates compassionate, supportive counseling guidance using Meta Wonder 1.0 logic.
    Identifies if crisis helpline needs to be highlighted immediately.
    """
    q_lower = user_query.lower()

    # Crisis trigger words
    is_crisis = any(w in q_lower for w in [
        "சாக", "தற்கொலை", "உயிரை", "வாழப் பிடிக்கவில்லை", "suicide", "end my life", "kill myself", "depressed", "depression"
    ])

    if is_crisis:
        reply_ta = (
            "🚨 *நாங்கள் உங்களுடன் இருக்கிறோம். தயவுசெய்து அவசர முடிவெடுக்காதீர்கள்!*\n\n"
            "உங்கள் வாழ்க்கை மிக மிக விலைமதிப்பற்றது. இப்போது உங்களுக்கு இருக்கும் இந்தத் துன்பம் ஒரு தற்காலிகமான மேகம் மட்டுமே, கடந்து போய்விடும்.\n\n"
            "தயவுசெய்து உடனடியாக இந்த இலவச உதவி எண்ணை அழையுங்கள்:\n"
            "📞 **14416** (தமிழ்நாடு மாணவர் & மனநல உதவி எண் - 24 மணி நேரமும் இலவசம்)\n"
            "📞 **044-24640050** (சினேகா உதவி மையம்)\n\n"
            "அவர்கள் உங்கள் ரகசியங்களை பாதுகாத்து அன்புடன் வழிகாட்டுவார்கள். நீங்கள் தனியாக இல்லை தோழா!"
        )
        return {
            "is_crisis": True,
            "status": "crisis_intercepted",
            "reply_ta": reply_ta,
            "helplines": STATUTORY_HELPLINES
        }

    # Standard counseling flow
    matched_module = WELLBEING_MODULES[0]
    if any(w in q_lower for w in ["சோர்வு", "தூக்கம்", "கவனம்", "tire", "burnout", "sleep"]):
        matched_module = WELLBEING_MODULES[1]
    elif any(w in q_lower for w in ["பெற்றோர்", "நண்பர்", "ஒப்பீடு", "அழுத்தம்", "parent", "peer", "compare"]):
        matched_module = WELLBEING_MODULES[2]

    return {
        "is_crisis": False,
        "status": "counseling_provided",
        "matched_module": matched_module["id"],
        "reply_ta": format_wellbeing_module_message(matched_module["id"]),
        "affirmation": matched_module["affirmation_ta"],
        "thirukkural": matched_module["thirukkural"]
    }


if __name__ == "__main__":
    print("Mental health modules:", len(WELLBEING_MODULES))
    print(format_whatsapp_mental_health_menu()["header_text"])
    print(format_wellbeing_module_message("exam_anxiety")[:250])
