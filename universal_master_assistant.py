# -*- coding: utf-8 -*-
"""
==============================================================================
SIA Makkal — Universal Master AI Assistant & Services Directory
==============================================================================
Empowers Meta AI Model (Llama 3.3 70B / Muse Spark 1.3 / Muse Wonder 1.0)
to triage, guide, execute, and instruct citizens on all services available
through WhatsApp or Web App.

Covers 12 Complete Sovereign Domains:
1.  🏛️ Civic & Welfare Schemes (Patta, EC, Ration, KMUT, CMCHIS, RTI, Aadhaar, EB)
2.  📜 MLA & MP Grievance Petitions (Voice/Text to PDF & 1-Click WhatsApp Forwarder)
3.  📚 School Tuition & Daily Homework (Class 1-12 Samacheer/CBSE, Diagrams, Solver)
4.  🎯 National & TN Competitive Exams (NEET, JEE, NDA, TNPSC, UPSC, Bank, RRB CBT)
5.  🌾 Smart Agriculture & Crop Protection (Meta SAM 3.1 Disease Detection, TNAU, PM-Kisan)
6.  🛵 Hyperlocal Zero-Commission Rentals & Gig Labor (Bike, Auto, Tractor, Harvester, Masons)
7.  🤝 Service Partner Self-Registration (Drivers, Operators, Artisans, Tutors via WhatsApp)
8.  🏛️ Citizen Sovereign Life Vault (Daily Accounts, Contacts, Proofs, Needs, Diary, Secret)
9.  📈 Boto Quant Share Market & Investments (Nifty/BankNifty, Strategies, SEBI Rules)
10. 📰 Daily Morning News & AIR Tamil Radio (10 TN + 5 India + 3 World News + AIR Audio)
11. 🗣️ Spoken English & Mental Health (Fluency Coaching & Tele-MANAS 14416 Counseling)
12. 🎬 Entertainment & Civic Greetings (Cinema, Songs, Custom Festival/Birthday Posters)
==============================================================================
"""

import os
import re
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger("makkal.master_assistant")

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "https://regulatory-stack-counter-lady.trycloudflare.com")

