# -*- coding: utf-8 -*-
"""
append_3step_domain_training_samples.py
Appends ultra-concise 3-step direct action training samples to makkal_domain_training_dataset.jsonl
and recompiles the domain training engine exports for Baseten LoRA / Meta Model SFT.
"""

import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = r"D:\api\makkal-agent-ai"
sys.path.insert(0, ROOT_DIR)

DATASET_FILE = os.path.join(ROOT_DIR, "data", "makkal_domain_training_dataset.jsonl")

TRAINING_SAMPLES = [
    {
        "id": "wa_3step_direct_action_petition_001",
        "domain": "whatsapp_conversational_triage",
        "meta_model": "muse-spark-1.3",
        "user_query": "எனக்கு ஒரு மனு வேண்டும் / மனு PDF",
        "assistant_response": "வணக்கம்! எந்த பிரச்சனைக்கு மனு தயாரிக்க வேண்டும்?\n1. 💧 குடிநீர் வசதி மனு\n2. 🛣️ சாலை & தெருவிளக்கு மனு\n3. 🏛️ முதியோர் உதவித்தொகை மனு\n\nவிருப்பத்தைத் தொடுங்கள் அல்லது 10 விநாடி வாய்ஸ் நோட் அனுப்புங்கள். உடனடியாக சீல் வைக்கப்பட்ட அதிகாரப்பூர்வ PDF மனு தயாராகி உங்கள் MLA வாட்ஸ்அப்பிற்கு அனுப்பப்படும்!",
        "interactive_buttons": ["💧 குடிநீர் வசதி மனு", "🛣️ சாலை & விளக்கு", "🏛️ முதியோர் உதவித்தொகை"],
        "statutory_rules": ["Tamil Nadu Legislative Assembly Rules", "DPDP Act 2023"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_agri_002",
        "domain": "agri_pathology_paddy",
        "meta_model": "muse-spark-1.3",
        "user_query": "நெல் பயிரில் இலை கருகி புள்ளி புள்ளியா இருக்கு, என்ன மருந்து தெளிக்கலாம்?",
        "assistant_response": "✅ நெல் குலைநோய் (Paddy Blast) TNAU இயற்கை மருந்து:\n1. சூடோமோனாஸ் ஃப்ளோரசன்ஸ்: 2.5 கிராம்/லிட்டர் நீரில் கலந்து காலை/மாலை தெளிக்கவும்.\n2. யூரியா உரம் இடுவதை தற்காலிகமாக நிறுத்தவும்.\n3. செலவு: ₹80 மட்டுமே (இரசாயன பூச்சிக்கொல்லி ₹1,500 மிச்சம்)!\n\n📸 உங்கள் பயிர் இலையை படம் பிடித்து அனுப்பினால் SAM 3.1 விஷன் உடனே பரிசோதிக்கும்.",
        "interactive_buttons": ["🌾 பூச்சி மருந்து", "🌧️ வானிலை அறிக்கை"],
        "statutory_rules": ["TNAU Organic Crop Protection Protocol 2026"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_cattle_003",
        "domain": "agronomy_welfare",
        "meta_model": "muse-spark-1.3",
        "user_query": "மாட்டுக்கு மடி வீங்கி இருக்கு, பால் கறக்க முடியல அவசர உதவி",
        "assistant_response": "🐄 மடிவீக்க நோய் அவசர மூலிகை முதலுதவி (TANUVAS):\n1. சோற்றுக் கற்றாழை 250g + மஞ்சள் தூள் 60g + வெற்றிலை சுண்ணாம்பு 15g.\n2. மிக்சியில் விழுதாக அரைத்து மடியில் தினமும் 4-5 முறை பூசவும்.\n3. 24 மணிநேரத்தில் வீக்கம் முற்றிலும் குணமாகும்!\nசெலவு: ₹20 மட்டுமே (டாக்டர் கட்டணம் ₹2,000 மிச்சம்). அவசர உதவிக்கு 0452-2589012 அழைக்கலாம்.",
        "interactive_buttons": ["🩹 மடிநோய் முதலுதவி", "🥛 பால் பெருக்க தீவனம்"],
        "statutory_rules": ["TANUVAS Ethno-Veterinary Practices 2025"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_grocery_004",
        "domain": "whatsapp_vernacular_dialogue",
        "meta_model": "muse-spark-1.3",
        "user_query": "மளிகை சாமான்கள் வாங்கணும் / அரிசி பருப்பு வேணும்",
        "assistant_response": "✅ மளிகை ஆர்டர் உறுதி செய்யப்பட்டது!\n• கடை: சோழவந்தான் முருகன் ஸ்டோர்ஸ்\n• பொருட்கள்: பொன்னி அரிசி 10kg + துவரம் பருப்பு 1kg\n• மொத்தத் தொகை: ₹780 (0% கமிஷன், நேரடி கடை விலையே)\n• டெலிவரி: அடுத்த 30 நிமிடங்களில் உங்கள் வீடு தேடி வரும்!\n• டெலிவரி OTP: 4182",
        "interactive_buttons": ["🛒 மளிகை ஆர்டர்", "📊 உழவர் மண்டி விலை"],
        "statutory_rules": ["SIA Sovereign 0% Kirana Charter"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_transport_005",
        "domain": "redtaxi_travel",
        "meta_model": "muse-spark-1.3",
        "user_query": "ஆட்டோ புக் பண்ணனும் / டாக்ஸி சவாரி",
        "assistant_response": "✅ ஆட்டோ முன்பதிவு உறுதியானது!\n• ஓட்டுநர்: S. வேலு (SIA சரிபார்க்கப்பட்ட ஓட்டுநர்)\n• வாகனம்: பஜாஜ் மேக்ஸிமா ஆட்டோ (TN 58 AB 4092)\n• வருகை நேரம்: 3 நிமிடங்கள்\n• சவாரி தொடக்க OTP: 6395\n• கட்டணம்: ₹12 / கிமீ (0% கமிஷன், இரவு நேர கூடுதல் கட்டணம் இல்லை)!",
        "interactive_buttons": ["🛺 ஆட்டோ புக்", "🚗 கார் புக்"],
        "statutory_rules": ["Tamil Nadu Motor Vehicles Act Metered Fares"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_food_006",
        "domain": "whatsapp_vernacular_dialogue",
        "meta_model": "muse-spark-1.3",
        "user_query": "பசிக்குது சாப்பாடு ஆர்டர் / வீட்டு உணவு",
        "assistant_response": "✅ சமுதாய உணவக ஆர்டர் உறுதி செய்யப்பட்டது!\n• உணவகம்: அன்னபூரணி மகளிர் குழு சமையலகம்\n• உணவு: 2 வாழை இலை பாரம்பரிய சைவ சாப்பாடு\n• தொகை: ₹170 (சாப்பாடு ₹85 x 2, டெலிவரி ₹20 மட்டுமே)\n• டெலிவரி: 20 நிமிடங்களில் உங்கள் இல்லம் தேடி வரும்!\n• டெலிவரி OTP: 5821",
        "interactive_buttons": ["🍱 சாப்பாடு ஆர்டர்", "📋 மெனு கார்டு"],
        "statutory_rules": ["Tamil Nadu SHG Livelihoods Mission 2026"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_patta_007",
        "domain": "civic_land_patta",
        "meta_model": "sam-3.1",
        "user_query": "பட்டா பெயர் மாற்றம் செய்ய எவ்வளவு செலவாகும்?",
        "assistant_response": "📑 பட்டா நில ஆவண ஆய்வு முடிவு (RSO 31):\n• உட்பிரிவு இல்லாத பட்டா பெயர் மாற்றம்: ₹0 (முற்றிலும் இலவசம்).\n• உட்பிரிவு உள்ள பட்டா மாற்றம்: அரசு கட்டணம் ₹60 மட்டுமே.\n• இடைத்தரகர்களுக்கு கூடுதல் பணம் தர வேண்டாம்!\n• அதிகாரப்பூர்வ தளம்: eservices.tn.gov.in\nபத்திர புகைப்படத்தை அனுப்பினால் SAM 3.1 விஷன் உடனே பரிசோதிக்கும்.",
        "interactive_buttons": ["📜 பட்டா ஆய்வு", "🌾 FMB வரைபடம்"],
        "statutory_rules": ["Tamil Nadu Revenue Standing Order 31"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_cbt_008",
        "domain": "education_samacheer_science_10th",
        "meta_model": "muse-wonder-1.0",
        "user_query": "தேர்வு மாதிரி வினாடி வினா ஆரம்பி",
        "assistant_response": "🎯 TNPSC குரூப் 4 மாதிரி தேர்வு (கேள்வி 1/5):\n❓ 'அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு' - இதில் பயின்று வரும் அணி எது?\n\nA) உவமை அணி\nB) எடுத்துக்காட்டு உவமை அணி\nC) பிறிது மொழிதல் அணி\n\nசரியான விடையைத் தேர்ந்தெடுக்கவும் 👇",
        "interactive_buttons": ["B) எடுத்துக்காட்டு", "A) உவமை அணி", "C) பிறிது மொழிதல்"],
        "statutory_rules": ["Samacheer Kalvi Tamil Curriculum Class 10"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_spoken_009",
        "domain": "spoken_english",
        "meta_model": "muse-spark-1.3",
        "user_query": "ஆங்கிலம் பேச கத்துக்கணும் / Spoken English",
        "assistant_response": "🗣️ இன்றைய ஆங்கில வாக்கிய பயிற்சி (Daily Practice):\n📌 வாக்கியம்: \"I want to open a savings bank account.\"\n📌 தமிழ் பொருள்: \"நான் இந்த வங்கியில் ஒரு சேமிப்புக் கணக்கு தொடங்க விரும்புகிறேன்.\"\n📌 உச்சரிப்பு: \"ஐ வான்ட் டு ஓபன் எ சேவிங்ஸ் பேங்க் அக்கவுன்ட்\"\n\n🎙️ இந்த வாக்கியத்தை பேசி வாய்ஸ் நோட்டாக அனுப்பினால் Meta AI உங்கள் உச்சரிப்பை சரிபார்த்து தரும்!",
        "interactive_buttons": ["🗣️ வாக்கிய பயிற்சி", "🏢 நேர்காணல் பயிற்சி"],
        "statutory_rules": ["Valluvar Conversational Pedagogy"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_mental_health_010",
        "domain": "mental_health",
        "meta_model": "muse-spark-1.3",
        "user_query": "தேர்வு பயமா இருக்கு / ரொம்ப டென்ஷனா இருக்கு",
        "assistant_response": "🌬️ 4-7-8 மன அமைதி மூச்சுப் பயிற்சி:\n1. 4 விநாடிகள் மூச்சை உள்ளே இழுக்கவும்... 🫁\n2. 7 விநாடிகள் மூச்சை அடக்கவும்... ⏱️\n3. 8 விநாடிகள் மெதுவாக மூச்சை வெளியேற்றவும்... 🍃\n\n3 முறை இதைச் செய்யவும். உங்கள் பதற்றம் தணிந்து அமைதி கிடைக்கும்!\n📞 24/7 இலவச உதவி: 14416 (தமிழ்நாடு அரசு Tele-MANAS மையம்)",
        "interactive_buttons": ["🧘 அமைதி பயிற்சி", "📞 14416 அழைப்பு"],
        "statutory_rules": ["National Mental Health Mission Tele-MANAS"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_exam_roadmap_011",
        "domain": "tnpsc_gov_exams",
        "meta_model": "muse-spark-1.3",
        "user_query": "TNPSC குரூப் 4 பாடத்திட்டம் எப்படி படிக்கணும்?",
        "assistant_response": "🗺️ TNPSC குரூப் 4 முழுமையான தேர்வு வரைபடம்:\n1. பொதுத் தமிழ் (100 வினாக்கள் / 150 மதிப்பெண்கள்): 6-10 சமச்சீர் தமிழ் புத்தகம்.\n2. பொது அறிவு (75 வினாக்கள்) + திறனறி தேர்வு (25 வினாக்கள்): 100 வினாக்கள் / 150 மதிப்பெண்கள்.\n🎯 வெற்றி இலக்கு: 175+ வினாக்கள் சரியான விடை!\nஇலவச மாதிரி வினாத்தாள் பெற 'மாதிரி தேர்வு' என தட்டவும்.",
        "interactive_buttons": ["🗺️ TNPSC வரைபடம்", "🩺 NEET 7.5% விவரம்"],
        "statutory_rules": ["TNPSC Group 4 Gazetted Scheme of Examination"],
        "max_steps": 3,
        "zero_text_wall": True
    },
    {
        "id": "wa_3step_direct_action_machinery_012",
        "domain": "hyperlocal_gig",
        "meta_model": "muse-spark-1.3",
        "user_query": "டிராக்டர் வாடகைக்கு வேணும் / உழவு செய்ய மெஷின்",
        "assistant_response": "✅ டிராக்டர் வாடகை முன்பதிவு உறுதியானது!\n• இயந்திரம்: மஹிந்திரா 45HP டிராக்டர் + ரோட்டவேட்டர்\n• உழவர் உரிமையாளர்: பி. முருகேசன் (மேலூர், 2.5 கிமீ)\n• வாடகை: ₹850 / மணி (டீசல் & ஓட்டுநர் உட்பட)\n• தொலைபேசி: 94432 87654\n• 0% இடைத்தரகர் கட்டணம்! உரிமையாளர் உங்கள் வயலுக்கு வரத் தயாராக உள்ளார்.",
        "interactive_buttons": ["🚜 டிராக்டர் வாடகை", "🌾 அறுவடை இயந்திரம்"],
        "statutory_rules": ["RentO Sovereign Hyperlocal Farm Machinery Network"],
        "max_steps": 3,
        "zero_text_wall": True
    }
]

def append_and_train():
    existing_ids = set()
    if os.path.exists(DATASET_FILE):
        with open(DATASET_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        existing_ids.add(record.get("id"))
                    except Exception:
                        pass

    appended = 0
    with open(DATASET_FILE, "a", encoding="utf-8") as f:
        for sample in TRAINING_SAMPLES:
            if sample["id"] not in existing_ids:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
                appended += 1

    print(f"✓ Appended {appended} new 3-step direct action training samples to {DATASET_FILE}")

    # Re-compile and export via domain_training_engine
    from domain_training_engine import DomainTrainingEngine
    engine = DomainTrainingEngine(dataset_path=DATASET_FILE)
    export_res = engine.export_baseten_fine_tuning_dataset()
    train_res = engine.train_or_fine_tune_models()
    stats = engine.get_dataset_statistics()
    print(f"✓ Compiled & Exported Baseten Fine-Tuning datasets: {export_res}")
    print(f"✓ Training/Fine-Tuning Engine Status: {train_res}")
    print(f"✓ Total Domain Samples: {stats['total_samples']} across {len(stats['domains'])} domains")
    print(f"✓ Total Tokens Grounded: {stats['estimated_tokens']}")

if __name__ == "__main__":
    append_and_train()
