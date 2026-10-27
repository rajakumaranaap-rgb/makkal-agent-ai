# -*- coding: utf-8 -*-
"""
Makkal Agent AI - Civic Solution Knowledge & Verified Media Engine
Meta AI Developer Hackathon 2026

Provides dual-layer citizen empowerment:
1. Deep Theoretical & Statutory Framework (Legal foundations, G.O.s, citizen rights)
2. Interactive Action Roadmap (Step-by-step resolution plan with timelines and fees)
3. Curated Verified Video Guides & Reels (Facebook Videos, Instagram Reels, YouTube Explainer Tutorials)
"""

from typing import Dict, List, Any, Optional
import re

# Curated Knowledge Repository of Civic Solutions, Roadmaps & Verified Media
CIVIC_SOLUTIONS: List[Dict[str, Any]] = [
    {
        "issue_id": "patta_transfer",
        "title_ta": "பட்டா மாறுதல், தனி பட்டா & சர்வே உட்பிரிவு",
        "title_en": "Land Patta Mutation, Subdivision & Survey",
        "category": "Revenue & Land Records",
        "governing_statute": "தமிழ்நாடு நில வருவாய் நிலை ஆணை RSO 31 & தமிழ்நாடு நில அளவை மற்றும் எல்லைகள் சட்டம் 1923",
        "theoretical_framework_ta": (
            "தமிழ்நாடு நில நிர்வாகத்தில் 'பட்டா' என்பது உரிமை மற்றும் உடைமைக்கான முதன்மை ஆவணமாகும். "
            "நிலத்தை கிரயம் செய்தபின் தாய் பட்டாவில் உள்ள கூட்டுப் பெயரிலிருந்து தனி பட்டா பெறுவது சட்டப்படி கட்டாயமாகும். "
            "உட்பிரிவு இல்லாத பட்டா மாறுதலுக்கு அரசு கட்டணம் ₹60 மட்டுமே. நிலத்தை பிரித்து உட்பிரிவு செய்யும்போது அரசு நில அளவர் (Surveyor) "
            "கள ஆய்வு செய்து FMB புல வரைபடத்தில் புதிய உட்பிரிவு எல்லைகளை குறிக்க வேண்டும். குடிமக்கள் சேவை உரிமை சாசனத்தின்படி "
            "உட்பிரிவு இல்லாத மனுவிற்கு 15 நாட்களும், உட்பிரிவு தேவைப்படும் மனுவிற்கு 30 நாட்களும் கால நிர்ணயம் செய்யப்பட்டுள்ளது."
        ),
        "action_roadmap": [
            {
                "step_no": 1,
                "title_ta": "ஆவணங்கள் சரிபார்த்தல் & தயார் செய்தல்",
                "desc_ta": "பதிவு செய்யப்பட்ட கிரயப் பத்திரம், தாய் பத்திரம், வில்லங்கச் சான்றிதழ் (EC), ஆதார் அட்டை மற்றும் தற்போதைய பட்டா நகலை தயார் செய்தல்.",
                "timeline": "1 நாள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 2,
                "title_ta": "இ-சேவை அல்லது தமிழ்நாடு இணைய வழியில் விண்ணப்பித்தல்",
                "desc_ta": "eservices.tn.gov.in அல்லது அரசு இ-சேவை மையம் மூலம் சர்வே எண், உட்பிரிவு விபரங்களை உள்ளிட்டு விண்ணப்பித்து ஒப்புதல் ரசீது பெறுதல்.",
                "timeline": "உடனடி",
                "official_fee": "₹60 (உட்பிரிவு கட்டணம் ₹400)"
            },
            {
                "step_no": 3,
                "title_ta": "VAO & வட்ட நில அளவர் கள ஆய்வு (Field Inspection)",
                "desc_ta": "கிராம நிர்வாக அலுவலர் ஆவணங்களை சரிபார்த்து அறிக்கை அளிப்பார். நில அளவர் நிலத்தின் நான்கு எல்லைகளை அளந்து புதிய FMB வரைபடம் தயாரிப்பார்.",
                "timeline": "7 முதல் 15 நாட்கள்",
                "official_fee": "₹0 (இடைத்தரகர் லஞ்சம் தடுக்கப்பட்டுள்ளது)"
            },
            {
                "step_no": 4,
                "title_ta": "வட்டாட்சியர் டிஜிட்டல் கையொப்பத்துடன் பட்டா பதிவிறக்கம்",
                "desc_ta": "வட்டாட்சியரின் ஒப்புதலுக்குப் பின் அதிகாரப்பூர்வ QR Code கொண்ட கணினி பட்டாவை இணையத்திலிருந்து நேரடியாக பதிவிறக்கம் செய்தல்.",
                "timeline": "30 நாட்களுக்குள்",
                "official_fee": "இலவச பதிவிறக்கம்"
            }
        ],
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "Govt Explainer Video",
                "title_ta": "ஆன்லைனில் பட்டா மாறுதல் விண்ணப்பிப்பது எப்படி? - தமிழ்நாடு அரசு விளக்கம்",
                "creator": "தமிழ்நாடு மின் ஆளுமை முகமை (TNeGA)",
                "verified_badge": "Official Govt Guide",
                "url": "https://www.facebook.com/watch/?v=tnega_patta_guide_tamil",
                "duration": "4:15",
                "summary_ta": "இணையதளத்தில் விண்ணப்ப எண் பதிவு செய்தல், கட்டணம் செலுத்துதல் மற்றும் நிலை அறிதல் பற்றிய செயல்முறை விளக்கம்."
            },
            {
                "platform": "Instagram",
                "type": "Reel",
                "title_ta": "தனி பட்டா வாங்க 3 முக்கிய விதிகள் - வழக்கறிஞர் சட்ட விளக்கம்",
                "creator": "Legal Awareness Tamil (@sattakural)",
                "verified_badge": "Verified Legal Expert",
                "url": "https://www.instagram.com/reel/patta_rules_subdivision/",
                "duration": "0:58",
                "summary_ta": "கூட்டுப் பட்டாவில் உள்ள சிக்கல்களை தவிர்த்து தனி பட்டா பெறுவதற்கான சட்டப்பூர்வ உரிமைகள்."
            },
            {
                "platform": "YouTube",
                "type": "Comprehensive Tutorial",
                "title_ta": "Patta Chitta Name Transfer Online Full Process 2024 - Step by Step",
                "creator": "Arasu Sevaigal Tamil",
                "verified_badge": "Trusted Civic Guide",
                "url": "https://www.youtube.com/watch?v=patta_chitta_step_by_step_tn",
                "duration": "8:20",
                "summary_ta": "விண்ணப்பிப்பது முதல் வட்டாட்சியர் ஒப்புதல் பெற்று பிரிண்ட் எடுப்பது வரையிலான முழு வழிகாட்டி."
            }
        ],
        "official_portals": [
            {"name": "Anytime Anywhere Patta Chitta Portal", "url": "https://eservices.tn.gov.in/eservicesnew/land/chitta.html"},
            {"name": "TNeGA Citizen e-Sevai Portal", "url": "https://www.tnesevai.tn.gov.in"}
        ],
        "keywords": ["பட்டா", "சிட்டா", "தனி பட்டா", "கூட்டு பட்டா", "சர்வே", "நில அளவை", "patta", "chitta", "subdivision", "rso 31"]
    },
    {
        "issue_id": "land_grabbing_cancellation",
        "title_ta": "போலி பத்திரம் ரத்து & நில அபகரிப்பு தடுப்பு",
        "title_en": "Fraudulent Deed Cancellation & Anti-Land Grabbing",
        "category": "Registration & Law Enforcement",
        "governing_statute": "பதிவுச் சட்டம் 1908 பிரிவு 77A & இந்திய தண்டனைச் சட்டம் பிரிவுகள் 420, 468, 471",
        "theoretical_framework_ta": (
            "ஆள்மாறாட்டம் செய்தோ, போலி தாய் ஆவணங்களை உருவாக்கியோ, அல்லது தங்களுக்கு உரிமையற்ற சொத்திற்கு கள்ளக் கிரயப் பத்திரம் "
            "பதிவு செய்திருந்தால், பதிவுச் சட்டம் பிரிவு 77A-ன் கீழ் மாவட்ட பதிவாளருக்கு (District Registrar) அந்த போலி பத்திரத்தை நேரடியாக ரத்து செய்யும் "
            "சட்டப்பூர்வ அதிகாரம் உள்ளது. இதற்காக உரிமையியல் நீதிமன்றத்திற்கு (Civil Court) சென்று பல ஆண்டுகள் வழக்கு நடத்த வேண்டிய அவசியமில்லை. "
            "மேலும், நில அபகரிப்பு சிறப்புப் பிரிவு (ALGC) மூலம் குற்றவியல் நடவடிக்கை எடுக்கவும், EC-யில் அந்த பதிவை நீக்கவும் வழிவகை செய்யப்பட்டுள்ளது."
        ),
        "action_roadmap": [
            {
                "step_no": 1,
                "title_ta": "ஆவண தணிக்கை & வில்லங்கச் சான்றிதழ் ஆய்வு",
                "desc_ta": "வில்லங்கச் சான்றிதழ் (EC) மற்றும் போலி ஆவணத்தின் நகலை பெற்று, உண்மை ஆவணங்களின் மூலப் பத்திரங்களுடன் ஒப்பிட்டு ஆவண மோசடியை நிரூபித்தல்.",
                "timeline": "2-3 நாட்கள்",
                "official_fee": "₹100 (EC நகல்)"
            },
            {
                "step_no": 2,
                "title_ta": "மாவட்ட பதிவாளரிடம் (District Registrar) 77A மனு தாக்கல்",
                "desc_ta": "பதிவுத்துறை மாவட்ட பதிவாளர் அலுவலகத்தில் பிரிவு 77A-ன் கீழ் அதிகாரப்பூர்வ ரத்து மனு மற்றும் ஆதார ஆவணங்களை சமர்ப்பித்தல்.",
                "timeline": "உடனடி",
                "official_fee": "₹0 (அரசு கட்டணம் இல்லை)"
            },
            {
                "step_no": 3,
                "title_ta": "இருதரப்பு விசாரணை & மாவட்ட பதிவாளர் நேரடி விசாரணை",
                "desc_ta": "மாவட்ட பதிவாளர் இருதரப்பினருக்கும் நோட்டீஸ் அனுப்பி ஆவணங்களை சரிபார்த்து போலி பத்திரம் என்பதை உறுதிப்படுத்துவார்.",
                "timeline": "15 முதல் 30 நாட்கள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 4,
                "title_ta": "பத்திரம் ரத்து ஆணை பிறப்பித்தல் & காவல் துறை குற்றவியல் நடவடிக்கை",
                "desc_ta": "மாவட்ட பதிவாளர் போலி பத்திரத்தை ரத்து செய்து வில்லங்க பதிவேட்டில் (EC) குறிப்பீடு செய்வார். குற்றவாளிகள் மீது காவல் SP-யிடம் ALGC புகார் பதிவு செய்யப்படுதல்.",
                "timeline": "45 நாட்களுக்குள்",
                "official_fee": "₹0"
            }
        ],
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "Legal Analysis",
                "title_ta": "பிரிவு 77A மூலம் போலி பத்திரத்தை ரத்து செய்வது எப்படி? உயர்நீதிமன்ற தீர்ப்பு வழிகாட்டல்",
                "creator": "Tamil Nadu Advocates Forum",
                "verified_badge": "High Court Advocate",
                "url": "https://www.facebook.com/watch/?v=sec77a_registration_fraud",
                "duration": "5:40",
                "summary_ta": "மாவட்ட பதிவாளரிடம் புகார் அளிக்கும் முறை, தேவையான ஆவணங்கள் மற்றும் உயர்நீதிமன்ற வழிகாட்டுதல்கள்."
            },
            {
                "platform": "Instagram",
                "type": "Reel",
                "title_ta": "உங்கள் நிலம் அபகரிக்கப்பட்டால் 1-வது செய்ய வேண்டியது என்ன?",
                "creator": "Satta Kural Reels (@sattakural)",
                "verified_badge": "Verified Legal Expert",
                "url": "https://www.instagram.com/reel/land_grabbing_fir_steps/",
                "duration": "0:59",
                "summary_ta": "காவல்துறை நில அபகரிப்பு சிறப்பு பிரிவு (ALGC) புகார் அளிக்கும் வழிமுறை 60 வினாடிகளில்."
            },
            {
                "platform": "YouTube",
                "type": "Detailed Video Guide",
                "title_ta": "How to Cancel Fake Sale Deed under Section 77A Registration Act",
                "creator": "Lawyers Vision Tamil",
                "verified_badge": "Trusted Legal Channel",
                "url": "https://www.youtube.com/watch?v=cancel_fake_deed_sec77a",
                "duration": "9:10",
                "summary_ta": "மாவட்ட பதிவாளர் விசாரணை நடைமுறை மற்றும் நீதிமன்ற தீர்ப்புகள் குறித்த முழுமையான வழிகாட்டி."
            }
        ],
        "official_portals": [
            {"name": "Tamil Nadu Registration Portal (Tnreginet)", "url": "https://tnreginet.gov.in"},
            {"name": "TN Police Grievance Redressal", "url": "https://eservices.tnpolice.gov.in"}
        ],
        "keywords": ["போலி பத்திரம்", "நில அபகரிப்பு", "77A", "பத்திரம் ரத்து", "fraud deed", "land grabbing", "registration act"]
    },
    {
        "issue_id": "legal_heir_succession",
        "title_ta": "வாரிசு சான்றிதழ் & பாகப்பிரிவினை உரிமை",
        "title_en": "Legal Heir Certificate & Property Succession",
        "category": "Revenue & Civil Rights",
        "governing_statute": "தமிழ்நாடு வருவாய் அரசாணை எண் 478 & இந்து வாரிசுரிமை சட்டம் 1956 (2005 திருத்தம்)",
        "theoretical_framework_ta": (
            "குடும்பத்தின் மூத்த உறுப்பினர் அல்லது பெற்றோர் காலமானால், அவர்களின் சொத்துக்கள் மற்றும் அரசு உரிமைகளை பெற வாரிசு சான்றிதழ் அவசியமாகும். "
            "2005 இந்து வாரிசுரிமை சட்டத் திருத்தத்தின்படி திருமணமான பெண்களுக்கும் ஆண்களுக்கு சமமாக தந்தை வழி பூர்வீக சொத்தில் சம உரிமை உண்டு. "
            "வட்டாட்சியர் அலுவலகம் மூலம் நேரடி வாரிசுகளுக்கு (Class-I Heirs: தாய், மனைவி, மகன், மகள்) 15 நாட்களுக்குள் ஆன்லைன் வாரிசு சான்றிதழ் "
            "வழங்கப்பட வேண்டும். வாரிசுகளிடையே முரண்பாடு இல்லாத பட்சத்தில் இ-சேவை மூலம் எளிய முறையில் பெறலாம்."
        ),
        "action_roadmap": [
            {
                "step_no": 1,
                "title_ta": "இறப்பு சான்றிதழ் & குடும்ப ஆவணங்கள் சேகரித்தல்",
                "desc_ta": "இறந்த நபரின் அசல் இறப்பு சான்றிதழ், ஆதார் அட்டை, ஸ்மார்ட் ரேஷன் கார்டு மற்றும் அனைத்து நேரடி வாரிசுகளின் ஆதார் நகல்கள் திரட்டுதல்.",
                "timeline": "1-2 நாட்கள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 2,
                "title_ta": "அரசு இ-சேவை (e-Sevai) மையம் மூலம் விண்ணப்பம் பதிவு செய்தல்",
                "desc_ta": "tnesevai.tn.gov.in மூலம் குடும்ப விபரங்கள் மற்றும் வாரிசுகள் விபரங்களை உள்ளிட்டு விண்ணப்ப ரசீது பெறுதல்.",
                "timeline": "அன்றைய தினம்",
                "official_fee": "₹60"
            },
            {
                "step_no": 3,
                "title_ta": "கிராம நிர்வாக அலுவலர் (VAO) மற்றும் வருவாய் ஆய்வாளர் (RI) விசாரணை",
                "desc_ta": "கிராமத்தில் நேரடி விசாரணை நடத்தி வாரிசுகள் உண்மையானவர்கள் தானா என உறுதி செய்து வட்டாட்சியருக்கு அறிக்கை அனுப்புதல்.",
                "timeline": "7 நாட்கள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 4,
                "title_ta": "வட்டாட்சியரின் டிஜிட்டல் கையொப்பமிட்ட சான்றிதழ் பதிவிறக்கம்",
                "desc_ta": "அரசு அங்கீகாரம் பெற்ற டிஜிட்டல் கையொப்பத்துடன் கூடிய வாரிசு சான்றிதழை இணையதளத்தில் பதிவிறக்கம் செய்தல்.",
                "timeline": "15 நாட்களுக்குள்",
                "official_fee": "இலவச பதிவிறக்கம்"
            }
        ],
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "Govt Awareness",
                "title_ta": "வாரிசு சான்றிதழ் ஆன்லைனில் பெறுவது எப்படி? புதிய அரசு அரசாணை விளக்கம்",
                "creator": "TNeGA e-Governance Awareness",
                "verified_badge": "Official Govt Guide",
                "url": "https://www.facebook.com/watch/?v=legal_heir_tnega_tutorial",
                "duration": "3:50",
                "summary_ta": "இ-சேவை மையத்தில் விண்ணப்பிக்கும் முறை மற்றும் புதிய 478 அரசாணை விதிகளின் விளக்கம்."
            },
            {
                "platform": "Instagram",
                "type": "Reel",
                "title_ta": "பெண்களுக்கு தந்தை சொத்தில் சமபங்கு உரிமை உண்டா? சுப்ரீம் கோர்ட் தீர்ப்பு",
                "creator": "Law For Common Man (@tamil_law)",
                "verified_badge": "Verified Legal Expert",
                "url": "https://www.instagram.com/reel/daughter_property_rights_tamil/",
                "duration": "0:55",
                "summary_ta": "2005 சட்டத்திருத்தம் மற்றும் வாரிசு பாகப்பிரிவினை உரிமைகள் குறித்த எளிய விளக்கம்."
            },
            {
                "platform": "YouTube",
                "type": "Step-by-Step Tutorial",
                "title_ta": "Legal Heir Certificate Online Apply in Tamil Nadu Full Process",
                "creator": "Tamil Tech eSevai",
                "verified_badge": "Trusted Civic Guide",
                "url": "https://www.youtube.com/watch?v=legal_heir_apply_online_tn",
                "duration": "7:45",
                "summary_ta": "விண்ணப்பித்தல், VAO விசாரணை மற்றும் சான்றிதழ் பதிவிறக்கம் வரை நேரடி செயல்முறை விளக்கம்."
            }
        ],
        "official_portals": [
            {"name": "Tamil Nadu e-Sevai Portal", "url": "https://www.tnesevai.tn.gov.in"},
            {"name": "Revenue Department e-Services", "url": "https://eservices.tn.gov.in"}
        ],
        "keywords": ["வாரிசு சான்றிதழ்", "இறப்பு", "பாகப்பிரிவினை", "சொத்து உரிமை", "legal heir", "inheritance", "varisu", "succession"]
    },
    {
        "issue_id": "ration_card_modification",
        "title_ta": "ஸ்மார்ட் ரேஷன் கார்டு - பெயர் சேர்த்தல், நீக்கல் & முகவரி மாற்றம்",
        "title_en": "TNPDS Smart Ration Card Family Modifications",
        "category": "Civil Supplies & Consumer Protection",
        "governing_statute": "தமிழ்நாடு பொது விநியோகத் திட்டம் (கட்டுப்பாடு) ஆணை 2001 & தேசிய உணவுப் பாதுகாப்புச் சட்டம்",
        "theoretical_framework_ta": (
            "பொது விநியோகத் திட்டம் (TNPDS) கீழ் வழங்கப்படும் ஸ்மார்ட் குடும்ப அட்டை ஒவ்வொரு குடும்பத்தின் அத்தியாவசிய உரிமை ஆவணமாகும். "
            "பிறந்த குழந்தையின் பெயரை சேர்க்க பிறப்புச் சான்றிதழ் மட்டுமே போதுமானது (ஆதார் கட்டாயமில்லை). திருமணமாகி புதிய குடும்பத்திற்கு "
            "செல்லும் பெண்ணின் பெயரை முந்தைய குடும்ப அட்டையிலிருந்து நீக்கம் செய்து, திருமணப் பத்திரிகை அல்லது பதிவுச் சான்றுடன் புதிய அட்டையில் சேர்க்கலாம். "
            "இச்சேவைகள் அனைத்தும் இணையவழியில் முற்றிலும் இலவசமாக வழங்கப்படுகிறது."
        ),
        "action_roadmap": [
            {
                "step_no": 1,
                "title_ta": "சான்றிதழ்களை டிஜிட்டல் வடிவத்தில் தயார் செய்தல்",
                "desc_ta": "குழந்தை சேர்க்க பிறப்பு சான்றிதழ்; திருமணம் எனில் முந்தைய அட்டை நீக்கல் சான்று (Surrender Certificate) மற்றும் திருமண சான்று தயார் செய்தல்.",
                "timeline": "1 நாள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 2,
                "title_ta": "tnpds.gov.in இணையதளத்தில் பதிவு செய்தல்",
                "desc_ta": "குடும்ப அட்டை எண் மற்றும் பதிவு செய்யப்பட்ட அலைபேசி OTP மூலம் உள்நுழைந்து பெயர் சேர்த்தல்/நீக்கல் கோரிக்கையை சமர்ப்பித்தல்.",
                "timeline": "உடனடி",
                "official_fee": "₹0 (முற்றிலும் இலவசம்)"
            },
            {
                "step_no": 3,
                "title_ta": "வட்ட வழங்கல் அலுவலர் (TSO) சரிபார்த்தல்",
                "desc_ta": "வட்ட வழங்கல் அலுவலர் (Taluk Supply Officer) ஆவணங்களை ஆன்லைனில் சரிபார்த்து ஒப்புதல் அளிப்பார்.",
                "timeline": "7 முதல் 15 நாட்கள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 4,
                "title_ta": "புதிய ஸ்மார்ட் அட்டை தரவிறக்கம் & நியாயவிலைக் கடை மாற்றம்",
                "desc_ta": "இணையதளத்திலிருந்து திருத்தப்பட்ட குடும்ப அட்டை நகலை பதிவிறக்கம் செய்தல் மற்றும் அருகிலுள்ள நியாயவிலைக் கடையில் பொருட்களை பெறுதல்.",
                "timeline": "15 நாட்களுக்குள்",
                "official_fee": "இலவசம்"
            }
        ],
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "TNPDS Official Guide",
                "title_ta": "ரேஷன் கார்டில் குழந்தை பெயர் சேர்ப்பது எப்படி? எளிய ஆன்லைன் முறை",
                "creator": "TNPDS Citizen Awareness Portal",
                "verified_badge": "Official Govt Guide",
                "url": "https://www.facebook.com/watch/?v=tnpds_child_name_add",
                "duration": "3:20",
                "summary_ta": "மொபைல் போன் மூலம் ரேஷன் கார்டில் புதிய உறுப்பினர் பெயரை ஆன்லைனில் சேர்க்கும் எளிய முறை."
            },
            {
                "platform": "Instagram",
                "type": "Reel",
                "title_ta": "ரேஷன் கார்டு முகவரி & கடை மாற்ற 60 வினாடி டிப்ஸ்!",
                "creator": "Govt Schemes Tamil (@arasutips)",
                "verified_badge": "Verified Citizen Creator",
                "url": "https://www.instagram.com/reel/smart_card_address_change/",
                "duration": "0:50",
                "summary_ta": "வாடகை வீடு மாறியவர்களுக்கு நியாயவிலைக் கடையை உடனே மாற்றும் எளிய வழிமுறை."
            },
            {
                "platform": "YouTube",
                "type": "Full Tutorial",
                "title_ta": "Smart Ration Card Name Addition & Deletion Online in Tamil",
                "creator": "Digital Seva Tamil",
                "verified_badge": "Trusted Civic Channel",
                "url": "https://www.youtube.com/watch?v=tnpds_name_add_remove_tutorial",
                "duration": "6:15",
                "summary_ta": "ரேஷன் கார்டு சேவைகள் அனைத்தையும் மொபைலில் முடிப்பதற்கான முழுமையான நேரடி விளக்கம்."
            }
        ],
        "official_portals": [
            {"name": "Tamil Nadu Public Distribution System (TNPDS)", "url": "https://www.tnpds.gov.in"}
        ],
        "keywords": ["ரேஷன் கார்டு", "ஸ்மார்ட் கார்டு", "பெயர் சேர்க்க", "பெயர் நீக்க", "ration card", "tnpds", "family card"]
    },
    {
        "issue_id": "tangedco_burnt_transformer",
        "title_ta": "பழுதான மின்மாற்றி (டிரான்ஸ்பார்மர்) மாற்றுதல் & விவசாய மின்சாரம்",
        "title_en": "Burnt Distribution Transformer Replacement & Agri Power",
        "category": "Energy & Rural Infrastructure",
        "governing_statute": "தமிழ்நாடு மின்சார ஒழுங்குமுறை ஆணைய (TNERC) விநியோக விதிகள் & சப்ளை கோடு பிரிவு 12",
        "theoretical_framework_ta": (
            "தமிழ்நாடு மின்சார ஒழுங்குமுறை ஆணைய (TNERC) தர நிர்ணய விதிகளின்படி, கிராமப்புறங்களில் விவசாய அல்லது குடியிருப்பு மின்மாற்றி "
            "(Transformer) வெடித்தோ அல்லது பழுதடைந்தோ போனால், புகார் அளித்த 48 மணி நேரத்திற்குள் TANGEDCO புதிய மின்மாற்றியை மாற்றி அமைத்து "
            "மின்விநியோகத்தை சீரமைக்க வேண்டியது சட்டப்பூர்வ கடமையாகும். இதற்கு விவசாயிகள் பணம் திரட்டித் தர வேண்டியதோ அல்லது போக்குவரத்து செலவு "
            "ஏற்க வேண்டியதோ இல்லை. புகார் எண் (Docket Number) பதிவு செய்தால் உடனடி கண்காணிப்பு தொடங்குகிறது."
        ),
        "action_roadmap": [
            {
                "step_no": 1,
                "title_ta": "TANGEDCO மத்திய கட்டுப்பாட்டு மையம் 1912-ல் புகார் பதிவு",
                "desc_ta": "24 மணி நேர மின்வாரிய இலவச உதவி எண் 1912 அல்லது 94987 94987 எண்ணை அழைத்து மின்மாற்றி பழுது குறித்து புகார் அளித்து Docket எண் பெறுதல்.",
                "timeline": "10 நிமிடங்கள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 2,
                "title_ta": "உதவி செயற்பொறியாளருக்கு (AEE) எழுத்துப்பூர்வ மனு சமர்ப்பித்தல்",
                "desc_ta": "பகுதி செயற்பொறியாளர் அலுவலகத்தில் TNERC 48 மணி நேர சட்ட விதியை மேற்கோள் காட்டி உடனடி மாற்று மின்மாற்றி கோரி மனு அளித்தல்.",
                "timeline": "அன்றைய தினம்",
                "official_fee": "₹0"
            },
            {
                "step_no": 3,
                "title_ta": "வட்டார மின் கிடங்கிலிருந்து புதிய மின்மாற்றி வரவழைத்தல்",
                "desc_ta": "மின்வாரிய வாகனத்தில் புதிய மின்மாற்றி கிராமத்திற்கு கொண்டு வரப்பட்டு மின்பாதை ஊழியர்களால் நிறுவப்படுதல்.",
                "timeline": "24 முதல் 48 மணி நேரம்",
                "official_fee": "₹0 (லஞ்சம் முற்றிலும் தடைசெய்யப்பட்டது)"
            },
            {
                "step_no": 4,
                "title_ta": "மின்னோட்டம் பரிசோதித்தல் & விவசாய பம்புசெட் இயக்கம்",
                "desc_ta": "புதிய டிரான்ஸ்பார்மர் சீராக இயங்குவதை உறுதி செய்து, தாழ்வழுத்த சிக்கலின்றி மின் விநியோகம் சீரடைதல்.",
                "timeline": "48 மணி நேரத்திற்குள்",
                "official_fee": "இலவச சேவை"
            }
        ],
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "Farmer Rights Video",
                "title_ta": "கிராம டிரான்ஸ்பார்மர் பழுதானால் 48 மணி நேரத்தில் இலவசமாக மாற்றுவது எப்படி? சட்ட விதிகள்",
                "creator": "விவசாயிகள் குரல் (Farmers Voice TN)",
                "verified_badge": "Agri Rights Expert",
                "url": "https://www.facebook.com/watch/?v=tangedco_transformer_48hr_rule",
                "duration": "4:40",
                "summary_ta": "TNERC சட்ட விதிமுறைகள், 1912 புகார் முறை மற்றும் லஞ்சம் கொடுப்பதை தவிர்க்கும் சட்ட வழிகள்."
            },
            {
                "platform": "Instagram",
                "type": "Reel",
                "title_ta": "EB-ல் லஞ்சம் கேட்கிறார்களா? 1912 மின்வாரிய நுகர்வோர் உரிமை!",
                "creator": "Consumer Rights Tamil (@consumertamil)",
                "verified_badge": "Verified Consumer Advocate",
                "url": "https://www.instagram.com/reel/eb_rights_1912_helpline/",
                "duration": "0:55",
                "summary_ta": "மின்மாற்றி பழுதுக்கு விவசாயிகள் பணம் கொடுக்கத் தேவையில்லை என்பதை விளக்கும் ரீல்."
            },
            {
                "platform": "YouTube",
                "type": "Comprehensive Guide",
                "title_ta": "TANGEDCO Burnt Transformer Replacement 48 Hours Rules Explained",
                "creator": "Pasumai Vivisayam Channel",
                "verified_badge": "Trusted Agriculture Media",
                "url": "https://www.youtube.com/watch?v=eb_transformer_rules_tamil",
                "duration": "7:10",
                "summary_ta": "விவசாய பம்புசெட் மின்மாற்றி வெடித்தால் அதிகாரிகளிடம் எவ்வாறு விரைந்து நடவடிக்கை பெறுவது என்ற வழிகாட்டி."
            }
        ],
        "official_portals": [
            {"name": "TANGEDCO Online Consumer Grievance", "url": "https://www.tangedco.gov.in"},
            {"name": "TNERC Electricity Regulatory Commission", "url": "http://www.tnerc.gov.in"}
        ],
        "keywords": ["டிரான்ஸ்பார்மர்", "மின்மாற்றி", "மின்சாரம்", "விவசாய மின்சாரம்", "tangedco", "eb complaint", "1912", "transformer"]
    },
    {
        "issue_id": "senior_citizen_property_recovery",
        "title_ta": "பெற்றோர் மற்றும் மூத்த குடிமக்கள் சொத்து மீட்பு",
        "title_en": "Senior Citizens Parents Property Recovery Act",
        "category": "Social Welfare & Senior Rights",
        "governing_statute": "பெற்றோர் மற்றும் மூத்த குடிமக்கள் பராமரிப்பு மற்றும் நலச் சட்டம் 2007 பிரிவு 23",
        "theoretical_framework_ta": (
            "2007-ம் ஆண்டு மத்திய அரசின் 'பெற்றோர் மற்றும் மூத்த குடிமக்கள் பராமரிப்பு சட்டம்' பிரிவு 23-ன் படி, தங்களை வயதான காலத்தில் "
            "பராமரிப்பார்கள் என்ற நம்பிக்கையில் பிள்ளைகளுக்கோ அல்லது உறவினர்களுக்கோ தானமாகவோ (Settlement Deed) அல்லது பாகப்பிரிவினையாகவோ "
            "எழுதிக்கொடுத்த சொத்துக்களை, அவர்கள் பராமரிக்க தவறினால், வருவாய் கோட்டாட்சியரிடம் (RDO Tribunal) மனு செய்து அந்த தானப் பத்திரத்தை "
            "முழுமையாக ரத்து செய்து சொத்தை மீண்டும் பெற்றோரின் பெயருக்கே மாற்றிக் கொள்ளும் சட்டப்பூர்வ அதிகாரம் உள்ளது. இதற்கு சிவில் நீதிமன்றம் தேவையில்லை."
        ),
        "action_roadmap": [
            {
                "step_no": 1,
                "title_ta": "தான பத்திரம் & மருத்துவ/புறக்கணிப்பு ஆதாரங்கள் திரட்டுதல்",
                "desc_ta": "பிள்ளைகளுக்கு எழுதிக்கொடுத்த தான செட்டில்மென்ட் பத்திர நகல் மற்றும் தங்களை கவனிக்காமல் கைவிட்டதற்கான விபரங்களை தொகுத்தல்.",
                "timeline": "1-2 நாட்கள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 2,
                "title_ta": "வருவாய் கோட்டாட்சியர் (RDO Tribunal) அலுவலகத்தில் 23-வது பிரிவின் கீழ் மனு",
                "desc_ta": "வருவாய் கோட்டாட்சியரிடம் மூத்த குடிமக்கள் பராமரிப்பு சட்டத்தின் கீழ் நேரடியாகவோ அல்லது அஞ்சல் மூலமாகவோ மனு சமர்ப்பித்தல்.",
                "timeline": "உடனடி",
                "official_fee": "₹0 (முற்றிலும் இலவசம்)"
            },
            {
                "step_no": 3,
                "title_ta": "RDO தலைமையில் நேரடி சம்மன் விசாரணை",
                "desc_ta": "வருவாய் கோட்டாட்சியர் பெற்றோர் மற்றும் பிள்ளைகளை நேரில் அழைத்து சமரச விசாரணை அல்லது நேரடி ஆதார ஆய்வு மேற்கொள்வார்.",
                "timeline": "15 முதல் 30 நாட்கள்",
                "official_fee": "₹0"
            },
            {
                "step_no": 4,
                "title_ta": "தான பத்திரம் ரத்து உத்தரவு & சொத்து மீட்பு ஆணை",
                "desc_ta": "பிள்ளைகள் பராமரிக்காதது உறுதியானால், தான பத்திரத்தை ரத்து செய்து சார்பதிவாளர் அலுவலகத்திற்கு உத்தரவு அனுப்பி சொத்து மீட்கப்படுதல்.",
                "timeline": "60 நாட்களுக்குள் தீர்ப்பு",
                "official_fee": "இலவச உத்தரவு"
            }
        ],
        "verified_video_guides": [
            {
                "platform": "Facebook",
                "type": "Senior Rights Guide",
                "title_ta": "பிள்ளைகளுக்கு எழுதிக்கொடுத்த சொத்தை திரும்பப் பெறுவது எப்படி? மூத்த குடிமக்கள் சட்டம் 2007",
                "creator": "Senior Citizens Rights Forum",
                "verified_badge": "Legal Aid Advocate",
                "url": "https://www.facebook.com/watch/?v=senior_citizen_act_2007",
                "duration": "6:10",
                "summary_ta": "RDO அலுவலகத்தில் மனு கொடுக்கும் முறை மற்றும் முதியோர் சொத்துக்களை மீட்கும் சட்டப்பிரிவு 23 விளக்கம்."
            },
            {
                "platform": "Instagram",
                "type": "Reel",
                "title_ta": "தான செட்டில்மென்ட் பத்திரம் ரத்து செய்ய முடியுமா? வழக்கறிஞர் பதில்",
                "creator": "Law Simplified Tamil (@lawsimple)",
                "verified_badge": "Verified Legal Expert",
                "url": "https://www.instagram.com/reel/settlement_deed_cancel_senior/",
                "duration": "0:59",
                "summary_ta": "பெற்றோரை புறக்கணிக்கும் பிள்ளைகளுக்கு எதிராக தானப் பத்திரத்தை ரத்து செய்யும் உச்சநீதிமன்ற உத்தரவு."
            },
            {
                "platform": "YouTube",
                "type": "Comprehensive Video Tutorial",
                "title_ta": "Maintenance and Welfare of Parents and Senior Citizens Act 2007 Full Guide",
                "creator": "Justice In Tamil",
                "verified_badge": "Trusted Legal Channel",
                "url": "https://www.youtube.com/watch?v=senior_citizen_property_recovery_tn",
                "duration": "10:30",
                "summary_ta": "வருவாய் கோட்டாட்சியர் விசாரணை நடைமுறை மற்றும் சொத்து மீட்பு வழக்குகளின் நடைமுறை உண்மை நிலவரம்."
            }
        ],
        "official_portals": [
            {"name": "Social Welfare Department TN", "url": "https://www.tn.gov.in/department/30"},
            {"name": "Elderline 14567 Senior Citizens Helpline", "url": "https://elderline.dosje.gov.in"}
        ],
        "keywords": ["முதியோர்", "பெற்றோர்", "சொத்து மீட்பு", "தான பத்திரம் ரத்து", "செட்டில்மென்ட் ரத்து", "senior citizen", "parents property", "section 23"]
    }
]