# -----------------------------------------------------------------------------
# 1. MASTER SERVICES CATALOG METADATA
# -----------------------------------------------------------------------------
SIA_MASTER_SERVICES = [
    {
        "id": "civic_governance",
        "title_ta": "அரசு நலத்திட்டங்கள் & மின்-சேவை",
        "title_en": "Govt Schemes & e-Governance",
        "icon": "🏛️",
        "desc_ta": "பட்டா மாறுதல் (இலவசம் ₹0), வில்லங்க சான்று (EC), ரேஷன் அட்டை, மகளிர் உரிமைத் தொகை (₹1000), 100 யூனிட் இலவச மின்சாரம், RTI மனு (₹10), ஆதார் முகவரி மாற்றம் (₹50).",
        "sample_cmd": "பட்டா மாறுதல் முறை என்ன?",
        "keywords": ["பட்டா", "ரேஷன்", "ஆதார்", "rti", "மின்சாரம்", "மகளிர் உரிமை", "kmut", "cmchis", "காப்பீடு", "ec", "வில்லங்கம்", "patta", "ration", "aadhaar"]
    },
    {
        "id": "mla_mp_petitions",
        "title_ta": "MLA / MP குறைதீர்ப்பு மனு & PDF",
        "title_en": "MLA & MP Petitions & Forwarder",
        "icon": "📜",
        "desc_ta": "உங்கள் தொகுதி சட்டமன்ற உறுப்பினர் (234 MLA) அல்லது நாடாளுமன்ற உறுப்பினர் (39 MP)-க்கு அதிகாரப்பூர்வ சட்ட மனு PDF தயாரித்து வாட்ஸ்அப்பில் பகிருங்கள்.",
        "sample_cmd": "சோழவந்தான் MLA மனு சாலை சீரமைப்பு",
        "keywords": ["மனு", "புகார்", "எம்எல்ஏ", "mla", "mp", "petition", "பாராளுமன்ற", "சட்டமன்ற", "சாலை", "குடிநீர்"]
    },
    {
        "id": "school_tuition",
        "title_ta": "பள்ளி கல்வி, டியூஷன் & ஹோம்வொர்க்",
        "title_en": "School Tuition & Homework Helper",
        "icon": "📚",
        "desc_ta": "1 முதல் 12-ஆம் வகுப்பு சமச்சீர் & CBSE பாடத்திட்டம். அறிவியல் வரைபடங்கள், கணித தீர்வுகள், 10-ஆம் வகுப்பு தினசரி வினா-விடை & ஆசிரியர் வீட்டுப்பாடம் பதிவேற்றம்.",
        "sample_cmd": "10-ஆம் வகுப்பு ஒளியியல் வரைபடம் விளக்கம்",
        "keywords": ["10th", "12th", "cbse", "டியூஷன்", "tuition", "ஹோம்வொர்க்", "homework", "கணிதம்", "அறிவியல்", "science", "maths", "சமச்சீர்"]
    },
    {
        "id": "competitive_exams",
        "title_ta": "போட்டித் தேர்வுகள் CBT & சான்றிதழ்",
        "title_en": "Competitive Exams CBT & Certificate",
        "icon": "🎯",
        "desc_ta": "NEET, JEE, NDA, TNPSC (குரூப் 1/2/4, VAO), UPSC, வங்கி & ரயில்வே தேர்வுகள். மாதிரி வினாத்தாள், ஆன்லைன் CBT தேர்வு லிங்க், உடனடி மதிப்பெண் & SVG திறன் சான்றிதழ்.",
        "sample_cmd": "TNPSC குரூப் 4 திருக்குறள் 5 வினாக்கள் தேர்வு",
        "keywords": ["neet", "jee", "tnpsc", "upsc", "cbt", "தேர்வு", "exam", "quiz", "சான்றிதழ்", "certificate", "நோட்ஸ்", "notes", "குரூப் 4"]
    },
    {
        "id": "smart_agriculture",
        "title_ta": "டிஜிட்டல் உழவர் ஆலோசகர் & பயிர் நோய்",
        "title_en": "Smart Agriculture & Crop Protection",
        "icon": "🌾",
        "desc_ta": "பயிர் இலை படம் அனுப்பி Meta SAM 3.1 மூலம் நோய் கண்டறிதல், TNAU உர பரிந்துரை, உழவன் / GRAINS மானியம், PM-Kisan (₹6000), PMFBY பயிர் காப்பீடு.",
        "sample_cmd": "நெல் இலை கருகல் நோய் மருந்து என்ன?",
        "keywords": ["பயிர்", "நெல்", "விவசாயம்", "உழவன்", "உரம்", "நோய்", "இலை", "crop", "agri", "pm kisan", "grains", "tnau"]
    },
    {
        "id": "hyperlocal_rentals",
        "title_ta": "ஹைப்பர்-லோக்கல் வாடகை & தொழிலாளர்",
        "title_en": "Hyperlocal Rentals & Gig Labor",
        "icon": "🛵",
        "desc_ta": "0% கமிஷன் நேரடி வாடகை: பைக் டாக்சி (₹10/கிமீ), ஆட்டோ, கார், 45HP டிராக்டர், நெல் அறுவடை இயந்திரம், கொத்தனார், பிளம்பர், எலக்ட்ரீஷியன். நேரடி UPI & 4-இலக்க OTP.",
        "sample_cmd": "625214 பைக் வேணும்",
        "keywords": ["பைக்", "ஆட்டோ", "கார்", "டிராக்டர்", "அறுவடை", "கொத்தனார்", "பிளம்பர்", "வாடகை", "bike", "auto", "tractor", "harvester", "mason"]
    },
    {
        "id": "partner_registration",
        "title_ta": "கூட்டாளர்கள் நேரடி சுய-பதிவு",
        "title_en": "Service Partner Self-Registration",
        "icon": "🤝",
        "desc_ta": "ஓட்டுநர்கள், டிராக்டர்/அறுவடை உரிமையாளர்கள், கைவினைஞர்கள், ஆசிரியர்கள் நேரடியாக இலவசமாக பதிவு செய்து வாடிக்கையாளர் முன்பதிவுகளைப் பெறலாம்.",
        "sample_cmd": "பதிவு ஓட்டுநர் ரமேஷ் பைக் 625214 9840112233",
        "keywords": ["பதிவு", "கூட்டாளர்", "சேர", "register", "partner registration", "ஓட்டுநர் பதிவு"]
    },
    {
        "id": "citizen_life_vault",
        "title_ta": "குடிமக்கள் டிஜிட்டல் பெட்டகம்",
        "title_en": "Citizen Sovereign Life Vault",
        "icon": "🏛️",
        "desc_ta": "தினசரி வரவு செலவு கணக்கு, குடும்ப மருத்துவர் தொடர்புகள், ஆதார்/ரேஷன் ஆவணங்கள், குடும்ப பயோ, எதிர்கால திட்டங்கள் & PIN '7890' ரகசிய பெட்டகம்.",
        "sample_cmd": "வரவு ₹15000 நெல் விற்ற பணம்",
        "keywords": ["வரவு", "செலவு", "கணக்கு", "மீதி", "பெட்டகம்", "டைரி", "திட்டம்", "ரகசியம்", "vault", "expense", "income", "secret 7890"]
    },
    {
        "id": "share_market_boto",
        "title_ta": "போடோ குவாண்ட் பங்குச்சந்தை வழிகாட்டி",
        "title_en": "Boto Quant Share Market Guidance",
        "icon": "📈",
        "desc_ta": "நிஃப்டி, பேங்க்நிஃப்டி புட்-கால் ரேஷியோ (PCR), பங்கு தொழில்நுட்ப பகுப்பாய்வு (RSI, SuperTrend, EMA 20/50), SEBI வழிகாட்டுதல் முதலீட்டு குறிப்புகள்.",
        "sample_cmd": "RELIANCE பங்கு நிலவரம் என்ன?",
        "keywords": ["பங்கு", "பங்குச்சந்தை", "நிஃப்டி", "கிரிப்டோ", "nifty", "share", "stock", "boto", "sebi", "fno", "முதலீடு"]
    },
    {
        "id": "daily_news_air",
        "title_ta": "தினசரி காலை செய்திகள் & AIR வானொலி",
        "title_en": "Morning News & AIR Radio Bulletins",
        "icon": "📰",
        "desc_ta": "காலை வணக்கம் சொன்னவுடன்: 10 தமிழ்நாடு செய்திகள் + 5 இந்திய செய்திகள் + 3 சர்வதேச செய்திகள் + அகில இந்திய வானொலி (AIR) தமிழ் செய்தி ஒலி வடிவம்.",
        "sample_cmd": "காலை வணக்கம் இன்றைய செய்திகள்",
        "keywords": ["செய்திகள்", "காலை வணக்கம்", "good morning", "news", "வானொலி", "air audio", "செய்தி"]
    },
    {
        "id": "spoken_english_mental_health",
        "title_ta": "பேச்சு ஆங்கிலம் & மாணவர் மனநலம்",
        "title_en": "Spoken English & Mental Wellbeing",
        "icon": "🗣️",
        "desc_ta": "அன்றாட பேச்சு ஆங்கில பயிற்சி, நேர்காணல் வழிகாட்டல். தேர்வு பயம், மன அழுத்தம் போக்க Tele-MANAS (14416) அரசு ஆலோசனை & சுவாசப் பயிற்சிகள்.",
        "sample_cmd": "English self introduction practice",
        "keywords": ["english", "spoken english", "ஆங்கிலம்", "மன அழுத்தம்", "பயம்", "stress", "counseling", "14416", "tele-manas"]
    },
    {
        "id": "entertainment_posters",
        "title_ta": "பொழுதுபோக்கு & வாழ்த்து போஸ்டர்",
        "title_en": "Entertainment & Civic Posters",
        "icon": "🎬",
        "desc_ta": "சினிமா செய்திகள், தமிழ் பாடல்கள் பரிந்துரை, மற்றும் தலைவர்கள் பிறந்தநாள் / பொங்கல் / தீபாவளி வாழ்த்து போஸ்டர் 1-கிளிக்கில் உருவாக்கம்.",
        "sample_cmd": "விஜய் பிறந்தநாள் வாழ்த்து போஸ்டர்",
        "keywords": ["பாடல்", "பாட்டு", "music", "cinema", "வாழ்த்து", "போஸ்டர்", "greeting", "birthday", "poster"]
    }
]

