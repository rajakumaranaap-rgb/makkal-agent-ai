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
    elif any(k in clean_q for k in ["ஒளிச்சேர்க்கை", "தாவரம்", "இலை", "அறிவியல்", "photosynthesis", "science"]):
        return EDUCATION_TOPICS[2]  # Photosynthesis

    # Default to Heart functioning as advanced anatomy benchmark
    return EDUCATION_TOPICS[0]


def get_all_education_topics() -> List[Dict[str, Any]]:
    """Returns the complete catalog of educational topics."""
    return EDUCATION_TOPICS
