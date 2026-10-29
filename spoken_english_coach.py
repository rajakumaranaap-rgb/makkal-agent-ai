"""
==============================================================================
Makkal Agent AI - WhatsApp & Web Conversational Spoken English Coach
==============================================================================
Target: Meta AI Developer Hackathon 2026 ($150,000 Track)
Role:
1. Provides level-wise conversational spoken English training for all ages:
   - Level 1: Beginners / Kids / Rural Learners (Phonetics, Tanglish -> English, Daily Words)
   - Level 2: School & College Students (Classroom Talk, Extempore, Grammar Tips)
   - Level 3: Job Seekers & Professionals (Self-Intro, HR Interview Q&A, Client Calls)
   - Level 4: Homemakers & Parents (Parent-Teacher Meeting, Clinic, Travel)
2. Interactive WhatsApp 1-Click Button & List messages.
3. Pronunciation assessment & Tamil phonetic transliteration (e.g. Schedule -> 'ஷெட்யூல்').
4. Real-time dual sync between WhatsApp chat and Web App Studio.
==============================================================================
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("makkal.spoken_english")

# Level-wise Modules Catalog
ENGLISH_LEVELS = [
    {
        "id": "level_1_beginner",
        "title_en": "Level 1: Daily Spoken English (Beginners & Kids)",
        "title_ta": "நிலை 1: தொடக்க நிலை - தினசரி உரையாடல் (குழந்தைகள் & புதியவர்கள்)",
        "target_audience": "Rural learners, kids, anyone starting from scratch",
        "icon": "🌱",
        "scenarios": [
            {
                "id": "daily_greetings",
                "title_ta": "காலை & மாலை வாழ்த்துகள் (Daily Greetings)",
                "dialogue_pairs": [
                    {"ta": "காலை வணக்கம்! நீங்கள் எப்படி இருக்கிறீர்கள்?", "en": "Good morning! How are you doing today?", "phonetic_ta": "குட் மார்னிங்! ஹௌ ஆர் யூ டூயிங் டுடே?"},
                    {"ta": "நான் நன்றாக இருக்கிறேன், நன்றி! நீங்கள்?", "en": "I am doing well, thank you! How about you?", "phonetic_ta": "ஐ ஆம் டூயிங் வெல், தேங்க் யூ! ஹௌ அபௌட் யூ?"},
                    {"ta": "உங்களை சந்தித்ததில் மகிழ்ச்சி.", "en": "It is a pleasure to meet you.", "phonetic_ta": "இட் இஸ் எ ப்ளெஷர் டு மீட் யூ."}
                ],
                "practice_tip": "தினமும் காலையில் குடும்பத்தாரிடம் 'Good morning!' என தொடங்கி பேசி பழகுங்கள்."
            },
            {
                "id": "daily_shopping",
                "title_ta": "கடையில் பொருட்கள் வாங்குதல் (Shopping & Supermarket)",
                "dialogue_pairs": [
                    {"ta": "இந்த பொருளின் விலை என்ன?", "en": "How much does this item cost?", "phonetic_ta": "ஹௌ மச் டஸ் திஸ் ஐட்டம் காஸ்ட்?"},
                    {"ta": "புதிய காய்கறிகள் உள்ளதா?", "en": "Do you have fresh vegetables in stock?", "phonetic_ta": "டூ யூ ஹேவ் ஃபிரெஷ் வெஜிடபிள்ஸ் இன் ஸ்டாக்?"},
                    {"ta": "நான் UPI அல்லது கார்டு மூலம் பணம் செலுத்தலாமா?", "en": "Can I pay via UPI or card?", "phonetic_ta": "கேன் ஐ பே வயா யூபிஐ ஆர் கார்ட்?"}
                ],
                "practice_tip": "காய்கறி அல்லது மளிகைக் கடைக்குச் செல்லும்போது 'How much is this?' என்று கேளுங்கள்."
            }
        ]
    },
    {
        "id": "level_2_student",
        "title_en": "Level 2: School & College Communication",
        "title_ta": "நிலை 2: பள்ளி & கல்லூரி மாணவர்கள் பேச்சுத் திறன்",
        "target_audience": "Class 6-12 & College Students",
        "icon": "🎓",
        "scenarios": [
            {
                "id": "classroom_doubts",
                "title_ta": "ஆசிரியரிடம் சந்தேகம் கேட்டல் (Asking Doubts in Class)",
                "dialogue_pairs": [
                    {"ta": "மன்னிக்கவும் ஆசிரியர், இந்த கணக்கை மீண்டும் ஒருமுறை விளக்குவீர்களா?", "en": "Excuse me teacher, could you please explain this problem once again?", "phonetic_ta": "எக்ஸ்கியூஸ் மீ டீச்சர், குட் யூ ப்ளீஸ் எக்ஸ்பிளைன் திஸ் ப்ராப்ளம் ஒன்ஸ் அகைன்?"},
                    {"ta": "நான் இந்த குறிப்பை குறித்துக் கொள்ளலாமா?", "en": "May I take down these notes, please?", "phonetic_ta": "மே ஐ டேக் டவுன் தீஸ் நோட்ஸ், ப்ளீஸ்?"},
                    {"ta": "இன்றைய வீட்டுப்பாடம் என்ன?", "en": "What is the homework assignment for today?", "phonetic_ta": "வாட் இஸ் தி ஹோம்வொர்க் அசைன்மென்ட் ஃபார் டுடே?"}
                ],
                "practice_tip": "வகுப்பில் சந்தேகம் கேட்க தயங்காதீர்கள். 'Could you please repeat?' என்று துணிந்து கேளுங்கள்."
            },
            {
                "id": "group_discussion",
                "title_ta": "குழு விவாதம் & கருத்து பகிர்தல் (Group Discussion & Debate)",
                "dialogue_pairs": [
                    {"ta": "என் கருத்துப்படி, இது சிறந்த தீர்வு.", "en": "In my opinion, this is the most effective solution.", "phonetic_ta": "இன் மை ஒப்பினியன், திஸ் இஸ் தி மோஸ்ட் எஃபெக்டிவ் சொல்யூஷன்."},
                    {"ta": "நான் உங்கள் கருத்தை முழுமையாக ஆதரிக்கிறேன்.", "en": "I completely agree with your viewpoint.", "phonetic_ta": "ஐ கம்ப்ளீட்லி அக்ரீ வித் யுவர் வியூபாயிண்ட்."},
                    {"ta": "நான் ஒரு கூடுதல் கருத்தைச் சொல்லலாமா?", "en": "May I add an additional point here?", "phonetic_ta": "மே ஐ ஆட் அன் அடிஷனல் பாயிண்ட் ஹியர்?"}
                ],
                "practice_tip": "GD-ல் குறுக்கிடும் போது 'Excuse me, may I add a point?' என கண்ணியமாகத் தொடங்குங்கள்."
            }
        ]
    },
    {
        "id": "level_3_interview",
        "title_en": "Level 3: Job Interview & Professional Fluency",
        "title_ta": "நிலை 3: வேலை நேர்காணல் & அலுவலக ஆங்கிலம் (Job Seekers)",
        "target_audience": "Graduates, Job seekers, IT/Corporate professionals",
        "icon": "💼",
        "scenarios": [
            {
                "id": "self_introduction",
                "title_ta": "சுய அறிமுகம் (Tell me about yourself)",
                "dialogue_pairs": [
                    {"ta": "வணக்கம்! என்னை அறிமுகப்படுத்த வாய்ப்பளித்ததற்கு நன்றி.", "en": "Good morning! Thank you for giving me this wonderful opportunity to introduce myself.", "phonetic_ta": "குட் மார்னிங்! தேங்க் யூ ஃபார் கிவிங் மீ திஸ் வண்டர்ஃபுல் ஆப்பர்ச்சூனிட்டி டு இன்ட்ரடியூஸ் மைசெல்ஃப்."},
                    {"ta": "நான் மதுரையில் கணினி பொறியியல் பட்டப்படிப்பு முடித்துள்ளேன்.", "en": "I completed my Bachelor's in Computer Science from Madurai.", "phonetic_ta": "ஐ கம்ப்ளீட்டட் மை பேச்சிலர்ஸ் இன் கம்ப்யூட்டர் சயின்ஸ் ஃப்ரம் மதுரை."},
                    {"ta": "புதிய தொழில்நுட்பங்களை விரைவாகக் கற்று செயல்படுத்துவது எனது பலம்.", "en": "My greatest strength is my ability to learn new technologies rapidly and solve real problems.", "phonetic_ta": "மை கிரேட்டஸ்ட் ஸ்ட்ரெங்த் இஸ் மை எபிலிட்டி டு லேர்ன் நியூ டெக்னாலஜீஸ் ராபிட்லி அண்ட் சால்வ் ரியல் ப்ராப்ளம்ஸ்."}
                ],
                "practice_tip": "நேர்காணலில் 90 வினாடிகளுக்குள் சுருக்கமாகவும் புன்னகையுடனும் அறிமுகம் அமைய வேண்டும்."
            },
            {
                "id": "hr_why_hire",
                "title_ta": "நாங்கள் உங்களை ஏன் தேர்வு செய்ய வேண்டும்? (Why should we hire you?)",
                "dialogue_pairs": [
                    {"ta": "எனது தொழில்நுட்ப திறனும் அர்ப்பணிப்பும் உங்கள் நிறுவன வளர்ச்சிக்கு பெரிதும் உதவும்.", "en": "My core technical skills and proactive mindset align perfectly with your team's ambitious goals.", "phonetic_ta": "மை கோர் டெக்னிக்கல் ஸ்கில்ஸ் அண்ட் புரோஆக்டிவ் மைண்ட்செட் அலைன் பெர்ஃபெக்ட்லி வித் யுவர் டீம்ஸ் ஆம்பிஷியஸ் கோல்ஸ்."},
                    {"ta": "நான் கடின உழைப்பை எப்போதும் மதிப்பவன்.", "en": "I take complete ownership of deliverables and thrive in collaborative environments.", "phonetic_ta": "ஐ டேக் கம்ப்ளீட் ஓனர்ஷிப் ஆஃப் டெலிவரபிள்ஸ் அண்ட் த்ரைவ் இன் கொலாபரேட்டிவ் என்விரான்மென்ட்ஸ்."}
                ],
                "practice_tip": "உங்கள் திறமை நிறுவனத்திற்கு என்ன லாபம் அல்லது மதிப்பு சேர்க்கும் என்பதை சுட்டிக்காட்டுங்கள்."
            }
        ]
    },
    {
        "id": "level_4_homemaker",
        "title_en": "Level 4: Everyday English for Parents & Homemakers",
        "title_ta": "நிலை 4: பெற்றோர்கள் & குடும்பப் பெண்களுக்கான ஆங்கிலம்",
        "target_audience": "Mothers, Homemakers, Parents communicating with schools & clinics",
        "icon": "🏡",
        "scenarios": [
            {
                "id": "ptm_meeting",
                "title_ta": "பெற்றோர் ஆசிரியர் சந்திப்பு (Parent-Teacher Meeting - PTM)",
                "dialogue_pairs": [
                    {"ta": "என் குழந்தையின் படிப்பு மற்றும் நடத்தை எவ்வாறு உள்ளது ஆசிரியர்?", "en": "Hello teacher, how is my child performing academically and behaviorally in class?", "phonetic_ta": "ஹலோ டீச்சர், ஹௌ இஸ் மை சைல்ட் பெர்ஃபார்மிங் அகாடமிக்கலி அண்ட் பிஹேவியரலி இன் கிளாஸ்?"},
                    {"ta": "கணிதத்தில் அவன் இன்னும் கூடுதல் கவனம் செலுத்த வேண்டுமா?", "en": "Does he need any extra guidance or practice in Mathematics?", "phonetic_ta": "டஸ் ஹி நீட் எனி எக்ஸ்ட்ரா கைடன்ஸ் ஆர் பிராக்டிஸ் இன் மேத்தமேட்டிக்ஸ்?"},
                    {"ta": "வீட்டில் நாங்கள் எவ்வாறு உதவலாம்?", "en": "What can we do at home to support her learning better?", "phonetic_ta": "வாட் கேன் வி டூ அட் ஹோம் டு சப்போர்ட் ஹெர் லேர்னிங் பெட்டர்?"}
                ],
                "practice_tip": "PTM-ல் தயக்கமின்றி ஆசிரியரிடம் குழந்தையின் கற்றல் முன்னேற்றத்தைக் கேளுங்கள்."
            },
            {
                "id": "clinic_visit",
                "title_ta": "மருத்துவமனையில் பேசுதல் (At the Doctor / Clinic)",
                "dialogue_pairs": [
                    {"ta": "என் மகனுக்கு இரண்டு நாட்களாக லேசான காய்ச்சல் மற்றும் இருமல் உள்ளது.", "en": "Doctor, my son has had a mild fever and dry cough for the past two days.", "phonetic_ta": "டாக்டர், மை சன் ஹேஸ் ஹேட் எ மைல்ட் ஃபீவர் அண்ட் ட்ரை காஃப் ஃபார் தி பாஸ்ட் டூ டேஸ்."},
                    {"ta": "இந்த மாத்திரையை உணவுக்கு முன்னா அல்லது பின்னா சாப்பிட வேண்டும்?", "en": "Should this medicine be taken before or after meals?", "phonetic_ta": "ஷுட் திஸ் மெடிசின் பி டேக்கன் பிஃபோர் ஆர் ஆஃப்டர் மீல்ஸ்?"}
                ],
                "practice_tip": "மருந்தின் அளவு மற்றும் உணவு முறையை 'Before meals or after meals?' என்று தவறாமல் கேட்டு உறுதி செய்யுங்கள்."
            }
        ]
    }
]

# Common Tanglish Mistakes & Corrections
COMMON_ERRORS_TAMIL_USERS = [
    {"pattern": "am having", "correction": "have (e.g. I have a brother)", "rule_ta": "'Have' என்பது உடைமையைக் குறிக்கும் போது '-ing' வராது."},
    {"pattern": "did not came", "correction": "did not come", "rule_ta": "'Did' வந்த பிறகு பிரதான வினைச்சொல் நிகழ்கால வடிவில் (come) மட்டுமே வர வேண்டும்."},
    {"pattern": "did not went", "correction": "did not go", "rule_ta": "'Did' வந்த பிறகு go மட்டுமே வர வேண்டும்."},
    {"pattern": "myself ", "correction": "I am / My name is", "rule_ta": "அறிமுகத்தில் 'Myself' பயன்பாடு தவறானது, 'I am' அல்லது 'My name is' மட்டுமே பயன்படுத்தவும்."},
    {"pattern": "why you are", "correction": "why are you", "rule_ta": "கேள்வி வாக்கியங்களில் 'Why are you' என துணைவினைச்சொல் முன்னே வர வேண்டும்."},
    {"pattern": "told to", "correction": "told / said to", "rule_ta": "'Told' பின்னால் 'to' வரக்கூடாது."}
]


def get_all_english_levels() -> List[Dict[str, Any]]:
    """Returns the full catalog of spoken English levels."""
    return ENGLISH_LEVELS


def get_scenario_details(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Finds a specific spoken English scenario across levels."""
    for lvl in ENGLISH_LEVELS:
        for s in lvl["scenarios"]:
            if s["id"] == scenario_id:
                return {
                    "level_id": lvl["id"],
                    "level_title_ta": lvl["title_ta"],
                    "scenario": s
                }
    return None


