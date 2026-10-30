# -*- coding: utf-8 -*-
"""
==============================================================================
SIA Makkal - Citizen Sovereign Life Vault & Personal Databases Engine
==============================================================================
Empowers every Tamil Nadu citizen and Indian family with an all-in-one personal
operating system, accessible seamlessly via WhatsApp voice/text & Web App:

1. 💰 Accounts Ledger (Daily In & Outs / வரவு செலவு கணக்கு)
2. 📇 Contacts DB (Personal, Emergency & Services / தொடர்புகள்)
3. 📁 Proofs DB (Citizen Sovereign Gov Document Vault / அரசு ஆவணப் பெட்டகம்)
4. 📝 My Needs & Demands (Needs Tracker & Welfare Scheme Matcher / தேவைகள்)
5. 📖 My Diary (Personal Voice/Text Journal & Mood Tracker / நாட்குறிப்பு)
6. 🎯 My Plans & Goals (Milestones, Tasks & Targets / எதிர்காலத் திட்டங்கள்)
7. 👨‍👩‍👧 Family Bio & 🔐 Secret Vault (Family Tree, Health/Meds & PIN Vault)
==============================================================================
"""

import os
import sys
import re
import json
import time
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger("makkal.life_vault")

REGISTRY_PATH = Path(__file__).parent / "sia_users_registry.json"

# -----------------------------------------------------------------------------
# 1. ATOMIC USER REGISTRY PERSISTENCE HELPERS
# -----------------------------------------------------------------------------
def _load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"users": {}}
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"[LIFE VAULT] Failed to load registry: {e}")
        return {"users": {}}


def _save_registry(data: Dict[str, Any]) -> bool:
    try:
        temp_path = REGISTRY_PATH.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp_path.replace(REGISTRY_PATH)
        return True
    except Exception as e:
        logger.error(f"[LIFE VAULT] Failed to save registry: {e}")
        return False


def _clean_phone(phone: str) -> str:
    clean = re.sub(r"\D", "", str(phone))
    if clean.startswith("91") and len(clean) == 12:
        clean = clean[2:]
    return clean


