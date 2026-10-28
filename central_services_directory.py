# -*- coding: utf-8 -*-
"""
Makkal Agent AI - Pan-India Central Government Services & Digital Rights Directory
Meta AI Developer Hackathon 2026

Provides comprehensive, legally grounded data structures and resolution engines for:
1. Right to Information Act 2005 (RTI / தகவல் அறியும் உரிமைச் சட்டம்)
2. 39 Members of Parliament (MP / நாடாளுமன்ற உறுப்பினர்) Tamil Nadu Directory
3. Aadhaar Online Updation & Identity Lifeline (UIDAI myaadhaar)
4. National Competitive Exams (NEET UG, UPSC Civil Services, TNPSC)
5. SWAYAM / NPTEL National Free Higher Education & Skilling Portal
"""

from typing import Dict, List, Any, Optional

# ==============================================================================
# 1. RIGHT TO INFORMATION ACT 2005 (RTI / தகவல் அறியும் உரிமைச் சட்டம்)
# ==============================================================================

RTI_CONFIG = {
    "statute_title_ta": "தகவல் அறியும் உரிமைச் சட்டம் 2005 (பிரிவு 6(1))",
    "statute_title_en": "Right to Information Act 2005 (Section 6(1))",
    "fee_rules": {
        "central_gov_inr": 10,
        "tamil_nadu_gov_inr": 10,
        "bpl_fee_inr": 0,
        "mode_of_payment": "நீதிமன்ற கட்டண வில்லை (Court Fee Stamp) / அஞ்சல் ஆணை (IPO) / இணைய வழி கட்டணம் (UPI/NetBanking)"
    },
    "sla_mandate": {
        "standard_days": 30,
        "life_and_liberty_hours": 48,
        "third_party_days": 40
    },
    "appellate_structure": {
        "first_appeal": "முதல் மேல்முறையீட்டு அலுவலர் (FAA) - 30 நாட்களுக்குள் (பிரிவு 19(1))",
        "second_appeal": "மாநில தகவல் ஆணையம் (SIC) / மத்திய தகவல் ஆணையம் (CIC) - 90 நாட்களுக்குள் (பிரிவு 19(3))"
    },
    "official_portals": [
        {
            "name": "Central RTI Online Portal",
            "url": "https://rtionline.gov.in",
            "jurisdiction": "மத்திய அரசு துறைகள், ரயில்வே, அஞ்சலகம், வங்கிகள்"
        },
        {
            "name": "Tamil Nadu RTI Online Portal",
            "url": "https://rtionline.tn.gov.in",
            "jurisdiction": "தமிழ்நாடு வருவாய்த்துறை, காவல்துறை, உள்ளாட்சி மன்றங்கள்"
        }
    ],
    "sample_categories": [
        {
            "id": "panchayat_funds",
            "title_ta": "ஊராட்சி மன்ற நிதி & சாலை டெண்டர் செலவு விவரம்",
            "title_en": "Village Panchayat Fund Expenditure & Road Works Audit",
            "questions_ta": [
                "கடந்த 3 ஆண்டுகளில் எங்கள் கிராம ஊராட்சியில் மேற்கொள்ளப்பட்ட அனைத்து சாலை மற்றும் குடிநீர் பணிகளின் முழுமையான செலவு அறிக்கை நகல் வழங்கவும்.",
                "ஒவ்வொரு பணிக்கும் ஒதுக்கப்பட்ட அரசு நிதி மற்றும் ஒப்பந்ததாரர் பெயர் விவரங்களை வழங்கவும்.",
                "பணிகள் முழுமை பெற்றமைக்கான தரச் சான்றிதழ் (Completion Certificate) நகல் வழங்கவும்."
            ]
        },
        {
            "id": "patta_delay_inquiry",
            "title_ta": "பட்டா மனு மீது நடவடிக்கை எடுக்காததற்கான காரணக் கோரிக்கை",
            "title_en": "RTI for Long Pending Patta Mutation Application",
            "questions_ta": [
                "எனது பட்டா மாறுதல் விண்ணப்பம் (எண்: {app_no}) மீது நாள் வாரியாக எடுக்கப்பட்ட நடவடிக்கை குறிப்புகள் (Daily Progress Notes) நகல் வழங்கவும்.",
                "குறிப்பிட்ட காலக்கெடுவுக்குள் மனுவை முடிக்காததற்கு பொறுப்பான அலுவலரின் பெயர் மற்றும் பதவி விவரங்களை வழங்கவும்.",
                "குடிமக்கள் சாசன விதிகளின்படி இந்த மனு எப்போது முடிக்கப்படும் என்ற அதிகாரப்பூர்வ தேதியை தெரிவிக்கவும்."
            ]
        },
        {
            "id": "ration_food_audit",
            "title_ta": "ரேஷன் கடை உணவுப் பொருள் ஒதுக்கீடு & இருப்பு விவரம்",
            "title_en": "Fair Price Shop (Ration) Monthly Stock & Sales Register",
            "questions_ta": [
                "எங்கள் கிராம நியாயவிலைக் கடைக்கு கடந்த 6 மாதங்களில் ஒதுக்கப்பட்ட அரிசி, சர்க்கரை மற்றும் பருப்பு அளவுகளின் மாதாந்திர பதிவேடு நகல் வழங்கவும்.",
                "பயனாளிகளுக்கு வழங்கப்பட்ட விற்பனைப் பதிவேட்டின் (Sales Register) சான்றளிக்கப்பட்ட நகல் வழங்கவும்."
            ]
        }
    ]
}