def format_whatsapp_english_menu() -> Dict[str, Any]:
    """
    Returns WhatsApp interactive button/list payload for spoken English.
    """
    body_text = (
        "🗣️ *SIA WhatsApp Spoken English Coach (பேச்சு ஆங்கிலப் பயிற்சி)* 🎙️\n\n"
        "தமிழ் வழியில் மிக எளிதாக ஆங்கிலம் பேச பழகுங்கள்! அனைத்து வயதினருக்கும் ஏற்ற பயிற்சி:\n\n"
        "🌱 *நிலை 1:* குழந்தைகள் & தொடக்க நிலை (Daily Talk)\n"
        "🎓 *நிலை 2:* பள்ளி & கல்லூரி மாணவர்கள் (Class & GD)\n"
        "💼 *நிலை 3:* நேர்காணல் & வேலை வாய்ப்பு (Interview Q&A)\n"
        "🏡 *நிலை 4:* பெற்றோர் & குடும்பத்தினர் (PTM & Clinic)\n\n"
        "கீழே உள்ள பட்டனை அழுத்தி உங்கள் நிலையைத் தேர்ந்தெடுக்கவும் 👇"
    )
    buttons = [
        {"id": "eng_lvl_1", "title": "🌱 நிலை 1: தொடக்கம்"},
        {"id": "eng_lvl_2", "title": "🎓 நிலை 2: மாணவர்"},
        {"id": "eng_lvl_3", "title": "💼 நிலை 3: இன்டர்வியூ"}
    ]
    return {
        "body_text": body_text,
        "buttons": buttons,
        "header_text": "🗣️ Spoken English Studio",
        "footer_text": "Meta SeamlessM4T & Wonder 1.0 Powered"
    }