# -----------------------------------------------------------------------------
# 2. UNIVERSAL SYSTEM PROMPT FOR META AI MODELS
# -----------------------------------------------------------------------------
UNIVERSAL_SYSTEM_PROMPT = """
You are 'SIA' (மக்கள் Agent / Super Intelligent Assistant), the official, authoritative, and compassionate Sovereign Digital Companion for the citizens and families of Tamil Nadu, India.
You operate powered by Meta AI models (Llama 3.3 70B, Muse Spark 1.3, Muse Wonder 1.0, Meta SAM 3.1, SeamlessM4T) running on sovereign infrastructure with 0% data retention.

CORE IDENTITY & ETHOS:
1. You are NOT a passive text chatbot; you are an ACTION AGENT that protects citizens from corruption, eliminates middleman exploitation (இடைத்தரகர் இல்லாத நேரடி சேவை), and provides immediate, practical solutions.
2. Tone: Warm, respectful, colloquial Tamil (எளிய பேச்சுத் தமிழ்) mixed naturally with English / Tanglish as preferred by the user.
3. Every response must be clear, actionable, and structured with:
   📌 எளிய விளக்கம் (Crisp 1-2 sentence solution)
   📋 உடனடி நடவடிக்கை / அடுத்த கட்டம் (Exact single step to take now)
   💰 அரசு கட்டணம் vs இடைத்தரகர் எச்சரிக்கை (Official fee vs zero middleman exploitation)
   🔗 நேரடி இணைப்பு அல்லது SIA கட்டளை (Official portal link or SIA WhatsApp command)

COMPLETE MASTER CAPABILITIES YOU FULLY ORCHESTRATE:
1. CIVIC & REVENUE SCHEMES: Patta mutation (Sub-division ₹60, without sub-division ₹0), EC (₹0 search, ₹30 certified copy), Ration Card (TNePDS ₹0), Kalaignar Magalir Urimai Thogai (KMUT ₹1,000/mo), CMCHIS health cover (₹5 Lakhs), TANGEDCO 100 units free electricity, RTI Section 6(1) (₹10, BPL ₹0), Aadhaar update (₹50 only).
2. MLA & MP GRIEVANCE PETITIONS: Draft official legal petitions from user voice/text into structured PDFs. Instant 1-click forwarder to all 234 TN MLAs and 39 MPs via WhatsApp/Email.
3. SCHOOL TUITION & HOMEWORK: Samacheer Kalvi & CBSE Classes 1 to 12. Step-by-step math solver, science ray diagrams, 10th daily revision questions, teacher assignment guidance.
4. COMPETITIVE EXAMS (CBT) & SKILL CERTIFICATES: NEET, JEE, NDA, TNPSC Group 1/2/4/VAO, UPSC Civil Services, Banking (IBPS/SBI), Railway (RRB). Generate timed CBT online quizzes, instant scores, bilingual explanations, Mermaid study notes, and tamper-proof SVG skill certificates.
5. SMART AGRICULTURE: Leaf disease detection via Meta SAM 3.1 & Modal GPU, TNAU weed and fertilizer norms, Uzhavan/GRAINS subsidies, PM-Kisan (₹6,000/yr), 100% free agricultural power, 70% PM-KUSUM solar subsidy.
6. HYPERLOCAL RENTALS & GIG LABOR: 0% aggregator commission. Bike taxi (₹10/km), auto, cab, omni van, tata ace, 45HP tractor, paddy harvester (₹2,400/hr), drone sprayer (₹450/ac), head mason (₹1,000/day), helper (₹650/day), plumber, electrician, coconut climber. Dispatches with 4-digit security OTP & direct UPI payment link.
7. PARTNER SELF-REGISTRATION: Any driver, machine owner, artisan, or tutor can register directly by sending: "பதிவு ஓட்டுநர் [பெயர்] [வாகனம்] [பின்கோடு] [போன்]".
8. CITIZEN SOVEREIGN LIFE VAULT: Daily In/Outs Ledger, Contacts DB (family doctor, electrician), Proofs DB (Aadhaar, Ration, Patta), Needs tracker & auto-welfare matching, Personal Diary, Plans Board, Family Bio, and PIN '7890' Secret Vault.
9. SHARE MARKET & BOTO QUANT: Nifty/BankNifty spot, PCR ratio, stock analysis (RSI, SuperTrend, EMA 20/50), SEBI risk disclosures, gold loan vs agri loan optimization.
10. DAILY MORNING NEWS & AIR RADIO: Morning briefing with 10 Tamil Nadu + 5 India + 3 World news, and All India Radio (AIR) Tamil audio news bulletin player.
11. SPOKEN ENGLISH & MENTAL HEALTH: Spoken English dialogs, self-introduction, interview practice; Tele-MANAS (14416) stress helpline, exam anxiety relief, 4-7-8 breathing exercises.
12. ENTERTAINMENT & CIVIC POSTERS: Song suggestions, cinema trivia, personalized leader birthday/festival greeting posters.

GROUNDING DIRECTIVE (MANDATORY):
- If the user asks what you can do, show the categorized master menu with sample commands.
- If the user specifies a location/pincode, immediately trigger or guide them to the relevant local service.
- If a user needs help with ANY legal, educational, agricultural, financial, or personal problem, explain the official solution patiently and show them how SIA can execute it for them.
"""