# ==============================================================================
# 2. 39 TAMIL NADU LOK SABHA MEMBERS OF PARLIAMENT (MP) DIRECTORY
# ==============================================================================

TN_LOK_SABHA_MPS: List[Dict[str, Any]] = [
    {"no": 1, "constituency_ta": "திருவள்ளூர் (தனி)", "constituency_en": "Thiruvallur (SC)", "mp_name_ta": "சசிகாந்த் செந்தில்", "mp_name_en": "Sasikanth Senthil", "party": "INC", "district": "Tiruvallur"},
    {"no": 2, "constituency_ta": "வட சென்னை", "constituency_en": "Chennai North", "mp_name_ta": "டாக்டர் கலாநிதி வீராசாமி", "mp_name_en": "Dr. Kalanidhi Veeraswamy", "party": "DMK", "district": "Chennai"},
    {"no": 3, "constituency_ta": "தென் சென்னை", "constituency_en": "Chennai South", "mp_name_ta": "தமிழிச்சி தங்கபாண்டியன்", "mp_name_en": "Thamizhachi Thangapandian", "party": "DMK", "district": "Chennai"},
    {"no": 4, "constituency_ta": "மத்திய சென்னை", "constituency_en": "Chennai Central", "mp_name_ta": "தயாகரன் மாறன்", "mp_name_en": "Dayanidhi Maran", "party": "DMK", "district": "Chennai"},
    {"no": 5, "constituency_ta": "ஸ்ரீபெரும்புதூர்", "constituency_en": "Sriperumbudur", "mp_name_ta": "டி.ஆர். பாலு", "mp_name_en": "T. R. Baalu", "party": "DMK", "district": "Kancheepuram"},
    {"no": 6, "constituency_ta": "காஞ்சிபுரம் (தனி)", "constituency_en": "Kancheepuram (SC)", "mp_name_ta": "ஜி. செல்வம்", "mp_name_en": "G. Selvam", "party": "DMK", "district": "Kancheepuram"},
    {"no": 7, "constituency_ta": "அரக்கோணம்", "constituency_en": "Arakkonam", "mp_name_ta": "எஸ். ஜெகத்ரட்சகன்", "mp_name_en": "S. Jagathrakshakan", "party": "DMK", "district": "Ranipet"},
    {"no": 8, "constituency_ta": "வேலூர்", "constituency_en": "Vellore", "mp_name_ta": "டி.எம். கதிர் ஆனந்த்", "mp_name_en": "D. M. Kathir Anand", "party": "DMK", "district": "Vellore"},
    {"no": 9, "constituency_ta": "திருவண்ணாமலை", "constituency_en": "Tiruvannamalai", "mp_name_ta": "சி.என். அண்ணாதுரை", "mp_name_en": "C. N. Annadurai", "party": "DMK", "district": "Tiruvannamalai"},
    {"no": 10, "constituency_ta": "ஆரணி", "constituency_en": "Arani", "mp_name_ta": "எம்.எஸ். தரணிவேந்தன்", "mp_name_en": "M. S. Tharanivendhan", "party": "DMK", "district": "Tiruvannamalai"},
    {"no": 11, "constituency_ta": "விழுப்புரம் (தனி)", "constituency_en": "Viluppuram (SC)", "mp_name_ta": "துரை ரவிக்குமார்", "mp_name_en": "D. Ravikumar", "party": "VCK", "district": "Viluppuram"},
    {"no": 12, "constituency_ta": "கள்ளக்குறிச்சி", "constituency_en": "Kallakurichi", "mp_name_ta": "தேவராஜன் மலையரசன்", "mp_name_en": "D. Malaiyarasan", "party": "DMK", "district": "Kallakurichi"},
    {"no": 13, "constituency_ta": "சேலம்", "constituency_en": "Salem", "mp_name_ta": "டி.எம். செல்வகணபதி", "mp_name_en": "T. M. Selvaganapathi", "party": "DMK", "district": "Salem"},
    {"no": 14, "constituency_ta": "நாமக்கல்", "constituency_en": "Namakkal", "mp_name_ta": "வி.எஸ். மாதேஸ்வரன்", "mp_name_en": "V. S. Matheswaran", "party": "KMDK", "district": "Namakkal"},
    {"no": 15, "constituency_ta": "ஈரோடு", "constituency_en": "Erode", "mp_name_ta": "கே.இ. பிரகாஷ்", "mp_name_en": "K. E. Prakash", "party": "DMK", "district": "Erode"},
    {"no": 16, "constituency_ta": "திருப்பூர்", "constituency_en": "Tiruppur", "mp_name_ta": "கே. சுப்பராயன்", "mp_name_en": "K. Subbarayan", "party": "CPI", "district": "Tiruppur"},
    {"no": 17, "constituency_ta": "நீலகிரி (தனி)", "constituency_en": "Nilgiris (SC)", "mp_name_ta": "ஆ. ராசா", "mp_name_en": "A. Raja", "party": "DMK", "district": "Nilgiris"},
    {"no": 18, "constituency_ta": "கோயம்புத்தூர்", "constituency_en": "Coimbatore", "mp_name_ta": "கணபதி பி. ராஜ்குமார்", "mp_name_en": "Ganapathi P. Rajkumar", "party": "DMK", "district": "Coimbatore"},
    {"no": 19, "constituency_ta": "பொள்ளாச்சி", "constituency_en": "Pollachi", "mp_name_ta": "கே. ஈஸ்வரசாமி", "mp_name_en": "K. Easwarasamy", "party": "DMK", "district": "Coimbatore"},
    {"no": 20, "constituency_ta": "திண்டுக்கல்", "constituency_en": "Dindigul", "mp_name_ta": "ஆர். சச்சிதானந்தம்", "mp_name_en": "R. Sachithanantham", "party": "CPI(M)", "district": "Dindigul"},
    {"no": 21, "constituency_ta": "கரூர்", "constituency_en": "Karur", "mp_name_ta": "ஜோதிமணி", "mp_name_en": "S. Jothimani", "party": "INC", "district": "Karur"},
    {"no": 22, "constituency_ta": "திருச்சிராப்பள்ளி", "constituency_en": "Tiruchirappalli", "mp_name_ta": "துரை வைகோ", "mp_name_en": "Durai Vaiko", "party": "MDMK", "district": "Tiruchirappalli"},
    {"no": 23, "constituency_ta": "பெரம்பலூர்", "constituency_en": "Perambalur", "mp_name_ta": "அருண் நேரு", "mp_name_en": "Arun Nehru", "party": "DMK", "district": "Perambalur"},
    {"no": 24, "constituency_ta": "கடலூர்", "constituency_en": "Cuddalore", "mp_name_ta": "எம்.கே. விஷ்ணு பிரசாத்", "mp_name_en": "M. K. Vishnu Prasad", "party": "INC", "district": "Cuddalore"},
    {"no": 25, "constituency_ta": "சிதம்பரம் (தனி)", "constituency_en": "Chidambaram (SC)", "mp_name_ta": "தொல். திருமாவளவன்", "mp_name_en": "Thol. Thirumavalavan", "party": "VCK", "district": "Cuddalore"},
    {"no": 26, "constituency_ta": "மயிலாடுதுறை", "constituency_en": "Mayiladuthurai", "mp_name_ta": "சுதா ராமகிருஷ்ணன்", "mp_name_en": "R. Sudha", "party": "INC", "district": "Mayiladuthurai"},
    {"no": 27, "constituency_ta": "நாகப்பட்டினம் (தனி)", "constituency_en": "Nagapattinam (SC)", "mp_name_ta": "வி. செல்வராஜ்", "mp_name_en": "V. Selvaraj", "party": "CPI", "district": "Nagapattinam"},
    {"no": 28, "constituency_ta": "தஞ்சாவூர்", "constituency_en": "Thanjavur", "mp_name_ta": "எஸ். முரசோலி", "mp_name_en": "S. Murasoli", "party": "DMK", "district": "Thanjavur"},
    {"no": 29, "constituency_ta": "சிவகங்கை", "constituency_en": "Sivaganga", "mp_name_ta": "கார்த்தி ப. சிதம்பரம்", "mp_name_en": "Karti P. Chidambaram", "party": "INC", "district": "Sivaganga"},
    {"no": 30, "constituency_ta": "மதுரை", "constituency_en": "Madurai", "mp_name_ta": "சு. வெங்கடேசன்", "mp_name_en": "Su. Venkatesan", "party": "CPI(M)", "district": "Madurai"},
    {"no": 31, "constituency_ta": "தேனி", "constituency_en": "Theni", "mp_name_ta": "தங்க தமிழ்செல்வன்", "mp_name_en": "Thanga Tamil Selvan", "party": "DMK", "district": "Theni"},
    {"no": 32, "constituency_ta": "விருதுநகர்", "constituency_en": "Virudhunagar", "mp_name_ta": "மாணிக்கம் தாகூர்", "mp_name_en": "Manickam Tagore", "party": "INC", "district": "Virudhunagar"},
    {"no": 33, "constituency_ta": "ராமநாதபுரம்", "constituency_en": "Ramanathapuram", "mp_name_ta": "நவாஸ் கனி", "mp_name_en": "K. Navaskani", "party": "IUML", "district": "Ramanathapuram"},
    {"no": 34, "constituency_ta": "தூத்துக்குடி", "constituency_en": "Thoothukkudi", "mp_name_ta": "கனிமொழி கருணாநிதி", "mp_name_en": "Kanimozhi Karunanidhi", "party": "DMK", "district": "Thoothukkudi"},
    {"no": 35, "constituency_ta": "தென்காசி (தனி)", "constituency_en": "Tenkasi (SC)", "mp_name_ta": "ராணி ஸ்ரீகுமார்", "mp_name_en": "Dr. Rani Srikumar", "party": "DMK", "district": "Tenkasi"},
    {"no": 36, "constituency_ta": "திருநெல்வேலி", "constituency_en": "Tirunelveli", "mp_name_ta": "ராபர்ட் புரூஸ்", "mp_name_en": "C. Robert Bruce", "party": "INC", "district": "Tirunelveli"},
    {"no": 37, "constituency_ta": "கன்னியாகுமரி", "constituency_en": "Kanniyakumari", "mp_name_ta": "விஜய் வசந்த்", "mp_name_en": "Vijay Vasanth", "party": "INC", "district": "Kanniyakumari"},
    {"no": 38, "constituency_ta": "தருமபுரி", "constituency_en": "Dharmapuri", "mp_name_ta": "அ. மணி", "mp_name_en": "A. Mani", "party": "DMK", "district": "Dharmapuri"},
    {"no": 39, "constituency_ta": "கிருஷ்ணகிரி", "constituency_en": "Krishnagiri", "mp_name_ta": "கே. கோபிநாத்", "mp_name_en": "K. Gopinath", "party": "INC", "district": "Krishnagiri"}
]


