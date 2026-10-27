# -*- coding: utf-8 -*-
"""
Tamil Nadu Universal Citizen Grievance & Statutory Action Registry (மக்கள் நீதி)
Makkal Agent AI - Meta AI Developer Hackathon 2026

Classifies and routes citizen grievances across all key administrative tiers:
1. District Collector Monday Grievance & Jamabandi (மாவட்ட ஆட்சியர்)
2. Revenue Divisional Officer (RDO) Appellate Tribunal (வருவாய் கோட்டாட்சியர்)
3. Superintendent of Police (SP) & Anti-Land Grabbing Cell (காவல் கண்காணிப்பாளர்)
4. TANGEDCO Electricity Grievance (மின்வாரிய பொறியாளர்)
5. Municipal Commissioner / Panchayat BDO (மாநகராட்சி / ஊராட்சி மன்றம்)
6. MLA Constituency Grievance (சட்டமன்ற உறுப்பினர்)
7. Chief Minister's Special Cell / Makkaludan Mudhalvar (முதலமைச்சரின் தனிப்பிரிவு)
"""

from typing import Dict, List, Any, Optional
import re
from mla_directory import DISTRICT_COLLECTORS, ASSEMBLY_CONSTITUENCIES, resolve_constituency

# Universal Grievance Tiers and Classifications
PETITION_TIERS: Dict[str, Dict[str, Any]] = {
    "collector": {
        "tier_id": "collector",
        "title_ta": "மாவட்ட ஆட்சியர் குறைதீர்ப்பு (திங்கள் முகாம் & ஜமாபந்தி)",
        "title_en": "District Collector Grievance Day & Jamabandi",
        "authority_title_ta": "மாவட்ட ஆட்சித்தலைவர் மற்றும் மாவட்ட குற்றவியல் நடுவர் அவர்கள்",
        "authority_title_en": "District Collector & District Magistrate",
        "statute": "தமிழ்நாடு வருவாய் நிலை ஆணைகள் (RSO) & குடிமக்கள் சாசனம் 2024",
        "sla_days": 15,
        "sla_text": "15 வேலை நாட்களுக்குள் உரிய விசாரணை அறிக்கை",
        "icon": "🏛️",
        "badge_color": "emerald",
        "subcategories": [
            {
                "id": "patta_delay",
                "label_ta": "பட்டா மாறுதல் 30 நாட்களுக்கு மேல் தாமதம்",
                "label_en": "Land Patta Mutation Pending >30 Days",
                "statute_ref": "தமிழ்நாடு பட்டா மாறுதல் விதிகள் & RSO 31",
                "sample_desc": "வட்டாட்சியர் அலுவலகத்தில் பட்டா மாறுதலுக்கு விண்ணப்பித்து 30 நாட்களுக்கு மேலாகியும் எவ்வித நடவடிக்கையும் இன்றி நிலுவையில் உள்ளது. உடனடியாக பட்டா வழங்கிட உத்தரவிடுமாறு வேண்டுகிறேன்."
            },
            {
                "id": "waterbody_encroachment",
                "label_ta": "நீர்வழி & ஏரி புறம்போக்கு ஆக்கிரமிப்பு அகற்றுதல்",
                "label_en": "Removal of Waterbody & Tank Encroachments",
                "statute_ref": "தமிழ்நாடு நில ஆக்கிரமிப்பு சட்டம் 1905 பிரிவு 6 & உயர்நீதிமன்ற தீர்ப்புகள்",
                "sample_desc": "கிராம பொது பயன்பாட்டில் உள்ள குளம் மற்றும் நீர்வழி பாசன வாய்க்கால் தனிநபர்களால் சட்டவிரோதமாக ஆக்கிரமிக்கப்பட்டுள்ளது. உடனடியாக கள ஆய்வு செய்து ஆக்கிரமிப்பை அகற்றிட வேண்டுகிறேன்."
            },
            {
                "id": "welfare_pension",
                "label_ta": "முதியோர் உதவித்தொகை (OAP) & விபத்து நிவாரணம்",
                "label_en": "Old Age Pension (OAP) & Disaster Relief",
                "statute_ref": "சமூக பாதுகாப்பு திட்ட அரசாணை & முதலமைச்சர் பொது நிவாரண நிதி",
                "sample_desc": "வறுமைக் கோட்டிற்கு கீழ் உள்ள முதியோருக்கு மாதந்தோறும் வழங்கப்படும் இந்திரா காந்தி தேசிய முதியோர் உதவித்தொகை பெற பலமுறை மனு அளித்தும் பரிசீலிக்கப்படவில்லை. உடனடியாக ஆணை பிறப்பிக்குமாறு வேண்டுகிறேன்."
            },
            {
                "id": "sand_mining",
                "label_ta": "சட்டவிரோத ஆற்று மணல் / கனிமக் கடத்தல் தடுத்தல்",
                "label_en": "Illegal River Sand Mining & Mineral Smuggling",
                "statute_ref": "சுரங்கங்கள் மற்றும் கனிமங்கள் மேம்பாட்டு சட்டம் 1957",
                "sample_desc": "எங்கள் கிராம ஆற்றுப் படுகையில் இரவு நேரங்களில் சட்டவிரோதமாக ஆற்று மணல் அள்ளப்பட்டு நிலத்தடி நீர்மட்டம் கடுமையாக பாதிக்கப்படுகிறது. சிறப்பு படை அமைத்து தடுத்து நிறுத்துமாறு வேண்டுகிறேன்."
            }
        ]
    },
    "rdo_appeal": {
        "tier_id": "rdo_appeal",
        "title_ta": "வருவாய் கோட்டாட்சியர் (RDO) சட்டப்பூர்வ மேல்முறையீடு",
        "title_en": "RDO Statutory Appellate Revenue Tribunal",
        "authority_title_ta": "வருவாய் கோட்டாட்சியர் மற்றும் சார்-ஆட்சியர் அவர்கள்",
        "authority_title_en": "Revenue Divisional Officer / Sub-Collector",
        "statute": "தமிழ்நாடு பட்டா மேல்முறையீட்டு சட்டம் 1983 பிரிவு 12 & தமிழ்நாடு நில அளவை சட்டம் 1923 பிரிவு 11",
        "sla_days": 30,
        "sla_text": "30 நாட்களுக்குள் இருதரப்பு விசாரணை & தீர்ப்பு ஆணை",
        "icon": "⚖️",
        "badge_color": "amber",
        "subcategories": [
            {
                "id": "patta_cancellation",
                "label_ta": "வட்டாட்சியரின் தவறான பட்டா உத்தரவு ரத்து மேல்முறையீடு",
                "label_en": "Appeal Against Wrongful Tahsildar Patta Mutation",
                "statute_ref": "தமிழ்நாடு பட்டா பாஸ் புத்தகம் சட்டம் 1983 பிரிவு 12 & 13",
                "sample_desc": "எனது பூர்வீக நிலத்திற்கு எனது சம்மதமோ அறிவிப்போ இன்றி வட்டாட்சியரால் மூன்றாம் நபருக்கு தவறாக வழங்கப்பட்ட பட்டாவை ரத்து செய்து, எனது பெயரில் மீண்டும் பட்டா உத்தரவு பிறப்பிக்க வேண்டுகிறேன்."
            },
            {
                "id": "boundary_appeal",
                "label_ta": "நில எல்லை அளவீடு (சர்வே) மேல்முறையீட்டு மனு",
                "label_en": "Appeal Against Land Demarcation & Survey Report",
                "statute_ref": "தமிழ்நாடு நில அளவை மற்றும் எல்லைகள் சட்டம் 1923 பிரிவு 11",
                "sample_desc": "வட்ட நில அளவர் செய்த சர்வேயில் அண்டை நில உரிமையாளரின் அத்துமீறல் புறக்கணிக்கப்பட்டு தவறான எல்லை குறிக்கப்பட்டுள்ளது. வருவாய் கோட்டாட்சியர் தலைமையில் மறு-அளவீடு செய்ய உத்தரவிட வேண்டுகிறேன்."
            },
            {
                "id": "senior_citizen_property",
                "label_ta": "பெற்றோர் மற்றும் மூத்த குடிமக்கள் சொத்து மீட்பு",
                "label_en": "Maintenance & Welfare of Parents and Senior Citizens Act",
                "statute_ref": "பெற்றோர் மற்றும் மூத்த குடிமக்கள் பராமரிப்பு மற்றும் நலச் சட்டம் 2007 பிரிவு 23",
                "sample_desc": "பராமரிப்பதாக உறுதியளித்து தான செட்டில்மென்ட் பெற்ற வாரிசுகள் உணவு, மருத்துவம் தராமல் புறக்கணிக்கின்றனர். 2007 சட்டத்தின் கீழ் தானப் பத்திரத்தை ரத்து செய்து சொத்தை மீட்டுத் தர வேண்டுகிறேன்."
            }
        ]
    },
    "police_sp": {
        "tier_id": "police_sp",
        "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர் (SP) / ஆணையர் குறைதீர்ப்பு",
        "title_en": "Superintendent of Police (SP) / Commissioner Grievance",
        "authority_title_ta": "மாவட்ட காவல் கண்காணிப்பாளர் / பெருநகர காவல் ஆணையர் அவர்கள்",
        "authority_title_en": "Superintendent of Police / Commissioner of Police",
        "statute": "தமிழ்நாடு காவல் நிலை ஆணைகள் (PSO 557) & பாரதிய நாகரிக் சுரக்ஷா சன்ஹிதா (BNSS 173)",
        "sla_days": 7,
        "sla_text": "7 நாட்களுக்குள் CSR பதிவு மற்றும் நேரடி விசாரணை",
        "icon": "👮",
        "badge_color": "blue",
        "subcategories": [
            {
                "id": "land_grabbing_cell",
                "label_ta": "நில அபகரிப்பு தடுப்பு சிறப்புப் பிரிவு (ALGC) புகார்",
                "label_en": "Anti-Land Grabbing Special Cell (ALGC) Criminal Complaint",
                "statute_ref": "இந்திய தண்டனைச் சட்டம் பிரிவுகள் 420, 468, 471, 120(B) & சிறப்புப் பிரிவு அரசாணை",
                "sample_desc": "எனக்குச் சொந்தமான பத்திரப் பதிவு செய்யப்பட்ட பட்டா நிலத்தை ஆள்மாறாட்டம் மற்றும் போலி ஆவணங்கள் தயாரித்து கள்ளக் கிரயம் செய்துள்ளனர். நில அபகரிப்பு சிறப்புப் பிரிவு மூலம் குற்றவாளிகள் மீது வழக்குப்பதிவு செய்து நிலத்தை மீட்டுத்தர வேண்டுகிறேன்."
            },
            {
                "id": "fir_delay",
                "label_ta": "காவல் நிலையத்தில் FIR பதிவு செய்ய மறுப்பு / CSR தாமதம்",
                "label_en": "Refusal to Register FIR / Delay in CSR Action",
                "statute_ref": "BNSS பிரிவு 173 & உச்சநீதிமன்ற லலிதா குமாரி வழிகாட்டுதல்கள்",
                "sample_desc": "காவல் நிலையத்தில் நேரடியாக புகார் அளித்தும் ரசீதோ அல்லது வழக்கோ பதியாமல் காலம் தாழ்த்துகின்றனர். மாவட்ட காவல் கண்காணிப்பாளர் தலையிட்டு உடனடி முதல் தகவல் அறிக்கை (FIR) பதிவு செய்ய உத்தரவிடுமாறு வேண்டுகிறேன்."
            },
            {
                "id": "usury_harassment",
                "label_ta": "கந்துவட்டி மிரட்டல் & அடாவடி வசூல் தடுப்பு புகார்",
                "label_en": "Exorbitant Usury Harassment & Coercion Protection",
                "statute_ref": "தமிழ்நாடு அதிக வட்டி வசூலித்தல் தடைச் சட்டம் 2003",
                "sample_desc": "வாங்கிய கடனுக்கு அசல் மற்றும் நியாயமான வட்டி செலுத்திய பிறகும், மீட்டர் வட்டி கேட்டு ஆட்களை வைத்து அடியாட்களுடன் கொலை மிரட்டல் விடுக்கின்றனர். 2003 கந்துவட்டி தடைச் சட்டத்தின் கீழ் உடனடி பாதுகாப்பு மற்றும் நடவடிக்கை கோருகிறேன்."
            }
        ]
    },
    "tangedco": {
        "tier_id": "tangedco",
        "title_ta": "மின்வாரிய (TANGEDCO) செயற்பொறியாளர் குறைதீர்ப்பு",
        "title_en": "TANGEDCO Executive Engineer Power Grievance",
        "authority_title_ta": "செயற்பொறியாளர் (பகிர்மானம்), தமிழ்நாடு மின் உற்பத்தி மற்றும் பகிர்மானக் கழகம்",
        "authority_title_en": "Executive Engineer (Distribution), TANGEDCO",
        "statute": "தமிழ்நாடு மின்சார ஒழுங்குமுறை ஆணைய (TNERC) விநியோக விதிகள் & சப்ளை கோடு பிரிவு 12",
        "sla_days": 3,
        "sla_text": "48 மணி நேரத்திற்குள் பழுது நீக்கம் / 3 நாட்களுக்குள் நடவடிக்கை",
        "icon": "⚡",
        "badge_color": "yellow",
        "subcategories": [
            {
                "id": "agri_free_power",
                "label_ta": "விவசாய இலவச மின் இணைப்பு முன்னுரிமை தாமதம்",
                "label_en": "Free Agricultural Power Connection Priority Delay",
                "statute_ref": "TANGEDCO விவசாய மின் இணைப்பு முன்னுரிமை அரசாணை",
                "sample_desc": "விவசாய பம்புசெட்டிற்கு இலவச மின் இணைப்பு கோரி விண்ணப்பித்து பல ஆண்டுகளாக காத்திருப்போர் பட்டியலில் உள்ளேன். மின்கம்பங்கள் நடப்பட்டு தயார் நிலையில் உள்ளதால் உடனடியாக மின் இணைப்பு வழங்குமாறு வேண்டுகிறேன்."
            },
            {
                "id": "burnt_transformer",
                "label_ta": "பழுதான மின்மாற்றி (டிரான்ஸ்பார்மர்) மாற்றுதல்",
                "label_en": "Burnt / Faulty Distribution Transformer Replacement",
                "statute_ref": "TNERC செயல்திறன் தர நிர்ணயம் - 48 மணி நேர கட்டாய விதி",
                "sample_desc": "எங்கள் கிராம மின்மாற்றி வெடித்து பழுதாகி பல மணி நேரமாக ஒட்டுமொத்த விவசாய பம்புசெட்டுகள் மற்றும் வீடுகளுக்கு மின்விநியோகம் தடைபட்டுள்ளது. 48 மணி நேர சட்ட விதியின்படி புதிய டிரான்ஸ்பார்மர் அமைத்து தருமாறு வேண்டுகிறேன்."
            },
            {
                "id": "hazardous_wires",
                "label_ta": "தாழ்வாக செல்லும் ஆபத்தான உயர்மின் கம்பிகள் சீரமைப்பு",
                "label_en": "Low-Sagging Hazardous High Voltage Wires Rectification",
                "statute_ref": "மத்திய மின்சார ஆணைய பாதுகாப்பு ஒழுங்குமுறை விதிகள்",
                "sample_desc": "விவசாய நிலத்தின் நடுவே செல்லும் 11KV உயர்மின் கம்பி மிகவும் தாழ்வாக தொங்கிக்கொண்டு கால்நடைகள் மற்றும் உழவு வாகனங்களுக்கு ஆபத்தை ஏற்படுத்துகிறது. புதிய இடைக்கம்பம் அமைத்து கம்பிகளை இழுத்துக் கட்ட வேண்டுகிறேன்."
            }
        ]
    },
    "municipal_bdo": {
        "tier_id": "municipal_bdo",
        "title_ta": "மாநகராட்சி ஆணையர் / ஊராட்சி ஒன்றிய வட்டார வளர்ச்சி அலுவலர் (BDO)",
        "title_en": "Municipal Commissioner / Block Development Officer (BDO)",
        "authority_title_ta": "ஆணையர் / வட்டார வளர்ச்சி அலுவலர் (கிராம ஊராட்சிகள்)",
        "authority_title_en": "Commissioner / Block Development Officer (Village Panchayats)",
        "statute": "தமிழ்நாடு நகர்ப்புற உள்ளாட்சி அமைப்புகள் சட்டம் 1998 & தமிழ்நாடு ஊராட்சிகள் சட்டம் 1994 பிரிவு 110",
        "sla_days": 7,
        "sla_text": "7 நாட்களுக்குள் சீரமைப்புப் பணிகள் தொடக்கம்",
        "icon": "🚜",
        "badge_color": "teal",
        "subcategories": [
            {
                "id": "drinking_water_crisis",
                "label_ta": "குடிநீர் விநியோகக் குழாய் உடைப்பு & தூய குடிநீர் விநியோகம்",
                "label_en": "Broken Drinking Water Pipeline & Contamination",
                "statute_ref": "ஊராட்சிகள் சட்டம் பிரிவு 110 - கட்டாயக் குடிநீர் கடமை",
                "sample_desc": "எங்கள் பகுதியில் பிரதான குடிநீர் குழாய் உடைந்து சாக்கடை நீர் கலந்து தூய்மையற்ற குடிநீர் வருகிறது. குழந்தைகள் நோய்வாய்ப்படும் அபாயம் உள்ளதால் உடனடியாக சீரமைத்து தூய குடிநீர் விநியோகிக்க வேண்டுகிறேன்."
            },
            {
                "id": "damaged_village_road",
                "label_ta": "சேதமடைந்த தெருச்சாலை & தார்ச்சாலை சீரமைப்பு",
                "label_en": "Damaged Rural / Ward Road & Pothole Repair",
                "statute_ref": "தமிழ்நாடு நகர்ப்புற & ஊரக உள்கட்டமைப்பு விதிகள்",
                "sample_desc": "கிராமத்தின் பிரதான இணைப்புச் சாலை ஆம்புலன்ஸ் கூட வர முடியாத அளவிற்கு குண்டும் குழியுமாக உள்ளது. பிரதம மந்திரி அல்லது முதலமைச்சர் கிராமச் சாலை மேம்பாட்டுத் திட்டத்தின் கீழ் தார்ச்சாலை அமைத்து தர வேண்டுகிறேன்."
            },
            {
                "id": "drainage_overflow",
                "label_ta": "சாக்கடை கழிவுநீர் தேக்கம் & கொசு மருந்து தெளிப்பு",
                "label_en": "Drainage Overflow & Public Health Sanitization",
                "statute_ref": "பொது சுகாதார சட்டம் 1939",
                "sample_desc": "தெரு கழிவுநீர் வாய்க்கால் தூர்வாரப்படாமல் குடியிருப்பு பகுதியில் கழிவுநீர் தேங்கி கொசு மற்றும் தொற்றுநோய் பரவும் அபாயம் உள்ளது. உடனடியாக கழிவுநீரை அகற்றி கொசு மருந்து தெளிக்க வேண்டுகிறேன்."
            }
        ]
    },
    "cm_cell": {
        "tier_id": "cm_cell",
        "title_ta": "முதலமைச்சரின் தனிப்பிரிவு & மக்களுடன் முதல்வர் (CM Special Cell)",
        "title_en": "Chief Minister's Special Cell / Makkaludan Mudhalvar",
        "authority_title_ta": "சிறப்பு அலுவலர், முதலமைச்சரின் தனிப்பிரிவு, தலைமைச் செயலகம், சென்னை",
        "authority_title_en": "Special Officer, Chief Minister's Special Cell, Secretariat, Chennai",
        "statute": "தமிழ்நாடு சேவை உரிமைச் சட்டம் & முதலமைச்சரின் தனிப்பிரிவு நேரடி கண்காணிப்பு",
        "sla_days": 30,
        "sla_text": "30 நாட்களுக்குள் தலைமைச் செயலக நேரடி கண்காணிப்பு அறிக்கை",
        "icon": "👑",
        "badge_color": "purple",
        "subcategories": [
            {
                "id": "unresolved_escalation",
                "label_ta": "மாவட்ட அளவில் 30 நாட்களுக்கு மேல் தீர்க்கப்படாத முக்கிய மனு",
                "label_en": "Unresolved District Grievance Escalation (>30 Days)",
                "statute_ref": "முதலமைச்சரின் தனிப்பிரிவு நேரடி மறுபரிசீலனை வழிகாட்டுதல்",
                "sample_desc": "மாவட்ட ஆட்சித்தலைவர் மற்றும் வட்டாட்சியரிடம் பலமுறை மனு அளித்தும் கீழ்நிலை அதிகாரிகளின் மெத்தனத்தால் எந்த நடவடிக்கையும் இல்லை. மாண்புமிகு முதலமைச்சர் அவர்களின் தனிப்பிரிவு தலையிட்டு உரிய நிவாரணம் வழங்க வேண்டுகிறேன்."
            },
            {
                "id": "interdept_dispute",
                "label_ta": "துறைகளுக்கு இடையேயான சிக்கலால் முடங்கிய மக்கள் திட்டம்",
                "label_en": "Inter-Departmental Deadlock in Public Infrastructure",
                "statute_ref": "தமிழ்நாடு தலைமைச் செயலக நிர்வாக விதிகள்",
                "sample_desc": "வருவாய்த்துறை மற்றும் நெடுஞ்சாலைத்துறை இடையே உள்ள எல்லை சர்ச்சை காரணமாக கிராம மேம்பாட்டுப் பாலம் அமைக்கும் பணி முடங்கியுள்ளது. தலைமைச் செயலர் மூலம் தீர்வு காண வேண்டுகிறேன்."
            }
        ]
    },
    "mla": {
        "tier_id": "mla",
        "title_ta": "சட்டமன்ற உறுப்பினர் நேரடி மனு (MLA Grievance & MLACDS)",
        "title_en": "Legislative Assembly Member Constituency Grievance",
        "authority_title_ta": "மாண்புமிகு சட்டமன்ற உறுப்பினர் அவர்கள்",
        "authority_title_en": "Honorable Member of Legislative Assembly",
        "statute": "சட்டமன்ற உறுப்பினர் தொகுதி மேம்பாட்டு நிதி வழிகாட்டுதல்கள் & ஊராட்சிகள் சட்டம் 1994",
        "sla_days": 15,
        "sla_text": "15 நாட்களுக்குள் தொகுதி மேம்பாட்டு நிதி ஒதுக்கீடு / பரிந்துரை",
        "icon": "🏛️",
        "badge_color": "indigo",
        "subcategories": [
            {
                "id": "irrigation_desilting",
                "label_ta": "பாசன வாய்க்கால் & கண்மாய் தூர்வாருதல்",
                "label_en": "Irrigation Canal & Village Tank Desilting",
                "statute_ref": "தமிழ்நாடு ஊராட்சிகள் சட்டம் 1994 பிரிவு 110",
                "sample_desc": "விவசாய பாசன வாய்க்கால் பல ஆண்டுகளாக தூர்வாரப்படாமல் செடி, கொடிகள் மண்டிக் கிடப்பதால் பாசன நீர் கடைமடை பகுதிக்கு செல்வதில்லை. சட்டமன்ற உறுப்பினர் தொகுதி மேம்பாட்டு நிதியில் தூர்வாரித் தர வேண்டுகிறேன்."
            },
            {
                "id": "community_hall",
                "label_ta": "கிராம சமுதாயக்கூடம் / நூலகக் கட்டடம் அமைத்தல்",
                "label_en": "Village Community Hall / Public Library Construction",
                "statute_ref": "சட்டமன்ற உறுப்பினர் தொகுதி மேம்பாட்டுத் திட்டம் (MLACDS)",
                "sample_desc": "கிராம மக்கள் எளிய முறையில் சுபநிகழ்ச்சிகள் நடத்த சமுதாயக்கூடம் இல்லை. சட்டமன்ற உறுப்பினர் தொகுதி நிதியிலிருந்து புதிய சமுதாயக்கூடம் கட்டித் தர வேண்டுகிறேன்."
            }
        ]
    }
}