# -----------------------------------------------------------------------------
# 3. MASTER MENU FORMATTER FOR WHATSAPP & WEB
# -----------------------------------------------------------------------------
def format_whatsapp_master_menu() -> Dict[str, Any]:
    """
    Constructs the official SIA Master Services Menu for WhatsApp interactive messaging.
    """
    body_text = (
        "🌟 *வணக்கம்! நான் SIA (மக்கள் AI - Super Intelligent Assistant)*\n"
        "தமிழ்நாடு மக்களுக்கான முழுமையான டிஜிட்டல் உதவியாளர்.\n"
        "இடைத்தரகர் இல்லாத, 0% கமிஷன் கொண்ட அனைத்து சேவைகளும் உங்கள் விரல் நுனியில்!\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🏛️ *SIA முக்கிய சேவைகள் பட்டியல்:*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "1️⃣ *அரசு சேவைகள்:* பட்டா, ரேஷன், ஆதார், RTI, மகளிர் உரிமை\n"
        "2️⃣ *குறைதீர்ப்பு மனு:* MLA / MP-க்கு நேரடி PDF மனு & வாட்ஸ்அப் பகிர்வு\n"
        "3️⃣ *பள்ளி கல்வி:* 1-12 வகுப்பு டியூஷன், ஹோம்வொர்க், வரைபடங்கள்\n"
        "4️⃣ *போட்டித் தேர்வுகள்:* NEET, JEE, TNPSC, UPSC ஆன்லைன் CBT தேர்வு & சான்றிதழ்\n"
        "5️⃣ *டிஜிட்டல் விவசாயம்:* இலை படம் அனுப்பி பயிர் நோய் கண்டறிதல் & உழவன் உதவி\n"
        "6️⃣ *ஹைப்பர்-லோக்கல் வாடகை:* பைக், ஆட்டோ, டிராக்டர், அறுவடை, கொத்தனார் (0% கமிஷன்)\n"
        "7️⃣ *கூட்டாளர் பதிவு:* ஓட்டுநர் & இயந்திர உரிமையாளர்கள் நேரடி பதிவு\n"
        "8️⃣ *மக்கள் பெட்டகம்:* வரவு செலவு கணக்கு & PIN '7890' ரகசிய பெட்டகம்\n"
        "9️⃣ *பங்குச்சந்தை:* போடோ குவாண்ட் நிஃப்டி & முதலீட்டு வழிகாட்டி\n"
        "🔟 *காலை செய்திகள்:* 18 முக்கிய செய்திகள் & AIR வானொலி ஆடியோ\n"
        "1️⃣1️⃣ *பேச்சு ஆங்கிலம் & மனநலம்:* Tele-MANAS 14416 தேர்வு பயம் ஆலோசனை\n"
        "1️⃣2️⃣ *வாழ்த்து போஸ்டர்:* சினிமா & பண்டிகை போஸ்டர் உருவாக்கம்\n1️⃣3️⃣ *வீட்டு உணவு & மெஸ்:* வாழை இலை சாப்பாடு, இட்லி, தோசை (0% கமிஷன்)\n1️⃣4️⃣ *மளிகை & அங்காடி:* பின்கோடு மளிகை கடை, பிக் பாஸ்கெட் போன்ற பொருட்கள் (30 நிமிடம்)\n1️⃣5️⃣ *கடன் & பத்திரங்கள்:* கூட்டுறவு கடன், கந்துவட்டி தடுப்பு (12%-18%), அடமான பத்திரம்\n1️⃣6️⃣ *காயலான் & ஸ்கிராப்:* பழைய இரும்பு, பித்தளை, தாமிரம், பேட்டரிக்கு நேரடி ரொக்கம்\n1️⃣7️⃣ *கால்நடை & தானிய ஏலம்:* உழவர் நேரடி மாடு, ஆடு, நெல் மூட்டை விற்பனை ஏலம்\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 *நீங்கள் செய்ய வேண்டியது:* உங்கள் தேவையை எளிய தமிழில் தட்டச்சு செய்யுங்கள் அல்லது கீழே உள்ள பொத்தானை கிளிக் செய்யுங்கள்!"
    )

    buttons = [
        {"id": "menu_civic", "title": "🏛️ அரசு சேவைகள்"},
        {"id": "menu_rentals", "title": "🛵 பைக் / வாடகை"},
        {"id": "menu_exams", "title": "🎯 மாதிரி தேர்வுகள்"}
    ]

    return {
        "header_text": "🌟 SIA மக்கள் AI — முழு வழிகாட்டி",
        "body_text": body_text,
        "footer_text": "SIA Makkal AI • Meta AI Hackathon 2026",
        "buttons": buttons
    }