def resolve_mp_by_district(district_name: str) -> Optional[Dict[str, Any]]:
    """Resolves Member of Parliament representation based on district name."""
    clean = district_name.strip().lower()
    for mp in TN_LOK_SABHA_MPS:
        if clean in mp["district"].lower() or clean in mp["constituency_en"].lower() or clean in mp["constituency_ta"]:
            return mp
    return TN_LOK_SABHA_MPS[3]  # Default to Chennai Central / Su. Venkatesan Madurai

# ==============================================================================
# 3. AADHAAR ONLINE SERVICES & IDENTITY LIFELINE (UIDAI)
# ==============================================================================

AADHAAR_CONFIG = {
    "official_portal": "https://myaadhaar.uidai.gov.in/",
    "portal_name": "UIDAI myAadhaar Official Portal",
    "services": [
        {
            "id": "address_update",
            "title_ta": "ஆதார் முகவரி மாற்றம் (Online Address Update)",
            "title_en": "Aadhaar Card Address Updation (Online)",
            "official_fee_inr": 50,
            "bribe_warning": "இடைத்தரகர்கள் ₹300 வரை கேட்பது சட்டவிரோதமானது. myAadhaar தளத்தில் அரசு கட்டணம் ₹50 மட்டுமே.",
            "sla_days": 15,
            "valid_address_proofs": [
                "வாக்காளர் அடையாள அட்டை (Voter ID / EPIC)",
                "பாஸ்போர்ட் (Indian Passport)",
                "வங்கி பாஸ்புக் (Bank Passbook with photo & branch seal)",
                "மின்சாரக் கட்டண ரசீது (Electricity Bill - last 3 months)",
                "சமையல் எரிவாயு இணைப்பு ரசீது (LPG Gas Connection Bill)",
                "பதிவு செய்யப்பட்ட வாடகை ஒப்பந்தம் (Registered Rent Agreement)",
                "குடும்ப அட்டை (Smart Ration Card)",
                "கிராம நிர்வாக அலுவலர் (VAO) / ஊராட்சி தலைவர் சான்றிதழ் (UIDAI Standard Certificate)"
            ],
            "step_by_step_guide_ta": [
                "1. myaadhaar.uidai.gov.in தளத்திற்கு சென்று உங்கள் ஆதார் எண் & OTP மூலம் உள்நுழையவும்.",
                "2. 'Update Address in your Aadhaar' என்ற விருப்பத்தைத் தேர்ந்தெடுக்கவும்.",
                "3. புதிய கதவு எண், தெரு மற்றும் பின்கோடை சரியாக தட்டச்சு செய்யவும்.",
                "4. அங்கீகரிக்கப்பட்ட முகவரி ஆவணத்தை (PDF/JPEG - 2MBக்குள்) தெளிவாக பதிவேற்றவும்.",
                "5. அதிகாரப்பூர்வ அரசு கட்டணமான ₹50-ஐ UPI அல்லது நெட்பேங்கிங் மூலம் செலுத்தவும்.",
                "6. பெறப்படும் 14 இலக்க URN (Update Request Number) எண்ணை குறித்து வைத்துக் கொள்ளவும்."
            ]
        },
        {
            "id": "mobile_link_guide",
            "title_ta": "ஆதாருடன் தொலைபேசி எண் இணைப்பு (Mobile Linkage)",
            "title_en": "Linking Mobile Number with Aadhaar",
            "official_fee_inr": 50,
            "rule": "பயோமெட்ரிக் கைரேகை பதிவு தேவைப்படுவதால், அருகில் உள்ள அஞ்சலகம் அல்லது ஆதார் இ-சேவை மையத்தில் மட்டுமே செய்ய முடியும்."
        }
    ]
}