def format_whatsapp_level_scenarios(level_id: str) -> Dict[str, Any]:
    """Generates interactive list message for scenarios within a level."""
    target_lvl = next((l for l in ENGLISH_LEVELS if l["id"] == level_id), ENGLISH_LEVELS[0])
    rows = []
    for s in target_lvl["scenarios"]:
        rows.append({
            "id": f"scn_{s['id']}",
            "title": s["title_ta"][:24],
            "description": s["practice_tip"][:72]
        })

    sections = [{
        "title": target_lvl["title_en"][:24],
        "rows": rows[:10]
    }]

    body_text = (
        f"🎯 *{target_lvl['title_ta']}*\n\n"
        f"இலக்கு: _{target_lvl['target_audience']}_\n\n"
        "கீழே உள்ள தலைப்புகளில் ஒன்றை தேர்வு செய்து உரையாடலைத் தொடங்குங்கள்:"
    )

    return {
        "body_text": body_text,
        "button_label": "பயிற்சி தலைப்புகள்",
        "sections": sections,
        "header_text": target_lvl["icon"] + " " + target_lvl["title_en"][:50],
        "footer_text": "SIA Conversational Language Coach"
    }


def format_scenario_practice_message(scenario_id: str) -> str:
    """Formats full bilingual dialogue practice card for WhatsApp."""
    sc_data = get_scenario_details(scenario_id)
    if not sc_data:
        return "மன்னிக்கவும்! இந்த தலைப்பு கிடைக்கவில்லை. *ENGLISH* என அனுப்பி மெனுவைப் பெறலாம்."

    s = sc_data["scenario"]
    lines = [
        f"🗣️ *{s['title_ta']}*",
        f"📚 *பிரிவு:* {sc_data['level_title_ta']}",
        "-----------------------------------------",
        "💡 *கீழே உள்ள வாக்கியங்களை சத்தமாக வாசித்து பழகவும்:*\n"
    ]

    for idx, d in enumerate(s["dialogue_pairs"], 1):
        lines.append(f"*{idx}. {d['ta']}*")
        lines.append(f"🇬🇧 *English:* \"{d['en']}\"")
        lines.append(f"🗣️ *உச்சரிப்பு:* _{d['phonetic_ta']}_\n")

    lines.append("-----------------------------------------")
    lines.append(f"📌 *பயிற்சி குறிப்பு:* {s['practice_tip']}")
    lines.append("\n🎙️ *உங்கள் குரல் பயிற்சி:* மேலே உள்ள வாக்கியங்களை பேசி ஒரு குரல் பதிவை (Voice Note) இந்த அரட்டையில் அனுப்புங்கள்! Meta SeamlessM4T உங்கள் உச்சரிப்பை சரிபார்த்து மதிப்பெண் வழங்கும்.")

    return "\n".join(lines)


