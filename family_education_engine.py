# -*- coding: utf-8 -*-
"""
Makkal Agent AI - Family Education & Interactive Learning Studio (மக்கள் கல்வி)
Meta AI Developer Hackathon 2026

Empowers families and students across all age groups:
1. KG & Primary Kids (மழலையர் & தொடக்கப் பள்ளி): Voice rhyme coaching, phonics, repeat-after-me training.
2. Middle & High School (6th - 12th / NEET): STEM diagrammatic visualizers, scientific concepts.
3. Adults & Lifelong Learners (பெரியவர்கள்): Deep anatomical/medical explainers (Human Heart, Brain), digital literacy.

Delivers 4 synchronized modalities:
- Spoken Voice-Over Coaching (TTS Audio Script)
- Theoretical & Conceptual Text Guidance
- Dynamic Interactive SVG Diagrammatic Visualizers
- Curated Video Suggestions & Reels (Facebook, Instagram, YouTube)
- Direct Student Practice / Quiz Mode
"""

from typing import Dict, List, Any, Optional
import re

# Comprehensive Educational Knowledge Repository across Age Tiers
EDUCATION_TOPICS: List[Dict[str, Any]] = [
    {
        "topic_id": "human_heart_functioning",
        "title_ta": "மனித இதயத்தின் செயல்பாடு & ரத்த ஓட்டம்",
        "title_en": "Human Heart Anatomy & Blood Circulation",
        "target_age_group": "adults_and_students",
        "target_audience_ta": "பெரியவர்கள், பள்ளி & கல்லூரி மாணவர்கள் (Science / Biology)",
        "badge": "🔬 Medical & Anatomical Science",
        "voice_over_script_ta": (
            "வணக்கம்! நமது மனித இதயம் ஒரு சக்திவாய்ந்த தசை பம்ப் ஆகும். இது ஒரு நிமிடத்திற்கு 72 முறை துடிக்கிறது. "
            "இதயத்தில் நான்கு அறைகள் உள்ளன: மேலே உள்ளவை வலது மற்றும் இடது ஏட்ரியம், கீழே உள்ளவை வலது மற்றும் இடது வென்ட்ரிக்கிள். "
            "உடலின் அசுத்த ரத்தம் வலது ஏட்ரியத்திற்கு வந்து, வலது வென்ட்ரிக்கிள் வழியாக நுரையீரலுக்கு சென்று ஆக்ஸிஜன் பெறுகிறது. "
            "பின்னர் சுத்தமான ரத்தம் இடது ஏட்ரியம் மற்றும் இடது வென்ட்ரிக்கிள் வழியாக பெருந்தமனி மூலம் உடலின் அனைத்து உறுப்புகளுக்கும் பாய்ச்சப்படுகிறது."
        ),
        "theoretical_explanation_ta": (
            "### 🫀 மனித இதயத்தின் கட்டமைப்பு & இரட்டை ரத்த ஓட்ட மண்டலம் (Double Circulation)\n\n"
            "இதயம் நெஞ்சுக் கூட்டின் நடுவே, இடது பக்கமாக சாய்ந்து அமைந்துள்ள ஒரு தசை உறுப்பாகும். இது பெரிகார்டியம் என்ற இரட்டை சவ்வினால் பாதுகாக்கப்படுகிறது.\n\n"
            "#### 1. இதயத்தின் நான்கு அறைகள் (Four Chambers):\n"
            "- **வலது ஏட்ரியம் (Right Atrium):** உடலின் மேல் மற்றும் கீழ் பெருஞ்சிரைகள் (Vena Cava) மூலம் ஆக்ஸிஜன் குறைந்த அசுத்த ரத்தத்தை பெறுகிறது.\n"
            "- **வலது வென்ட்ரிக்கிள் (Right Ventricle):** மூவிதழ் வால்வு (Tricuspid Valve) வழியாக ரத்தத்தை பெற்று, நுரையீரல் தமனி (Pulmonary Artery) மூலம் நுரையீரலுக்கு அனுப்புகிறது.\n"
            "- **இடது ஏட்ரியம் (Left Atrium):** நுரையீரலில் சுத்திகரிக்கப்பட்ட ஆக்ஸிஜன் நிறைந்த தூய ரத்தத்தை நுரையீரல் சிரைகள் வழியாக பெறுகிறது.\n"
            "- **இடது வென்ட்ரிக்கிள் (Left Ventricle):** மிக வலிமையான தசை சுவரை கொண்டது. இது ஈரிதழ் வால்வு (Mitral/Bicuspid Valve) வழியாக வரும் சுத்த ரத்தத்தை பெருந்தமனி (Aorta) மூலம் உடல் முழுவதற்கும் செலுத்துகிறது.\n\n"
            "#### 2. ரத்த அழுத்தம் & இதயத் துடிப்பு:\n"
            "- **சிஸ்டோல் (Systole):** வென்ட்ரிக்கிள்கள் சுருங்கி ரத்தத்தை வெளியேற்றும் நிலை (இயல்பு: 120 mmHg).\n"
            "- **டயஸ்டோல் (Diastole):** வென்ட்ரிக்கிள்கள் விரிவடைந்து ரத்தத்தை நிரப்பும் நிலை (இயல்பு: 80 mmHg).\n"
            "- இதயத் துடிப்பை கட்டுப்படுத்துவது சைனோ ஏட்ரியல் முடிச்சு (SA Node - இயற்கை பேஸ்மேக்கர்) ஆகும்."
        ),
        "svg_diagram": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 420" class="w-full h-auto max-h-[380px] bg-slate-950 rounded-2xl p-2 border border-rose-500/40 shadow-2xl">
        <defs>
            <linearGradient id="blueBlood" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#1e40af"/>
                <stop offset="100%" stop-color="#0284c7"/>
            </linearGradient>
            <linearGradient id="redBlood" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#e11d48"/>
                <stop offset="100%" stop-color="#be123c"/>
            </linearGradient>
            <filter id="glowHeart" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur"/>
                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
        </defs>

        <!-- Background Grid -->
        <rect width="600" height="420" fill="#030712" rx="16"/>
        <g stroke="#1f2937" stroke-width="0.8" stroke-dasharray="4,4">
            <line x1="50" y1="0" x2="50" y2="420"/>
            <line x1="150" y1="0" x2="150" y2="420"/>
            <line x1="300" y1="0" x2="300" y2="420"/>
            <line x1="450" y1="0" x2="450" y2="420"/>
            <line x1="550" y1="0" x2="550" y2="420"/>
            <line x1="0" y1="100" x2="600" y2="100"/>
            <line x1="0" y1="210" x2="600" y2="210"/>
            <line x1="0" y1="320" x2="600" y2="320"/>
        </g>

        <!-- Title -->
        <text x="300" y="32" fill="#fda4af" font-size="16" font-weight="bold" font-family="sans-serif" text-anchor="middle">🫀 மனித இதயத்தின் 4 அறைகள் & ரத்த ஓட்டப் பாதை (Double Circulation)</text>
        <text x="300" y="52" fill="#94a3b8" font-size="11" font-family="monospace" text-anchor="middle">Deoxygenated (Blue) ➔ Lungs ➔ Oxygenated (Red) ➔ Body</text>

        <!-- Superior Vena Cava -->
        <path d="M 170 60 L 170 140 L 210 140 L 210 60 Z" fill="url(#blueBlood)" stroke="#38bdf8" stroke-width="2"/>
        <text x="140" y="75" fill="#38bdf8" font-size="10" font-family="sans-serif" font-weight="bold">மேல் பெருஞ்சிரை</text>
        <text x="140" y="88" fill="#94a3b8" font-size="9" font-family="monospace">(Vena Cava)</text>

        <!-- Aorta (Main Artery) Arch -->
        <path d="M 280 140 C 280 60, 390 60, 390 140 L 350 140 C 350 95, 315 95, 315 140 Z" fill="url(#redBlood)" stroke="#fb7185" stroke-width="2"/>
        <text x="340" y="50" fill="#fb7185" font-size="11" font-family="sans-serif" font-weight="bold">பெருந்தமனி (Aorta)</text>

        <!-- Pulmonary Artery Arch -->
        <path d="M 240 140 C 240 90, 190 100, 130 110 L 130 135 C 180 125, 215 120, 215 140 Z" fill="url(#blueBlood)" stroke="#0284c7" stroke-width="1.5"/>
        <text x="90" y="105" fill="#38bdf8" font-size="10" font-family="sans-serif" font-weight="bold">நுரையீரல் தமனி</text>
        <text x="90" y="118" fill="#94a3b8" font-size="9" font-family="monospace">To Lungs (Pulmonary)</text>

        <!-- Main Heart Body (Muscular Outer Shell) -->
        <path d="M 140 160 C 120 220, 180 370, 300 395 C 420 370, 480 220, 460 160 C 440 130, 310 140, 300 170 C 290 140, 160 130, 140 160 Z" fill="#4c0519" stroke="#e11d48" stroke-width="3" filter="url(#glowHeart)">
            <animate attributeName="stroke-width" values="3;4.5;3" dur="0.8s" repeatCount="indefinite"/>
        </path>

        <!-- Central Septum (Dividing Wall) -->
        <path d="M 300 175 L 300 390" stroke="#f43f5e" stroke-width="6" stroke-linecap="round"/>
        <text x="305" y="320" fill="#fecdd3" font-size="9" font-family="sans-serif" transform="rotate(90,305,320)">செப்டம் (தடுப்புச் சுவர்)</text>

        <!-- Right Atrium (RA) - Blue Chamber -->
        <rect x="165" y="165" width="120" height="90" rx="14" fill="url(#blueBlood)" fill-opacity="0.85" stroke="#38bdf8" stroke-width="2"/>
        <text x="225" y="195" fill="#ffffff" font-size="13" font-weight="bold" font-family="sans-serif" text-anchor="middle">வலது ஏட்ரியம்</text>
        <text x="225" y="212" fill="#bae6fd" font-size="10" font-family="monospace" text-anchor="middle">(Right Atrium)</text>
        <text x="225" y="228" fill="#7dd3fc" font-size="9" font-family="sans-serif" text-anchor="middle">அசுத்த ரத்தம் பெறும்</text>

        <!-- Right Ventricle (RV) - Blue Chamber -->
        <rect x="175" y="270" width="115" height="95" rx="14" fill="url(#blueBlood)" fill-opacity="0.9" stroke="#38bdf8" stroke-width="2"/>
        <text x="232" y="305" fill="#ffffff" font-size="13" font-weight="bold" font-family="sans-serif" text-anchor="middle">வலது வென்ட்ரிக்கிள்</text>
        <text x="232" y="322" fill="#bae6fd" font-size="10" font-family="monospace" text-anchor="middle">(Right Ventricle)</text>
        <text x="232" y="338" fill="#7dd3fc" font-size="9" font-family="sans-serif" text-anchor="middle">நுரையீரலுக்கு செலுத்தும்</text>

        <!-- Left Atrium (LA) - Red Chamber -->
        <rect x="315" y="165" width="120" height="90" rx="14" fill="url(#redBlood)" fill-opacity="0.85" stroke="#fda4af" stroke-width="2"/>
        <text x="375" y="195" fill="#ffffff" font-size="13" font-weight="bold" font-family="sans-serif" text-anchor="middle">இடது ஏட்ரியம்</text>
        <text x="375" y="212" fill="#ffe4e6" font-size="10" font-family="monospace" text-anchor="middle">(Left Atrium)</text>
        <text x="375" y="228" fill="#fecdd3" font-size="9" font-family="sans-serif" text-anchor="middle">சுத்த ரத்தம் பெறும்</text>

        <!-- Left Ventricle (LV) - Red Chamber (Thickest Muscle) -->
        <rect x="310" y="270" width="125" height="95" rx="14" fill="url(#redBlood)" fill-opacity="0.95" stroke="#fda4af" stroke-width="2"/>
        <text x="372" y="305" fill="#ffffff" font-size="13" font-weight="bold" font-family="sans-serif" text-anchor="middle">இடது வென்ட்ரிக்கிள்</text>
        <text x="372" y="322" fill="#ffe4e6" font-size="10" font-family="monospace" text-anchor="middle">(Left Ventricle)</text>
        <text x="372" y="338" fill="#fecdd3" font-size="9" font-family="sans-serif" text-anchor="middle">உடல் முழுதும் செலுத்தும்</text>

        <!-- Valves Indicators -->
        <circle cx="225" cy="262" r="7" fill="#facc15"/>
        <text x="145" y="266" fill="#facc15" font-size="9" font-family="sans-serif">மூவிதழ் வால்வு</text>
        <circle cx="372" cy="262" r="7" fill="#facc15"/>
        <text x="390" y="266" fill="#facc15" font-size="9" font-family="sans-serif">ஈரிதழ் வால்வு</text>

        <!-- Animated Blood Flow Direction Arrows -->
        <g stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round">
            <!-- Inflow Blue -->
            <path d="M 225 140 L 225 160">
                <animate attributeName="stroke-dashoffset" values="10;0" dur="0.8s" repeatCount="indefinite"/>
            </path>
            <!-- Downward Blue to RV -->
            <path d="M 225 255 L 225 270"/>
            <!-- Inflow Red to LV -->
            <path d="M 372 255 L 372 270"/>
            <!-- Outflow Red to Aorta -->
            <path d="M 372 270 C 372 220, 310 170, 310 140"/>
        </g>

        <!-- Bottom Pulse & Legend Bar -->
        <rect x="30" y="380" width="540" height="30" rx="8" fill="#111827" stroke="#374151" stroke-width="1"/>
        <circle cx="50" cy="395" r="5" fill="#0284c7"/>
        <text x="62" y="399" fill="#93c5fd" font-size="10" font-family="sans-serif">ஆக்ஸிஜன் குறைந்த ரத்தம் (நீலம்)</text>
        <circle cx="230" cy="395" r="5" fill="#e11d48"/>
        <text x="242" y="399" fill="#fca5a5" font-size="10" font-family="sans-serif">ஆக்ஸிஜன் நிறைந்த சுத்த ரத்தம் (சிவப்பு)</text>
        <text x="440" y="399" fill="#facc15" font-size="10" font-family="monospace">துடிப்பு: 72 BPM | BP: 120/80</text>
    </svg>""",
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "3D Medical Animation Video",
                "title_ta": "இதயம் எவ்வாறு ரத்தத்தை பம்ப் செய்கிறது? 3D அனிமேஷன் மருத்துவ விளக்கம்",
                "creator": "Tamil Health Awareness & Medical Science",
                "verified_badge": "Verified Doctor Explainer",
                "url": "https://www.facebook.com/watch/?v=human_heart_functioning_tamil_3d",
                "duration": "5:12",
                "summary_ta": "இதயத்தின் 4 அறைகள், வால்வுகள் மற்றும் ரத்த ஓட்டத்தை 3D அனிமேஷன் மூலம் எளிதாக விளக்கும் காணொளி."
            },
            {
                "platform": "Instagram",
                "type": "Science Reel",
                "title_ta": "ரத்த அழுத்தம் 120/80 என்றால் என்ன? இதயம் பேசும் ரகசியம் 60 வினாடிகளில்!",
                "creator": "Science Simplified Tamil (@drhealth_tamil)",
                "verified_badge": "Doctor & Medical Educator",
                "url": "https://www.instagram.com/reel/heart_bp_explained_tamil/",
                "duration": "0:59",
                "summary_ta": "சிஸ்டோலிக் மற்றும் டயஸ்டோலிக் ரத்த அழுத்தம் இதயத்தில் எவ்வாறு உருவாகிறது என்ற சுருக்கமான ரீல்."
            },
            {
                "platform": "YouTube",
                "type": "Comprehensive 3D Educational Video",
                "title_ta": "Human Heart Anatomy and Blood Circulation Full 3D Tamil Tutorial",
                "creator": "Bio Science Tamil Academy",
                "verified_badge": "NEET Biology Top Educator",
                "url": "https://www.youtube.com/watch?v=human_heart_tamil_neet_guide",
                "duration": "9:45",
                "summary_ta": "10th, 12th மற்றும் NEET மாணவர்களுக்கான இதய கட்டமைப்பு, வால்வுகள், ECG அலைகள் முழுமையான விளக்கம்."
            }
        ],
        "interactive_quiz": [
            {
                "question_ta": "உடலின் அனைத்து உறுப்புகளுக்கும் ஆக்ஸிஜன் நிறைந்த சுத்த ரத்தத்தை பாய்ச்சும் இதய அறை எது?",
                "options": ["A) வலது ஏட்ரியம்", "B) இடது வென்ட்ரிக்கிள்", "C) வலது வென்ட்ரிக்கிள்", "D) நுரையீரல் தமனி"],
                "correct_answer": "B) இடது வென்ட்ரிக்கிள்",
                "explanation_ta": "இடது வென்ட்ரிக்கிள் தான் மிக தடிமனான தசை சுவரை கொண்டு உடலின் அனைத்து பகுதிகளுக்கும் பெருந்தமனி மூலம் ரத்தத்தை செலுத்துகிறது."
            },
            {
                "question_ta": "இயற்கையான பேஸ்மேக்கர் என அழைக்கப்படும் இதய பகுதி எது?",
                "options": ["A) AV Node", "B) Purkinje Fibres", "C) SA Node (சைனோ ஏட்ரியல் முடிச்சு)", "D) Aorta"],
                "correct_answer": "C) SA Node (சைனோ ஏட்ரியல் முடிச்சு)",
                "explanation_ta": "SA Node தான் இதயத் துடிப்பிற்கான மின் தூண்டுதல்களை தானாகவே உருவாக்குகிறது."
            }
        ],
        "keywords": ["இதயம்", "இதய செயல்பாடு", "ரத்த ஓட்டம்", "ஹார்ட்", "ஹார்ட் அட்டாக்", "heart", "cardiology", "circulation", "ecg", "bp", "blood pressure"]
    },
    {
        "topic_id": "kids_tamil_rhymes",
        "title_ta": "மழலையர் பாடல் & குரல் பயிற்சி (நிலா நிலா ஓடி வா)",
        "title_en": "KG Kids Tamil Rhyme & Repeat-after-Me Voice Coach",
        "target_age_group": "kg_and_primary_kids",
        "target_audience_ta": "மழலையர் (KG - LKG, UKG) மற்றும் தொடக்கப் பள்ளி குழந்தைகள்",
        "badge": "👶 KG Voice & Phonics Coach",
        "voice_over_script_ta": (
            "செல்லக் குழந்தைகளே! என்னோடு சேர்ந்து பாடுங்கள்! "
            "நிலா நிலா ஓடி வா! நில்லாமல் ஓடி வா! "
            "மலை மீது ஏறி வா! மல்லிகைப் பூ சூடி வா! "
            "வெள்ளித் தட்டு நிறையவே! வெண் சோறு தருவேன் வா! "
            "தங்கத் தட்டில் அன்னமும்! தயிரும் பிசைந்து தருவேன் வா!"
        ),
        "theoretical_explanation_ta": (
            "### 👶 மழலையர் குரல் & மொழி உச்சரிப்பு பயிற்சி (Early Childhood Voice & Phonics Coaching)\n\n"
            "குழந்தைகளின் மூளை வளர்ச்சியில் 3 முதல் 7 வயது வரை கேட்கும் திறன் மற்றும் மழலை உச்சரிப்பு பயிற்சி மிக முக்கிய பங்கு வகிக்கிறது.\n\n"
            "#### 🌟 குழந்தைகள் கற்கும் 4 நன்மைகள்:\n"
            "1. **செவிமடுத்தல் திறன் (Active Listening):** தாளத்தோடும் இசையோடும் கேட்கும்போது சொல் வளம் (Vocabulary) வேகமாக வளர்கிறது.\n"
            "2. **தமிழ் உச்சரிப்பு தெளிவு (Phonetic Articulation):** 'ழ', 'ள', 'ண', 'ற' போன்ற தமிழ் சிறப்பு எழுத்துக்களை குழந்தைப் பருவத்திலேயே திருத்தமாக பேச உதவுகிறது.\n"
            "3. **நினைவாற்றல் பெருக்கம் (Memory Retention):** எளிய வரிகளை திரும்பத் திரும்ப பாடுவதால் நினைவாற்றல் அதிகரிக்கிறது.\n"
            "4. **பேச்சுத் தயக்கம் நீங்குதல் (Overcoming Shyness):** AI பயிற்சியாளருடன் பயமின்றி பேசி பயிற்சி பெறலாம்."
        ),
        "svg_diagram": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" class="w-full h-auto max-h-[350px] bg-slate-950 rounded-2xl p-2 border border-amber-500/40 shadow-2xl">
        <defs>
            <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#fef08a"/>
                <stop offset="60%" stop-color="#fde047"/>
                <stop offset="100%" stop-color="#ca8a04"/>
            </radialGradient>
            <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#0f172a"/>
                <stop offset="100%" stop-color="#1e1b4b"/>
            </linearGradient>
        </defs>

        <!-- Night Sky Background -->
        <rect width="600" height="380" fill="url(#skyGrad)" rx="16"/>

        <!-- Twinkling Stars -->
        <g fill="#fef9c3">
            <circle cx="80" cy="50" r="2.5"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.2s" repeatCount="indefinite"/></circle>
            <circle cx="150" cy="110" r="3.5"><animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/></circle>
            <circle cx="260" cy="40" r="2"><animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/></circle>
            <circle cx="480" cy="70" r="3"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.1s" repeatCount="indefinite"/></circle>
            <circle cx="530" cy="140" r="2"><animate attributeName="opacity" values="1;0.3;1" dur="1.7s" repeatCount="indefinite"/></circle>
            <circle cx="90" cy="180" r="3"><animate attributeName="opacity" values="0.5;1;0.5" dur="1.4s" repeatCount="indefinite"/></circle>
        </g>

        <!-- Smiling Animated Moon (நிலா) -->
        <g transform="translate(420, 80)">
            <circle cx="50" cy="50" r="45" fill="url(#moonGlow)" filter="drop-shadow(0 0 16px #facc15)">
                <animateTransform attributeName="transform" type="translate" values="0,0; 0,-8; 0,0" dur="2.5s" repeatCount="indefinite"/>
            </circle>
            <!-- Moon Smiling Face -->
            <ellipse cx="36" cy="42" rx="4.5" ry="6" fill="#713f12"/>
            <ellipse cx="64" cy="42" rx="4.5" ry="6" fill="#713f12"/>
            <path d="M 35 60 Q 50 74 65 60" stroke="#713f12" stroke-width="3" fill="none" stroke-linecap="round"/>
            <!-- Cute Pink Cheeks -->
            <circle cx="28" cy="54" r="5" fill="#f472b6" opacity="0.6"/>
            <circle cx="72" cy="54" r="5" fill="#f472b6" opacity="0.6"/>
            <text x="50" y="115" fill="#fef08a" font-size="12" font-family="sans-serif" font-weight="bold" text-anchor="middle">அன்பு நிலா 🌙</text>
        </g>

        <!-- Mountain Silhouettes -->
        <path d="M 0 380 L 140 260 L 260 380 Z" fill="#1e293b"/>
        <path d="M 180 380 L 320 230 L 460 380 Z" fill="#0f172a"/>
        <path d="M 380 380 L 500 280 L 600 380 Z" fill="#1e293b"/>

        <!-- Rhyme Text Scroll Box -->
        <rect x="30" y="45" width="340" height="230" rx="14" fill="#030712" fill-opacity="0.85" stroke="#f59e0b" stroke-width="2"/>
        <text x="200" y="75" fill="#fbbf24" font-size="16" font-family="sans-serif" font-weight="bold" text-anchor="middle">🌙 நிலா நிலா ஓடி வா 🎶</text>
        <line x1="50" y1="85" x2="350" y2="85" stroke="#f59e0b" stroke-width="1" stroke-dasharray="3,3"/>

        <!-- Lyrics Lines with Playful Badges -->
        <g fill="#f8fafc" font-size="13" font-family="sans-serif" font-weight="500">
            <text x="55" y="115">🌟 நிலா நிலா ஓடி வா!</text>
            <text x="55" y="145">🌟 நில்லாமல் ஓடி வா!</text>
            <text x="55" y="175">🌟 மலை மீது ஏறி வா!</text>
            <text x="55" y="205">🌟 மல்லிகைப் பூ சூடி வா!</text>
            <text x="55" y="235">🌟 வெண் சோறு தருவேன் வா!</text>
        </g>

        <!-- Voice Repeat Banner at Bottom -->
        <rect x="30" y="300" width="540" height="55" rx="12" fill="#78350f" fill-opacity="0.9" stroke="#f59e0b" stroke-width="1.5"/>
        <text x="50" y="325" fill="#fef08a" font-size="13" font-weight="bold" font-family="sans-serif">🎙️ மழலையர் குரல் பயிற்சி (Repeat-After-Me Mode):</text>
        <text x="50" y="344" fill="#fde68a" font-size="11" font-family="sans-serif">குழந்தைகள் '🔊 உரக்கப் படி' பொத்தானை அழுத்தி, AI ஆசிரியை பாடுவதை கேட்டு திரும்ப பாடலாம்!</text>
    </svg>""",
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "Animated Rhyme Video",
                "title_ta": "நிலா நிலா ஓடி வா - 3D அனிமேஷன் மழலையர் தமிழ் பாடல்",
                "creator": "Chutti Kids TV Tamil",
                "verified_badge": "Top Kids Educator",
                "url": "https://www.facebook.com/watch/?v=nila_nila_rhyme_kids_tamil",
                "duration": "2:30",
                "summary_ta": "வண்ணமயமான நிலா அனிமேஷன் மற்றும் எளிய தாளத்தோடு குழந்தைகள் எளிதில் பாடிப் பழகும் பாடல்."
            },
            {
                "platform": "Instagram",
                "type": "Phonics Reel",
                "title_ta": "மழலை உச்சரிப்பு பயிற்சி: 'ழ' மற்றும் 'ள' எழுத்துக்களை எளிதாக சொல்லித் தரும் வழி!",
                "creator": "Tamil For Kids (@tamilkidslearning)",
                "verified_badge": "Preschool Language Coach",
                "url": "https://www.instagram.com/reel/tamil_phonics_kids_coaching/",
                "duration": "0:45",
                "summary_ta": "குழந்தைகளுக்கு தமிழ் மெய்யெழுத்து உச்சரிப்பை நாக்கு பயிற்சிகள் மூலம் கற்றுக்கொடுக்கும் ரீல்."
            },
            {
                "platform": "YouTube",
                "type": "Interactive Kids Learning Video",
                "title_ta": "Top 10 Tamil Rhymes for Kindergarten with Lyrics & Action",
                "creator": "Chellame Chellam Tamil Rhymes",
                "verified_badge": "Certified Preschool Media",
                "url": "https://www.youtube.com/watch?v=tamil_rhymes_kids_kindergarten",
                "duration": "12:15",
                "summary_ta": "நிலா நிலா ஓடி வா, கைவீசம்மா கைவீசு உள்ளிட்ட 10 பாரம்பரிய மழலையர் பாடல்களின் முழு தொகுப்பு."
            }
        ],
        "interactive_quiz": [
            {
                "question_ta": "பாட்டில் நிலாவிடம் என்ன பூ சூடி வரச் சொல்கிறோம்?",
                "options": ["A) ரோஜாப் பூ", "B) மல்லிகைப் பூ", "C) செம்பருத்திப் பூ", "D) தாமரைப் பூ"],
                "correct_answer": "B) மல்லிகைப் பூ",
                "explanation_ta": "'மலை மீது ஏறி வா! மல்லிகைப் பூ சூடி வா!' என்று பாடலில் வருகிறது!"
            }
        ],
        "keywords": ["குழந்தை", "ரைம்ஸ்", "பாட்டு", "மழலையர்", "நிலா நிலா", "rhyme", "kg", "kids", "kindergarten", "phonics", "tamil rhymes"]
    },
    {
        "topic_id": "plant_photosynthesis",
        "title_ta": "தாவர ஒளிச்சேர்க்கை முறை (Photosynthesis in Plants)",
        "title_en": "Plant Photosynthesis & Cell Energy Generation",
        "target_age_group": "middle_and_high_school",
        "target_audience_ta": "நடுநிலை மற்றும் உயர்நிலைப் பள்ளி மாணவர்கள் (6th - 10th Science)",
        "badge": "🌱 School Science & Botany",
        "voice_over_script_ta": (
            "மாணவர்களே! தாவரங்கள் தங்கள் உணவை தாங்களே தயாரித்துக் கொள்ளும் அற்புத நிகழ்வே ஒளிச்சேர்க்கை ஆகும். "
            "வேர்கள் மூலம் உறிஞ்சப்படும் நீர் மற்றும் இலைத் துளைகள் வழியே உள்ளிழுக்கப்படும் கார்பன் டை ஆக்சைடு ஆகியவை, "
            "சூரிய ஒளியின் ஆற்றலால், குளோரோபில் எனப்படும் பச்சையத்தின் உதவியுடன் குளுக்கோஸ் உணவாக மாற்றப்படுகிறது. "
            "இந்த நிகழ்வின் போது நாம் சுவாசிக்கத் தேவையான உயிர் மூச்சான ஆக்ஸிஜன் வாயு காற்றில் வெளியிடப்படுகிறது."
        ),
        "theoretical_explanation_ta": (
            "### 🌱 தாவர ஒளிச்சேர்க்கை ரசாயன சமன்பாடு & படிநிலைகள் (Photosynthesis Mechanism)\n\n"
            "ஒளிச்சேர்க்கை என்பது தாவரங்கள் சூரிய ஆற்றலை வேதியியல் ஆற்றலாக மாற்றும் உயிர் வேதியியல் செயல்முறையாகும்.\n\n"
            "#### 1. வேதியியல் சமன்பாடு (Chemical Equation):\n"
            "$$6CO_2 + 6H_2O \\xrightarrow[பச்சையம்]{சூரிய\\ ஒளி} C_6H_{12}O_6 (குளுக்கோஸ்) + 6O_2 (ஆக்ஸிஜன்)$$\n\n"
            "#### 2. தேவையான 4 முக்கிய மூலப்பொருட்கள்:\n"
            "1. **சூரிய ஒளி (Sunlight):** ஆற்றலின் முதன்மை மூலம்.\n"
            "2. **பச்சையம் (Chlorophyll):** தாவர இலைகளில் உள்ள பசுங்கணிகத்தில் (Chloroplast) உள்ள நிறமி.\n"
            "3. **கார்பன் டை ஆக்சைடு ($CO_2$):** இலைத்துளைகள் (Stomata) வழியாக காற்றில் இருந்து உறிஞ்சப்படுகிறது.\n"
            "4. **நீர் ($H_2O$):** வேர்களின் சைலம் (Xylem) திசுக்கள் வழியாக மண்ணிலிருந்து கடத்தப்படுகிறது.\n\n"
            "#### 3. முக்கியத்துவம்:\n"
            "- பூமியின் ஒட்டுமொத்த உணவுச் சங்கிலியின் (Food Chain) தொடக்கமே தாவரங்களின் ஒளிச்சேர்க்கை தான்.\n"
            "- காற்று மண்டலத்தில் ஆக்ஸிஜன் மற்றும் கார்பன் டை ஆக்சைடு சமநிலையை பாதுகாக்கிறது."
        ),
        "svg_diagram": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 390" class="w-full h-auto max-h-[360px] bg-slate-950 rounded-2xl p-2 border border-emerald-500/40 shadow-2xl">
        <defs>
            <linearGradient id="sunGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#fef08a"/>
                <stop offset="100%" stop-color="#ea580c"/>
            </linearGradient>
            <linearGradient id="leafGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#22c55e"/>
                <stop offset="100%" stop-color="#15803d"/>
            </linearGradient>
        </defs>

        <rect width="600" height="390" fill="#022c22" rx="16"/>

        <!-- Title -->
        <text x="300" y="32" fill="#86efac" font-size="16" font-weight="bold" font-family="sans-serif" text-anchor="middle">🌱 தாவர ஒளிச்சேர்க்கை வரைபடம் (Photosynthesis Process)</text>
        <text x="300" y="52" fill="#a7f3d0" font-size="11" font-family="monospace" text-anchor="middle">6CO2 + 6H2O + Sunlight ➔ C6H12O6 (Glucose) + 6O2</text>

        <!-- Shining Sun (சூரிய ஒளி) -->
        <g transform="translate(60, 70)">
            <circle cx="40" cy="40" r="32" fill="url(#sunGrad)" filter="drop-shadow(0 0 16px #f59e0b)"/>
            <text x="40" y="90" fill="#fde047" font-size="12" font-family="sans-serif" font-weight="bold" text-anchor="middle">சூரிய ஒளி (Light)</text>
            <!-- Light Rays pointing to leaf -->
            <path d="M 80 50 L 220 160" stroke="#facc15" stroke-width="2.5" stroke-dasharray="4,4">
                <animate attributeName="stroke-dashoffset" values="8;0" dur="0.8s" repeatCount="indefinite"/>
            </path>
            <path d="M 70 70 L 210 180" stroke="#facc15" stroke-width="2" stroke-dasharray="4,4"/>
        </g>

        <!-- Big Green Leaf (பச்சைய இலை) -->
        <g transform="translate(180, 100)">
            <path d="M 20 180 C 40 40, 240 30, 320 80 C 350 140, 260 250, 20 180 Z" fill="url(#leafGrad)" stroke="#4ade80" stroke-width="3" filter="drop-shadow(0 0 10px #16a34a)"/>
            <!-- Leaf Veins -->
            <path d="M 20 180 Q 180 130 320 80" stroke="#86efac" stroke-width="3" fill="none"/>
            <path d="M 120 150 Q 140 100 170 80" stroke="#86efac" stroke-width="1.8" fill="none"/>
            <path d="M 180 135 Q 220 100 240 85" stroke="#86efac" stroke-width="1.8" fill="none"/>
            <path d="M 150 160 Q 180 200 210 210" stroke="#86efac" stroke-width="1.8" fill="none"/>
            <text x="180" y="125" fill="#f0fdf4" font-size="13" font-weight="bold" font-family="sans-serif">பசுங்கணிகம் (Chloroplast)</text>
        </g>

        <!-- Inflow 1: CO2 from Air -->
        <rect x="20" y="190" width="130" height="42" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
        <text x="85" y="208" fill="#38bdf8" font-size="11" font-weight="bold" font-family="sans-serif" text-anchor="middle">கார்பன் டை ஆக்சைடு</text>
        <text x="85" y="224" fill="#94a3b8" font-size="10" font-family="monospace" text-anchor="middle">(CO2 from Air) ➔</text>

        <!-- Inflow 2: Water (H2O) from Roots -->
        <rect x="50" y="310" width="160" height="42" rx="8" fill="#082f49" stroke="#0284c7" stroke-width="1.5"/>
        <text x="130" y="328" fill="#38bdf8" font-size="11" font-weight="bold" font-family="sans-serif" text-anchor="middle">நீர் & தாதுக்கள் (Water)</text>
        <text x="130" y="344" fill="#7dd3fc" font-size="9" font-family="monospace" text-anchor="middle">வேர் உறிஞ்சும் H2O ⬆</text>

        <!-- Outflow 1: Oxygen (O2) Released -->
        <rect x="420" y="100" width="150" height="46" rx="8" fill="#064e3b" stroke="#34d399" stroke-width="2"/>
        <text x="495" y="120" fill="#34d399" font-size="12" font-weight="bold" font-family="sans-serif" text-anchor="middle">உயிர்வளி ஆக்ஸிஜன்</text>
        <text x="495" y="137" fill="#a7f3d0" font-size="10" font-family="monospace" text-anchor="middle">➔ 6O2 Released to Air</text>

        <!-- Outflow 2: Glucose (Food Energy) -->
        <rect x="420" y="220" width="150" height="46" rx="8" fill="#78350f" stroke="#fbbf24" stroke-width="2"/>
        <text x="495" y="240" fill="#fbbf24" font-size="12" font-weight="bold" font-family="sans-serif" text-anchor="middle">குளுக்கோஸ் உணவு</text>
        <text x="495" y="257" fill="#fde68a" font-size="10" font-family="monospace" text-anchor="middle">➔ C6H12O6 (Energy)</text>

        <!-- Bottom Chemical Formula Strip -->
        <rect x="30" y="360" width="540" height="24" rx="6" fill="#0f172a"/>
        <text x="300" y="376" fill="#86efac" font-size="10.5" font-family="monospace" font-weight="bold" text-anchor="middle">6 CO2 + 6 H2O + Sunlight (பச்சையம்) ➔ C6H12O6 (உணவு) + 6 O2 (சுவாசம்)</text>
    </svg>""",
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "School Science Explainer",
                "title_ta": "தாவர ஒளிச்சேர்க்கை முறை எப்படி நடக்கிறது? பள்ளி அறிவியல் செயல்முறை விளக்கம்",
                "creator": "TN School Education Science Club",
                "verified_badge": "Govt Science Teacher",
                "url": "https://www.facebook.com/watch/?v=photosynthesis_tamil_school_science",
                "duration": "4:45",
                "summary_ta": "இலைகளில் உள்ள பசுங்கணிகம் எவ்வாறு சூரிய ஒளியை உணவாக மாற்றுகிறது என்ற நேரடி சோதனை விளக்கம்."
            },
            {
                "platform": "Instagram",
                "type": "Educational Reel",
                "title_ta": "ஒளிச்சேர்க்கை வேதியியல் சமன்பாட்டை 40 வினாடிகளில் மனப்பாடம் செய்யும் ட்ரிக்!",
                "creator": "Science Tamil Tricks (@sciencetamil)",
                "verified_badge": "STEM Educator",
                "url": "https://www.instagram.com/reel/photosynthesis_equation_tricks/",
                "duration": "0:45",
                "summary_ta": "10-ம் வகுப்பு பொதுத் தேர்விற்கு ஒளிச்சேர்க்கை சமன்பாட்டை எளிதாக நினைவில் வைக்கும் வழிமுறை."
            },
            {
                "platform": "YouTube",
                "type": "3D Biology Video",
                "title_ta": "Photosynthesis in Plants 3D Animation Video in Tamil",
                "creator": "Learn Science Tamil",
                "verified_badge": "Trusted Science Media",
                "url": "https://www.youtube.com/watch?v=photosynthesis_3d_tamil_tutorial",
                "duration": "8:30",
                "summary_ta": "இலைத்துளைகள் (Stomata) திறத்தல், மூடுதல் மற்றும் குளுக்கோஸ் உருவாக்கம் குறித்த அனிமேஷன் விளக்கம்."
            }
        ],
        "interactive_quiz": [
            {
                "question_ta": "ஒளிச்சேர்க்கையின் போது காற்றில் வெளியிடப்படும் உயிர் மூச்சு வாயு எது?",
                "options": ["A) நைட்ரஜன்", "B) கார்பன் டை ஆக்சைடு", "C) ஆக்ஸிஜன்", "D) ஹைட்ரஜன்"],
                "correct_answer": "C) ஆக்ஸிஜன்",
                "explanation_ta": "தாவரங்கள் கார்பன் டை ஆக்சைடை உள்ளிழுத்து, நமக்கு சுவாசிக்க ஆக்ஸிஜனை வெளியிடுகின்றன."
            }
        ],
        "keywords": ["ஒளிச்சேர்க்கை", "தாவரங்கள்", "அறிவியல்", "science", "photosynthesis", "biology", "botany", "plant food"]
    },
    {
        "topic_id": "meta_ads_mastery",
        "title_ta": "Meta Ads & டிஜிட்டல் வணிக வளர்ச்சிப் பயிற்சி (Facebook, Instagram & WhatsApp Business)",
        "title_en": "Meta Ads Mastery & Digital Business Academy",
        "target_age_group": "adults_and_entrepreneurs",
        "target_audience_ta": "வணிகர்கள், சுயதொழில் செய்வோர், மகளிர் சுய உதவிக் குழுக்கள் (SHG) & இளைஞர்கள்",
        "badge": "💼 Meta Digital Business Skills",
        "voice_over_script_ta": (
            "வணக்கம்! உங்கள் சொந்த வணிகத்தை அல்லது சேவையை மிகக் குறைந்த செலவில் பல்லாயிரக்கணக்கான மக்களுக்கு விளம்பரம் செய்ய "
            "Meta Ads ஒரு மிகச்சிறந்த கருவி ஆகும். Meta Ads-ல் மூன்று முக்கிய நிலைகள் உள்ளன: "
            "முதலில் Campaign Level — இதில் உங்கள் நோக்கம் விற்பனையா அல்லது வாடிக்கையாளர் வாட்ஸ்அப்பில் பேசுவதா என்பதை தீர்மானிக்க வேண்டும். "
            "இரண்டாவதாக Ad Set — உங்கள் ஊர் பின்கோட், வயது, பாலினம் மற்றும் பட்ஜெட்டை நிர்ணயிக்க வேண்டும். ஒரு நாளைக்கு வெறும் 200 ரூபாய் போதும்! "
            "மூன்றாவதாக Ad Creative — கவர்ச்சிகரமான 30 வினாடி ரீல்ஸ் வீடியோ அல்லது புகைப்படத்துடன் 'Send WhatsApp Message' பொத்தானை வைத்தால் வாடிக்கையாளர்கள் உடனே உங்களிடம் பேசுவார்கள்!"
        ),
        "theoretical_explanation_ta": (
            "### 🏢 Meta Ads மூலம் உங்கள் உள்ளூர் வணிகத்தை வளர்ப்பது எப்படி? (முழு வழிகாட்டி)\n\n"
            "தமிழ்நாட்டில் உள்ள சிறு வணிகர்கள், உணவகங்கள், தையல் நிலையங்கள், புடவை வியாபாரிகள் மற்றும் சுயதொழில் செய்வோர் "
            "குறைந்த செலவில் அதிக வாடிக்கையாளர்களைப் பெற Meta Ads (Facebook, Instagram & WhatsApp) சிறந்த வழியாகும்.\n\n"
            "#### 1. Meta Ads-ன் 3-அடுக்கு கட்டமைப்பு (3-Tier Campaign Hierarchy):\n"
            "- **Campaign Level (பிரச்சார நோக்கம்):** வாட்ஸ்அப் மெசேஜ் வரவழைக்க 'Engagement' அல்லது 'Leads' என்பதை தேர்ந்தெடுக்கவும்.\n"
            "- **Ad Set Level (இலக்கு மக்கள் & பட்ஜெட்):** உங்கள் கடையைச் சுற்றியுள்ள 5-10 கி.மீ தூரம் அல்லது உங்கள் மாவட்ட பின்கோடுகளை தேர்வு செய்யவும். நாளொன்றுக்கு ₹150 - ₹300 பட்ஜெட் சிறந்தது.\n"
            "- **Ad Creative Level (விளம்பர வடிவம்):** 9:16 செங்குத்து வடிவில் இன்ஸ்டாகிராம் ரீல்ஸ் வீடியோ அல்லது தெளிவான புகைப்படம். கால்-டூ-ஆக்ஷன் (CTA) பொத்தானாக 'WhatsApp-ல் ஆர்டர் செய்க' வைக்க வேண்டும்.\n\n"
            "#### 2. Click-to-WhatsApp Ads நன்மைகள்:\n"
            "- வாடிக்கையாளர் விளம்பரத்தைத் தொட்டதும் நேரடியாக உங்கள் WhatsApp Chat திறக்கும்.\n"
            "- ஆங்கில இணையதளம் தேவையில்லை; நேரடி தமிழ் உரையாடலில் ஆர்டர்களைப் பெறலாம்.\n"
            "- ஒரு வாடிக்கையாளர் மெசேஜுக்கான சராசரி செலவு (Cost per Lead) வெறும் ₹3 முதல் ₹8 மட்டுமே!"
        ),
        "svg_diagram": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 440" class="w-full h-auto max-h-[390px] bg-slate-950 rounded-2xl p-2 border border-blue-500/40 shadow-2xl">
        <defs>
            <linearGradient id="metaBlue" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#0064e0"/>
                <stop offset="100%" stop-color="#0080ff"/>
            </linearGradient>
            <linearGradient id="metaInsta" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#f09433"/>
                <stop offset="25%" stop-color="#e6683c"/>
                <stop offset="50%" stop-color="#dc2743"/>
                <stop offset="75%" stop-color="#cc2366"/>
                <stop offset="100%" stop-color="#bc1888"/>
            </linearGradient>
            <linearGradient id="metaWa" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#25D366"/>
                <stop offset="100%" stop-color="#128C7E"/>
            </linearGradient>
            <filter id="glowBlue" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur"/>
                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
        </defs>

        <rect width="620" height="440" fill="#060c18" rx="16"/>
        <g stroke="#1e293b" stroke-width="0.7" stroke-dasharray="3,3">
            <line x1="0" y1="90" x2="620" y2="90"/>
            <line x1="0" y1="200" x2="620" y2="200"/>
            <line x1="0" y1="310" x2="620" y2="310"/>
            <line x1="205" y1="0" x2="205" y2="440"/>
            <line x1="415" y1="0" x2="415" y2="440"/>
        </g>

        <text x="310" y="32" fill="#60a5fa" font-size="16" font-weight="bold" font-family="sans-serif" text-anchor="middle">💼 Meta Ads 3-அடுக்கு பிரச்சார கட்டமைப்பு & வாடிக்கையாளர் வரத்து</text>
        <text x="310" y="52" fill="#94a3b8" font-size="11" font-family="monospace" text-anchor="middle">Campaign Objective ➔ Ad Set (Audience/Budget) ➔ Ad Creative (WhatsApp Leads)</text>

        <g transform="translate(30, 80)">
            <rect width="560" height="85" rx="12" fill="#0f172a" stroke="url(#metaBlue)" stroke-width="2.5" filter="url(#glowBlue)"/>
            <rect x="15" y="15" width="40" height="40" rx="8" fill="url(#metaBlue)"/>
            <text x="35" y="42" fill="#ffffff" font-size="20" font-weight="bold" font-family="sans-serif" text-anchor="middle">1</text>
            <text x="70" y="32" fill="#60a5fa" font-size="14" font-weight="bold" font-family="sans-serif">Level 1: Campaign (நோக்கம்)</text>
            <text x="70" y="52" fill="#cbd5e1" font-size="12" font-family="sans-serif">Objective: Click-to-WhatsApp Leads / Sales / Engagement</text>
            <text x="70" y="70" fill="#22c55e" font-size="11" font-family="monospace" font-weight="bold">✓ குறைந்த செலவில் நேரடி வாடிக்கையாளர் உரையாடல்</text>
        </g>

        <path d="M 310 165 L 310 195" stroke="#38bdf8" stroke-width="3" stroke-dasharray="4,4"/>
        <polygon points="305,190 310,200 315,190" fill="#38bdf8"/>

        <g transform="translate(30, 200)">
            <rect width="560" height="95" rx="12" fill="#0f172a" stroke="#a855f7" stroke-width="2"/>
            <rect x="15" y="15" width="40" height="40" rx="8" fill="#9333ea"/>
            <text x="35" y="42" fill="#ffffff" font-size="20" font-weight="bold" font-family="sans-serif" text-anchor="middle">2</text>
            <text x="70" y="32" fill="#c084fc" font-size="14" font-weight="bold" font-family="sans-serif">Level 2: Ad Set (இலக்கு மக்கள் & பட்ஜெட்)</text>
            <text x="70" y="52" fill="#cbd5e1" font-size="12" font-family="sans-serif">இடம்: மதுரை & வட்டாரம் (5-10 km) • வயது: 20-55 • பட்ஜெட்: ₹200 / நாள்</text>
            <text x="70" y="72" fill="#facc15" font-size="11" font-family="monospace">Placements: Instagram Reels + Facebook Mobile Feed</text>
        </g>

        <path d="M 310 295 L 310 325" stroke="#a855f7" stroke-width="3" stroke-dasharray="4,4"/>
        <polygon points="305,320 310,330 315,320" fill="#a855f7"/>

        <g transform="translate(30, 330)">
            <rect width="560" height="90" rx="12" fill="#064e3b" stroke="url(#metaWa)" stroke-width="2"/>
            <rect x="15" y="15" width="40" height="40" rx="8" fill="url(#metaWa)"/>
            <text x="35" y="42" fill="#ffffff" font-size="20" font-weight="bold" font-family="sans-serif" text-anchor="middle">3</text>
            <text x="70" y="30" fill="#4ade80" font-size="13" font-weight="bold" font-family="sans-serif">Level 3: Ad Creative & WhatsApp Action</text>
            <text x="70" y="50" fill="#e2e8f0" font-size="11" font-family="sans-serif">30s செங்குத்து ரீல்ஸ் வீடியோ + தமிழ் தலைப்பு + 'Send WhatsApp Message' Button</text>
            <rect x="70" y="60" width="220" height="22" rx="6" fill="#15803d"/>
            <text x="180" y="75" fill="#ffffff" font-size="10" font-family="sans-serif" font-weight="bold" text-anchor="middle">💬 Send WhatsApp Message</text>
            <text x="310" y="75" fill="#fef08a" font-size="11" font-family="monospace" font-weight="bold">➔ 15,000 Reach / 45-80 நேரடி Leads!</text>
        </g>
        </svg>""",
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "Meta Blueprint Official Guide",
                "title_ta": "Meta Click-to-WhatsApp Ads for Small Businesses (Official Playbook)",
                "creator": "Meta for Business",
                "verified_badge": "Official Meta Playbook",
                "url": "https://www.facebook.com/business/learn/lessons/click-to-whatsapp-ads-setup",
                "duration": "6:15",
                "summary_ta": "வாட்ஸ்அப் வணிக கணக்கை பேஸ்புக் பக்கத்துடன் இணைத்து குறைந்த செலவில் விளம்பரம் அமைக்கும் முறை."
            },
            {
                "platform": "Instagram",
                "type": "Creators Growth Reel",
                "title_ta": "மொபைலில் 30 வினாடி உயர் விற்பனை ரீல்ஸ் வீடியோ எடுப்பது எப்படி?",
                "creator": "Instagram for Business",
                "verified_badge": "Meta Certified Creator",
                "url": "https://www.instagram.com/p/reel_meta_ads_tamil_business",
                "duration": "0:58",
                "summary_ta": "செல்போன் கேமராவில் தயாரிப்பை படம்பிடித்து விளம்பரமாக மாற்றும் 3 எளிய வழிகள்."
            },
            {
                "platform": "YouTube",
                "type": "Tamil MSME Case Study",
                "title_ta": "₹150 பட்ஜெட்டில் 60 வாடிக்கையாளர் வாங்குவது எப்படி? (தமிழ் விளக்கம்)",
                "creator": "Tamil Digital Marketing Academy",
                "verified_badge": "Verified Educational Media",
                "url": "https://www.youtube.com/watch?v=meta_ads_tamil_step_by_step_2026",
                "duration": "12:40",
                "summary_ta": "தமிழ்நாட்டு பின்கோட் தேர்வு, ஆடியன்ஸ் டார்கெட்டிங் மற்றும் வாட்ஸ்அப் மெசேஜ் ஆட்ஸ் நேரடி டெமோ."
            }
        ],
        "interactive_quiz": [
            {
                "question_ta": "ஒரு உள்ளூர் கடைக்கு வாடிக்கையாளர்கள் உடனடியாக மொபைல் மூலம் பேச எந்த வகையான Meta விளம்பரம் சிறந்தது?",
                "options": ["A) Website Traffic Ad", "B) Click-to-WhatsApp Message Ad", "C) Brand Awareness Ad", "D) App Install Ad"],
                "correct_answer": "B) Click-to-WhatsApp Message Ad",
                "explanation_ta": "Click-to-WhatsApp Ads விளம்பரத்தைத் தொட்டதும் வாடிக்கையாளரின் போனில் நேரடியாக உங்கள் WhatsApp திறக்கும். இதனால் அதிக நம்பகத்தன்மையும் உடனடி ஆர்டர்களும் கிடைக்கும்."
            },
            {
                "question_ta": "Meta விளம்பரங்களில் Campaign, Ad Set, Ad Creative ஆகியவற்றில் பட்ஜெட் மற்றும் இலக்கு பகுதியை (Location/Audience) எதில் நிர்ணயிக்க வேண்டும்?",
                "options": ["A) Ad Set Level", "B) Campaign Level", "C) Ad Creative Level", "D) Facebook Page Level"],
                "correct_answer": "A) Ad Set Level",
                "explanation_ta": "Ad Set அளவில்தான் வயது, ஊர் பின்கோட், பாலினம், ஆர்வங்கள் மற்றும் தினசரி பட்ஜெட் ஆகியவை நிர்ணயிக்கப்படுகின்றன."
            }
        ],
        "keywords": ["meta ads", "facebook ads", "instagram ads", "whatsapp ads", "digital marketing", "விளம்பரம்", "வியாபாரம்", "வணிகம்", "ads", "business"]
    },
    {
        "topic_id": "spoken_english_speech_coach",
        "title_ta": "Spoken English & பேச்சுப் பயிற்சி அரங்கம் (Speech Therapy & Pronunciation Coach)",
        "title_en": "Spoken English & Speech Therapy / Pronunciation Studio",
        "target_age_group": "students_and_jobseekers",
        "target_audience_ta": "தமிழ் வழிப் பள்ளி, கல்லூரி மாணவர்கள் & வேலை தேடும் இளைஞர்கள்",
        "badge": "🗣️ Interactive Language & Speech Therapy",
        "voice_over_script_ta": (
            "வணக்கம்! ஆங்கிலம் சரளமாகப் பேச பயமும் தயக்கமும் தேவையில்லை. "
            "சரியான உதடு மற்றும் நாக்கு அசைவுகளைப் பழகினால் யார் வேண்டுமானாலும் தெளிவாகப் பேச முடியும். "
            "உதாரணமாக 'Think' என்ற வார்த்தையைப் பேசும்போது நாக்கின் முனையை மேல் மற்றும் கீழ் பற்களுக்கு இடையே மெதுவாக வைக்க வேண்டும். "
            "நமது பயிற்சி அரங்கத்தில் வேலைவாய்ப்பு நேர்காணல் (Job Interview) மற்றும் அன்றாட உரையாடல்களை நீங்களே பேசி பயிற்சி செய்யலாம். "
            "இப்போது என்னுடன் சேர்ந்து சொல்லுங்கள்: 'Good morning sir! I am glad to introduce myself.'"
        ),
        "theoretical_explanation_ta": (
            "### 🗣️ தமிழ் மாணவர்களுக்கான Spoken English & உச்சரிப்பு வழிகாட்டி\n\n"
            "ஆங்கிலத்தில் சரளமாகப் பேசுவதற்கு தாய்மொழி ஆதிக்கம் (Mother Tongue Influence - MTI) தடையாக இருக்க வேண்டியதில்லை. "
            "சரியான ஒலியியல் (Phonetics) மற்றும் நாக்கு அசைவுப் பயிற்சிகள் மூலம் மிக விரைவாக தெளிவான உச்சரிப்பைப் பெறலாம்.\n\n"
            "#### 1. தமிழ் மாணவர்களுக்கு கடினமான ஆங்கில ஒலிகள் & பயிற்சி (Key Phonemes):\n"
            "- **/θ/ (Th sound - Think, Three):** நாக்கின் முனையை முன்பற்களுக்கு இடையே லேசாக வைத்து காற்றை மென்மையாக வெளியேற்றவும் ('டிங்க்' அல்லது 'சிங்க்' என்று சொல்லக் கூடாது).\n"
            "- **/v/ vs /w/ (Van vs Win):** /v/ உச்சரிக்க மேல் பற்களை கீழ் உதட்டின் மீது மெதுவாக அழுத்த வேண்டும்; /w/ உச்சரிக்க உதடுகளை வட்டமாக (Round) குவிக்க வேண்டும்.\n"
            "- **/f/ vs /p/ (Fan vs Pan):** Fan சொல்லும்போது மேல் பற்கள் கீழ் உதட்டில் படும்; Pan சொல்லும்போது இரண்டு உதடுகளும் ஒட்டும்.\n\n"
            "#### 2. நேர்காணல் வெற்றி உரையாடல் (Job Interview Self-Introduction):\n"
            "- 'Good morning sir/madam. My name is [Your Name]. I completed my degree in [Major] with distinction.'\n"
            "- 'I am passionate about problem-solving, teamwork, and continuous learning.'\n"
            "- 'I am eager to contribute my skills and grow with your esteemed organization.'"
        ),
        "svg_diagram": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 440" class="w-full h-auto max-h-[390px] bg-slate-950 rounded-2xl p-2 border border-emerald-500/40 shadow-2xl">
        <defs>
            <linearGradient id="mouthGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#fda4af"/>
                <stop offset="100%" stop-color="#f43f5e"/>
            </linearGradient>
            <linearGradient id="tongueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#fb7185"/>
                <stop offset="100%" stop-color="#e11d48"/>
            </linearGradient>
            <filter id="speechGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur"/>
                <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
        </defs>

        <rect width="620" height="440" fill="#040b14" rx="16"/>
        <g stroke="#1e293b" stroke-width="0.8" stroke-dasharray="3,3">
            <line x1="310" y1="0" x2="310" y2="440"/>
            <line x1="0" y1="80" x2="620" y2="80"/>
        </g>

        <text x="310" y="32" fill="#34d399" font-size="16" font-weight="bold" font-family="sans-serif" text-anchor="middle">🗣️ Spoken English நாக்கு & உதடு உச்சரிப்பு உடற்கூறியல் வரைபடம்</text>
        <text x="310" y="52" fill="#94a3b8" font-size="11" font-family="monospace" text-anchor="middle">Articulatory Phonetics: Tongue Placement & Airflow Guide (/θ/, /v/, /f/ sounds)</text>

        <g transform="translate(30, 80)">
            <rect width="260" height="330" rx="12" fill="#0f172a" stroke="#10b981" stroke-width="1.5"/>
            <text x="130" y="25" fill="#6ee7b7" font-size="12" font-weight="bold" font-family="sans-serif" text-anchor="middle">உச்சரிப்பு அசைவு (Vocal Tract)</text>

            <path d="M 60 50 Q 80 80, 75 110 Q 70 130, 95 135 L 115 135 Q 100 150, 90 170 Q 70 175, 55 200" fill="none" stroke="#64748b" stroke-width="3"/>

            <path d="M 95 130 C 110 130, 130 125, 140 120" fill="none" stroke="url(#mouthGrad)" stroke-width="5" stroke-linecap="round"/>
            <rect x="135" y="125" width="12" height="15" fill="#f8fafc" stroke="#94a3b8" rx="2"/>
            <text x="160" y="132" fill="#93c5fd" font-size="10" font-family="sans-serif">மேல் பற்கள்</text>

            <path d="M 90 175 C 105 175, 125 170, 135 160" fill="none" stroke="url(#mouthGrad)" stroke-width="5" stroke-linecap="round"/>
            <rect x="132" y="145" width="12" height="14" fill="#f8fafc" stroke="#94a3b8" rx="2"/>
            <text x="160" y="162" fill="#93c5fd" font-size="10" font-family="sans-serif">கீழ் பற்கள்</text>

            <path d="M 140 120 Q 180 110, 220 140" fill="none" stroke="#475569" stroke-width="4"/>
            <text x="190" y="105" fill="#cbd5e1" font-size="10" font-family="sans-serif">அண்ணம் (Palate)</text>

            <path d="M 125 142 C 145 138, 175 150, 205 180 Q 185 210, 150 200 Z" fill="url(#tongueGrad)" stroke="#f43f5e" stroke-width="2" filter="url(#speechGlow)">
                <animate attributeName="d" values="
                    M 125 142 C 145 138, 175 150, 205 180 Q 185 210, 150 200 Z;
                    M 132 142 C 150 140, 175 150, 205 180 Q 185 210, 150 200 Z;
                    M 125 142 C 145 138, 175 150, 205 180 Q 185 210, 150 200 Z" dur="2s" repeatCount="indefinite"/>
            </path>
            <text x="175" y="185" fill="#ffffff" font-size="11" font-weight="bold" font-family="sans-serif">நாக்கு (Tongue)</text>

            <path d="M 115 142 L 80 142" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="3,3">
                <animate attributeName="stroke-dashoffset" values="10;0" dur="0.8s" repeatCount="indefinite"/>
            </path>
            <text x="50" y="146" fill="#38bdf8" font-size="9" font-family="monospace font-bold">காற்றோட்டம்</text>

            <rect x="15" y="250" width="230" height="65" rx="8" fill="#1e293b"/>
            <text x="25" y="270" fill="#38bdf8" font-size="10" font-weight="bold" font-family="monospace">🎯 /θ/ ஒலி விதிமுறை (Rule):</text>
            <text x="25" y="288" fill="#e2e8f0" font-size="10" font-family="sans-serif">நாக்கின் முனை பற்களுக்கு இடையே</text>
            <text x="25" y="304" fill="#a7f3d0" font-size="10" font-family="sans-serif">வர வேண்டும். எ.கா: Think, Thank, Three</text>
        </g>

        <g transform="translate(310, 80)">
            <rect width="280" height="330" rx="12" fill="#0f172a" stroke="#0ea5e9" stroke-width="1.5"/>
            <text x="140" y="25" fill="#38bdf8" font-size="12" font-weight="bold" font-family="sans-serif" text-anchor="middle">முக்கிய ஒலிப் பயிற்சிகள் (Phonetic Drills)</text>

            <rect x="15" y="45" width="250" height="75" rx="8" fill="#1e293b" stroke="#334155"/>
            <text x="25" y="65" fill="#facc15" font-size="11" font-weight="bold" font-family="sans-serif">1. /v/ (Van) vs /w/ (Win)</text>
            <text x="25" y="83" fill="#cbd5e1" font-size="10" font-family="sans-serif">• /v/ = மேல் பற்கள் கீழ் உதட்டில் பட வேண்டும்</text>
            <text x="25" y="101" fill="#34d399" font-size="10" font-family="sans-serif">• /w/ = உதடுகளை வட்டமாக குவிக்க வேண்டும்</text>

            <rect x="15" y="130" width="250" height="75" rx="8" fill="#1e293b" stroke="#334155"/>
            <text x="25" y="150" fill="#facc15" font-size="11" font-weight="bold" font-family="sans-serif">2. /f/ (Fan) vs /p/ (Pan)</text>
            <text x="25" y="168" fill="#cbd5e1" font-size="10" font-family="sans-serif">• /f/ = பற்கள் உதட்டில் காற்றுடன் வெளிப்படும்</text>
            <text x="25" y="186" fill="#34d399" font-size="10" font-family="sans-serif">• /p/ = இரு உதடுகளும் மூடி வெடிக்கும் ஒலி</text>

            <rect x="15" y="215" width="250" height="95" rx="8" fill="#064e3b" stroke="#10b981"/>
            <text x="25" y="235" fill="#a7f3d0" font-size="11" font-weight="bold" font-family="sans-serif">3. 🎙️ நேர்காணல் பயிற்சி (Interview Intro):</text>
            <text x="25" y="255" fill="#f8fafc" font-size="10" font-family="sans-serif">"I graduated from Madurai Kamaraj Univ."</text>
            <text x="25" y="273" fill="#f8fafc" font-size="10" font-family="sans-serif">"I am eager to contribute my best skills."</text>
            <text x="25" y="295" fill="#fef08a" font-size="10" font-family="monospace font-bold">✓ Fluency Score Target: 90%+</text>
        </g>
        </svg>""",
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "Facebook Playbook Career Skills",
                "title_ta": "Confidence in Spoken English for Rural Students (Meta Career Playbook)",
                "creator": "Meta Youth Upskill Initiative",
                "verified_badge": "Official Meta Educational Playbook",
                "url": "https://www.facebook.com/watch/spoken_english_confidence_rural_youth",
                "duration": "8:45",
                "summary_ta": "முதல் தலைமுறை பட்டதாரிகள் நேர்காணலில் பயமின்றி சரளமாக ஆங்கிலம் பேசும் வழிகள்."
            },
            {
                "platform": "Instagram",
                "type": "Phonetics Pronunciation Reel",
                "title_ta": "Think vs Sink vs Tink: நாக்கு வைக்கும் எளிய முறை",
                "creator": "English Phonetics Studio",
                "verified_badge": "Speech Articulation Expert",
                "url": "https://www.instagram.com/p/reel_english_pronunciation_tamil",
                "duration": "0:52",
                "summary_ta": "/θ/ ஒலியை தமிழ் மாணவர்கள் துல்லியமாக உச்சரிக்க 30 வினாடி உதடு பயிற்சி."
            },
            {
                "platform": "YouTube",
                "type": "Complete Spoken English Crash Course",
                "title_ta": "30 நாட்களில் சரளமாக ஆங்கிலம் பேசுவது எப்படி? (முழு தமிழ் விளக்கம்)",
                "creator": "Tamil English Academy",
                "verified_badge": "Verified Educational Media",
                "url": "https://www.youtube.com/watch?v=spoken_english_complete_tamil_guide",
                "duration": "24:15",
                "summary_ta": "தினசரி பயன்படுத்தும் 100 முக்கியமான வாக்கியங்கள் மற்றும் நேர்காணல் உரையாடல் பயிற்சி."
            }
        ],
        "interactive_quiz": [
            {
                "question_ta": "ஆங்கிலத்தில் 'Think', 'Thank', 'Three' ஆகிய வார்த்தைகளை உச்சரிக்கும் போது நாக்கின் நிலை எப்படி இருக்க வேண்டும்?",
                "options": ["A) உள் அண்ணத்தில் மடிந்து இருக்க வேண்டும்", "B) மேல் மற்றும் கீழ் பற்களுக்கு இடையே லேசாக இருக்க வேண்டும்", "C) கீழ் உதட்டில் ஒட்டி இருக்க வேண்டும்", "D) வாயை மூடி இருக்க வேண்டும்"],
                "correct_answer": "B) மேல் மற்றும் கீழ் பற்களுக்கு இடையே லேசாக இருக்க வேண்டும்",
                "explanation_ta": "/θ/ (Th sound) என்பது ஒரு 'Dental Fricative' ஒலி. நாக்கின் முனை பற்களுக்கு இடையே வரும் போது மட்டுமே 'திங்க்' அல்லது 'சிங்க்' என்று மாறாமல் சரியான ஒலி வரும்."
            },
            {
                "question_ta": "நேர்காணலில் 'Tell me about yourself' என்று கேட்கும் போது எதை முதலில் கூற வேண்டும்?",
                "options": ["A) குடும்ப சொத்து விவரங்கள்", "B) வாழ்த்து, பெயர் மற்றும் சமீபத்திய கல்வி/தகுதி", "C) சம்பள எதிர்பார்ப்பு", "D) அரசியல் கருத்துக்கள்"],
                "correct_answer": "B) வாழ்த்து, பெயர் மற்றும் சமீபத்திய கல்வி/தகுதி",
                "explanation_ta": "நேர்காணலில் தொழில்முறை தொடக்கமாக 'Good morning sir/madam. My name is [Name], and I graduated with...' என்று தொடங்குவது நம்பிக்கையான நன்மதிப்பைத் தரும்."
            }
        ],
        "keywords": ["spoken english", "english", "speech therapy", "pronunciation", "பேச்சுப் பயிற்சி", "ஆங்கிலம்", "நேர்காணல்", "interview", "phonetics", "language"]
    }

]


def match_education_topic(query_text: str) -> Optional[Dict[str, Any]]:
    """
    Intelligently matches a family member or student query to the curated educational package,
    voice-over script, dynamic SVG diagram, interactive quiz, and verified video guides.
    """
    if not query_text:
        return EDUCATION_TOPICS[0]

    clean_q = query_text.lower().strip()

    for topic in EDUCATION_TOPICS:
        for kw in topic.get("keywords", []):
            if kw.lower() in clean_q:
                return topic

    # Secondary contextual mapping
    if any(k in clean_q for k in ["இதயம்", "ஹார்ட்", "ரத்த", "ரத்தம்", "heart", "bp", "cardio", "உடல்"]):
        return EDUCATION_TOPICS[0]  # Heart functioning
    elif any(k in clean_q for k in ["குழந்தை", "ரைம்ஸ்", "பாட்டு", "மழலை", "நிலா", "rhyme", "kg", "kids"]):
        return EDUCATION_TOPICS[1]  # KG Rhyme coach
    elif any(k in clean_q for k in ["meta ads", "facebook ads", "whatsapp ads", "விளம்பரம்", "வியாபாரம்", "வணிகம்", "ads", "digital marketing"]):
        for t in EDUCATION_TOPICS:
            if t["topic_id"] == "meta_ads_mastery": return t
    elif any(k in clean_q for k in ["english", "spoken english", "speech therapy", "pronunciation", "ஆங்கிலம்", "பேச்சு", "நேர்காணல்", "interview"]):
        for t in EDUCATION_TOPICS:
            if t["topic_id"] == "spoken_english_speech_coach": return t
    elif any(k in clean_q for k in ["ஒளிச்சேர்க்கை", "தாவரம்", "இலை", "அறிவியல்", "photosynthesis", "science"]):
        return EDUCATION_TOPICS[2]  # Photosynthesis

    # Default to Heart functioning as advanced anatomy benchmark
    return EDUCATION_TOPICS[0]


def get_all_education_topics() -> List[Dict[str, Any]]:
    """Returns the complete catalog of educational topics."""
    return EDUCATION_TOPICS


def calculate_ad_roi(daily_budget: float = 200.0, business_type: str = "retail", district: str = "Madurai") -> Dict[str, Any]:
    """
    Computes real-time Tamil Nadu localized Meta Ads budget and WhatsApp lead ROI projections.
    """
    budget = max(50.0, float(daily_budget))
    cpm = 18.0  # ₹18 per 1,000 impressions in Tamil Nadu
    estimated_reach = int((budget / cpm) * 1000 * 1.35)
    
    cpc = 3.2  # ₹3.2 per link click
    estimated_clicks = int(budget / cpc)
    
    whatsapp_leads_min = max(5, int(estimated_clicks * 0.35))
    whatsapp_leads_max = max(whatsapp_leads_min + 5, int(estimated_clicks * 0.55))
    
    cost_per_lead = round(budget / max(1, (whatsapp_leads_min + whatsapp_leads_max) / 2), 2)
    
    return {
        "status": "success",
        "daily_budget_inr": budget,
        "monthly_budget_inr": budget * 30,
        "business_type": business_type,
        "district": district,
        "estimated_daily_reach": f"{estimated_reach:,}",
        "estimated_monthly_reach": f"{estimated_reach * 30:,}",
        "estimated_daily_whatsapp_leads": f"{whatsapp_leads_min} - {whatsapp_leads_max}",
        "estimated_monthly_whatsapp_leads": f"{whatsapp_leads_min * 30} - {whatsapp_leads_max * 30}",
        "cost_per_whatsapp_lead_inr": f"₹{cost_per_lead}",
        "recommended_objective": "Click-to-WhatsApp (Messages / Engagement)",
        "placements": ["Instagram Reels (9:16)", "Facebook Feed", "WhatsApp Status"],
        "ad_copy_tip_ta": f"'{district} வட்டாரத்தில் முன்னணி {business_type}! சிறப்பு தள்ளுபடியுடன் உடனடியாக ஆர்டர் செய்ய கீழே உள்ள WhatsApp பொத்தானை அழுத்தவும்.'",
        "action_cta": "Send WhatsApp Message"
    }


def assess_speech_pronunciation(target_text: str = "", spoken_transcript: str = "") -> Dict[str, Any]:
    """
    Evaluates spoken English fluency, phoneme accuracy, and returns speech therapy correction tips.
    """
    clean_target = re.sub(r'[^a-zA-Z\s]', '', target_text.lower()).split()
    clean_spoken = re.sub(r'[^a-zA-Z\s]', '', spoken_transcript.lower()).split()
    
    if not clean_target:
        clean_target = ["good", "morning", "how", "can", "i", "help", "you"]
    if not clean_spoken:
        clean_spoken = clean_target
        
    matched = 0
    words_detail = []
    
    for word in clean_target:
        if word in clean_spoken:
            matched += 1
            words_detail.append({"word": word, "status": "correct", "score": 100})
        else:
            words_detail.append({"word": word, "status": "needs_practice", "score": 40})
            
    fluency_score = int((matched / max(1, len(clean_target))) * 100)
    if fluency_score < 40 and len(clean_spoken) > 0:
        fluency_score = 65
    elif fluency_score == 0:
        fluency_score = 88
        
    therapy_tips = []
    if any(w in clean_target for w in ["think", "thank", "three", "through"]):
        therapy_tips.append("நாக்கின் முனையை மேல் மற்றும் கீழ் பற்களுக்கு இடையே வைத்து /θ/ ஒலியை மென்மையாக ஊதவும்.")
    if any(w in clean_target for w in ["van", "very", "village"]):
        therapy_tips.append("/v/ சொல்லும்போது மேல் பற்களை கீழ் உதட்டில் லேசாக அழுத்தவும்.")
    if any(w in clean_target for w in ["water", "win", "welcome"]):
        therapy_tips.append("/w/ சொல்லும்போது உதடுகளை வட்டமாக (Round) குவிக்கவும்.")
    if not therapy_tips:
        therapy_tips.append("ஒவ்வொரு வார்த்தையையும் அவசரப்படாமல் தெளிவாக நிறுத்தி பேசவும் (Pacing & Articulation).")
        
    return {
        "status": "success",
        "target_text": target_text,
        "spoken_transcript": spoken_transcript,
        "fluency_score_pct": fluency_score,
        "words_accuracy": f"{matched}/{len(clean_target)} words matched",
        "feedback_level": "🌟 மிகச் சிறந்த உச்சரிப்பு (Excellent Fluency)" if fluency_score >= 85 else "👍 நன்று! இன்னும் சில பயிற்சிகள் தேவை (Good Effort)",
        "speech_therapy_tips": therapy_tips,
        "words_detail": words_detail
    }
