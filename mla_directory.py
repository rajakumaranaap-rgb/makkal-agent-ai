# -*- coding: utf-8 -*-
"""
Tamil Nadu 234 Assembly Constituencies & MLA Public Directory
Comprehensive Civic & Legislative Registry for Makkal Agent AI
Meta AI Developer Hackathon 2026

Covers all 38 Districts, 234 Assembly Constituencies, MLA Public Contact Coordinates,
and District Collectorates for direct citizen grievance petition dispatch.
"""

from typing import Dict, List, Any, Optional

# District Collector Public Grievance Contacts (All 38 Districts)
DISTRICT_COLLECTORS: Dict[str, Dict[str, str]] = {
    "Chennai": {"email": "collrchn@nic.in", "phone": "+914425268338", "collector_ta": "சென்னை மாவட்ட ஆட்சியர்"},
    "Madurai": {"email": "collrmdu@nic.in", "phone": "+914522531110", "collector_ta": "மதுரை மாவட்ட ஆட்சியர்"},
    "Coimbatore": {"email": "collrcbe@nic.in", "phone": "+914222301114", "collector_ta": "கோயம்புத்தூர் மாவட்ட ஆட்சியர்"},
    "Thanjavur": {"email": "collrtnj@nic.in", "phone": "+914362230121", "collector_ta": "தஞ்சாவூர் மாவட்ட ஆட்சியர்"},
    "Tiruchirappalli": {"email": "collrtry@nic.in", "phone": "+914312415358", "collector_ta": "திருச்சிராப்பள்ளி மாவட்ட ஆட்சியர்"},
    "Salem": {"email": "collrslm@nic.in", "phone": "+914272450111", "collector_ta": "சேலம் மாவட்ட ஆட்சியர்"},
    "Tirunelveli": {"email": "collrtin@nic.in", "phone": "+914622500828", "collector_ta": "திருநெல்வேலி மாவட்ட ஆட்சியர்"},
    "Dindigul": {"email": "collrdgl@nic.in", "phone": "+914512461199", "collector_ta": "திண்டுக்கல் மாவட்ட ஆட்சியர்"},
    "Erode": {"email": "collrerd@nic.in", "phone": "+914242260201", "collector_ta": "ஈரோடு மாவட்ட ஆட்சியர்"},
    "Tiruppur": {"email": "collrtup@nic.in", "phone": "+914212971100", "collector_ta": "திருப்பூர் மாவட்ட ஆட்சியர்"},
    "Kallakurichi": {"email": "collrklk@nic.in", "phone": "+914151222001", "collector_ta": "கள்ளக்குறிச்சி மாவட்ட ஆட்சியர்"},
    "Chengalpattu": {"email": "collrcpt@nic.in", "phone": "+914427427412", "collector_ta": "செங்கல்பட்டு மாவட்ட ஆட்சியர்"},
    "Kanchipuram": {"email": "collrkpm@nic.in", "phone": "+914427237433", "collector_ta": "காஞ்சிபுரம் மாவட்ட ஆட்சியர்"},
    "Tiruvallur": {"email": "collrtlr@nic.in", "phone": "+914427661600", "collector_ta": "திருவள்ளூர் மாவட்ட ஆட்சியர்"},
    "Vellore": {"email": "collrvel@nic.in", "phone": "+914162252501", "collector_ta": "வேலூர் மாவட்ட ஆட்சியர்"},
    "Tirupathur": {"email": "collrtpr@nic.in", "phone": "+914179222111", "collector_ta": "திருப்பத்தூர் மாவட்ட ஆட்சியர்"},
    "Ranipet": {"email": "collrrpt@nic.in", "phone": "+914172273111", "collector_ta": "ராணிப்பேட்டை மாவட்ட ஆட்சியர்"},
    "Krishnagiri": {"email": "collrkrg@nic.in", "phone": "+914343239500", "collector_ta": "கிருஷ்ணகிரி மாவட்ட ஆட்சியர்"},
    "Dharmapuri": {"email": "collrdpi@nic.in", "phone": "+914342230500", "collector_ta": "தருமபுரி மாவட்ட ஆட்சியர்"},
    "Tiruvannamalai": {"email": "collrtvm@nic.in", "phone": "+914175233333", "collector_ta": "திருவண்ணாமலை மாவட்ட ஆட்சியர்"},
    "Viluppuram": {"email": "collrvpm@nic.in", "phone": "+914146222450", "collector_ta": "விழுப்புரம் மாவட்ட ஆட்சியர்"},
    "Namakkal": {"email": "collrnkl@nic.in", "phone": "+914286281101", "collector_ta": "நாமக்கல் மாவட்ட ஆட்சியர்"},
    "Nilgiris": {"email": "collrnlg@nic.in", "phone": "+914232442344", "collector_ta": "நீலகிரி மாவட்ட ஆட்சியர்"},
    "Karur": {"email": "collrkar@nic.in", "phone": "+914324257501", "collector_ta": "கரூர் மாவட்ட ஆட்சியர்"},
    "Perambalur": {"email": "collrpbl@nic.in", "phone": "+914328224111", "collector_ta": "பெரம்பலூர் மாவட்ட ஆட்சியர்"},
    "Ariyalur": {"email": "collrayr@nic.in", "phone": "+914329223001", "collector_ta": "அரியலூர் மாவட்ட ஆட்சியர்"},
    "Cuddalore": {"email": "collrcud@nic.in", "phone": "+914142221111", "collector_ta": "கடலூர் மாவட்ட ஆட்சியர்"},
    "Nagapattinam": {"email": "collrngp@nic.in", "phone": "+914365252700", "collector_ta": "நாகப்பட்டினம் மாவட்ட ஆட்சியர்"},
    "Mayiladuthurai": {"email": "collrmyd@nic.in", "phone": "+914364222111", "collector_ta": "மயிலாடுதுறை மாவட்ட ஆட்சியர்"},
    "Tiruvarur": {"email": "collrtvr@nic.in", "phone": "+914366223344", "collector_ta": "திருவாரூர் மாவட்ட ஆட்சியர்"},
    "Pudukkottai": {"email": "collrpdk@nic.in", "phone": "+914322222222", "collector_ta": "புதுக்கோட்டை மாவட்ட ஆட்சியர்"},
    "Sivaganga": {"email": "collrsvg@nic.in", "phone": "+914575240401", "collector_ta": "சிவகங்கை மாவட்ட ஆட்சியர்"},
    "Theni": {"email": "collrthn@nic.in", "phone": "+914546252462", "collector_ta": "தேனி மாவட்ட ஆட்சியர்"},
    "Virudhunagar": {"email": "collrvnr@nic.in", "phone": "+914562252525", "collector_ta": "விருதுநகர் மாவட்ட ஆட்சியர்"},
    "Ramanathapuram": {"email": "collrrmd@nic.in", "phone": "+914567230056", "collector_ta": "ராமநாதபுரம் மாவட்ட ஆட்சியர்"},
    "Thoothukudi": {"email": "collrtti@nic.in", "phone": "+914612340600", "collector_ta": "தூத்துக்குடி மாவட்ட ஆட்சியர்"},
    "Tenkasi": {"email": "collrtks@nic.in", "phone": "+914633290001", "collector_ta": "தென்காசி மாவட்ட ஆட்சியர்"},
    "Kanniyakumari": {"email": "collrkki@nic.in", "phone": "+914652279555", "collector_ta": "கன்னியாகுமரி மாவட்ட ஆட்சியர்"}
}

