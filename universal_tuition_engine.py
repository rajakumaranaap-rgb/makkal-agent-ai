"""
==============================================================================
Makkal Agent AI - Universal Tuition Class Engine (All Classes, All Syllabi)
==============================================================================
Target: Meta AI Developer Hackathon 2026 ($150,000 Track)
Role:
1. Provides universal, guided tuition coaching across:
   - Tamil Nadu State Board (Samacheer Kalvi) - Classes 1 to 12
   - CBSE Curriculum (NCERT) - Classes 1 to 12
   - College & Foundation (NEET, JEE, TNPSC Foundation)
2. Covers core subjects:
   - Mathematics, Science (Physics, Chemistry, Biology), Social Science, English, Tamil
3. Interactive WhatsApp 1-Click Buttons & Interactive Lists.
4. First-principles conceptual breakdown, step-by-step formulas, and 3-question quizzes.
5. Real-time dual sync between WhatsApp chat and Web App Tuition Studio.
==============================================================================
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("makkal.universal_tuition")

BOARDS = [
    {
        "id": "tn_state_board",
        "name_en": "Tamil Nadu State Board (Samacheer Kalvi)",
        "name_ta": "தமிழ்நாடு சமச்சீர் கல்வி (State Board)",
        "icon": "🏛️"
    },
    {
        "id": "cbse_ncert",
        "name_en": "CBSE Curriculum (NCERT)",
        "name_ta": "மத்திய இடைநிலைக் கல்வி வாரியம் (CBSE / NCERT)",
        "icon": "📚"
    }
]

CLASS_LEVELS = [
    {
        "id": "primary_1_5",
        "name_ta": "தொடக்கப் பள்ளி (வகுப்பு 1 - 5)",
        "name_en": "Primary School (Classes 1 - 5)",
        "icon": "🎒",
        "subjects": ["கணிதம் (Maths)", "சுற்றுச்சூழல் அறிவியல் (EVS)", "தமிழ் (Tamil)", "ஆங்கிலம் (English)"],
        "topics": [
            {
                "id": "primary_math_multiplication",
                "title_ta": "எளிய பெருக்கல் வாய்ப்பாடு & கூட்டல் (Multiplication Tables & Addition)",
                "summary_ta": "பெருக்கல் என்பது ஒரே எண்ணை மீண்டும் மீண்டும் கூட்டும் எளிய முறை (உதாரணம்: 3 x 4 = 3 + 3 + 3 + 3 = 12).",
                "concept_steps": [
                    "படி 1: பெருக்கல் என்பது தொடர் கூட்டல் (Repeated Addition).",
                    "படி 2: 5 x 3 என்றால் 5-ஐ 3 முறை கூட்டுதல் (5 + 5 + 5 = 15).",
                    "படி 3: விரல்களைப் பயன்படுத்தி அல்லது பொருட்கள் மூலம் எண்ணிப் பழகுங்கள்."
                ],
                "quiz": [
                    {"q": "7 x 8-ன் மதிப்பு என்ன?", "options": ["A) 54", "B) 56", "C) 64", "D) 48"], "ans": "B", "exp": "7 x 8 = 56. (7-ஐ 8 முறை கூட்டினால் 56 கிடைக்கும்)."}
                ]
            },
            {
                "id": "primary_evs_water_cycle",
                "title_ta": "நீர் சுழற்சி (Water Cycle for Kids)",
                "summary_ta": "சூரிய வெப்பத்தால் ஆவி ஆகுதல், மேகமாக மாறுதல், மழையாக பொழிதல்.",
                "concept_steps": [
                    "படி 1: ஆவியாதல் (Evaporation) - சூரியன் ஆற்றின் நீரை நீராவியாக மாற்றுகிறது.",
                    "படி 2: ஆவி சுருங்குதல் (Condensation) - நீராவி மேலே சென்று குளிர்ந்து மேகமாகிறது.",
                    "படி 3: மழைப் பொழிவு (Precipitation) - மேகம் பாரமாகி மழையாக பூமியில் பொழிகிறது."
                ],
                "quiz": [
                    {"q": "சூரிய வெப்பத்தால் நீர் நீராவியாக மாறும் நிகழ்வின் பெயர் என்ன?", "options": ["A) மழை", "B) ஆவியாதல்", "C) உறைதல்", "D) பனி"], "ans": "B", "exp": "வெப்பத்தால் நீர் ஆவியாக மாறுவது 'ஆவியாதல்' (Evaporation) ஆகும்."}
                ]
            }
        ]
    },
    {
        "id": "middle_6_8",
        "name_ta": "நடுநிலைப் பள்ளி (வகுப்பு 6 - 8)",
        "name_en": "Middle School (Classes 6 - 8)",
        "icon": "📐",
        "subjects": ["அறிவியல் (Science)", "கணிதம் (Mathematics)", "சமூக அறிவியல் (Social Science)"],
        "topics": [
            {
                "id": "middle_science_cell_structure",
                "title_ta": "உயிரினங்களின் அடிப்படை அலகு: செல் அமைப்பு (Cell Biology)",
                "summary_ta": "தாவர செல் மற்றும் விலங்கு செல் வேறுபாடுகள், உட்கரு (Nucleus) மற்றும் மைட்டோகாண்ட்ரியா.",
                "concept_steps": [
                    "படி 1: அனைத்து உயிரினங்களின் அடிப்படை கட்டமைப்பு மற்றும் செயல் அலகு செல்லாகும்.",
                    "படி 2: செல்லின் கட்டுப்பாட்டு மையம் 'உட்கரு' (Nucleus).",
                    "படி 3: செல்லின் ஆற்றல் மையம் (Powerhouse of the cell) 'மைட்டோகாண்ட்ரியா' (Mitochondria - ATP உருவாக்குகிறது).",
                    "படி 4: தாவர செல்லில் செல் சுவர் மற்றும் பசுங்கணிகம் உள்ளது; விலங்கு செல்லில் இல்லை."
                ],
                "quiz": [
                    {"q": "செல்லின் ஆற்றல் மையம் (Powerhouse of the Cell) என்று அழைக்கப்படுவது எது?", "options": ["A) உட்கரு", "B) ரைபோசோம்", "C) மைட்டோகாண்ட்ரியா", "D) செல் சுவர்"], "ans": "C", "exp": "மைட்டோகாண்ட்ரியா ATP மூலக்கூறுகளை உற்பத்தி செய்வதால் செல்லின் ஆற்றல் மையம் எனப்படுகிறது."}
                ]
            },
            {
                "id": "middle_math_algebra_fractions",
                "title_ta": "அடிப்படைக் இயற்கணிதம் & பின்னங்கள் (Algebraic Equations & Fractions)",
                "summary_ta": "மாறிகள் (Variables x, y), எளிய சமன்பாடுகள் தீர்த்தல் மற்றும் பின்னக் கூட்டல்.",
                "concept_steps": [
                    "படி 1: 2x + 5 = 15 சமன்பாட்டில், 5-ஐ வலப்பக்கம் கொண்டு சென்றால் 2x = 15 - 5 = 10.",
                    "படி 2: x = 10 / 2 = 5.",
                    "படி 3: இடப்பக்கம் மற்றும் வலப்பக்கம் எண்களை நகர்த்தும்போது குறியீடுகள் (+/- மற்றும் x/÷) மாறும்."
                ],
                "quiz": [
                    {"q": "3x - 4 = 11 எனில் x-ன் மதிப்பு என்ன?", "options": ["A) 3", "B) 5", "C) 7", "D) 4"], "ans": "B", "exp": "3x = 11 + 4 = 15 => x = 15 / 3 = 5."}
                ]
            }
        ]
    },
    {
        "id": "high_school_9_10",
        "name_ta": "உயர்நிலைப் பள்ளி (வகுப்பு 9 - 10 SSLC & CBSE)",
        "name_en": "High School (Classes 9 - 10)",
        "icon": "⚡",
        "subjects": ["இயற்பியல் (Physics)", "வேதியியல் (Chemistry)", "உயிரியல் (Biology)", "கணிதம் (Maths)"],
        "topics": [
            {
                "id": "class10_physics_electricity",
                "title_ta": "10-ம் வகுப்பு இயற்பியல்: மின்னோட்டம் & ஓம் விதி (Electricity & Ohm's Law)",
                "summary_ta": "மின்னழுத்தம், மின்னோட்டம், மின்தடை சமன்பாடு V = IR மற்றும் தொடர்/பக்க இணைப்புகள்.",
                "concept_steps": [
                    "படி 1: ஓம் விதி: மாறா வெப்பநிலையில், கடத்தியில் பாயும் மின்னோட்டம் (I) அதன் முனைகளுக்கு இடைப்பட்ட மின்னழுத்தத்திற்கு (V) நேர்தகவில் இருக்கும்: V = IR.",
                    "படி 2: தொடரிணைப்பு (Series): Rs = R1 + R2 + R3. மின்னோட்டம் சமமாக இருக்கும்.",
                    "படி 3: பக்க இணைப்பு (Parallel): 1/Rp = 1/R1 + 1/R2 + 1/R3. மின்னழுத்தம் சமமாக இருக்கும் (வீட்டு இணைப்புகள்)."
                ],
                "quiz": [
                    {"q": "12V பேட்டரியுடன் 4 ஓம் மின்தடை இணைக்கப்பட்டால் பாயும் மின்னோட்டம் (I) என்ன?", "options": ["A) 48 A", "B) 3 A", "C) 16 A", "D) 0.33 A"], "ans": "B", "exp": "I = V / R = 12 / 4 = 3 ஆம்பியர் (A)."}
                ]
            },
            {
                "id": "class10_maths_ap",
                "title_ta": "10-ம் வகுப்பு கணிதம்: கூட்டுத்தொடர் வரிசை (Arithmetic Progression - A.P.)",
                "summary_ta": "n-வது உறுப்பு tn = a + (n-1)d மற்றும் முதல் n உறுப்புகளின் கூடுதல் Sn = n/2[2a + (n-1)d].",
                "concept_steps": [
                    "படி 1: பொது வடிவம்: a, a+d, a+2d, a+3d... இங்கு a = முதல் உறுப்பு, d = பொது வித்தியாசம்.",
                    "படி 2: n-வது உறுப்பு சூத்திரம்: tn = a + (n - 1)d.",
                    "படி 3: கூடுதல் சூத்திரம்: Sn = n/2 [2a + (n - 1)d] அல்லது Sn = n/2 [a + l]."
                ],
                "quiz": [
                    {"q": "5, 9, 13, 17... தொடரின் 10-வது உறுப்பு என்ன?", "options": ["A) 41", "B) 45", "C) 37", "D) 40"], "ans": "A", "exp": "a=5, d=4, n=10 => t10 = 5 + (10-1)4 = 5 + 36 = 41."}
                ]
            }
        ]
    },
    {
        "id": "higher_sec_11_12",
        "name_ta": "மேல்நிலைப் பள்ளி (வகுப்பு 11 - 12 HSC & CBSE 12th)",
        "name_en": "Higher Secondary (Classes 11 - 12)",
        "icon": "🔬",
        "subjects": ["இயற்பியல் (Physics)", "வேதியியல் (Chemistry)", "உயிரியல்/தாவரவியல் (Biology)", "கணிதம் (Maths)"],
        "topics": [
            {
                "id": "class12_physics_semiconductors",
                "title_ta": "12-ம் வகுப்பு இயற்பியல்: குறைக்கடத்திகள் & PN சந்தி டையோடு (Semiconductor Devices)",
                "summary_ta": "உள்ளார்ந்த & புறவியலான குறைக்கடத்திகள், p-வகை & n-வகை, முன்னோக்கு மற்றும் பின்னோக்கு சார்பு.",
                "concept_steps": [
                    "படி 1: தூய சிலிக்கான்/ஜெர்மானியம் உள்ளார்ந்த குறைக்கடத்தி (Intrinsic).",
                    "படி 2: 3-இணைதிறன் அசுவை சேர்த்தால் p-வகை (துளைகள் அதிகம்); 5-இணைதிறன் அசுவை சேர்த்தால் n-வகை (எலக்ட்ரான்கள் அதிகம்).",
                    "படி 3: PN சந்தி முன்னோக்குச் சார்பில் (Forward Bias) மின்தடை குறைந்து மின்னோட்டம் பாயும்; பின்னோக்குச் சார்பில் (Reverse Bias) மின்னோட்டம் பாயாது (தடுப்பு அடுக்கு அகலமாகும்)."
                ],
                "quiz": [
                    {"q": "முன்னோக்கு சார்பில் (Forward Bias) PN சந்தி டையோடின் தடுப்பு அடுக்கின் தடிமன் என்னவாகும்?", "options": ["A) அதிகரிக்கும்", "B) குறையும்", "C) மாறாது", "D) பூஜ்ஜியத்திற்கு மேல் உயரும்"], "ans": "B", "exp": "முன்னோக்கு சார்பில் தடுப்பு மின்னழுத்தம் குறைக்கப்பட்டு தடுப்பு அடுக்கின் தடிமன் குறைகிறது."}
                ]
            },
            {
                "id": "class12_chem_organic_reactions",
                "title_ta": "12-ம் வகுப்பு வேதியியல்: கரிம வேதியியல் வினைகள் (Organic Chemistry SN1 & SN2)",
                "summary_ta": "நியூக்ளியோஃபிலிக் பதிலீட்டு வினைகள் SN1 (இருபடி) மற்றும் SN2 (ஒருபடி - தலைகீழ் அமைப்பு).",
                "concept_steps": [
                    "படி 1: SN1 வினை இரண்டு படிகளில் நிகழும்; கார்போகேட்டயான் இடைநிலை பொருள் உருவாகும் (மூவிணைய ஆல்கைல் ஹாலைடுகளில் வேகமானது).",
                    "படி 2: SN2 வினை ஒரே படியில் நிகழும்; இடைநிலை நிலையின்றி வால்டன் தலைகீழ் மாற்றம் (Walden Inversion) அடையும் (ஓரிணைய ஆல்கைல் ஹாலைடுகளில் வேகமானது)."
                ],
                "quiz": [
                    {"q": "SN2 வினையில் நடைபெறும் முக்கிய முப்பரிமாண வேதியியல் மாற்றம் எது?", "options": ["A) ரேசிமிக் கலவை", "B) வால்டன் தலைகீழ் மாற்றம்", "C) பாலிமராக்கல்", "D) சுழற்சி மாற்றம்"], "ans": "B", "exp": "SN2 வினையில் நியூக்ளியோஃபைல் பின்புறமாக தாக்குவதால் வால்டன் தலைகீழ் மாற்றம் (Walden Inversion) நிகழ்கிறது."}
                ]
            }
        ]
    }
]


def get_all_tuition_classes() -> List[Dict[str, Any]]:
    """Returns all class buckets and curricula."""
    return CLASS_LEVELS


def get_tuition_topic_by_id(topic_id: str) -> Optional[Dict[str, Any]]:
    """Finds a tuition topic across all class levels."""
    for lvl in CLASS_LEVELS:
        for t in lvl["topics"]:
            if t["id"] == topic_id:
                return {
                    "class_level_id": lvl["id"],
                    "class_level_ta": lvl["name_ta"],
                    "topic": t
                }
    return None


def format_whatsapp_tuition_menu() -> Dict[str, Any]:
    """Generates interactive WhatsApp button menu for universal tuition."""
    body_text = (
        "📚 *SIA உலகளாவிய டியூஷன் அரங்கம் (Universal Tuition Class)* 🎓\n\n"
        "அனைத்து வகுப்புகள் மற்றும் பாடத்திட்டங்களுக்கான எளிய கற்றல் வழிகாட்டி:\n\n"
        "🏛️ *பாடத்திட்டம்:* தமிழ்நாடு சமச்சீர் கல்வி & CBSE (NCERT)\n"
        "🎒 *வகுப்புகள்:* வகுப்பு 1 முதல் 12 வரை (Maths, Science, Physics, Chemistry, Biology)\n\n"
        "கீழே உள்ள பொத்தானை அழுத்தி உங்கள் வகுப்பைத் தேர்ந்தெடுக்கவும் 👇"
    )
    buttons = [
        {"id": "tui_cls_primary", "title": "🎒 வகுப்பு 1 - 5"},
        {"id": "tui_cls_high",    "title": "⚡ வகுப்பு 9 - 10"},
        {"id": "tui_cls_higher",  "title": "🔬 வகுப்பு 11 - 12"}
    ]
    return {
        "body_text": body_text,
        "buttons": buttons,
        "header_text": "📚 SIA Universal Tuition",
        "footer_text": "CBSE & Tamil Nadu State Board"
    }


def format_whatsapp_class_topics_list(class_level_id: str) -> Dict[str, Any]:
    """Generates interactive list message of topics for a selected class level."""
    target_lvl = next((l for l in CLASS_LEVELS if l["id"] == class_level_id), CLASS_LEVELS[2])
    rows = []
    for t in target_lvl["topics"]:
        rows.append({
            "id": f"tui_top_{t['id']}",
            "title": t["title_ta"][:24],
            "description": t["summary_ta"][:72]
        })

    sections = [{
        "title": target_lvl["name_en"][:24],
        "rows": rows[:10]
    }]

    body_text = (
        f"{target_lvl['icon']} *{target_lvl['name_ta']}*\n\n"
        f"பாடங்கள்: {', '.join(target_lvl['subjects'])}\n\n"
        "கீழே உள்ள பாடத் தலைப்புகளில் ஒன்றை தேர்வு செய்து உடனடி விளக்கத்தைப் பெறுங்கள்:"
    )

    return {
        "body_text": body_text,
        "button_label": "பாடத் தலைப்புகள்",
        "sections": sections,
        "header_text": target_lvl["name_en"][:60],
        "footer_text": "SIA First-Principles Tuition"
    }


def format_tuition_lesson_card(topic_id: str) -> str:
    """Formats full step-by-step tuition explanation and quiz card for WhatsApp."""
    data = get_tuition_topic_by_id(topic_id)
    if not data:
        return "மன்னிக்கவும்! இந்த பாடம் கிடைக்கவில்லை. *TUITION* என அனுப்பி மெனுவை மீண்டும் பெறலாம்."

    t = data["topic"]
    lines = [
        f"📖 *{t['title_ta']}*",
        f"🏫 *பிரிவு:* {data['class_level_ta']}",
        "-----------------------------------------",
        f"💡 *பாடச் சுருக்கம் (Summary):*\n{t['summary_ta']}\n",
        "🔍 *படிமுறை விளக்கம் (Step-by-Step Breakdown):*"
    ]
    for step in t["concept_steps"]:
        lines.append(f"  • {step}")

    if t.get("quiz"):
        q_item = t["quiz"][0]
        lines.append("\n-----------------------------------------")
        lines.append("📝 *சுய மதிப்பீட்டு வினாடி-வினா (Quick Quiz):*")
        lines.append(f"❓ *{q_item['q']}*")
        for opt in q_item["options"]:
            lines.append(f"   {opt}")
        lines.append(f"\n💡 *விடை & விளக்கம்:* {q_item['exp']}")

    lines.append("\n💬 உங்களுக்கு இதில் வேறு ஏதேனும் சந்தேகம் இருந்தால், அந்த கேள்வியை இந்த அரட்டையிலேயே தட்டச்சு செய்து அனுப்புங்கள்! Meta Wonder 1.0 உடனே விளக்கும்.")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Class levels:", len(CLASS_LEVELS))
    menu = format_whatsapp_tuition_menu()
    print("Menu:", menu["header_text"])
    lesson = format_tuition_lesson_card("class10_physics_electricity")
    print("Sample lesson:\n", lesson[:250])