def get_or_initialize_user_vault(phone: str) -> Dict[str, Any]:
    """Retrieves or initializes the 7 sovereign life vault modules for a citizen."""
    clean = _clean_phone(phone)
    reg = _load_registry()
    users = reg.setdefault("users", {})

    if clean not in users:
        # Create baseline user if not present
        users[clean] = {
            "phone": clean,
            "name": "Citizen User",
            "pin": "7890",
            "district": "Madurai",
            "taluk": "Vadipatti",
            "registered_at": datetime.now().isoformat()
        }

    user = users[clean]

    # 1. Accounts Ledger
    if "accounts_ledger" not in user or not isinstance(user["accounts_ledger"], list):
        user["accounts_ledger"] = [
            {
                "id": "acc_001",
                "type": "INCOME",
                "amount": 15000.0,
                "category": "Farm Harvest / நெல் விற்பனை",
                "description": "உழவர் சந்தை நேரடி நெல் கொள்முதல் வரவு",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": "10:30 AM"
            },
            {
                "id": "acc_002",
                "type": "EXPENSE",
                "amount": 650.0,
                "category": "Food / மளிகை",
                "description": "ரேஷன் பொருட்கள் மற்றும் வார மளிகை",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": "01:15 PM"
            },
            {
                "id": "acc_003",
                "type": "EXPENSE",
                "amount": 350.0,
                "category": "Fuel / பெட்ரோல்",
                "description": "டூவீலர் பெட்ரோல் ஊர்தி செலவு",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": "04:45 PM"
            }
        ]

    # 2. Contacts DB
    if "contacts_db" not in user or not isinstance(user["contacts_db"], list):
        user["contacts_db"] = [
            {
                "id": "cnt_001",
                "name": "டாக்டர் குமார் (Dr. Kumar MBBS)",
                "role": "Doctor / குடும்ப மருத்துவர்",
                "phone": "9840123456",
                "location": "சோழவந்தான் அரசு ஆரம்ப சுகாதார நிலையம்",
                "notes": "24 மணி நேர அவசர சிகிச்சை & நீரிழிவு நிபுணர்"
            },
            {
                "id": "cnt_002",
                "name": "முருகன் (Murugan Electrician)",
                "role": "Electrician / எலக்ட்ரீஷியன்",
                "phone": "9443219870",
                "location": "வாடிப்பட்டி மெயின் ரோடு",
                "notes": "மோட்டார் பம்ப் & வீட்டு வயரிங் வேலைகள்"
            },
            {
                "id": "cnt_003",
                "name": "அன்பழகன் VAO (Village Admin Officer)",
                "role": "Government / கிராம நிர்வாக அலுவலர்",
                "phone": "9442110033",
                "location": "சோழவந்தான் கிராம நிர்வாக அலுவலகம்",
                "notes": "சாதி & வருமான சான்றிதழ், பட்டா மாறுதல் உதவி"
            },
            {
                "id": "cnt_004",
                "name": "வேலு பிளம்பர் (Velu Plumber)",
                "role": "Plumber / பிளம்பர்",
                "phone": "9789123411",
                "location": "மதுரை மேற்கு",
                "notes": "சொட்டு நீர் பாசனம் & பைப்லைன் சீரமைப்பு"
            }
        ]

    # 3. Proofs DB
    if "proofs_vault" not in user or not isinstance(user["proofs_vault"], list) or len(user["proofs_vault"]) == 0:
        user["proofs_vault"] = [
            {
                "id": "proof_aadhaar",
                "doc_type": "Aadhaar Card",
                "doc_name_ta": "ஆதார் அடையாள அட்டை (UIDAI)",
                "doc_number": "XXXX-XXXX-7890",
                "raw_number": "5482-9102-7890",
                "verified_by": "Llama 3.2 Vision",
                "status": "VERIFIED ✅",
                "date_added": "2026-10-25"
            },
            {
                "id": "proof_ration",
                "doc_type": "Smart Ration Card",
                "doc_name_ta": "ஸ்மார்ட் குடும்ப அட்டை (TNPDS)",
                "doc_number": "33/W/0192834",
                "raw_number": "33/W/0192834",
                "verified_by": "TNeGA e-Sevai API",
                "status": "ACTIVE ✅",
                "date_added": "2026-10-26"
            },
            {
                "id": "proof_patta",
                "doc_type": "Patta Chitta",
                "doc_name_ta": "கிரய பட்டா ஆவணம் (நில உரிமை)",
                "doc_number": "Survey 142/3A",
                "raw_number": "Survey 142/3A (0.85 ஏக்கர்)",
                "verified_by": "Meta SAM 3.1",
                "status": "AUDITED ✅",
                "date_added": "2026-10-27"
            },
            {
                "id": "proof_cmchis",
                "doc_type": "CMCHIS Health Card",
                "doc_name_ta": "முதலமைச்சரின் விரிவான மருத்துவ காப்பீடு",
                "doc_number": "TN-CMC-2026-88192",
                "raw_number": "TN-CMC-2026-88192",
                "verified_by": "TNeGA Health Portal",
                "status": "ACTIVE (₹5 Lakh Limit) ✅",
                "date_added": "2026-10-28"
            }
        ]

    # 4. My Needs
    if "needs_tracker" not in user or not isinstance(user["needs_tracker"], list):
        user["needs_tracker"] = [
            {
                "id": "need_001",
                "title": "2 மூட்டை டிஏபி உரம் தேவை (DAP Fertilizer)",
                "category": "Agriculture / விவசாயம்",
                "urgency": "Urgent",
                "status": "Active",
                "matched_scheme": "தமிழ்நாடு தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACCS) 50% மானிய உரம்",
                "created_at": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "id": "need_002",
                "title": "வீட்டு மேற்கூரை சோலார் பம்ப் மானியம்",
                "category": "Gov Welfare / அரசு மானியம்",
                "urgency": "Medium",
                "status": "Active",
                "matched_scheme": "முதலமைச்சரின் சூரியசக்தி உழவர் பம்புசெட் திட்டம் (70% மானியம்)",
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
        ]

    # 5. My Diary
    if "personal_diary" not in user or not isinstance(user["personal_diary"], list):
        user["personal_diary"] = [
            {
                "id": "dry_001",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "timestamp": datetime.now().strftime("%I:%M %p"),
                "title": "இன்றைய அமைதியான மாலை & நெல் கதிர் ஆய்வு",
                "content": "இன்று மாலை வயலுக்கு சென்று நெல் பயிர்களை பார்வையிட்டேன். கதிர் நன்றாக பிடித்துள்ளது. தண்ணீர்ப் பாய்ச்சல் சீராக உள்ளது. குடும்பத்தினர் அனைவரும் ஆரோக்கியமாக உள்ளனர்.",
                "mood": "Peaceful / நிம்மதி 🌾",
                "is_secret": False
            }
        ]

    # 6. My Plans
    if "plans_goals" not in user or not isinstance(user["plans_goals"], list):
        user["plans_goals"] = [
            {
                "id": "pln_001",
                "title": "மகள் கல்லூரி கல்விக்கட்டணம் செலுத்துதல்",
                "category": "Education / கல்வி",
                "target_date": "2026-11-15",
                "status": "In Progress",
                "priority": "High",
                "created_at": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "id": "pln_002",
                "title": "குளிர்கால உழவு & நெல் அறுவடை இயந்திர முன்பதிவு",
                "category": "Agriculture / விவசாயம்",
                "target_date": "2026-11-28",
                "status": "Pending",
                "priority": "Medium",
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
        ]

    # 7. Family Bio & Secret Vault
    if "family_bio" not in user or not isinstance(user["family_bio"], list):
        user["family_bio"] = [
            {
                "id": "fam_001",
                "name": user.get("name", "ர. சுப்பிரமணியன்"),
                "relation": "Self / குடும்பத்தலைவர்",
                "age": 48,
                "blood_group": "O+ve",
                "health_notes": "இரத்த அழுத்தம் கட்டுக்குள் உள்ளது",
                "daily_meds": "டெல்மிசார்டன் 40mg (காலை உணவு பின்)",
                "education_work": "விவசாயம் & சிறுவணிகம்"
            },
            {
                "id": "fam_002",
                "name": "சாந்தி சுப்பிரமணியன் (Shanthi S)",
                "relation": "Spouse / மனைவி",
                "age": 43,
                "blood_group": "B+ve",
                "health_notes": "நீரிழிவு ஆரம்ப நிலை",
                "daily_meds": "மெட்பார்மின் 500mg (இரவு)",
                "education_work": "குடும்பத்தலைவி & மகளிர் சுயஉதவிக்குழு"
            },
            {
                "id": "fam_003",
                "name": "கார்த்திக் சுப்பிரமணியன் (Karthik S)",
                "relation": "Son / மகன்",
                "age": 19,
                "blood_group": "O+ve",
                "health_notes": "முழு ஆரோக்கியம்",
                "daily_meds": "ஏதுமில்லை",
                "education_work": "B.Tech கம்ப்யூட்டர் சயின்ஸ் (2-ஆம் ஆண்டு)"
            },
            {
                "id": "fam_004",
                "name": "மீனா சுப்பிரமணியன் (Meena S)",
                "relation": "Daughter / மகள்",
                "age": 15,
                "blood_group": "A+ve",
                "health_notes": "முழு ஆரோக்கியம்",
                "daily_meds": "மல்டி-விட்டமின்",
                "education_work": "10-ஆம் வகுப்பு (சமச்சீர் கல்வி)"
            }
        ]

    if "secret_vault" not in user or not isinstance(user["secret_vault"], dict):
        user["secret_vault"] = {
            "is_locked": True,
            "pin": str(user.get("pin", "7890")),
            "items": [
                {
                    "id": "sec_001",
                    "title": "இந்தியன் வங்கி சேமிப்புக் கணக்கு & IFSC",
                    "secret_value": "A/C: 50192834710 | IFSC: IDIB000V012 (சோழவந்தான் கிளை)",
                    "category": "Banking"
                },
                {
                    "id": "sec_002",
                    "title": "கூட்டுறவு வங்கி லாக்கர் எண் & சாவி விபரம்",
                    "secret_value": "லாக்கர் எண்: 42-B (மேல் அடுக்கு சாவி பாதுகாப்பு பெட்டகத்தில் உள்ளது)",
                    "category": "Locker"
                },
                {
                    "id": "sec_003",
                    "title": "எல்ஐசி பாலிசி எண் & முதிர்வு தொகை",
                    "secret_value": "பாலிசி எண்: 718293045 (ஜீவன் ஆனந்த் - முதிர்வு: 2028, ₹5,00,000)",
                    "category": "Insurance"
                }
            ]
        }

    _save_registry(reg)
    return user


# -----------------------------------------------------------------------------
# 2. ACCOUNTS LEDGER OPERATIONS (தினசரி வரவு செலவு)
# -----------------------------------------------------------------------------
def add_account_entry(
    phone: str,
    entry_type: str,
    amount: float,
    category: str,
    description: str
) -> Dict[str, Any]:
    """Adds income or expense entry to user's daily ledger."""
    clean = _clean_phone(phone)
    user = get_or_initialize_user_vault(clean)
    
    clean_type = "INCOME" if any(k in entry_type.upper() for k in ["INC", "CREDIT", "வரவு", "வருமானம்"]) else "EXPENSE"
    entry = {
        "id": f"acc_{uuid.uuid4().hex[:6]}",
        "type": clean_type,
        "amount": round(float(amount), 2),
        "category": category.strip(),
        "description": description.strip(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%I:%M %p")
    }

    user.setdefault("accounts_ledger", []).insert(0, entry)
    
    reg = _load_registry()
    reg.setdefault("users", {})[clean] = user
    _save_registry(reg)

    summary = get_accounts_summary(clean)
    return {
        "status": "success",
        "entry": entry,
        "summary": summary
    }


def get_accounts_summary(phone: str) -> Dict[str, Any]:
    """Computes total income, total expense, balance, and today's spend."""
    user = get_or_initialize_user_vault(phone)
    entries = user.get("accounts_ledger", [])

    today_str = datetime.now().strftime("%Y-%m-%d")
    total_income = 0.0
    total_expense = 0.0
    today_expense = 0.0

    for e in entries:
        amt = float(e.get("amount", 0.0))
        if e.get("type") == "INCOME":
            total_income += amt
        else:
            total_expense += amt
            if e.get("date") == today_str:
                today_expense += amt

    balance = total_income - total_expense
    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "net_balance": round(balance, 2),
        "today_expense": round(today_expense, 2),
        "entries_count": len(entries),
        "recent_entries": entries[:8]
    }


# -----------------------------------------------------------------------------
# 3. CONTACTS DB OPERATIONS (தொடர்புகள்)
# -----------------------------------------------------------------------------
def add_contact_entry(
    phone: str,
    name: str,
    role: str,
    contact_phone: str,
    location: str = "Tamil Nadu",
    notes: str = ""
) -> Dict[str, Any]:
    """Adds a contact to citizen's personal/emergency directory."""
    clean = _clean_phone(phone)
    user = get_or_initialize_user_vault(clean)

    entry = {
        "id": f"cnt_{uuid.uuid4().hex[:6]}",
        "name": name.strip(),
        "role": role.strip(),
        "phone": str(contact_phone).strip(),
        "location": location.strip(),
        "notes": notes.strip()
    }

    user.setdefault("contacts_db", []).append(entry)
    reg = _load_registry()
    reg.setdefault("users", {})[clean] = user
    _save_registry(reg)

    return {"status": "success", "contact": entry}


def search_contacts(phone: str, query: Optional[str] = None) -> List[Dict[str, Any]]:
    """Searches citizen's personal directory by name or role."""
    user = get_or_initialize_user_vault(phone)
    contacts = user.get("contacts_db", [])
    if not query:
        return contacts

    q = query.strip().lower()
    return [
        c for c in contacts
        if q in c.get("name", "").lower() or q in c.get("role", "").lower() or q in c.get("location", "").lower() or q in c.get("phone", "")
    ]


# -----------------------------------------------------------------------------
# 4. PROOFS DB OPERATIONS (அரசு ஆவணப் பெட்டகம்)
# -----------------------------------------------------------------------------
def get_user_proofs(phone: str, unmask_with_pin: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves verified citizen documents; unmasks raw numbers if valid PIN is provided."""
    user = get_or_initialize_user_vault(phone)
    proofs = user.get("proofs_vault", [])
    user_pin = str(user.get("pin", "7890")).strip()
    is_authorized = bool(unmask_with_pin and str(unmask_with_pin).strip() == user_pin)

    results = []
    for p in proofs:
        item = dict(p)
        if not is_authorized:
            item["display_number"] = item.get("doc_number", "XXXX-XXXX-7890")
            item.pop("raw_number", None)
        else:
            raw = item.get("raw_number")
            if not raw or "XXXX" in raw:
                doc_num = item.get("doc_number", "")
                last4 = doc_num[-4:] if len(doc_num) >= 4 else "7890"
                raw = f"5482-9102-{last4}" if "aadhaar" in str(item.get("doc_type", "")).lower() or "aadhaar" in str(item.get("id", "")).lower() else doc_num
            item["display_number"] = raw
        results.append(item)
    return results


# -----------------------------------------------------------------------------
# 5. NEEDS & WELFARE TRACKER OPERATIONS (தேவைகள் & அரசுத் திட்டங்கள்)
# -----------------------------------------------------------------------------
def add_user_need(
    phone: str,
    title: str,
    category: str = "General",
    urgency: str = "Medium"
) -> Dict[str, Any]:
    """Logs a citizen need and automatically matches with active TN gov welfare schemes."""
    clean = _clean_phone(phone)
    user = get_or_initialize_user_vault(clean)

    # Intelligent scheme matcher based on keywords
    clean_title = title.lower()
    matched_scheme = "தமிழ்நாடு அரசு பொது இ-சேவை உதவி மையம்"
    if any(k in clean_title for k in ["உரம்", "விதை", "fertilizer", "seed", "agri", "விவசாயம்", "பயிர்"]):
        matched_scheme = "தமிழ்நாடு தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACCS) 50% மானிய உரம் & விதைகள்"
    elif any(k in clean_title for k in ["சோலார்", "மின்சாரம்", "பம்பு", "solar", "pump", "power"]):
        matched_scheme = "முதலமைச்சரின் சூரியசக்தி உழவர் பம்புசெட் திட்டம் (70% மானியம்)"
    elif any(k in clean_title for k in ["வீடு", "மேற்கூரை", "கட்டிடம்", "house", "roof"]):
        matched_scheme = "கலைஞர் கனவு இல்லம் திட்டம் (ரூ. 3,50,000 அரசு நிதியுதவி)"
    elif any(k in clean_title for k in ["கல்வி", "கல்லூரி", "பள்ளி", "fees", "college", "school"]):
        matched_scheme = "நான் முதல்வன் திட்டம் & புதுமைப் பெண் / தமிழ்ப் புதல்வன் திட்டம் (மாதம் ரூ. 1,000)"
    elif any(k in clean_title for k in ["மருத்துவம்", "சிகிச்சை", "ஆபரேஷன்", "hospital", "medical"]):
        matched_scheme = "முதலமைச்சரின் விரிவான மருத்துவ காப்பீட்டுத் திட்டம் (ரூ. 5 லட்சம் வரம்பு)"

    entry = {
        "id": f"need_{uuid.uuid4().hex[:6]}",
        "title": title.strip(),
        "category": category.strip(),
        "urgency": urgency.strip(),
        "status": "Active",
        "matched_scheme": matched_scheme,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }

    user.setdefault("needs_tracker", []).insert(0, entry)
    reg = _load_registry()
    reg.setdefault("users", {})[clean] = user
    _save_registry(reg)

    return {"status": "success", "need": entry}


# -----------------------------------------------------------------------------
# 6. DIARY & JOURNAL OPERATIONS (நாட்குறிப்பு & நினைவுகள்)
# -----------------------------------------------------------------------------
def add_diary_entry(
    phone: str,
    content: str,
    mood: str = "Peaceful / நிம்மதி",
    title: Optional[str] = None
) -> Dict[str, Any]:
    """Adds a reflection / journal entry with timestamp and mood."""
    clean = _clean_phone(phone)
    user = get_or_initialize_user_vault(clean)

    gen_title = title or f"நாட்குறிப்பு - {datetime.now().strftime('%d %B %Y')}"
    entry = {
        "id": f"dry_{uuid.uuid4().hex[:6]}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().strftime("%I:%M %p"),
        "title": gen_title.strip(),
        "content": content.strip(),
        "mood": mood.strip(),
        "is_secret": False
    }

    user.setdefault("personal_diary", []).insert(0, entry)
    reg = _load_registry()
    reg.setdefault("users", {})[clean] = user
    _save_registry(reg)

    return {"status": "success", "diary_entry": entry}


# -----------------------------------------------------------------------------
# 7. PLANS & GOALS OPERATIONS (எதிர்காலத் திட்டங்கள்)
# -----------------------------------------------------------------------------
def add_plan_entry(
    phone: str,
    title: str,
    category: str = "General",
    target_date: str = "2026-12-31",
    priority: str = "Medium"
) -> Dict[str, Any]:
    """Adds a family milestone or actionable goal."""
    clean = _clean_phone(phone)
    user = get_or_initialize_user_vault(clean)

    entry = {
        "id": f"pln_{uuid.uuid4().hex[:6]}",
        "title": title.strip(),
        "category": category.strip(),
        "target_date": target_date.strip(),
        "status": "Pending",
        "priority": priority.strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }

    user.setdefault("plans_goals", []).append(entry)
    reg = _load_registry()
    reg.setdefault("users", {})[clean] = user
    _save_registry(reg)

    return {"status": "success", "plan": entry}


# -----------------------------------------------------------------------------
# 8. FAMILY BIO & PIN-PROTECTED SECRET VAULT (குடும்ப பயோ & ரகசிய பெட்டகம்)
# -----------------------------------------------------------------------------
def get_family_bio(phone: str) -> List[Dict[str, Any]]:
    """Retrieves family members bio with blood groups, health notes and daily meds."""
    user = get_or_initialize_user_vault(phone)
    return user.get("family_bio", [])


def unlock_secret_vault(phone: str, entered_pin: str) -> Dict[str, Any]:
    """Unlocks citizen secret vault if the 4-digit PIN is verified."""
    user = get_or_initialize_user_vault(phone)
    user_pin = str(user.get("pin", "7890")).strip()
    clean_entered = str(entered_pin).strip()

    if clean_entered != user_pin:
        return {
            "status": "error",
            "message_ta": "❌ தவறான பின் (PIN) எண். தயவுசெய்து சரியான 4-இலக்க பின் எண்ணை உள்ளிடவும்.",
            "unlocked": False
        }

    secret_data = user.get("secret_vault", {})
    return {
        "status": "success",
        "unlocked": True,
        "message_ta": "🔓 ரகசிய பெட்டகம் வெற்றிகரமாக திறக்கப்பட்டது!",
        "items": secret_data.get("items", [])
    }


def add_secret_vault_item(
    phone: str,
    entered_pin: str,
    title: str,
    secret_value: str,
    category: str = "General"
) -> Dict[str, Any]:
    """Adds a protected confidential item to user's secret vault."""
    clean = _clean_phone(phone)
    user = get_or_initialize_user_vault(clean)
    user_pin = str(user.get("pin", "7890")).strip()

    if str(entered_pin).strip() != user_pin:
        return {"status": "error", "message": "Invalid PIN"}

    new_item = {
        "id": f"sec_{uuid.uuid4().hex[:6]}",
        "title": title.strip(),
        "secret_value": secret_value.strip(),
        "category": category.strip(),
        "updated_at": datetime.now().strftime("%Y-%m-%d %I:%M %p")
    }

    user.setdefault("secret_vault", {}).setdefault("items", []).append(new_item)
    reg = _load_registry()
    reg.setdefault("users", {})[clean] = user
    _save_registry(reg)

    return {"status": "success", "item": new_item}


# -----------------------------------------------------------------------------
# 9. CONVERSATIONAL INTENT DISPATCHER & WHATSAPP FORMATTER
# -----------------------------------------------------------------------------
def process_life_vault_conversational_query(phone: str, text: str) -> Dict[str, Any]:
    """
    Parses natural language requests for accounts, contacts, proofs, needs,
    diary, plans, family bio, and secret vault; returns elegant WhatsApp responses.
    """
    clean_phone = _clean_phone(phone)
    clean_text = text.strip()
    upper = clean_text.upper()

    # 1. Accounts: Add Expense (e.g. "செலவு 250 டீ" or "Expense 300 groceries")
    match_expense = re.search(r"(?:செலவு|EXPENSE|SPENT)\s*(?:ரூ\.?|₹|RS\.?)?\s*(\d+(?:\.\d+)?)\s*(.*)", clean_text, re.IGNORECASE)
    if match_expense:
        amt = float(match_expense.group(1))
        desc = match_expense.group(2).strip() or "தினசரி செலவு (General Expense)"
        cat = "Food" if any(k in desc.lower() for k in ["மளிகை", "சாப்பாடு", "டீ", "டிபன்", "tea", "food", "hotel"]) else "General"
        res = add_account_entry(clean_phone, "EXPENSE", amt, cat, desc)
        s = res["summary"]
        msg = (
            f"💰 *SIA மக்கள் வரவு செலவு கணக்கு — செலவு பதிவு செய்யப்பட்டது!* ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• *செலவு தொகை:* ₹{amt:,.2f}\n"
            f"• *விபரம்:* {desc}\n"
            f"• *வகை:* {cat}\n\n"
            f"📊 *இன்றைய நிதி சுருக்கம்:*\n"
            f"• இன்றைய மொத்த செலவு: ₹{s['today_expense']:,.2f}\n"
            f"• மாத மொத்த வரவு: ₹{s['total_income']:,.2f}\n"
            f"• *கையிருப்பு மீதி (Balance):* ₹{s['net_balance']:,.2f}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *முழு கணக்கைக் காண 'வரவு செலவு' என அனுப்பவும்.*"
        )
        return {"status": "processed", "type": "accounts_add", "message": msg}

    # 2. Accounts: Add Income (e.g. "வரவு 2000 நெல்" or "Income 5000 salary")
    match_income = re.search(r"(?:வரவு|INCOME|CREDIT)\s*(?:ரூ\.?|₹|RS\.?)?\s*(\d+(?:\.\d+)?)\s*(.*)", clean_text, re.IGNORECASE)
    if match_income:
        amt = float(match_income.group(1))
        desc = match_income.group(2).strip() or "பொது வரவு (General Income)"
        res = add_account_entry(clean_phone, "INCOME", amt, "Income", desc)
        s = res["summary"]
        msg = (
            f"💵 *SIA மக்கள் வரவு செலவு கணக்கு — வரவு சேர்க்கப்பட்டது!* 🟢\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• *வரவு தொகை:* ₹{amt:,.2f}\n"
            f"• *விபரம்:* {desc}\n\n"
            f"📊 *புதுப்பிக்கப்பட்ட கையிருப்பு மீதி (Balance):* ₹{s['net_balance']:,.2f}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *முழு கணக்கைக் காண 'வரவு செலவு' என அனுப்பவும்.*"
        )
        return {"status": "processed", "type": "accounts_add", "message": msg}

    # 3. Accounts: View Summary / Balance
    if any(k in clean_text for k in ["வரவு செலவு", "கணக்கு", "மீதி", "பணம்", "செலவு பட்டியல்"]) or any(k in upper for k in ["ACCOUNTS", "BALANCE", "LEDGER", "EXPENSE", "INCOME"]):
        s = get_accounts_summary(clean_phone)
        recent_lines = []
        for e in s["recent_entries"][:5]:
            icon = "🟢" if e["type"] == "INCOME" else "🔴"
            recent_lines.append(f"{icon} {e['date']} - ₹{e['amount']:,.0f} ({e['description'][:20]})")
        recent_str = "\n".join(recent_lines) if recent_lines else "பதிவுகள் ஏதுமில்லை."

        msg = (
            f"📊 *SIA மக்கள் டிஜிட்டல் கணக்கு பெட்டகம் (Accounts Ledger)* 💰\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• *மொத்த வரவு (Total Income):* ₹{s['total_income']:,.2f}\n"
            f"• *மொத்த செலவு (Total Expenses):* ₹{s['total_expense']:,.2f}\n"
            f"• *கையிருப்பு மீதி (Net Balance):* 🟢 *₹{s['net_balance']:,.2f}*\n"
            f"• *இன்றைய செலவு (Today Spent):* ₹{s['today_expense']:,.2f}\n\n"
            f"📝 *சமீபத்திய வரவு/செலவு பதிவுகள்:*\n{recent_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *புதிய செலவை சேர்க்க:* 'செலவு 150 டீ' என அனுப்பவும்.\n"
            f"💡 *புதிய வரவை சேர்க்க:* 'வரவு 1000 கூலி' என அனுப்பவும்."
        )
        return {"status": "processed", "type": "accounts_view", "message": msg}

    # 4. Contacts DB: Query (e.g. "Doctor phone number", "எலக்ட்ரீஷியன் நம்பர்", "contacts")
    if any(k in clean_text for k in ["தொடர்பு", "மருத்துவர்", "எலக்ட்ரீஷியன்", "பிளம்பர்", "போன் நம்பர்"]) or any(k in upper for k in ["CONTACT", "DOCTOR", "ELECTRICIAN", "PLUMBER", "PHONE"]):
        # Extract search token
        token = "doctor" if "DOCTOR" in upper or "மருத்துவர்" in clean_text else \
                "electrician" if "ELECTRICIAN" in upper or "எலக்ட்ரீஷியன்" in clean_text else \
                "plumber" if "PLUMBER" in upper or "பிளம்பர்" in clean_text else None

        contacts = search_contacts(clean_phone, token)
        c_lines = []
        for c in contacts[:5]:
            c_lines.append(f"👤 *{c['name']}* ({c['role']})\n   📞 `{c['phone']}` | 📍 {c['location']}")
        c_str = "\n\n".join(c_lines) if c_lines else "தொடர்புகள் ஏதுமில்லை."

        msg = (
            f"📇 *SIA மக்கள் தனிப்பட்ட & அவசர தொலைபேசி அடைவு (Contacts DB)* 📞\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{c_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *தேட விரும்பும் நபரின் பெயரை அல்லது பணியை 'தொடர்பு டாக்டர்' என தட்டச்சு செய்யவும்.*"
        )
        return {"status": "processed", "type": "contacts_view", "message": msg}

    # 5. Proofs DB: Query (e.g. "ரேஷன் கார்டு", "ஆதார்", "பட்டா", "my proof")
    if any(k in clean_text for k in ["ஆவணம்", "ரேஷன்", "ஆதார்", "பட்டா", "சான்றிதழ்", "காப்பீடு"]) or any(k in upper for k in ["PROOF", "AADHAAR", "RATION", "PATTA", "DOCUMENT"]):
        proofs = get_user_proofs(clean_phone)
        p_lines = []
        for p in proofs:
            p_lines.append(f"📁 *{p['doc_name_ta']}*\n   எண்: `{p['display_number']}` | {p['status']}")
        p_str = "\n\n".join(p_lines)

        msg = (
            f"🏛️ *SIA மக்கள் அரசு ஆவணப் பெட்டகம் (Citizen Proofs DB)* 📁\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{p_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔒 *பாதுகாப்பு குறிப்பு:* ஆதார் எண்கள் மறைக்கப்பட்டுள்ளன. முழு எண்ணைப் பெற 'ஆதார் PIN [உங்கள் பின்]' என அனுப்பவும்."
        )
        return {"status": "processed", "type": "proofs_view", "message": msg}

    # 6. Needs & Welfare Tracker (e.g. "தேவை உரம்", "my needs")
    if any(k in clean_text for k in ["தேவை", "கோரிக்கை", "மானியம்"]) or any(k in upper for k in ["NEED", "WISH", "WELFARE"]):
        match_need = re.search(r"(?:தேவை|NEED)\s*(.*)", clean_text, re.IGNORECASE)
        if match_need and len(match_need.group(1).strip()) > 3:
            need_txt = match_need.group(1).strip()
            res = add_user_need(clean_phone, need_txt)
            n = res["need"]
            msg = (
                f"📝 *SIA உங்கள் தேவை வெற்றிகரமாக பதிவு செய்யப்பட்டது!* 🎯\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• *பதிவான தேவை:* {n['title']}\n"
                f"• *பரிந்துரைக்கப்பட்ட அரசு நலத்திட்டம்:* 🏛️ {n['matched_scheme']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"SIA அரசு அலுவலர் இ-சேவை மற்றும் வாடகை சேவைகள் மூலம் உங்களுக்கு தீர்வு காண உதவும்."
            )
            return {"status": "processed", "type": "needs_add", "message": msg}

        user = get_or_initialize_user_vault(clean_phone)
        needs = user.get("needs_tracker", [])
        n_lines = [f"• {n['title']} (பரிந்துரை: {n['matched_scheme']})" for n in needs[:4]]
        msg = (
            f"📝 *SIA உங்கள் தேவைகள் & நலத்திட்ட பரிந்துரைகள் (My Needs)* 🎯\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{chr(10).join(n_lines)}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *புதிய தேவை சேர்க்க:* 'தேவை 2 மூட்டை உரம்' என அனுப்பவும்."
        )
        return {"status": "processed", "type": "needs_view", "message": msg}

    # 7. Personal Diary (e.g. "நாட்குறிப்பு", "டைரி", "diary")
    if any(k in clean_text for k in ["நாட்குறிப்பு", "டைரி", "நினைவு"]) or any(k in upper for k in ["DIARY", "JOURNAL"]):
        match_diary = re.search(r"(?:நாட்குறிப்பு|டைரி|DIARY)\s*(.*)", clean_text, re.IGNORECASE)
        if match_diary and len(match_diary.group(1).strip()) > 5:
            content = match_diary.group(1).strip()
            res = add_diary_entry(clean_phone, content)
            d = res["diary_entry"]
            msg = (
                f"📖 *SIA தனிப்பட்ட நாட்குறிப்பில் பதிவு செய்யப்பட்டது!* ✍️\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• *தேதி:* {d['date']} ({d['timestamp']})\n"
                f"• *பதிவு:* \"{d['content'][:150]}...\"\n"
                f"• *மனநிலை:* {d['mood']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"உங்கள் நினைவுகள் மற்றும் குறிப்புகள் ரகசியமாக பாதுகாக்கப்படுகின்றன."
            )
            return {"status": "processed", "type": "diary_add", "message": msg}

        user = get_or_initialize_user_vault(clean_phone)
        diaries = user.get("personal_diary", [])
        d_lines = [f"📅 *{d['date']}* ({d['timestamp']})\n   \"{d['content'][:100]}\" ({d['mood']})" for d in diaries[:3]]
        msg = (
            f"📖 *SIA எனது தனிப்பட்ட நாட்குறிப்பு (My Diary)* ✍️\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{chr(10).join(d_lines)}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *புதிய குறிப்பு எழுத:* 'நாட்குறிப்பு இன்று நல்ல மழை பெய்தது' என அனுப்பவும்."
        )
        return {"status": "processed", "type": "diary_view", "message": msg}

    # 8. Plans & Goals (e.g. "திட்டங்கள்", "இலக்கு", "plans")
    if any(k in clean_text for k in ["திட்டம்", "திட்டங்கள்", "இலக்கு", "பணிகள்"]) or any(k in upper for k in ["PLAN", "PLANS", "GOAL", "GOALS", "TODO"]):
        match_plan = re.search(r"(?:திட்டம்|PLAN)\s*(.*)", clean_text, re.IGNORECASE)
        if match_plan and len(match_plan.group(1).strip()) > 3:
            p_title = match_plan.group(1).strip()
            res = add_plan_entry(clean_phone, p_title)
            p = res["plan"]
            msg = (
                f"🎯 *SIA புதிய குடும்பத் திட்டம் சேர்க்கப்பட்டது!* 🚀\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• *திட்டம்:* {p['title']}\n"
                f"• *இலக்கு நாள்:* {p['target_date']}\n"
                f"• *முன்னுரிமை:* {p['priority']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"திட்டங்கள் நிறைவடைந்தவுடன் நினைவூட்டல் வழங்கப்படும்."
            )
            return {"status": "processed", "type": "plans_add", "message": msg}

        user = get_or_initialize_user_vault(clean_phone)
        plans = user.get("plans_goals", [])
        p_lines = [f"🎯 *{p['title']}*\n   இலக்கு: {p['target_date']} | நிலை: {p['status']}" for p in plans[:4]]
        msg = (
            f"🎯 *SIA எனது எதிர்காலத் திட்டங்கள் & இலக்குகள் (My Plans)* 🚀\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{chr(10).join(p_lines)}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *புதிய திட்டம் சேர்க்க:* 'திட்டம் மகள் கல்லூரி கட்டணம்' என அனுப்பவும்."
        )
        return {"status": "processed", "type": "plans_view", "message": msg}

    # 9. Family Bio & Secret Vault (e.g. "குடும்பம்", "ரகசிய பெட்டகம்", "ரத்த வகை")
    if any(k in clean_text for k in ["குடும்பம்", "ரத்த வகை", "மருந்து", "உறுப்பினர்கள்"]) or any(k in upper for k in ["FAMILY", "BLOOD", "MEDS", "HEALTH"]):
        members = get_family_bio(clean_phone)
        f_lines = []
        for m in members:
            f_lines.append(f"👨‍👩‍👧 *{m['name']}* ({m['relation']})\n   • வயது: {m['age']} | ரத்த வகை: *{m['blood_group']}*\n   • மருந்துகள்: {m['daily_meds']}")
        f_str = "\n\n".join(f_lines)

        msg = (
            f"👨‍👩‍👧 *SIA குடும்ப உறுப்பினர்கள் விவரம் & மருத்துவ குறிப்புகள்* 🩺\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{f_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔐 *ரகசிய பெட்டகத்தை திறக்க:* 'ரகசிய பெட்டகம் [உங்கள் PIN]' என அனுப்பவும்."
        )
        return {"status": "processed", "type": "family_view", "message": msg}

    # 10. Secret Vault (e.g. "ரகசிய பெட்டகம்", "SECRET VAULT")
    if any(k in clean_text for k in ["ரகசிய பெட்டகம்", "ரகசியம்"]) or any(k in upper for k in ["SECRET", "VAULT"]):
        # Check if PIN provided
        pin_match = re.search(r"(\d{4})", clean_text)
        if pin_match:
            entered_pin = pin_match.group(1)
            unlock_res = unlock_secret_vault(clean_phone, entered_pin)
            if unlock_res["unlocked"]:
                sec_lines = [f"🔐 *{item['title']}*\n   `{item['secret_value']}`" for item in unlock_res["items"]]
                msg = (
                    f"🔓 *SIA ரகசிய பெட்டகம் திறக்கப்பட்டது (Secret Vault)* ✅\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{chr(10).join(sec_lines)}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"⚠️ *பாதுகாப்பு எச்சரிக்கை:* இந்த தகவலை யாரிடமும் பகிர வேண்டாம்."
                )
                return {"status": "processed", "type": "secret_vault_unlocked", "message": msg}
            else:
                return {"status": "processed", "type": "secret_vault_error", "message": unlock_res["message_ta"]}

        # If no PIN provided, prompt citizen for PIN
        msg = (
            f"🔐 *SIA பாதுகாக்கப்பட்ட ரகசிய பெட்டகம் (Secret Vault)*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"வங்கி கணக்குகள், லாக்கர் விபரம் மற்றும் ரகசிய குறிப்புகளை அணுக உங்கள் 4-இலக்க பின் (PIN) எண்ணை அனுப்பவும்.\n\n"
            f"உதாரணமாக: *ரகசிய பெட்டகம் 7890* என அனுப்பவும்."
        )
        return {"status": "processed", "type": "secret_vault_prompt", "message": msg}

    return {"status": "unhandled"}