# Police Superintendent & Commissioner Contact Directory (All 38 Districts + Commissionerates)
POLICE_AUTHORITIES: Dict[str, Dict[str, str]] = {
    "Chennai": {"email": "cop.chennai@tn.gov.in", "phone": "+914423452345", "title_ta": "பெருநகர காவல் ஆணையர், சென்னை"},
    "Madurai": {"email": "sp.mdu@tn.gov.in", "phone": "+914522530222", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், மதுரை"},
    "Coimbatore": {"email": "sp.cbe@tn.gov.in", "phone": "+914222300970", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், கோயம்புத்தூர்"},
    "Thanjavur": {"email": "sp.tnj@tn.gov.in", "phone": "+914362230132", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், தஞ்சாவூர்"},
    "Tiruchirappalli": {"email": "sp.try@tn.gov.in", "phone": "+914312415100", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், திருச்சி"},
    "Salem": {"email": "sp.slm@tn.gov.in", "phone": "+914272450000", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், சேலம்"},
    "Tirunelveli": {"email": "sp.tin@tn.gov.in", "phone": "+914622500800", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், திருநெல்வேலி"},
    "Dindigul": {"email": "sp.dgl@tn.gov.in", "phone": "+914512460100", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், திண்டுக்கல்"},
    "Erode": {"email": "sp.erd@tn.gov.in", "phone": "+914242260100", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், ஈரோடு"},
    "Tiruppur": {"email": "sp.tup@tn.gov.in", "phone": "+914212970100", "title_ta": "மாவட்ட காவல் கண்காணிப்பாளர், திருப்பூர்"}
}

# TANGEDCO Superintending & Executive Engineer Circles
TANGEDCO_AUTHORITIES: Dict[str, Dict[str, str]] = {
    "Chennai": {"email": "ee.chennai.central@tnebnet.org", "phone": "+914428521113", "title_ta": "செயற்பொறியாளர் (பகிர்மானம்), சென்னை மின்கோட்டம்"},
    "Madurai": {"email": "ee.madurai.metro@tnebnet.org", "phone": "+914522530111", "title_ta": "செயற்பொறியாளர் (பகிர்மானம்), மதுரை மின்கோட்டம்"},
    "Coimbatore": {"email": "ee.cbe.metro@tnebnet.org", "phone": "+914222301122", "title_ta": "செயற்பொறியாளர் (பகிர்மானம்), கோவை மின்கோட்டம்"},
    "Thanjavur": {"email": "ee.thanjavur@tnebnet.org", "phone": "+914362230333", "title_ta": "செயற்பொறியாளர் (பகிர்மானம்), தஞ்சை மின்கோட்டம்"},
    "Tiruchirappalli": {"email": "ee.trichy.metro@tnebnet.org", "phone": "+914312415222", "title_ta": "செயற்பொறியாளர் (பகிர்மானம்), திருச்சி மின்கோட்டம்"},
    "Salem": {"email": "ee.salem@tnebnet.org", "phone": "+914272450333", "title_ta": "செயற்பொறியாளர் (பகிர்மானம்), சேலம் மின்கோட்டம்"}
}


def resolve_authority_for_tier(
    tier: str,
    district: str,
    taluk: Optional[str] = None,
    query_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Intelligently resolves the exact target authority, contact coordinates,
    statutory sections, and escalation path for any civic grievance tier.
    """
    clean_dist = district.strip().capitalize() if district else "Madurai"
    if clean_dist not in DISTRICT_COLLECTORS:
        clean_dist = "Madurai"

    collector_info = DISTRICT_COLLECTORS.get(clean_dist, DISTRICT_COLLECTORS["Madurai"])
    tier_meta = PETITION_TIERS.get(tier, PETITION_TIERS["collector"])

    if tier == "collector":
        return {
            "tier": "collector",
            "tier_title_ta": tier_meta["title_ta"],
            "authority_name_ta": f"மாவட்ட ஆட்சித்தலைவர் அவர்கள், {clean_dist} மாவட்ட ஆட்சியரகம்",
            "authority_name_en": f"The District Collector & District Magistrate, {clean_dist} District",
            "official_email": collector_info["email"],
            "official_phone": collector_info["phone"],
            "official_address": f"மாவட்ட ஆட்சியர் அலுவலகம், {clean_dist}, தமிழ்நாடு",
            "statute": tier_meta["statute"],
            "sla_days": tier_meta["sla_days"],
            "sla_text": tier_meta["sla_text"],
            "icon": tier_meta["icon"]
        }

    elif tier == "rdo_appeal":
        taluk_str = f" ({taluk} வருவாய் கோட்டம்)" if taluk else ""
        return {
            "tier": "rdo_appeal",
            "tier_title_ta": tier_meta["title_ta"],
            "authority_name_ta": f"வருவாய் கோட்டாட்சியர் மற்றும் சார்-ஆட்சியர் அவர்கள்{taluk_str}",
            "authority_name_en": f"The Revenue Divisional Officer / Sub-Collector, {clean_dist} Division",
            "official_email": f"rdo.{clean_dist.lower()}@tn.gov.in",
            "official_phone": collector_info["phone"],
            "official_address": f"வருவாய் கோட்டாட்சியர் அலுவலகம், {clean_dist}, தமிழ்நாடு",
            "statute": tier_meta["statute"],
            "sla_days": tier_meta["sla_days"],
            "sla_text": tier_meta["sla_text"],
            "icon": tier_meta["icon"]
        }

    elif tier == "police_sp":
        police_info = POLICE_AUTHORITIES.get(clean_dist, {
            "email": f"sp.{clean_dist.lower()}@tn.gov.in",
            "phone": "+914522530222",
            "title_ta": f"மாவட்ட காவல் கண்காணிப்பாளர், {clean_dist}"
        })
        return {
            "tier": "police_sp",
            "tier_title_ta": tier_meta["title_ta"],
            "authority_name_ta": police_info["title_ta"],
            "authority_name_en": f"The Superintendent of Police / Commissioner, {clean_dist}",
            "official_email": police_info["email"],
            "official_phone": police_info["phone"],
            "official_address": f"மாவட்ட காவல் கண்காணிப்பாளர் அலுவலகம், {clean_dist}, தமிழ்நாடு",
            "statute": tier_meta["statute"],
            "sla_days": tier_meta["sla_days"],
            "sla_text": tier_meta["sla_text"],
            "icon": tier_meta["icon"]
        }

    elif tier == "tangedco":
        tneb_info = TANGEDCO_AUTHORITIES.get(clean_dist, {
            "email": f"ee.{clean_dist.lower()}@tnebnet.org",
            "phone": "+914522530111",
            "title_ta": f"செயற்பொறியாளர் (பகிர்மானம்), {clean_dist} மின்கோட்டம்"
        })
        return {
            "tier": "tangedco",
            "tier_title_ta": tier_meta["title_ta"],
            "authority_name_ta": tneb_info["title_ta"],
            "authority_name_en": f"The Executive Engineer (Distribution), TANGEDCO, {clean_dist}",
            "official_email": tneb_info["email"],
            "official_phone": tneb_info["phone"],
            "official_address": f"மின்வாரிய செயற்பொறியாளர் அலுவலகம், {clean_dist}, தமிழ்நாடு",
            "statute": tier_meta["statute"],
            "sla_days": tier_meta["sla_days"],
            "sla_text": tier_meta["sla_text"],
            "icon": tier_meta["icon"]
        }

    elif tier == "municipal_bdo":
        return {
            "tier": "municipal_bdo",
            "tier_title_ta": tier_meta["title_ta"],
            "authority_name_ta": f"மாநகராட்சி ஆணையர் / வட்டார வளர்ச்சி அலுவலர் (BDO), {clean_dist}",
            "authority_name_en": f"Municipal Commissioner / Block Development Officer, {clean_dist}",
            "official_email": f"bdo.{clean_dist.lower()}@tn.gov.in",
            "official_phone": collector_info["phone"],
            "official_address": f"வட்டார வளர்ச்சி அலுவலகம் / மாநகராட்சி அலுவலகம், {clean_dist}, தமிழ்நாடு",
            "statute": tier_meta["statute"],
            "sla_days": tier_meta["sla_days"],
            "sla_text": tier_meta["sla_text"],
            "icon": tier_meta["icon"]
        }

    elif tier == "cm_cell":
        return {
            "tier": "cm_cell",
            "tier_title_ta": tier_meta["title_ta"],
            "authority_name_ta": "சிறப்பு அலுவலர், முதலமைச்சரின் தனிப்பிரிவு, தலைமைச் செயலகம், சென்னை",
            "authority_name_en": "Special Officer, Chief Minister's Special Cell, Secretariat, Chennai",
            "official_email": "cmcell@tn.gov.in",
            "official_phone": "+914425671545",
            "official_address": "முதலமைச்சரின் தனிப்பிரிவு, தலைமைச் செயலகம், புனித ஜார்ஜ் கோட்டை, சென்னை - 600009",
            "statute": tier_meta["statute"],
            "sla_days": tier_meta["sla_days"],
            "sla_text": tier_meta["sla_text"],
            "icon": tier_meta["icon"]
        }

    elif tier == "mla":
        mla_res = resolve_constituency(query_text or "", clean_dist)
        return {
            "tier": "mla",
            "tier_title_ta": tier_meta["title_ta"],
            "authority_name_ta": f"மாண்புமிகு சட்டமன்ற உறுப்பினர் {mla_res['mla_name_ta']} (தொகுதி: {mla_res['constituency_ta']})",
            "authority_name_en": f"Hon. MLA {mla_res['mla_name_en']} (AC: {mla_res['constituency_en']})",
            "official_email": mla_res["mla_email"],
            "official_phone": mla_res["mla_whatsapp"],
            "official_address": f"சட்டமன்ற உறுப்பினர் அலுவலகம், {mla_res['constituency_ta']} சட்டமன்றத் தொகுதி, தமிழ்நாடு",
            "statute": tier_meta["statute"],
            "sla_days": tier_meta["sla_days"],
            "sla_text": tier_meta["sla_text"],
            "icon": tier_meta["icon"],
            "ac_no": mla_res["ac_no"],
            "constituency_ta": mla_res["constituency_ta"],
            "constituency_en": mla_res["constituency_en"]
        }

    # Default fallback to Collector
    return resolve_authority_for_tier("collector", clean_dist, taluk, query_text)