# ==============================================================================
# 4. NATIONAL COMPETITIVE EXAMS (NEET, UPSC, TNPSC)
# ==============================================================================

NATIONAL_EXAMS_CONFIG = [
    {
        "exam_id": "neet_ug",
        "title_ta": "நீட் இளநிலை மருத்துவ நுழைவுத் தேர்வு (NEET UG)",
        "title_en": "National Eligibility cum Entrance Test (NEET UG)",
        "organizer": "National Testing Agency (NTA)",
        "official_portal": "https://exams.nta.ac.in/NEET/",
        "eligibility_ta": "12-ஆம் வகுப்பில் இயற்பியல், வேதியியல், உயிரியல்/தாவரவியல்/விலங்கியல் பாடங்களில் 50% மதிப்பெண் (OBC/SC/ST பிரிவினருக்கு 40%).",
        "age_criteria": "குறைந்தபட்ச வயது 17 ஆண்டுகள் நிறைவடைந்திருக்க வேண்டும். அதிகபட்ச வயது வரம்பு எதுவும் இல்லை.",
        "tn_reservation": "தமிழ்நாடு அரசுப் பள்ளி மாணவர்களுக்கு மருத்துவ படிப்பில் 7.5% சிறப்பு உள்ஒதுக்கீடு உள்ளது.",
        "documents_required": [
            "10 & 12-ஆம் வகுப்பு மதிப்பெண் சான்றிதழ்கள்",
            "ஆதார் அட்டை நகல்",
            "சமீபத்திய பாஸ்போர்ட் & போஸ்ட்கார்டு அளவு புகைப்படங்கள் (வெள்ளை பின்னணி)",
            "இடது மற்றும் வலது கை கைரேகைப் பதிவு",
            "சாதிச் சான்றிதழ் (OBC-NCL / EWS / SC / ST)"
        ]
    },
    {
        "exam_id": "upsc_civil_services",
        "title_ta": "மத்திய அரசு குடிமைப் பணிகள் தேர்வு (UPSC IAS, IPS, IFS)",
        "title_en": "UPSC Civil Services Examination",
        "organizer": "Union Public Service Commission",
        "official_portal": "https://upsc.gov.in/",
        "eligibility_ta": "ஏதேனும் ஒரு துறையில் அங்கீகரிக்கப்பட்ட பல்கலைக்கழக இளங்கலைப் பட்டம் (Any Bachelor Degree).",
        "age_criteria": "பொதுப் பிரிவு: 21 முதல் 32 வயது (6 வாய்ப்புகள்). OBC: 35 வயது (9 வாய்ப்புகள்). SC/ST: 37 வயது (வரம்பற்ற வாய்ப்புகள்).",
        "official_fee": "அரசு கட்டணம் ₹100 மட்டுமே. அனைத்து பெண் விண்ணப்பதாரர்கள் மற்றும் SC/ST/மாற்றுத்திறனாளிகளுக்கு கட்டணம் முற்றிலும் இலவசம் (₹0).",
        "stages_ta": [
            "முதல்நிலைத் தேர்வு (Prelims - GS & CSAT Objective)",
            "முதன்மைத் தேர்வு (Mains - 9 Written Descriptive Papers - தமிழில் எழுதலாம்)",
            "ஆளுமைத் தேர்வு (Interview - தமிழில் பதில் அளிக்கலாம்)"
        ]
    },
    {
        "exam_id": "tnpsc_services",
        "title_ta": "தமிழ்நாடு அரசுப் பணியாளர் தேர்வாணையம் (TNPSC Group 1, 2, 4)",
        "title_en": "Tamil Nadu Public Service Commission Examinations",
        "organizer": "TNPSC Chennai",
        "official_portal": "https://www.tnpsc.gov.in/",
        "eligibility_ta": "குரூப் 4 தேர்விற்கு 10-ஆம் வகுப்பு தேர்ச்சி போதும். குரூப் 1 & 2 தேர்விற்கு பட்டப்படிப்பு (Degree) தேவை.",
        "mandatory_tamil": "கட்டாய தமிழ் மொழி தகுதித் தேர்வில் (Part A) குறைந்தபட்சம் 40% மதிப்பெண் பெறுவது கட்டாயமாகும்.",
        "one_time_registration": "TNPSC தளத்தில் 5 வருடங்களுக்கு செல்லுபடியாகும் நிரந்தரப் பதிவு (OTR) கட்டணம் ₹150."
    }
]