def format_text_master_menu() -> str:
    """
    Plain text version of the master menu for standard text replies and web chat.
    """
    menu = format_whatsapp_master_menu()
    sample_cmds = (
        "\n\n💬 *உதாரண கட்டளைகள் (Sample Commands):*\n"
        "• `625214 பைக் வேணும்` — சோழவந்தான் பைக் வாடகை\n"
        "• `613001 நெல் அறுவடை இயந்திரம்` — தஞ்சாவூர் அறுவடை இயந்திரம்\n"
        "• `TNPSC குரூப் 4 மாதிரி தேர்வு` — 5 வினாக்கள் ஆன்லைன் தேர்வு\n"
        "• `வரவு ₹20000 / செலவு ₹450` — வரவு செலவு கணக்கு பதிவு\n"
        "• `ரகசிய பெட்டகம் 7890` — ஆவணப் பெட்டகத்தை திறக்க\n"
        "• `காலை வணக்கம்` — இன்றைய 18 செய்திகள் & AIR செய்தி ஒலி\n"
        "• `பதிவு ஓட்டுநர் பாலு பைக் 625214 9840112233` — ஓட்டுநர் பதிவு\n"
        f"🌐 இணைய தளம்: {PUBLIC_BASE_URL}"
    )
    return menu["body_text"] + sample_cmds


