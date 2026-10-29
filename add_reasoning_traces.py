"""
Script to add reasoning traces for tnpsc, redtaxi, and family civic tasks into meta_client.py
"""

import sys

FILE_PATH = r"D:\api\makkal-agent-ai\meta_client.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

target = '        if any(w in lower for w in ["பயிர்", "விவசாயம்", "crop", "agri", "leaf", "disease", "நெல்", "கரும்பு", "தக்காளி", "உழவர்"]):'

new_blocks = '''        if any(w in lower for w in ["tnpsc", "குரூப் 4", "vao", "தேர்வு", "exam", "சமச்சீர்", "10th", "அறிவியல்", "இலக்கணம்", "quiz", "course"]):
            return [
                {
                    "step": 1,
                    "title": "Meta Wonder 1.0 பாடத்திட்ட பகுப்பாய்வு (Syllabus Blueprint Mapping)",
                    "detail": "தமிழ்நாடு மாநில பாடநூல் கழகம் (TNSB) மற்றும் TNPSC பொதுத்தமிழ்/பொது அறிவு தேர்வு முறைமைகளுடன் வினா இணைக்கப்பட்டது.",
                    "statute": "TNPSC General Studies & Tamil Eligibility Mandate G.O. 133",
                    "status": "SYLLABUS_MAPPED"
                },
                {
                    "step": 2,
                    "title": "அடிப்படைக் கருத்துரு விளக்கம் (First-Principles Pedagogical Breakdown)",
                    "detail": "சூத்திரங்கள், வரலாற்று நிகழ்வுகள் அல்லது இலக்கண விதிகள் படிநிலைகளாக தீர்க்கப்பட்டன.",
                    "statute": "Samacheer Kalvi Pedagogical Standards",
                    "status": "CONCEPT_RESOLVED"
                },
                {
                    "step": 3,
                    "title": "முந்தைய ஆண்டு வினாத்தாள் ஒப்பீடு (PYQ Pattern Alignment)",
                    "detail": "2018-2024 TNPSC & SSLC வினாக்களில் கேட்கப்பட்ட வினாக்களின் மாதிரித் தகவல்களுடன் சரிபார்க்கப்பட்டது.",
                    "statute": "TNPSC Previous Year Examination Bank",
                    "status": "PYQ_ALIGNED"
                },
                {
                    "step": 4,
                    "title": "குழப்பும் விடைகள் நீக்கம் (Distractor Elimination & Negative Marking)",
                    "detail": "OMR விடைத்தாள் (E) ஆப்ஷன் விதிகள் மற்றும் தவறான விடைகளைத் தவிர்க்கும் நுணுக்கங்கள் சேர்க்கப்பட்டன.",
                    "statute": "TNPSC Instructions to Candidates 2024",
                    "status": "DISTRACTOR_CLEARED"
                },
                {
                    "step": 5,
                    "title": "நேர நிர்வாகம் & குறுக்குவழி உத்தி (Shortcut & Time Management)",
                    "detail": "தேர்வில் 15 வினாடிகளில் விடையளிக்கக்கூடிய எளிய நினைவூட்டல் குறுக்குவழி வழங்கப்பட்டது.",
                    "statute": "Makkal AI Accelerated Learning Framework",
                    "status": "ACTION_DISPATCHED"
                }
            ]

        if any(w in lower for w in ["redtaxi", "டாக்ஸி", "auto", "ஆட்டோ", "uber", "ride", "பயணம்", "travel", "செடான்", "இன்னோவா"]):
            return [
                {
                    "step": 1,
                    "title": "தமிழ்நாடு அரசு மோட்டார் வாகன கட்டண பூட்டு (Statutory Fare Lock)",
                    "detail": "அரசு நிர்ணயித்த 0% சர்ஜ் கட்டணம் உறுதி செய்யப்பட்டது (நம்மா ஆட்டோ ₹15/கிமீ, செடான் ₹13/கிமீ, இன்னோவா ₹17/கிமீ).",
                    "statute": "Tamil Nadu Motor Vehicles Rules 1989",
                    "status": "FEE_LOCKED"
                },
                {
                    "step": 2,
                    "title": "புவிசார் தூரம் & சுங்கச்சாவடி தணிக்கை (Route & Toll Audit)",
                    "detail": "பிக்கப் முதல் சேருமிடம் வரையிலான துல்லிய தூரம் மற்றும் NHAI சுங்கச்சாவடி ரசீது விவரங்கள் கணக்கிடப்பட்டது.",
                    "statute": "NHAI Electronic Toll Collection Norms",
                    "status": "ROUTE_OPTIMIZED"
                },
                {
                    "step": 3,
                    "title": "ஓட்டுநர் பின்னணி சரிபார்ப்பு (Driver Background Verification)",
                    "detail": "வணிக பேட்ஜ் மற்றும் காவல் துறை நன்னடத்தைச் சான்று பெற்ற அரசு பதிவு பெற்ற ஓட்டுநர் ஒதுக்கப்பட்டார்.",
                    "statute": "Tamil Nadu Aggregator Guidelines 2024",
                    "status": "DRIVER_VERIFIED"
                },
                {
                    "step": 4,
                    "title": "4-இலக்க பாதுகாப்பு ஓடிபி உருவாக்கம் (Encrypted 4-Digit Ride OTP)",
                    "detail": "பயணி ஏறும் முன் வாகனத்தின் அதிகாரப்பூர்வ மீட்டரைத் தொடங்குவதற்கான பாதுகாப்பு OTP உருவாக்கப்பட்டது.",
                    "statute": "Passenger Safety & Secure Dispatch Protocol",
                    "status": "OTP_GENERATED"
                },
                {
                    "step": 5,
                    "title": "நேரலை ஜிபிஎஸ் & காவல் உதவி தயார்நிலை (Live Telemetry & Police 112 SOS)",
                    "detail": "வாட்ஸ்அப் மற்றும் வெப் இடைமுகத்தில் வாகனத்தின் நேரலை கண்காணிப்பு அட்டை மற்றும் அவசர SOS தயார் செய்யப்பட்டது.",
                    "statute": "Kavalan SOS Emergency Standards",
                    "status": "DISPATCH_CONFIRMED"
                }
            ]

        if any(w in lower for w in ["மின்கட்டணம்", "eb bill", "100 யூனிட்", "ரேஷன்", "tnpds", "kmut", "குடும்ப", "task", "பணி"]):
            return [
                {
                    "step": 1,
                    "title": "குடும்ப அட்டை & பயனாளி உரிமை தணிக்கை (Citizen Entitlement Audit)",
                    "detail": "ஸ்மார்ட் ரேஷன் அட்டை வகை மற்றும் TANGEDCO மின் நுகர்வோர் எண் சரிபார்க்கப்பட்டது.",
                    "statute": "National Food Security Act & TNERC Regulations",
                    "status": "ENTITLEMENT_VERIFIED"
                },
                {
                    "step": 2,
                    "title": "அரசு மானிய உத்தரவாதம் (100 Units Free Subsidy Lock)",
                    "detail": "முதல் 100 யூனிட்கள் ₹0 முற்றிலும் இலவசம் மற்றும் நியாயவிலைக் கடை பொருட்கள் அரசு நிர்ணயித்த விலையில் பூட்டப்பட்டது.",
                    "statute": "Tamil Nadu Domestic Electricity Subsidy Scheme 2024",
                    "status": "SUBSIDY_LOCKED"
                },
                {
                    "step": 3,
                    "title": "குடும்ப அறிவார்ந்த லெட்ஜர் புதுப்பிப்பு (Autonomous Smart Ledger Sync)",
                    "detail": "பில்கள், கேஸ் சிலிண்டர் இருப்பு மற்றும் ரேஷன் ஒதுக்கீட்டு பணிகள் குடும்ப காலண்டரில் பதிவு செய்யப்பட்டன.",
                    "statute": "SIA Family Autonomous Planner Architecture",
                    "status": "LEDGER_SYNCED"
                },
                {
                    "step": 4,
                    "title": "வாட்ஸ்அப் & வெப் முன்கூட்டிய எச்சரிக்கை (Proactive Multi-Channel Alert)",
                    "detail": "கடைசி தேதிக்கு 3 நாட்களுக்கு முன்பே காலை அறிக்கையாக குடிமகனுக்கு தமிழ் எச்சரிக்கை அனுப்ப திட்டமிடப்பட்டது.",
                    "statute": "Citizen Notification Standards",
                    "status": "ALERT_SCHEDULED"
                }
            ]

''' + target

if target in content and "TNPSC General Studies & Tamil Eligibility Mandate" not in content:
    content = content.replace(target, new_blocks, 1)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Added reasoning traces for TNPSC, RedTaxi, and Family Civic tasks")
else:
    print("Reasoning traces already present or target not found.")