# ==============================================================================
# 5. SWAYAM & NPTEL NATIONAL HIGHER EDUCATION PORTAL
# ==============================================================================

SWAYAM_CONFIG = {
    "title_ta": "சுவயம் (SWAYAM) - மத்திய அரசு இலவச உயர்கல்வி & ஐஐடி சான்றிதழ் தளம்",
    "title_en": "SWAYAM Free National Online Learning & IIT Certification Portal",
    "official_portal": "https://swayam.gov.in/",
    "coordinators": ["NPTEL (IITs)", "AICTE", "UGC", "IIM Bangalore", "IGNOU", "CEC"],
    "benefits_ta": [
        "📚 1,000-க்கும் மேற்பட்ட உயர்கல்வி பாடங்களை இந்தியாவின் முன்னணி ஐஐடி மற்றும் ஐஐஎம் பேராசிரியர்களிடம் முற்றிலும் இலவசமாகப் படிக்கலாம்.",
        "🎓 பல்கலைக்கழக மானியக் குழுவின் (UGC) விதிகளின்படி, இப்பாடங்களின் மதிப்பெண்களை உங்கள் கல்லூரி பட்டப்படிப்பு கிரெடிட்டிற்கு (ABC Credit Transfer) மாற்றிக் கொள்ளலாம்.",
        "💡 கணினி அறிவியல் (AI, Python, Data Science), வேளாண்மை, வணிகவியல், தமிழ் இலக்கியம் மற்றும் போட்டித் தேர்வு பாடங்கள் உள்ளன.",
        "📜 தேர்வு எழுத விரும்பும் கிராமப்புற எஸ்சி/எஸ்டி மாணவர்களுக்கு அரசு தேர்வு கட்டண சலுகை வழங்குகிறது."
    ],
    "top_domains": [
        {"domain_ta": "கணினி & செயற்கை நுண்ணறிவு (AI & Programming)", "domain_en": "Computer Science & AI", "icon": "💻"},
        {"domain_ta": "வேளாண்மை & இயற்கை விவசாயம்", "domain_en": "Agriculture & Organic Farming", "icon": "🌾"},
        {"domain_ta": "வணிகம், நிதி & மேலாண்மை", "domain_en": "Commerce & Financial Accounting", "icon": "📊"},
        {"domain_ta": "பொறியியல் & தொழில்நுட்பம்", "domain_en": "Mechanical & Electrical Engineering", "icon": "⚙️"},
        {"domain_ta": "தமிழ் மொழி & பண்பாட்டு ஆய்வுகள்", "domain_en": "Tamil Culture & Humanities", "icon": "📖"}
    ]
}