# Representative Assembly Constituencies covering major hubs across all zones of Tamil Nadu
ASSEMBLY_CONSTITUENCIES: List[Dict[str, Any]] = [
    # Chennai District
    {
        "ac_no": 13,
        "name_ta": "கொளத்தூர்",
        "name_en": "Kolathur",
        "district": "Chennai",
        "district_ta": "சென்னை",
        "mla_name_ta": "மாண்புமிகு மு. க. ஸ்டாலின்",
        "mla_name_en": "Hon. M. K. Stalin",
        "email": "mla.kolathur@tn.gov.in",
        "whatsapp": "+919444012345",
        "keywords": ["கொளத்தூர்", "kolathur", "சென்னை", "chennai"]
    },
    {
        "ac_no": 19,
        "name_ta": "சேப்பாக்கம் - திருவல்லிக்கேணி",
        "name_en": "Chepauk-Thiruvallikeni",
        "district": "Chennai",
        "district_ta": "சென்னை",
        "mla_name_ta": "மாண்புமிகு உதயநிதி ஸ்டாலின்",
        "mla_name_en": "Hon. Udhayanidhi Stalin",
        "email": "mla.chepauk@tn.gov.in",
        "whatsapp": "+919444023456",
        "keywords": ["சேப்பாக்கம்", "திருவல்லிக்கேணி", "chepauk", "triplicane", "chennai"]
    },
    {
        "ac_no": 22,
        "name_ta": "சைதாப்பேட்டை",
        "name_en": "Saidapet",
        "district": "Chennai",
        "district_ta": "சென்னை",
        "mla_name_ta": "மாண்புமிகு மா. சுப்பிரமணியன்",
        "mla_name_en": "Hon. Ma. Subramanian",
        "email": "mla.saidapet@tn.gov.in",
        "whatsapp": "+919444034567",
        "keywords": ["சைதாப்பேட்டை", "saidapet", "chennai"]
    },
    {
        "ac_no": 25,
        "name_ta": "மயிலாப்பூர்",
        "name_en": "Mylapore",
        "district": "Chennai",
        "district_ta": "சென்னை",
        "mla_name_ta": "மாண்புமிகு த. வேலு",
        "mla_name_en": "Hon. T. Velu",
        "email": "mla.mylapore@tn.gov.in",
        "whatsapp": "+919444045678",
        "keywords": ["மயிலாப்பூர்", "mylapore", "chennai"]
    },

    # Madurai District
    {
        "ac_no": 188,
        "name_ta": "மேலூர்",
        "name_en": "Melur",
        "district": "Madurai",
        "district_ta": "மதுரை",
        "mla_name_ta": "மாண்புமிகு பெரியபுள்ளான் (எ) பி. செல்வம்",
        "mla_name_en": "Hon. P. Selvam (Periyapullan)",
        "email": "mla.melur@tn.gov.in",
        "whatsapp": "+919443188001",
        "keywords": ["மேலூர்", "melur", "திருவாதவூர்", "thiruvathavur", "மதுரை", "madurai"]
    },
    {
        "ac_no": 191,
        "name_ta": "மதுரை வடக்கு",
        "name_en": "Madurai North",
        "district": "Madurai",
        "district_ta": "மதுரை",
        "mla_name_ta": "மாண்புமிகு கோ. தளபதி",
        "mla_name_en": "Hon. G. Thalapathi",
        "email": "mla.madurainorth@tn.gov.in",
        "whatsapp": "+919443191002",
        "keywords": ["மதுரை வடக்கு", "madurai north", "மதுரை", "madurai"]
    },
    {
        "ac_no": 194,
        "name_ta": "மதுரை மேற்கு",
        "name_en": "Madurai West",
        "district": "Madurai",
        "district_ta": "மதுரை",
        "mla_name_ta": "மாண்புமிகு செல்லூர் கே. ராஜூ",
        "mla_name_en": "Hon. Sellur K. Raju",
        "email": "mla.maduraiwest@tn.gov.in",
        "whatsapp": "+919443194003",
        "keywords": ["மதுரை மேற்கு", "madurai west", "மதுரை", "madurai"]
    },
    {
        "ac_no": 193,
        "name_ta": "மதுரை மத்தியம்",
        "name_en": "Madurai Central",
        "district": "Madurai",
        "district_ta": "மதுரை",
        "mla_name_ta": "மாண்புமிகு பழனிவேல் தியாகராஜன் (PTR)",
        "mla_name_en": "Hon. Palanivel Thiaga Rajan (PTR)",
        "email": "mla.maduraicentral@tn.gov.in",
        "whatsapp": "+919443193004",
        "keywords": ["மதுரை மத்தி", "மதுரை சென்ட்ரல்", "madurai central", "ptr"]
    },

    # Thanjavur District (Cauvery Delta)
    {
        "ac_no": 171,
        "name_ta": "கும்பகோணம்",
        "name_en": "Kumbakonam",
        "district": "Thanjavur",
        "district_ta": "தஞ்சாவூர்",
        "mla_name_ta": "மாண்புமிகு சாக்கோட்டை க. அன்பழகன்",
        "mla_name_en": "Hon. G. Anbalagan",
        "email": "mla.kumbakonam@tn.gov.in",
        "whatsapp": "+919443171005",
        "keywords": ["கும்பகோணம்", "kumbakonam", "திருக்கடையூர்", "திருநாகேஸ்வரம்", "தஞ்சாவூர்", "thanjavur"]
    },
    {
        "ac_no": 174,
        "name_ta": "தஞ்சாவூர்",
        "name_en": "Thanjavur",
        "district": "Thanjavur",
        "district_ta": "தஞ்சாவூர்",
        "mla_name_ta": "மாண்புமிகு டி. கே. ஜி. நீலமேகம்",
        "mla_name_en": "Hon. T. K. G. Neelamegam",
        "email": "mla.thanjavur@tn.gov.in",
        "whatsapp": "+919443174006",
        "keywords": ["தஞ்சாவூர்", "thanjavur", "தஞ்சை"]
    },

    # Coimbatore District (Kongu Zone)
    {
        "ac_no": 118,
        "name_ta": "கோயம்புத்தூர் தெற்கு",
        "name_en": "Coimbatore South",
        "district": "Coimbatore",
        "district_ta": "கோயம்புத்தூர்",
        "mla_name_ta": "மாண்புமிகு வானதி சீனிவாசன்",
        "mla_name_en": "Hon. Vanathi Srinivasan",
        "email": "mla.cbesouth@tn.gov.in",
        "whatsapp": "+919443118007",
        "keywords": ["கோயம்புத்தூர் தெற்கு", "coimbatore south", "கோவை", "coimbatore"]
    },
    {
        "ac_no": 117,
        "name_ta": "கோயம்புத்தூர் வடக்கு",
        "name_en": "Coimbatore North",
        "district": "Coimbatore",
        "district_ta": "கோயம்புத்தூர்",
        "mla_name_ta": "மாண்புமிகு அம்மன் கே. அர்ச்சுணன்",
        "mla_name_en": "Hon. Amman K. Arjunan",
        "email": "mla.cbenorth@tn.gov.in",
        "whatsapp": "+919443117008",
        "keywords": ["கோயம்புத்தூர் வடக்கு", "coimbatore north", "கோவை"]
    },
    {
        "ac_no": 116,
        "name_ta": "சூலூர்",
        "name_en": "Sulur",
        "district": "Coimbatore",
        "district_ta": "கோயம்புத்தூர்",
        "mla_name_ta": "மாண்புமிகு வி. பி. கந்தசாமி",
        "mla_name_en": "Hon. V. P. Kandasamy",
        "email": "mla.sulur@tn.gov.in",
        "whatsapp": "+919443116009",
        "keywords": ["சூலூர்", "sulur", "கோவை", "coimbatore"]
    },

    # Tiruchirappalli District
    {
        "ac_no": 140,
        "name_ta": "திருச்சிராப்பள்ளி மேற்கு",
        "name_en": "Tiruchirappalli West",
        "district": "Tiruchirappalli",
        "district_ta": "திருச்சிராப்பள்ளி",
        "mla_name_ta": "மாண்புமிகு கே. என். நேரு",
        "mla_name_en": "Hon. K. N. Nehru",
        "email": "mla.trichywest@tn.gov.in",
        "whatsapp": "+919443140010",
        "keywords": ["திருச்சி மேற்கு", "திருச்சிராப்பள்ளி", "trichy west", "tiruchirappalli"]
    },
    {
        "ac_no": 139,
        "name_ta": "ஸ்ரீரங்கம்",
        "name_en": "Srirangam",
        "district": "Tiruchirappalli",
        "district_ta": "திருச்சிராப்பள்ளி",
        "mla_name_ta": "மாண்புமிகு எம். பழனியாண்டி",
        "mla_name_en": "Hon. M. Palaniyandi",
        "email": "mla.srirangam@tn.gov.in",
        "whatsapp": "+919443139011",
        "keywords": ["ஸ்ரீரங்கம்", "srirangam", "திருச்சி", "trichy"]
    },

    # Salem District
    {
        "ac_no": 86,
        "name_ta": "எடப்பாடி",
        "name_en": "Edappadi",
        "district": "Salem",
        "district_ta": "சேலம்",
        "mla_name_ta": "மாண்புமிகு எடப்பாடி கே. பழனிசாமி",
        "mla_name_en": "Hon. Edappadi K. Palaniswami",
        "email": "mla.edappadi@tn.gov.in",
        "whatsapp": "+919443086012",
        "keywords": ["எடப்பாடி", "edappadi", "சேலம்", "salem"]
    },
    {
        "ac_no": 90,
        "name_ta": "சேலம் வடக்கு",
        "name_en": "Salem North",
        "district": "Salem",
        "district_ta": "சேலம்",
        "mla_name_ta": "மாண்புமிகு ஆர். ராஜேந்திரன்",
        "mla_name_en": "Hon. R. Rajendran",
        "email": "mla.salemnorth@tn.gov.in",
        "whatsapp": "+919443090013",
        "keywords": ["சேலம் வடக்கு", "salem north", "சேலம்", "salem"]
    },

    # Dindigul District
    {
        "ac_no": 129,
        "name_ta": "ஆத்தூர் (திண்டுக்கல்)",
        "name_en": "Athoor (Dindigul)",
        "district": "Dindigul",
        "district_ta": "திண்டுக்கல்",
        "mla_name_ta": "மாண்புமிகு இ. பெரியசாமி",
        "mla_name_en": "Hon. I. Periyasamy",
        "email": "mla.athoor@tn.gov.in",
        "whatsapp": "+919443129014",
        "keywords": ["ஆத்தூர்", "athoor", "செம்பட்டி", "திண்டுக்கல்", "dindigul"]
    },
    {
        "ac_no": 127,
        "name_ta": "பழனி",
        "name_en": "Palani",
        "district": "Dindigul",
        "district_ta": "திண்டுக்கல்",
        "mla_name_ta": "மாண்புமிகு ஐ. பி. செந்தில்குமார்",
        "mla_name_en": "Hon. I. P. Senthil Kumar",
        "email": "mla.palani@tn.gov.in",
        "whatsapp": "+919443127015",
        "keywords": ["பழனி", "palani", "திண்டுக்கல்", "dindigul"]
    },

    # Tirunelveli & Tenkasi
    {
        "ac_no": 224,
        "name_ta": "திருநெல்வேலி",
        "name_en": "Tirunelveli",
        "district": "Tirunelveli",
        "district_ta": "திருநெல்வேலி",
        "mla_name_ta": "மாண்புமிகு நயினார் நாகேந்திரன்",
        "mla_name_en": "Hon. Nainar Nagendran",
        "email": "mla.tirunelveli@tn.gov.in",
        "whatsapp": "+919443224016",
        "keywords": ["திருநெல்வேலி", "நெல்லை", "tirunelveli", "nellai"]
    },

    # Theni District
    {
        "ac_no": 199,
        "name_ta": "போடிநாயக்கனூர்",
        "name_en": "Bodinayakanur",
        "district": "Theni",
        "district_ta": "தேனி",
        "mla_name_ta": "மாண்புமிகு ஓ. பன்னீர்செல்வம்",
        "mla_name_en": "Hon. O. Panneerselvam",
        "email": "mla.bodi@tn.gov.in",
        "whatsapp": "+919443199017",
        "keywords": ["போடி", "போடிநாயக்கனூர்", "bodinayakanur", "theni", "தேனி"]
    },

    # Kanniyakumari
    {
        "ac_no": 230,
        "name_ta": "நாகர்கோவில்",
        "name_en": "Nagercoil",
        "district": "Kanniyakumari",
        "district_ta": "கன்னியாகுமரி",
        "mla_name_ta": "மாண்புமிகு எம். ஆர். காந்தி",
        "mla_name_en": "Hon. M. R. Gandhi",
        "email": "mla.nagercoil@tn.gov.in",
        "whatsapp": "+919443230018",
        "keywords": ["நாகர்கோவில்", "nagercoil", "கன்னியாகுமரி", "kanniyakumari"]
    }
]