# -----------------------------------------------------------------------------
# 4. INTELLIGENT QUERY TRIAGE & GUIDANCE ENGINE
# -----------------------------------------------------------------------------
def triage_and_guide_user_query(user_query: str, sender_phone: str = "6381029380") -> Dict[str, Any]:
    """
    Intelligently analyzes any user query, detects intent, and returns:
    1. Direct execution instructions or fulfillment
    2. Contextual next-action guidance
    3. Meta AI Model grounded response for open-ended queries
    """
    q_clean = user_query.strip().lower()

    # 1. Greetings & Master Help Menu Trigger
    greeting_keywords = [
        "வணக்கம்", "ஹலோ", "hello", "hi", "help", "உதவி", "சேவைகள்", "services",
        "menu", "மெனு", "வழிகாட்டி", "guide", "என்னென்ன", "what can you do", "options",
        "start", "தொடங்கு", "ஆரம்பி", "விவரம்"
    ]
    if any(q_clean == k or q_clean.startswith(k + " ") or q_clean.endswith(" " + k) for k in greeting_keywords) and len(q_clean.split()) <= 4:
        return {
            "status": "success",
            "type": "master_menu",
            "message": format_text_master_menu(),
            "interactive_menu": format_whatsapp_master_menu(),
            "suggested_actions": [
                {"title": "பைக் வாடகை", "cmd": "625214 பைக் வேணும்"},
                {"title": "போட்டித் தேர்வு", "cmd": "TNPSC மாதிரி தேர்வு"},
                {"title": "வரவு செலவு", "cmd": "என் வரவு செலவு கணக்கு நிலை என்ன?"}
            ]
        }

    # 2. Check matched domain from catalog with specificity scoring
    scored_domains = []
    for s in SIA_MASTER_SERVICES:
        score = 0
        for kw in s["keywords"]:
            if kw in q_clean:
                score += len(kw) * 2
        if score > 0:
            scored_domains.append((score, s))

    scored_domains.sort(key=lambda x: x[0], reverse=True)
    matched_domain = scored_domains[0][1] if scored_domains else None

    # If domain matched, generate authoritative guided action
    if matched_domain:
        domain_id = matched_domain["id"]
        guidance_text = (
            f"{matched_domain['icon']} *SIA {matched_domain['title_ta']} வழிகாட்டி*\n\n"
            f"📌 *சேவை விளக்கம்:* {matched_domain['desc_ta']}\n\n"
            f"🚀 *உடனடி நடவடிக்கை (Next Action):*\n"
            f"கீழ்க்கண்டவாறு செய்தி அனுப்பவும்:\n"
            f"👉 `{matched_domain['sample_cmd']}`\n\n"
            f"🌐 இணையதளம் மூலம் பயன்படுத்த: {PUBLIC_BASE_URL}"
        )
        return {
            "status": "success",
            "type": "domain_guidance",
            "domain_id": domain_id,
            "domain_title": matched_domain["title_ta"],
            "message": guidance_text,
            "sample_cmd": matched_domain["sample_cmd"]
        }

    # 3. Open-ended query -> Route to Meta AI model with Universal Grounding
    from meta_client import meta_client, DEFAULT_CHAT_MODEL
    
    messages = [
        {"role": "system", "content": UNIVERSAL_SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    try:
        # First attempt via Baseten Open-Weight or Chat Completion
        res = meta_client.chat_completion(messages=messages, model=DEFAULT_CHAT_MODEL)
        ai_reply = res.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        logger.warning(f"Meta chat completion fallback: {e}")
        ai_reply = (
            "வணக்கம்! உங்கள் கேள்வியை SIA முழுமையாக புரிந்துகொண்டது. "
            "தமிழ்நாடு அரசு மற்றும் மக்கள் சேவைகளில் உங்களுக்கு உதவ நான் தயாராக உள்ளேன். "
            "தங்கள் தேவையை மேலும் விளக்கமாக அல்லது பின்கோடுடன் அனுப்பவும்."
        )

    ai_reply_with_footer = (
        f"{ai_reply}\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 *SIA மக்கள் AI:* உதவி தேவைப்படின் எந்நேரமும் `உதவி` அல்லது `சேவைகள்` என அனுப்பவும்.\n"
        f"🌐 இணைய முகப்பு: {PUBLIC_BASE_URL}"
    )

    return {
        "status": "success",
        "type": "meta_ai_counsel",
        "message": ai_reply_with_footer
    }

# Global singleton
universal_assistant = {
    "catalog": SIA_MASTER_SERVICES,
    "system_prompt": UNIVERSAL_SYSTEM_PROMPT,
    "triage": triage_and_guide_user_query,
    "format_master_menu": format_whatsapp_master_menu,
    "format_text_menu": format_text_master_menu
}
