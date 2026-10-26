"""
Tamil Nadu Statutory e-Governance & Citizen Knowledge Base
Authoritative grounding context for Meta Muse Spark & Muse Wonder reasoning.
"""

from typing import List, Dict, Any

SERVICES_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "patta_chitta",
        "title_ta": "பட்டா / சிட்டா நில ஆவணம் & பெயர் மாற்றம்",
        "title_en": "Patta / Chitta Land Record & Transfer",
        "department_ta": "வருவாய்த்துறை (Revenue Department)",
        "portal_url": "https://eservices.tn.gov.in/eservicesnew/land/chitta.html",
        "official_fee_rs": 0,
        "transfer_fee_rs": 60,
        "delivery_time_days": "உடனடி பதிவிறக்கம் (Transfer: 15-30 நாட்கள்)",
        "required_documents_ta": [
            "கிரயப் பத்திரம் / தானப் பத்திரம் / பாகப்பிரிவினை பத்திரம் (Sale/Settlement Deed)",
            "முந்தைய பட்டா நகல் அல்லது தாய் பத்திரம் (Parent Document)",
            "வில்லங்கச் சான்றிதழ் (Encumbrance Certificate - EC)",
            "விண்ணப்பதாரரின் ஆதார் அட்டை (Aadhaar Card)",
            "நில வரைபடம் / FMB Sketch (உட்பிரிவு தேவைப்பட்டால்)"
        ],
        "statutory_rules_ta": "தமிழ்நாடு வருவாய்த்துறை நிலை ஆணை RSO 31-ன் கீழ் கூட்டு பட்டா அல்லது தனி பட்டா மாற்றம் செய்யப்படுகிறது. உட்பிரிவு இல்லாத பட்டா மாற்றத்திற்கு அரசு கட்டணம் ₹60 மட்டுமே. இடைத்தரகர்களுக்கு கூடுதல் பணம் தர வேண்டாம்.",
        "keywords": ["பட்டா", "சிட்டா", "நிலம்", "சர்வே எண்", "கிரயம்", "patta", "chitta", "land", "survey", "fmb", "tslr"]
    },
    {
        "id": "tnpds_ration",
        "title_ta": "ஸ்மார்ட் ரேஷன் கார்டு சேவைகள் (பெயர் சேர்த்தல் / நீக்கல்)",
        "title_en": "TNPDS Smart Family Card Services",
        "department_ta": "உணவு மற்றும் நுகர்வோர் பாதுகாப்புத்துறை",
        "portal_url": "https://www.tnpds.gov.in",
        "official_fee_rs": 0,
        "delivery_time_days": "15 நாட்கள்",
        "required_documents_ta": [
            "குழந்தை பெயர் சேர்க்க: பிறப்புச் சான்றிதழ் (Birth Certificate)",
            "திருமணம் காரணமாக சேர்க்க: திருமணப் பத்திரிகை அல்லது பதிவுச் சான்று & முந்தைய குடும்ப அட்டையிலிருந்து நீக்கப்பட்ட சான்று (Surrender Certificate)",
            "குடும்பத் தலைவரின் ஆதார் அட்டை & குடும்ப அட்டை எண்"
        ],
        "statutory_rules_ta": "ரேஷன் கார்டில் குடும்ப உறுப்பினர் பெயர் சேர்க்க அல்லது நீக்க அரசு கட்டணம் எதுவுமில்லை. விண்ணப்பம் வட்ட வழங்கல் அலுவலரால் (TSO) 15 நாட்களில் ஒப்புதல் அளிக்கப்படும்.",
        "keywords": ["ரேஷன்", "ரேஷன் கார்டு", "ஸ்மார்ட் கார்டு", "குழந்தை பெயர்", "பெயர் நீக்க", "ration", "tnpds", "family card"]
    },
    {
        "id": "legal_heir_cert",
        "title_ta": "வாரிசு சான்றிதழ் (Legal Heir Certificate)",
        "title_en": "Legal Heir Certificate",
        "department_ta": "வருவாய்த்துறை (Revenue Department)",
        "portal_url": "https://www.tnesevai.tn.gov.in",
        "official_fee_rs": 60,
        "delivery_time_days": "15 நாட்கள்",
        "required_documents_ta": [
            "இறந்தவரின் இறப்புச் சான்றிதழ் (Death Certificate)",
            "இறந்தவரின் ஆதார் அட்டை மற்றும் குடும்ப அட்டை",
            "அனைத்து நேரடி வாரிசுகளின் ஆதார் அட்டை & பிறப்பு சான்றிதழ்",
            "திருமணச் சான்றிதழ் (மனைவி/கணவர் விண்ணப்பித்தால்)",
            "கிராம நிர்வாக அலுவலர் (VAO) அறிக்கை"
        ],
        "statutory_rules_ta": "வாரிசு சான்றிதழ் வட்டாட்சியர் (Tahsildar) அலுவலகத்தால் வழங்கப்படுகிறது. நேரடி வாரிசுகள் (தாய், தந்தை, மனைவி/கணவர், மகன், மகள்) மட்டுமே இ-சேவை மூலம் விண்ணப்பிக்கலாம்.",
        "keywords": ["வாரிசு", "வாரிசு சான்றிதழ்", "இறப்பு", "legal heir", "inheritance", "varisu"]
    },
    {
        "id": "cmchis_health",
        "title_ta": "முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம் (CMCHIS ₹5 லட்சம்)",
        "title_en": "Chief Minister's Comprehensive Health Insurance Scheme",
        "department_ta": "மக்கள் நல்வாழ்வுத்துறை (Health & Family Welfare)",
        "portal_url": "https://www.cmchistn.com",
        "official_fee_rs": 0,
        "delivery_time_days": "அட்டை வழங்கல்: மாவட்ட ஆட்சியர் அலுவலகத்தில் உடனடி பதிவு",
        "required_documents_ta": [
            "குடும்ப ஸ்மார்ட் ரேஷன் கார்டு நகல்",
            "குடும்பத் தலைவர் மற்றும் அனைத்து உறுப்பினர்களின் ஆதார் அட்டை",
            "ஆண்டு வருமானச் சான்றிதழ் (ரூ. 1,20,000-க்குள் இருக்க வேண்டும்)",
            "கிராம நிர்வாக அலுவலர் (VAO) வருமான உறுதிப் படிவம்"
        ],
        "statutory_rules_ta": "அரசு மற்றும் அங்கீகரிக்கப்பட்ட தனியார் மருத்துவமனைகளில் ஆண்டுக்கு ₹5,00,000 வரை கட்டணமில்லா அறுவை சிகிச்சை மற்றும் சிகிச்சை பெறலாம்.",
        "keywords": ["மருத்துவ காப்பீடு", "காப்பீடு", "மருத்துவ அட்டை", "cmchis", "health insurance", "5 lakh"]
    },
    {
        "id": "kmut_rights",
        "title_ta": "கலைஞர் மகளிர் உரிமைத் திட்டம் (மாதம் ₹1,000)",
        "title_en": "Kalaignar Magalir Urimai Thittam (KMUT ₹1,000/month)",
        "department_ta": "சிறப்புத் திட்ட செயலாக்கத்துறை",
        "portal_url": "https://kmut.tn.gov.in",
        "official_fee_rs": 0,
        "delivery_time_days": "மாதாந்திர நேரடி வங்கிப் பரிமாற்றம் (DBT)",
        "required_documents_ta": [
            "ஸ்மார்ட் குடும்ப அட்டை (குடும்பத் தலைவியாக பெண் பெயர் இருக்க வேண்டும்)",
            "ஆதார் அட்டை (வங்கி கணக்குடன் இணைக்கப்பட்டது / NPCI Seeding)",
            "மின் நுகர்வோர் அட்டை எண் (ஆண்டு மின் பயன்பாடு 3600 யூனிட்டுகளுக்குள் இருக்க வேண்டும்)",
            "வங்கி கணக்குப் புத்தகம் (Aadhaar Linked Bank Passbook)"
        ],
        "statutory_rules_ta": "குடும்ப ஆண்டு வருமானம் ₹2.5 லட்சத்திற்குள் இருக்க வேண்டும். குடும்பத்தில் அரசு ஊழியர்கள், ஓய்வூதியதாரர்கள், 4 சக்கர வாகனம் வைத்திருப்பவர்கள் (டிராக்டர் தவிர) இருக்கக் கூடாது.",
        "keywords": ["மகளிர் உரிமை", "1000 ரூபாய்", "மகளிர் திட்டம்", "kmut", "magalir urimai", "women 1000"]
    }
]


def search_knowledge_base(query: str) -> List[Dict[str, Any]]:
    """Retrieves relevant Tamil Nadu e-Governance service rules matching the citizen's query."""
    q_lower = query.lower()
    matches = []
    for s in SERVICES_CATALOG:
        score = sum(1 for kw in s["keywords"] if kw in q_lower)
        if score > 0 or any(w in q_lower for w in s["title_ta"].split()):
            matches.append(s)
    return matches or SERVICES_CATALOG[:2]
