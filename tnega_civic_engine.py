"""
==============================================================================
Makkal Agent AI - TNeGA Civic & e-Governance Engine (இ-சேவை & அரசு சான்றிதழ்கள்)
Part of Meta AI Developer Hackathon 2026 ($150,000 Track)
==============================================================================
Provides statutory documentation checklists, step-by-step procedures, and official
government fee locking for Tamil Nadu e-Governance Agency (TNeGA) & e-Sevai services:
1. Patta / Chitta Extraction & Ownership Mutation (பட்டா / சிட்டா பெயர் மாற்றம்)
2. Encumbrance Certificate (EC - வில்லங்கச் சான்றிதழ் via TNREGINET)
3. Smart Ration Card Updates (குடும்ப அட்டை திருத்தங்கள் via TNePDS)
4. Higher Education Scholarships (புதுமைப் பெண், தமிழ்ப் புதல்வன், முதல் பட்டதாரி)
Blocks corrupt middleman extortion (₹1,500 - ₹3,500) by locking official statutory fees (₹0 - ₹60).
==============================================================================
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

TNEGA_CIVIC_SERVICES_DB: Dict[str, Dict[str, Any]] = {
    "patta_chitta": {
        "service_id": "patta_chitta",
        "service_name_ta": "பட்டா / சிட்டா நகல் எடுத்தல் & பட்டா பெயர் மாற்றம்",
        "service_name_en": "Patta / Chitta Extraction & Land Mutation",
        "department_ta": "வருவாய்த்துறை (Revenue & Disaster Management Dept)",
        "portal_name": "AnyWhere e-Sevai / e-Services (eservices.tn.gov.in)",
        "statutory_fee_lock": "₹60 (அரசு கட்டணம் மட்டுமே)",
        "middleman_extortion_blocked": "₹3,500 வரை இடைத்தரகர்கள் வசூலிக்கும் லஞ்சம் தடுக்கப்படுகிறது",
        "turnaround_days": "15 முதல் 30 வேலை நாட்கள் (வட்டார வருவாய் ஆய்வாளர் & வட்டாட்சியர் ஒப்புதல்)",
        "mandatory_checklist": [
            {
                "doc_code": "sale_deed",
                "doc_name_ta": "கிரையப் பத்திரம் / பத்திர நகல் (Registered Sale Deed)",
                "doc_name_en": "Registered Sale Deed / Title Deed",
                "is_mandatory": True,
                "notes_ta": "சார்பதிவாளர் அலுவலக பதிவு எண் மற்றும் தேதி தெளிவாக இருக்க வேண்டும்."
            },
            {
                "doc_code": "previous_patta",
                "doc_name_ta": "முந்தைய பட்டா நகல் (Previous Patta Copy)",
                "doc_name_en": "Parent Patta Copy",
                "is_mandatory": True,
                "notes_ta": "முந்தைய உரிமையாளர் பெயரில் உள்ள பட்டா எண் அல்லது சிட்டா நகல்."
            },
            {
                "doc_code": "encumbrance_certificate",
                "doc_name_ta": "வில்லங்கச் சான்றிதழ் (Encumbrance Certificate - EC)",
                "doc_name_en": "Encumbrance Certificate (EC)",
                "is_mandatory": True,
                "notes_ta": "குறைந்தது 13 முதல் 30 ஆண்டுகளுக்கான வில்லங்கச் சான்றிதழ் வில்லங்கம் இல்லை என்பதை உறுதி செய்ய வேண்டும்."
            },
            {
                "doc_code": "aadhaar_card",
                "doc_name_ta": "விண்ணப்பதாரரின் ஆதார் அட்டை (Aadhaar Card)",
                "doc_name_en": "Applicant's Aadhaar Card",
                "is_mandatory": True,
                "notes_ta": "ஆதார் அட்டையில் உள்ள பெயரும் பத்திரத்தில் உள்ள பெயரும் ஒன்றாக இருக்க வேண்டும்."
            },
            {
                "doc_code": "parent_document",
                "doc_name_ta": "முந்தைய தாய் பத்திரம் (Parent Title Deed / Link Documents)",
                "doc_name_en": "Parent Deed / Chain Documents",
                "is_mandatory": False,
                "notes_ta": "உரிமைத் தொடர்ச்சி (Title Continuity) உறுதி செய்ய தேவைப்படலாம்."
            },
            {
                "doc_code": "fmb_sketch",
                "doc_name_ta": "புல வரைபடம் (Field Measurement Book - FMB Sketch)",
                "doc_name_en": "FMB Sub-division Sketch",
                "is_mandatory": False,
                "notes_ta": "உட்பிரிவு பட்டா மாற்றம் (Sub-division Patta) என்றால் கிராம நிர்வாக அலுவலர் (VAO) வரைபடம் தேவை."
            },
            {
                "doc_code": "legal_heir_cert",
                "doc_name_ta": "வாரிசுச் சான்றிதழ் (Legal Heir Certificate - வாரிசுரிமை எனில்)",
                "doc_name_en": "Legal Heir Certificate (for inheritance)",
                "is_mandatory": False,
                "notes_ta": "பூர்வீக சொத்து அல்லது மறைந்த உரிமையாளரின் வாரிசுகள் பெயருக்கு மாற்றம் செய்யும்போது கட்டாயம்."
            }
        ],
        "step_by_step_workflow": [
            "1. eservices.tn.gov.in போர்ட்டலில் 'பட்டா மாறுதல் விண்ணப்பிக்க' (Apply Patta Transfer) கிளிக் செய்யவும்.",
            "2. மாவட்டம், வட்டம், கிராமம் தேர்ந்தெடுத்து சர்வே எண் மற்றும் உட்பிரிவு எண் உள்ளிடவும்.",
            "3. கிரையப் பத்திரம், முந்தைய பட்டா, வில்லங்கச் சான்றிதழ் மற்றும் ஆதார் அட்டையை PDF வடிவில் பதிவேற்றவும்.",
            "4. ₹60 அரசு கட்டணத்தை UPI / NetBanking மூலம் செலுத்தி ஒப்புதல் ரசீது (Ack Slip) பெறவும்.",
            "5. கிராம நிர்வாக அலுவலர் (VAO) மற்றும் வருவாய் ஆய்வாளர் (RI) நில ஆய்வு செய்து வட்டாட்சியர் (Tahsildar) புதிய பட்டாவை டிஜிட்டல் கையொப்பத்துடன் வெளியிடுவார்."
        ]
    },

    "encumbrance_certificate": {
        "service_id": "encumbrance_certificate",
        "service_name_ta": "வில்லங்கச் சான்றிதழ் (Encumbrance Certificate - EC)",
        "service_name_en": "Encumbrance Certificate (EC) via TNREGINET",
        "department_ta": "பதிவுத்துறை (Registration Department, Tamil Nadu)",
        "portal_name": "TNREGINET Portal (tnreginet.gov.in)",
        "statutory_fee_lock": "இணையதள பார்வை முற்றிலும் இலவசம்; சான்றளிக்கப்பட்ட நகல் (Certified Copy) ₹30 முதல் ₹100 மட்டுமே",
        "middleman_extortion_blocked": "₹1,500 வரை சார்பதிவாளர் அலுவலக புரோக்கர்கள் ஏமாற்றுவது தடுக்கப்படுகிறது",
        "turnaround_days": "இணையதளத்தில் உடனடி பதிவிறக்கம் (1975 முதல் இன்று வரை)",
        "mandatory_checklist": [
            {
                "doc_code": "sro_jurisdiction",
                "doc_name_ta": "சார்பதிவாளர் அலுவலகம் (Sub-Registrar Office - SRO எல்லை)",
                "doc_name_en": "Jurisdictional Sub-Registrar Office",
                "is_mandatory": True,
                "notes_ta": "சொத்து அமைந்துள்ள வருவாய் கிராமம் எந்த சார்பதிவாளர் அலுவலக எல்லைக்குள் வருகிறது என்பதை அறியவும்."
            },
            {
                "doc_code": "survey_details",
                "doc_name_ta": "சர்வே எண் & உட்பிரிவு எண் (Survey No & Sub-Division No)",
                "doc_name_en": "Survey & Sub-Division Coordinates",
                "is_mandatory": True,
                "notes_ta": "பத்திரத்தில் குறிப்பிடப்பட்டுள்ள சரியான புல எண் (Survey No)."
            },
            {
                "doc_code": "search_period",
                "doc_name_ta": "வில்லங்க தேடல் கால வரம்பு (Period of Search: 13 to 30 Years)",
                "doc_name_en": "Search Date Range",
                "is_mandatory": True,
                "notes_ta": "வங்கிக் கடன் மற்றும் நில விற்பனைக்கு குறைந்தபட்சம் 30 ஆண்டுகள் வில்லங்க தேடல் பரிந்துரைக்கப்படுகிறது."
            },
            {
                "doc_code": "deed_number",
                "doc_name_ta": "பத்திரப் பதிவு எண் (Document Number - தெரிந்தால்)",
                "doc_name_en": "Document Number / Year",
                "is_mandatory": False,
                "notes_ta": "பத்திர எண் தெரிந்தால் நேரடியாக விரைவாக வில்லங்கம் எடுக்கலாம்."
            }
        ],
        "step_by_step_workflow": [
            "1. tnreginet.gov.in போர்ட்டலில் 'மின்னணு சேவைகள்' -> 'வில்லங்கச் சான்றிதழ்' -> 'வில்லங்கச் சான்றிதழ் பார்வையிடுதல்' கிளிக் செய்யவும்.",
            "2. மண்டலம், மாவட்டம், சார்பதிவாளர் அலுவலகம், கிராமம் தேர்ந்தெடுக்கவும்.",
            "3. தொடக்க தேதி (எ.கா. 01/01/1990) மற்றும் முடிவு தேதி (இன்றைய தேதி) உள்ளிடவும்.",
            "4. சர்வே எண் மற்றும் உட்பிரிவு எண் உள்ளிட்டு 'தேடுக' கிளிக் செய்யவும்.",
            "5. திரையில் தோன்றும் வில்லங்க குறிப்பை சரிபார்த்து இலவசமாக PDF பதிவிறக்கம் செய்துகொள்ளலாம்."
        ]
    },

    "smart_ration_card": {
        "service_id": "smart_ration_card",
        "service_name_ta": "ஸ்மார்ட் குடும்ப அட்டை திருத்தங்கள் & உறுப்பினர் சேர்த்தல்/நீக்கல்",
        "service_name_en": "Smart Ration Card Updates & Member Addition/Deletion",
        "department_ta": "உணவு & நுகர்வோர் பாதுகாப்புத் துறை (TNePDS)",
        "portal_name": "TNePDS Portal (tnpds.gov.in) & இ-சேவை",
        "statutory_fee_lock": "100% முற்றிலும் இலவசம் (அரசு கட்டணம் ₹0; இ-சேவை மையத்தில் அதிகபட்சம் ₹30 மட்டுமே)",
        "middleman_extortion_blocked": "₹1,000 முதல் ₹2,000 வரை ரேஷன் கார்டு புரோக்கர்கள் வசூலிப்பது தடுக்கப்படுகிறது",
        "turnaround_days": "7 முதல் 15 வேலை நாட்கள் (வட்ட வழங்கல் அலுவலர் - TSO ஆய்வு)",
        "mandatory_checklist": [
            {
                "doc_code": "child_birth_cert",
                "doc_name_ta": "குழந்தை பிறப்புச் சான்றிதழ் (Member Addition - குழந்தை சேர்க்கை எனில்)",
                "doc_name_en": "Birth Certificate of Child",
                "is_mandatory": False,
                "notes_ta": "5 வயதுக்குட்பட்ட குழந்தைகளுக்கு பிறப்புச் சான்றிதழ் போதுமானது; 5 வயதுக்கு மேற்பட்டோருக்கு ஆதார் கட்டாயம்."
            },
            {
                "doc_code": "marriage_noc_cert",
                "doc_name_ta": "திருமணச் சான்றிதழ் / தாயக அட்டை நீக்கல் சான்று (Member Addition - திருமணத்திற்கு பின்)",
                "doc_name_en": "Marriage Certificate / Parent Card Deletion Certificate",
                "is_mandatory": False,
                "notes_ta": "மணமகள் அவரது பெற்றோர் குடும்ப அட்டையிலிருந்து பெயர் நீக்கப்பட்டதற்கான நீக்கல் சான்றிதழ் (Deletion Certificate) அவசியம்."
            },
            {
                "doc_code": "death_certificate",
                "doc_name_ta": "இறப்புச் சான்றிதழ் (Member Deletion - மரணம் எனில்)",
                "doc_name_en": "Death Certificate",
                "is_mandatory": False,
                "notes_ta": "குடும்ப உறுப்பினர் மறைந்தால் பெயரை நீக்குவதற்கு அரசு பதிவு செய்யப்பட்ட இறப்புச் சான்று."
            },
            {
                "doc_code": "address_proof",
                "doc_name_ta": "முகவரி ஆதார ஆவணம் (Address Change - முகவரி மாற்றம் எனில்)",
                "doc_name_en": "Electricity Bill / Gas Bill / Rental Agreement / Patta",
                "is_mandatory": False,
                "notes_ta": "மின் கட்டண ரசீது, சமையல் எரிவாயு அட்டை, வீட்டு வாடகை ஒப்பந்தம் அல்லது பட்டா."
            },
            {
                "doc_code": "head_aadhaar",
                "doc_name_ta": "குடும்பத் தலைவர் & உறுப்பினர்களின் ஆதார் அட்டை (Aadhaar Cards)",
                "doc_name_en": "Aadhaar Cards of All Members",
                "is_mandatory": True,
                "notes_ta": "அனைத்து குடும்ப உறுப்பினர்களின் ஆதாருடன் இணைக்கப்பட்ட மொபைல் எண் அவசியம்."
            }
        ],
        "step_by_step_workflow": [
            "1. tnpds.gov.in தளத்தில் குடும்ப அட்டையுடன் இணைந்த மொபைல் எண்ணை உள்ளிட்டு OTP மூலம் உள்நுழையவும்.",
            "2. 'உறுப்பினர் சேர்க்க' அல்லது 'குடும்ப அட்டை முகவரி மாற்ற' விருப்பத்தை தேர்வு செய்யவும்.",
            "3. உறுப்பினரின் ஆதார் எண், பாலினம், பிறந்த தேதி மற்றும் உறவுமுறையை உள்ளிடவும்.",
            "4. உரிய ஆவணத்தை (பிறப்புச் சான்றிதழ் / நீக்கல் சான்றிதழ் / முகவரி சான்று) பதிவேற்றவும்.",
            "5. விண்ணப்ப எண் (Reference Number) திரையில் தோன்றும்; 15 நாட்களில் வட்ட வழங்கல் அலுவலர் (TSO) ஒப்புதல் அளிப்பார்."
        ]
    },

    "higher_education_scholarships": {
        "service_id": "higher_education_scholarships",
        "service_name_ta": "தமிழ்நாடு உயர் கல்வி உதவித்தொகைகள் & புதுமைப் பெண் / தமிழ்ப் புதல்வன் திட்டம்",
        "service_name_en": "Tamil Nadu Higher Education Scholarships (Pudhumai Penn, Tamil Pudhalvan, First Graduate)",
        "department_ta": "சமூக நலத்துறை & ஆதிதிராவிடர் நலத்துறை, தமிழ்நாடு அரசு",
        "portal_name": "புதுமைப் பெண் போர்ட்டல் (pudhumaipenn.tn.gov.in) / e-Sevai / UMIS",
        "statutory_fee_lock": "100% இலவசம் (இ-சேவை மைய விண்ணப்பக் கட்டணம் ₹60 மட்டுமே)",
        "middleman_extortion_blocked": "₹2,000 வரை கல்லூரி சேர்க்கை புரோக்கர்கள் ஏமாற்றுவது தடுக்கப்படுகிறது",
        "turnaround_days": "கல்லூரி சரிபார்ப்பிற்கு பின் மாதாந்திர தவணையாக வங்கிக் கணக்கில் நேரடியாக வரவு (DBT)",
        "mandatory_checklist": [
            {
                "doc_code": "govt_school_bonafide",
                "doc_name_ta": "6 முதல் 12 ஆம் வகுப்பு வரை அரசுப் பள்ளி படிப்புச் சான்றிதழ் (Govt School 6th to 12th Certificate)",
                "doc_name_en": "Government School Bonafide Certificate (6th to 12th)",
                "is_mandatory": True,
                "notes_ta": "புதுமைப் பெண் (₹1,000/மாதம்) மற்றும் தமிழ்ப் புதல்வன் (₹1,000/மாதம்) திட்டத்திற்கு கட்டாயம்."
            },
            {
                "doc_code": "college_id_admission",
                "doc_name_ta": "கல்லூரி சேர்க்கை ஆவணம் & அடையாள அட்டை (College Admission & ID Card)",
                "doc_name_en": "College Allotment Order / Student ID Card",
                "is_mandatory": True,
                "notes_ta": "அங்கீகரிக்கப்பட்ட கலை, அறிவியல், பொறியியல் அல்லது பாலிடெக்னிக் கல்லூரி சேர்க்கை அட்டை."
            },
            {
                "doc_code": "first_graduate_cert",
                "doc_name_ta": "முதல் பட்டதாரி சான்றிதழ் (First Graduate Certificate - முதல் பட்டதாரி எனில்)",
                "doc_name_en": "First Graduate Certificate from Tahsildar",
                "is_mandatory": False,
                "notes_ta": "குடும்பத்தில் பட்டதாரி யாரும் இல்லை என்பதை உறுதி செய்யும் வட்டாட்சியர் சான்றிதழ் (கல்விக் கட்டண விலக்கு ₹25,000-₹50,000)."
            },
            {
                "doc_code": "income_community_cert",
                "doc_name_ta": "வருமானச் சான்றிதழ் & சாதிச் சான்றிதழ் (Income & Community Certificates)",
                "doc_name_en": "Income Certificate (< ₹2.5 Lakhs) & Community Certificate",
                "is_mandatory": True,
                "notes_ta": "போஸ்ட்-மெட்ரிக் கல்வி உதவித்தொகை மற்றும் கட்டண சலுகைக்கு ஆண்டு வருமானம் ₹2.5 லட்சத்திற்குள் இருக்க வேண்டும்."
            },
            {
                "doc_code": "aadhaar_bank_passbook",
                "doc_name_ta": "ஆதாருடன் இணைக்கப்பட்ட தேசியமயமாக்கப்பட்ட வங்கி பாஸ்புக் (Aadhaar Seeded Bank Account)",
                "doc_name_en": "Aadhaar-Linked Bank Account Passbook",
                "is_mandatory": True,
                "notes_ta": "மாதந்தோறும் ₹1,000 நேரடி உதவித்தொகை பெற NPCI ஆதாருடன் இணைக்கப்பட்ட வங்கிக் கணக்கு அவசியம்."
            }
        ],
        "step_by_step_workflow": [
            "1. கல்லூரி அலுவலகத்தில் உள்ள கல்வி உதவித்தொகை ஒருங்கிணைப்பாளரிடம் (Scholarship Coordinator) தொடர்பு கொள்ளவும்.",
            "2. புதுமைப் பெண் / தமிழ்ப் புதல்வன் திட்டத்திற்கு 6-12 அரசுப் பள்ளி மாற்றுச் சான்றிதழ் (TC) மற்றும் ஆதார் சமர்ப்பிக்கவும்.",
            "3. முதல் பட்டதாரி சலுகைக்கு இ-சேவை மையம் மூலம் வட்டாட்சியரிடம் முதல் பட்டதாரி சான்று பெற்று கல்லூரியில் சமர்ப்பிக்கவும்.",
            "4. UMIS மாணவர் போர்ட்டலில் கல்லூரி நிர்வாகம் விவரங்களை பதிவு செய்யும்.",
            "5. தமிழக அரசால் மாதம் ₹1,000 அல்லது கல்விக் கட்டணத் தொகை நேரடியாக மாணவரின் வங்கிக் கணக்கில் வரவு வைக்கப்படும்."
        ]
    }
}


def get_all_tnega_services() -> List[Dict[str, Any]]:
    """Returns catalog of supported TNeGA civic services with statutory fee locks."""
    output = []
    for key, val in TNEGA_CIVIC_SERVICES_DB.items():
        output.append({
            "service_id": key,
            "service_name_ta": val["service_name_ta"],
            "service_name_en": val["service_name_en"],
            "department_ta": val["department_ta"],
            "statutory_fee_lock": val["statutory_fee_lock"],
            "middleman_extortion_blocked": val["middleman_extortion_blocked"],
            "document_count": len(val["mandatory_checklist"])
        })
    return output


def get_tnega_service_checklist(service_id: str) -> Dict[str, Any]:
    """Returns complete checklist, step-by-step procedure, and statutory fee lock for a service."""
    service = TNEGA_CIVIC_SERVICES_DB.get(service_id.lower().strip())
    if not service:
        # Fuzzy fallback
        for k, v in TNEGA_CIVIC_SERVICES_DB.items():
            if k in service_id.lower() or service_id.lower() in v["service_name_en"].lower():
                service = v
                break
    if not service:
        return {"error": f"TNeGA Service '{service_id}' not found."}
    return service


def validate_citizen_document_bundle(service_id: str, uploaded_doc_codes: List[str]) -> Dict[str, Any]:
    """
    Cross-checks citizen's uploaded document list against the mandatory TNeGA checklist.
    Returns readiness percentage, missing mandatory documents, and guidance in spoken Tamil.
    """
    service = get_tnega_service_checklist(service_id)
    if "error" in service:
        return service

    checklist = service["mandatory_checklist"]
    mandatory_codes = [d["doc_code"] for d in checklist if d["is_mandatory"]]
    
    missing_docs = []
    present_docs = []

    for item in checklist:
        code = item["doc_code"]
        if code in uploaded_doc_codes:
            present_docs.append(item["doc_name_ta"])
        elif item["is_mandatory"]:
            missing_docs.append({
                "doc_code": code,
                "doc_name_ta": item["doc_name_ta"],
                "notes_ta": item["notes_ta"]
            })

    total_mandatory = len(mandatory_codes)
    fulfilled_mandatory = total_mandatory - len(missing_docs)
    readiness_percentage = int((fulfilled_mandatory / max(total_mandatory, 1)) * 100)

    is_ready = len(missing_docs) == 0

    if is_ready:
        advice_ta = (
            f"✅ வாழ்த்துகள்! {service['service_name_ta']} விண்ணப்பிக்க தேவையான அனைத்து கட்டாய ஆவணங்களும் உங்களிடம் உள்ளன. "
            f"இடைத்தரகர்களுக்கு ₹3,500 கொடுக்க வேண்டாம். அரசு கட்டணம் {service['statutory_fee_lock']} மட்டுமே செலுத்தி இ-சேவை மூலம் உடனே விண்ணப்பிக்கலாம்."
        )
    else:
        missing_names = ", ".join([d["doc_name_ta"] for d in missing_docs])
        advice_ta = (
            f"⚠️ கவனம்: {service['service_name_ta']} பெற உங்களிடம் இன்னும் {len(missing_docs)} கட்டாய ஆவணங்கள் தேவைப்படுகின்றன: "
            f"({missing_names}). இந்த ஆவணங்களை தயார் செய்துவிட்டு விண்ணப்பிக்கவும்."
        )

    return {
        "service_id": service_id,
        "service_name_ta": service["service_name_ta"],
        "readiness_percentage": readiness_percentage,
        "is_ready_for_esevai": is_ready,
        "present_documents": present_docs,
        "missing_mandatory_documents": missing_docs,
        "statutory_fee_lock": service["statutory_fee_lock"],
        "advice_ta": advice_ta
    }