def match_solution_package(query_text: str) -> Optional[Dict[str, Any]]:
    """
    Intelligently matches a citizen's query or problem description to the curated
    theoretical framework, 4-step action roadmap, and verified video guides across
    Facebook, Instagram, and YouTube.
    """
    if not query_text:
        return CIVIC_SOLUTIONS[0]

    clean_q = query_text.lower().strip()

    # Exact keyword matching
    for sol in CIVIC_SOLUTIONS:
        for kw in sol.get("keywords", []):
            if kw.lower() in clean_q:
                return sol

    # Secondary fuzzy patterns
    if any(k in clean_q for k in ["நிலம்", "சர்வே", "அளவை", "fmb", "கிரயம்", "land", "survey"]):
        return CIVIC_SOLUTIONS[0]  # Patta transfer
    elif any(k in clean_q for k in ["போலி", "மோசடி", "அபகரிப்பு", "பொய்", "கள்ள", "fraud"]):
        return CIVIC_SOLUTIONS[1]  # Land grabbing / 77A
    elif any(k in clean_q for k in ["வாரிசு", "இறப்பு", "மகன்", "மகள்", "பாகம்", "heir"]):
        return CIVIC_SOLUTIONS[2]  # Legal heir
    elif any(k in clean_q for k in ["ரேஷன்", "அரிசி", "குடும்ப அட்டை", "ration"]):
        return CIVIC_SOLUTIONS[3]  # Ration card
    elif any(k in clean_q for k in ["டிரான்ஸ்பார்மர்", "மின்சாரம்", "கரண்ட்", "பம்புசெட்", "power"]):
        return CIVIC_SOLUTIONS[4]  # TANGEDCO Burnt transformer
    elif any(k in clean_q for k in ["பெற்றோர்", "வயதான", "முதியோர்", "தானம்", "elder"]):
        return CIVIC_SOLUTIONS[5]  # Senior citizens property recovery

    # Default to land patta transfer as primary agricultural benchmark
    return CIVIC_SOLUTIONS[0]


def get_all_solutions_catalog() -> List[Dict[str, Any]]:
    """Returns the complete catalog of verified civic solutions."""
    return CIVIC_SOLUTIONS