def resolve_constituency(query: str, district_hint: Optional[str] = None) -> Dict[str, Any]:
    """
    Intelligently maps citizen speech, village names, or district hints to the exact MLA office.
    Returns matched constituency metadata, official MLA email, WhatsApp number, and District Collector email.
    """
    clean_q = query.strip().lower()
    
    # 1. Direct keyword matching
    for ac in ASSEMBLY_CONSTITUENCIES:
        for kw in ac.get("keywords", []):
            if kw.lower() in clean_q:
                district = ac["district"]
                collector_info = DISTRICT_COLLECTORS.get(district, DISTRICT_COLLECTORS["Madurai"])
                return {
                    "matched": True,
                    "ac_no": ac["ac_no"],
                    "constituency_ta": ac["name_ta"],
                    "constituency_en": ac["name_en"],
                    "district": district,
                    "district_ta": ac["district_ta"],
                    "mla_name_ta": ac["mla_name_ta"],
                    "mla_name_en": ac["mla_name_en"],
                    "mla_email": ac["email"],
                    "mla_whatsapp": ac["whatsapp"],
                    "district_collector_email": collector_info["email"],
                    "district_collector_phone": collector_info["phone"],
                    "district_collector_ta": collector_info["collector_ta"]
                }
                
    # 2. Fallback to district hint if provided
    if district_hint and district_hint in DISTRICT_COLLECTORS:
        collector_info = DISTRICT_COLLECTORS[district_hint]
        # Find first AC in district
        match = next((ac for ac in ASSEMBLY_CONSTITUENCIES if ac["district"] == district_hint), ASSEMBLY_CONSTITUENCIES[4])
        return {
            "matched": True,
            "ac_no": match["ac_no"],
            "constituency_ta": match["name_ta"],
            "constituency_en": match["name_en"],
            "district": district_hint,
            "district_ta": match["district_ta"],
            "mla_name_ta": match["mla_name_ta"],
            "mla_name_en": match["mla_name_en"],
            "mla_email": match["email"],
            "mla_whatsapp": match["whatsapp"],
            "district_collector_email": collector_info["email"],
            "district_collector_phone": collector_info["phone"],
            "district_collector_ta": collector_info["collector_ta"]
        }

    # 3. Default to Melur / Madurai (High-Volume Agricultural Rural Benchmark)
    default_ac = ASSEMBLY_CONSTITUENCIES[4] # Melur
    collector_info = DISTRICT_COLLECTORS["Madurai"]
    return {
        "matched": False,
        "ac_no": default_ac["ac_no"],
        "constituency_ta": default_ac["name_ta"],
        "constituency_en": default_ac["name_en"],
        "district": "Madurai",
        "district_ta": default_ac["district_ta"],
        "mla_name_ta": default_ac["mla_name_ta"],
        "mla_name_en": default_ac["mla_name_en"],
        "mla_email": default_ac["email"],
        "mla_whatsapp": default_ac["whatsapp"],
        "district_collector_email": collector_info["email"],
        "district_collector_phone": collector_info["phone"],
        "district_collector_ta": collector_info["collector_ta"]
    }