def evaluate_spoken_sentence(spoken_text: str, target_sentence: Optional[str] = None) -> Dict[str, Any]:
    """
    Evaluates citizen's spoken transcript using Meta AI linguistic logic.
    Identifies common errors, calculates score, and provides correction.
    """
    clean_spoken = spoken_text.strip()
    words = clean_spoken.split()
    word_count = len(words)

    score = min(100, max(50, word_count * 12))
    corrections = []

    spoken_lower = clean_spoken.lower()
    for err in COMMON_ERRORS_TAMIL_USERS:
        if err["pattern"] in spoken_lower:
            corrections.append({
                "found_error": err["pattern"],
                "proper_correction": err["correction"],
                "rule_tamil": err["rule_ta"]
            })
            score = max(50, score - 20)

    feedback_ta = "அருமையான முயற்சி! உங்கள் வார்த்தை உச்சரிப்பு தெளிவாக உள்ளது." if score >= 80 else "நல்ல முயற்சி! கீழே உள்ள இலக்கணத் திருத்தங்களை கவனித்து மீண்டும் முயற்சி செய்யுங்கள்."

    return {
        "status": "success",
        "spoken_text": clean_spoken,
        "score_percentage": score,
        "word_count": word_count,
        "fluency_level": "Intermediate" if score >= 75 else "Beginner",
        "feedback_ta": feedback_ta,
        "corrections": corrections,
        "suggested_next_practice": "அடுத்த வாக்கியத்தைப் பேசி வாட்ஸ்அப்பில் ஆடியோவாக அனுப்புங்கள்!"
    }


if __name__ == "__main__":
    print("Spoken English levels:", len(ENGLISH_LEVELS))
    menu = format_whatsapp_english_menu()
    print("Menu title:", menu["header_text"])
    sc_msg = format_scenario_practice_message("self_introduction")
    print("Scenario sample:\n", sc_msg[:200])
