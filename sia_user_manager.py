# -*- coding: utf-8 -*-
"""
SIA (Super Intelligent Agent) - Interactive WhatsApp User Registry & Onboarding
Meta AI Developer Hackathon 2026

Fully button/list-driven WhatsApp onboarding designed for illiterate and
low-literacy rural citizens.  Every step uses interactive reply-buttons or
list-selects so users never need to type free-form text (voice notes are
accepted for name input).

Cell number: 6381029380
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

logger = logging.getLogger("sia.user_manager")

REGISTRY_PATH = Path(__file__).parent / "sia_users_registry.json"
SIA_OFFICIAL_NUMBER = "6381029380"

# ── In-memory conversational state per phone ──
ONBOARDING_STAGES: Dict[str, Dict[str, Any]] = {}

DEFAULT_PROOFS = [
    {
        "id": "proof_aadhaar_01",
        "doc_type": "Aadhaar Card",
        "doc_name_ta": "ஆதார் அடையாள அட்டை",
        "doc_number": "XXXX-XXXX-7890",
        "verified_by": "Llama 3.2 Vision",
        "status": "VERIFIED",
        "date_added": "2026-10-25"
    },
    {
        "id": "proof_ration_01",
        "doc_type": "Smart Ration Card",
        "doc_name_ta": "ஸ்மார்ட் குடும்ப அட்டை (TNPDS)",
        "doc_number": "33/W/0192834",
        "verified_by": "TNeGA e-Sevai API",
        "status": "ACTIVE",
        "date_added": "2026-10-26"
    },
    {
        "id": "proof_patta_01",
        "doc_type": "Patta Chitta",
        "doc_name_ta": "கிரய பட்டா ஆவணம் (142/3A)",
        "doc_number": "Survey 142/3A",
        "verified_by": "Meta SAM 3.1",
        "status": "AUDITED",
        "date_added": "2026-10-27"
    }
]

# ── Tamil Nadu Districts for list-picker ──
TN_DISTRICTS = [
    ("ariyalur", "Ariyalur", "அரியலூர்"),
    ("chengalpattu", "Chengalpattu", "செங்கல்பட்டு"),
    ("chennai", "Chennai", "சென்னை"),
    ("coimbatore", "Coimbatore", "கோயம்புத்தூர்"),
    ("cuddalore", "Cuddalore", "கடலூர்"),
    ("dharmapuri", "Dharmapuri", "தர்மபுரி"),
    ("dindigul", "Dindigul", "திண்டுக்கல்"),
    ("erode", "Erode", "ஈரோடு"),
    ("kallakurichi", "Kallakurichi", "கள்ளக்குறிச்சி"),
    ("kancheepuram", "Kancheepuram", "காஞ்சிபுரம்"),
    ("karur", "Karur", "கரூர்"),
    ("krishnagiri", "Krishnagiri", "கிருஷ்ணகிரி"),
    ("madurai", "Madurai", "மதுரை"),
    ("mayiladuthurai", "Mayiladuthurai", "மயிலாடுதுறை"),
    ("nagapattinam", "Nagapattinam", "நாகப்பட்டினம்"),
    ("namakkal", "Namakkal", "நாமக்கல்"),
    ("nilgiris", "Nilgiris", "நீலகிரி"),
    ("perambalur", "Perambalur", "பெரம்பலூர்"),
    ("pudukkottai", "Pudukkottai", "புதுக்கோட்டை"),
    ("ramanathapuram", "Ramanathapuram", "ராமநாதபுரம்"),
    ("ranipet", "Ranipet", "ராணிப்பேட்டை"),
    ("salem", "Salem", "சேலம்"),
    ("sivaganga", "Sivaganga", "சிவகங்கை"),
    ("tenkasi", "Tenkasi", "தென்காசி"),
    ("thanjavur", "Thanjavur", "தஞ்சாவூர்"),
    ("theni", "Theni", "தேனி"),
    ("thoothukudi", "Thoothukudi", "தூத்துக்குடி"),
    ("tiruchirappalli", "Tiruchirappalli", "திருச்சிராப்பள்ளி"),
    ("tirunelveli", "Tirunelveli", "திருநெல்வேலி"),
    ("tirupattur", "Tirupattur", "திருப்பத்தூர்"),
    ("tiruvallur", "Tiruvallur", "திருவள்ளூர்"),
    ("tiruvannamalai", "Tiruvannamalai", "திருவண்ணாமலை"),
    ("tiruvarur", "Tiruvarur", "திருவாரூர்"),
    ("vellore", "Vellore", "வேலூர்"),
    ("villupuram", "Villupuram", "விழுப்புரம்"),
    ("virudhunagar", "Virudhunagar", "விருதுநகர்"),
]


# ══════════════════════════════════════════════════════════════════════════════
# Registry helpers (unchanged)
# ══════════════════════════════════════════════════════════════════════════════

def _clean_phone(phone: str) -> str:
    digits = "".join([c for c in str(phone) if c.isdigit()])
    return digits[-10:] if len(digits) >= 10 else digits


def load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        initial_data = {
            "users": {
                "6381029380": {
                    "phone": "6381029380",
                    "name": "ர. சுப்பிரமணியன் (R. Subramanian)",
                    "pin": "7890",
                    "district": "Madurai",
                    "taluk": "Vadipatti",
                    "village": "Sholavandan",
                    "family_head": "ர. சுப்பிரமணியன்",
                    "family_members_count": 4,
                    "registered_at": "2026-10-28T10:00:00",
                    "proofs_vault": DEFAULT_PROOFS,
                    "education_level": "Higher Secondary",
                    "last_active": "2026-10-28T10:30:00"
                }
            }
        }
        save_registry(initial_data)
        return initial_data
    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading registry: {e}")
        return {"users": {}}


def save_registry(data: Dict[str, Any]) -> None:
    try:
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving registry: {e}")


def is_user_registered(phone: str) -> bool:
    clean = _clean_phone(phone)
    reg = load_registry()
    return clean in reg.get("users", {})


def get_user_profile(phone: str) -> Optional[Dict[str, Any]]:
    clean = _clean_phone(phone)
    reg = load_registry()
    return reg.get("users", {}).get(clean)


def verify_user_pin(phone: str, pin: str) -> bool:
    user = get_user_profile(phone)
    if not user:
        return False
    return str(user.get("pin")).strip() == str(pin).strip()


def register_new_user(
    phone: str,
    name: str,
    pin: str,
    district: str = "Madurai",
    taluk: str = "Vadipatti",
    family_members_count: int = 4
) -> Dict[str, Any]:
    clean = _clean_phone(phone)
    reg = load_registry()
    user_data = {
        "phone": clean,
        "name": name.strip(),
        "pin": str(pin).strip(),
        "district": district.strip(),
        "taluk": taluk.strip(),
        "village": "Rural Taluk Center",
        "family_head": name.strip(),
        "family_members_count": int(family_members_count),
        "registered_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "proofs_vault": [
            {
                "id": f"proof_aadhaar_{clean[-4:]}",
                "doc_type": "Aadhaar Card",
                "doc_name_ta": "ஆதார் அட்டை",
                "doc_number": f"XXXX-XXXX-{clean[-4:]}",
                "verified_by": "Llama 3.2 Vision",
                "status": "VERIFIED",
                "date_added": time.strftime("%Y-%m-%d")
            }
        ],
        "education_level": "Samacheer Kalvi Learner",
        "last_active": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    if "users" not in reg:
        reg["users"] = {}
    reg["users"][clean] = user_data
    save_registry(reg)
    logger.info(f"[SIA] Registered: {name} ({clean})")
    return user_data


def add_proof_document(phone: str, doc_type: str, doc_number: str,
                       verified_by: str = "Llama 3.2 Vision") -> Dict[str, Any]:
    clean = _clean_phone(phone)
    reg = load_registry()
    user = reg.get("users", {}).get(clean)
    if not user:
        return {"status": "error", "message": "User not found"}
    new_doc = {
        "id": f"proof_{int(time.time())}",
        "doc_type": doc_type,
        "doc_name_ta": doc_type,
        "doc_number": doc_number,
        "verified_by": verified_by,
        "status": "VERIFIED",
        "date_added": time.strftime("%Y-%m-%d")
    }
    user.setdefault("proofs_vault", []).append(new_doc)
    save_registry(reg)
    return {"status": "success", "document": new_doc}


# ══════════════════════════════════════════════════════════════════════════════
# Message-builder helpers  –  returns message dicts, never sends directly
# ══════════════════════════════════════════════════════════════════════════════

def _msg_text(body: str) -> Dict[str, Any]:
    """Plain text message."""
    return {"type": "text", "text": body}


def _msg_buttons(body: str, buttons: List[Dict[str, str]],
                 header: str = "", footer: str = "") -> Dict[str, Any]:
    """
    Interactive reply-button message (max 3 buttons, title max 20 chars).
    buttons: [{"id": "btn_xxx", "title": "Label"}, ...]
    """
    msg: Dict[str, Any] = {
        "type": "button",
        "body": body,
        "buttons": buttons[:3],
    }
    if header:
        msg["header"] = header
    if footer:
        msg["footer"] = footer
    return msg


def _msg_list(body: str, button_label: str,
              sections: List[Dict[str, Any]],
              header: str = "", footer: str = "") -> Dict[str, Any]:
    """
    Interactive list-picker message.
    sections: [{"title": "Section", "rows": [{"id": "...", "title": "...", "description": "..."}]}]
    """
    msg: Dict[str, Any] = {
        "type": "list",
        "body": body,
        "button_label": button_label,
        "sections": sections,
    }
    if header:
        msg["header"] = header
    if footer:
        msg["footer"] = footer
    return msg


def _plain_text_fallback(messages: List[Dict[str, Any]]) -> str:
    """Generates a combined plain-text fallback for simulation endpoints."""
    parts = []
    for m in messages:
        if m["type"] == "text":
            parts.append(m["text"])
        elif m["type"] == "button":
            header = m.get("header", "")
            body = m.get("body", "")
            btn_labels = " | ".join(f"[{b['title']}]" for b in m.get("buttons", []))
            footer = m.get("footer", "")
            parts.append(f"{header}\n{body}\n{btn_labels}\n{footer}".strip())
        elif m["type"] == "list":
            header = m.get("header", "")
            body = m.get("body", "")
            rows_txt = []
            for sec in m.get("sections", []):
                for row in sec.get("rows", []):
                    rows_txt.append(f"  • {row['title']} - {row.get('description','')}")
            parts.append(f"{header}\n{body}\n" + "\n".join(rows_txt))
    return "\n\n".join(parts)


# ══════════════════════════════════════════════════════════════════════════════
# Service Menu builder
# ══════════════════════════════════════════════════════════════════════════════

def _build_service_menu() -> Dict[str, Any]:
    """Returns a list-picker message with all SIA service categories (max 10 rows for WhatsApp Cloud API compliance)."""
    return _msg_list(
        header="📋 SIA சேவைகள்",
        body=(
            "கீழே உள்ள பட்டியலில் உங்களுக்குத் தேவையான சேவையைத் தொடவும் 👇\n\n"
            "Tap the service you need from the list below 👇"
        ),
        button_label="📋 சேவைகள் பார்",
        sections=[
            {
                "title": "🏛️ அரசு சேவைகள்",
                "rows": [
                    {"id": "svc_land",    "title": "🏠 நிலம் & பட்டா",     "description": "பட்டா, சிட்டா, FMB, நில அளவீடு"},
                    {"id": "svc_ration",  "title": "📋 ரேஷன் & ஆதார்",     "description": "குடும்ப அட்டை, ஆதார் திருத்தம்"},
                    {"id": "svc_mla",     "title": "🗳️ அரசு மனு & RTI",    "description": "MLA/MP மனு, தகவல் அறியும் உரிமை"},
                ]
            },
            {
                "title": "🌾 வேளாண் & கல்வி",
                "rows": [
                    {"id": "svc_agri",    "title": "🌾 வேளாண்மை",          "description": "பயிர் நோய், மானியம், PM-KISAN"},
                    {"id": "svc_edu",     "title": "📚 கல்வி உதவி",        "description": "சமச்சீர் கல்வி, NEET, TNPSC"},
                    {"id": "svc_health",  "title": "💊 மருத்துவ காப்பீடு",  "description": "CMCHIS அரசு மருத்துவ காப்பீடு"},
                ]
            },
            {
                "title": "🔧 கணக்கு & Dashboard",
                "rows": [
                    {"id": "svc_vault",   "title": "📄 ஆவண பெட்டகம்",     "description": "சான்றிதழ்கள் பாதுகாப்பு சேமிப்பு"},
                    {"id": "svc_dash",    "title": "🧠 3D Dashboard",       "description": "SIA Super Intelligence Portal"},
                ]
            },
        ],
        footer="SIA • Super Intelligent Agent • Meta AI 2026"
    )


# ══════════════════════════════════════════════════════════════════════════════
# Main conversational flow  –  returns {messages: [...], reply: "...", ...}
# ══════════════════════════════════════════════════════════════════════════════

def handle_sia_whatsapp_flow(
    sender_phone: str,
    message_text: str,
    public_base_url: str,
    msg_type: str = "text",
    interactive_id: str = "",
    interactive_title: str = "",
) -> Optional[Dict[str, Any]]:
    """
    Fully interactive WhatsApp onboarding and service router.

    Parameters
    ----------
    sender_phone : raw phone string from webhook
    message_text : body text (or transcribed voice note)
    public_base_url : for magic-link generation
    msg_type : "text" | "interactive" | "audio"
    interactive_id : button_reply.id or list_reply.id
    interactive_title : button_reply.title or list_reply.title
    """
    from whatsapp_auth_manager import create_magic_auth_token

    clean_phone = _clean_phone(sender_phone)
    text = (message_text or "").strip()
    upper = text.upper()
    session = ONBOARDING_STAGES.get(clean_phone)

    # Determine the effective "action" – interactive ID takes priority
    action = interactive_id or upper

    # ────────────────────────────────────────────────────────────────────────
    #  CASE 0: Service menu actions (from logged-in user clicking a service)
    # ────────────────────────────────────────────────────────────────────────
    if action.startswith("svc_"):
        return _handle_service_action(clean_phone, action, public_base_url)

    # ────────────────────────────────────────────────────────────────────────
    #  CASE 1: Active registration session in progress
    # ────────────────────────────────────────────────────────────────────────
    if session:
        return _handle_onboarding_step(clean_phone, text, action, session, public_base_url)

    # ────────────────────────────────────────────────────────────────────────
    #  CASE 2: Button click – Register
    # ────────────────────────────────────────────────────────────────────────
    if action == "btn_register":
        return _start_registration(clean_phone)

    # ────────────────────────────────────────────────────────────────────────
    #  CASE 3: Button click – Login / PIN entry
    # ────────────────────────────────────────────────────────────────────────
    if action == "btn_login":
        if is_user_registered(clean_phone):
            return _ask_pin(clean_phone)
        else:
            return _start_registration(clean_phone)

    if action == "btn_pin_custom":
        # User chose to type a custom PIN
        if session is None:
            ONBOARDING_STAGES[clean_phone] = {"stage": "AWAIT_LOGIN_PIN", "phone": clean_phone}
        return _result([
            _msg_text(
                "🔐 உங்கள் 4-இலக்க PIN எண்ணை அனுப்பவும்\n"
                "Type your 4-digit PIN 👇"
            )
        ], stage="AWAIT_LOGIN_PIN")

    # ────────────────────────────────────────────────────────────────────────
    #  CASE 4: PIN entry (direct 4-digit number or "PIN xxxx")
    # ────────────────────────────────────────────────────────────────────────
    pin_digits = "".join([c for c in upper if c.isdigit()])
    is_pin = (
        (upper.startswith("PIN") and len(pin_digits) == 4) or
        (upper.isdigit() and len(upper) == 4) or
        action == "btn_pin_default"
    )
    if is_pin:
        if action == "btn_pin_default":
            pin_digits = "7890"
        if is_user_registered(clean_phone):
            return _login_with_pin(clean_phone, pin_digits, public_base_url)
        else:
            return _start_registration(clean_phone)

    # ────────────────────────────────────────────────────────────────────────
    #  CASE 5: Greeting / contains SIA / Hi / Hello / START
    # ────────────────────────────────────────────────────────────────────────
    SYSTEM_COMMAND_KEYWORDS = {
        "CLOSE", "LOGOUT", "EXIT", "QUIT", "LOCK", "TEST", "EXAM", "QUIZ", "TNPSC",
        "SAMACHEER", "FAMILY", "HUB", "FAM", "IAS", "IPS", "DOCTOR", "ENGINEER",
        "JUDGE", "SCIENTIST", "CEO", "CA", "AUDITOR", "AMBITION", "GK", "TODAY",
        "PENSION", "OAP", "KMUT", "MAGALIR", "MANDI", "MARKET", "PATTA", "RATION",
        "AADHAAR", "RTI", "ANS"
    }
    if any(upper == k or upper.startswith(k + " ") or upper.startswith(k + "-") for k in SYSTEM_COMMAND_KEYWORDS):
        return None
    if upper in ["A", "B", "C", "D"] or (len(upper) >= 3 and upper[0].isdigit() and upper[1] in "-:" and upper[2] in "ABCD"):
        return None

    contains_sia = "SIA" in upper or "சியா" in text
    if not is_user_registered(clean_phone) and any(w in upper for w in ["ACCESS", "REGISTER", "SIGNUP", "NEW", "WANT TO ACCESS"]):
        return _start_registration(clean_phone)

    is_greeting = upper in [
        "HI", "HELLO", "START", "LOGIN", "MENU",
        "வணக்கம்", "ஹலோ", "ஹாய்", "SIA",
    ] or contains_sia

    if is_greeting:
        return _send_welcome(clean_phone)

    # ────────────────────────────────────────────────────────────────────────
    #  CASE 6: Service menu request
    # ────────────────────────────────────────────────────────────────────────
    if action in ("btn_services", "btn_menu"):
        if is_user_registered(clean_phone):
            user = get_user_profile(clean_phone)
            msgs = [
                _msg_text(f"🙏 வணக்கம் *{user.get('name', '')}*!"),
                _build_service_menu()
            ]
            return _result(msgs, stage="SERVICE_MENU")
        else:
            return _send_welcome(clean_phone)

    # ────────────────────────────────────────────────────────────────────────
    #  CASE 7: Help
    # ────────────────────────────────────────────────────────────────────────
    if action in ("btn_help", "HELP", "HELP ME", "உதவி"):
        return _result([
            _msg_buttons(
                header="❓ SIA உதவி / Help",
                body=(
                    "நான் SIA - உங்கள் Super Intelligent Agent 🤖\n\n"
                    "📌 நான் என்ன செய்வேன்?\n"
                    "• 🏠 நில பட்டா, சிட்டா பெற உதவி\n"
                    "• 📋 ரேஷன் அட்டை புதுப்பித்தல்\n"
                    "• 🌾 பயிர் நோய் ஆலோசனை (AI கேமரா)\n"
                    "• 📚 சமச்சீர் கல்வி உதவி\n"
                    "• 📝 RTI / MLA மனு உருவாக்கம்\n"
                    "• 📄 ஆவணங்கள் பாதுகாப்பு\n\n"
                    "How can I help?\n"
                    "I assist with land records, ration cards, agriculture, education, petitions & more!"
                ),
                buttons=[
                    {"id": "btn_register", "title": "🆕 பதிவு செய்"},
                    {"id": "btn_login",    "title": "🔑 உள்நுழை"},
                    {"id": "btn_services", "title": "📋 சேவைகள்"},
                ],
                footer="SIA • Meta AI Hackathon 2026"
            )
        ], stage="HELP")

    # ────────────────────────────────────────────────────────────────────────
    #  Default: Not handled → return None so the main handler continues
    # ────────────────────────────────────────────────────────────────────────
    return None


# ══════════════════════════════════════════════════════════════════════════════
# Sub-flows
# ══════════════════════════════════════════════════════════════════════════════

def _send_welcome(clean_phone: str) -> Dict[str, Any]:
    """Welcome message with Register / Login / Help buttons."""
    registered = is_user_registered(clean_phone)

    if registered:
        user = get_user_profile(clean_phone)
        name = user.get("name", "நண்பரே") if user else "நண்பரே"
        msgs = [
            _msg_buttons(
                header="🌟 SIA (Super Intelligent Agent)",
                body=(
                    f"🙏 வணக்கம் *{name}*!\n\n"
                    f"உங்கள் எண் (+91 {clean_phone}) ஏற்கனவே பதிவு செய்யப்பட்டுள்ளது ✅\n\n"
                    "உங்கள் PIN அனுப்பி Dashboard-ஐ திறக்கலாம்\n"
                    "அல்லது சேவைகளை நேரடியாக பயன்படுத்தலாம்\n\n"
                    "Send your PIN to open Dashboard\n"
                    "or browse services directly 👇"
                ),
                buttons=[
                    {"id": "btn_login",    "title": "🔑 PIN அனுப்பு"},
                    {"id": "btn_services", "title": "📋 சேவைகள்"},
                    {"id": "btn_help",     "title": "❓ உதவி"},
                ],
                footer="Meta AI Hackathon 2026 🏆"
            )
        ]
        return _result(msgs, stage="WELCOME_REGISTERED", status="registered_ask_pin")
    else:
        msgs = [
            _msg_buttons(
                header="🌟 SIA (Super Intelligent Agent)",
                body=(
                    "🙏 வணக்கம்! நான் *SIA* - உங்கள் சூப்பர் இன்டெலிஜென்ட் ஏஜென்ட்\n\n"
                    "தமிழ்நாடு அரசு சேவைகள், நில ஆவணங்கள், வேளாண்மை, கல்வி "
                    "ஆகியவற்றுக்கு AI உதவி பெறலாம்.\n\n"
                    f"📱 உங்கள் எண்: +91 {clean_phone}\n"
                    "⏱️ பதிவு செய்ய 30 நொடிகள் போதும்!\n\n"
                    "Hello! I'm *SIA* - your AI assistant for\n"
                    "TN govt services, land records, agriculture & education.\n"
                    "Registration takes just 30 seconds! 👇"
                ),
                buttons=[
                    {"id": "btn_register", "title": "🆕 பதிவு செய்"},
                    {"id": "btn_login",    "title": "🔑 உள்நுழை"},
                    {"id": "btn_help",     "title": "❓ உதவி / Help"},
                ],
                footer="100% இலவசம் • 100% Free"
            )
        ]
        return _result(msgs, stage="WELCOME_NEW")


def _start_registration(clean_phone: str) -> Dict[str, Any]:
    """Begin the 4-step interactive registration."""
    ONBOARDING_STAGES[clean_phone] = {"stage": "ASK_NAME", "phone": clean_phone}
    msgs = [
        _msg_text(
            "📝 *SIA பதிவு தொடங்குகிறது!*\n"
            "Registration starting!\n\n"
            "4 எளிய படிகள் • 4 simple steps\n"
            "━━━━━━━━━━━━━━━━━━"
        ),
        _msg_buttons(
            header="👤 படி 1/3 • பெயர்",
            body=(
                "உங்கள் முழுப் பெயரை தட்டச்சு செய்யவும் ⌨️\n"
                "அல்லது குரல் பதிவு அனுப்பவும் 🎤\n\n"
                "Type your full name\n"
                "or send a voice note 🎤\n\n"
                "எடுத்துக்காட்டு: அருண் குமார்"
            ),
            buttons=[
                {"id": "btn_voice_name", "title": "🎤 குரலில் சொல்ல"},
            ],
            footer="படி 1/4 • Step 1/4"
        )
    ]
    return _result(msgs, stage="ASK_NAME")


def _ask_pin(clean_phone: str) -> Dict[str, Any]:
    """Ask registered user for their PIN to login."""
    ONBOARDING_STAGES[clean_phone] = {"stage": "AWAIT_LOGIN_PIN", "phone": clean_phone}
    user = get_user_profile(clean_phone)
    name = user.get("name", "") if user else ""
    msgs = [
        _msg_buttons(
            header="🔐 PIN உள்நுழைவு",
            body=(
                f"வணக்கம் *{name}*!\n\n"
                "உங்கள் 4-இலக்க ரகசிய PIN-ஐ அனுப்பவும்\n"
                "Send your 4-digit PIN 👇\n\n"
                "அல்லது கீழே உள்ள பொத்தானைத் தொடவும் 👇"
            ),
            buttons=[
                {"id": "btn_pin_custom",  "title": "⌨️ PIN தட்டச்சு"},
                {"id": "btn_help",        "title": "❓ PIN மறந்தேன்"},
            ],
            footer="படி: PIN எண்ணை அனுப்பவும்"
        )
    ]
    return _result(msgs, stage="AWAIT_LOGIN_PIN")


def _login_with_pin(clean_phone: str, pin: str, base_url: str) -> Dict[str, Any]:
    """Verify PIN and send magic dashboard link."""
    from whatsapp_auth_manager import create_magic_auth_token

    # Clean up any onboarding session
    ONBOARDING_STAGES.pop(clean_phone, None)

    if not verify_user_pin(clean_phone, pin):
        return _result([
            _msg_buttons(
                header="❌ தவறான PIN",
                body=(
                    f"நீங்கள் அனுப்பிய PIN (*{pin}*) தவறானது.\n"
                    "The PIN you entered is incorrect.\n\n"
                    "மீண்டும் முயற்சிக்கவும் 👇\n"
                    "Try again 👇"
                ),
                buttons=[
                    {"id": "btn_pin_custom", "title": "🔄 மீண்டும் முயற்சி"},
                    {"id": "btn_help",       "title": "❓ உதவி"},
                ],
            )
        ], stage="PIN_INVALID")

    user = get_user_profile(clean_phone)
    name = user.get("name", "") if user else ""
    auth_token = create_magic_auth_token(phone=clean_phone, secret_pin=pin)
    magic_url = f"{base_url}/auth/magic?token={auth_token['token']}&phone={clean_phone}"

    msgs = [
        _msg_text(
            f"✅ *PIN சரிபார்க்கப்பட்டது!*\n"
            f"🙏 வணக்கம் *{name}*!\n\n"
            f"🌟 உங்கள் SIA (Super Intelligent Agent) 3D Dashboard:\n"
            f"🧠 3D Neural Brain & 💓 Live Biometric Heartbeat Active:\n"
            f"👉 {magic_url}\n\n"
            f"⏱️ இணைப்பு 15 நிமிடம் செல்லும்\n"
            f"🔒 முடித்ததும் CLOSE அனுப்பவும்\n\n"
            f"Your SIA Dashboard link above ☝️\n"
            f"Valid for 15 minutes • Send CLOSE when done"
        ),
        _build_service_menu()
    ]
    return _result(msgs, stage="AUTHENTICATED", status="authenticated", magic_url=magic_url)


def _handle_onboarding_step(
    clean_phone: str, text: str, action: str,
    session: Dict[str, Any], base_url: str
) -> Dict[str, Any]:
    """Process the current registration / login step."""
    stage = session.get("stage")
    from whatsapp_auth_manager import create_magic_auth_token

    # ── Await login PIN ──
    if stage == "AWAIT_LOGIN_PIN":
        pin = "".join([c for c in text if c.isdigit()])
        if len(pin) == 4:
            ONBOARDING_STAGES.pop(clean_phone, None)
            return _login_with_pin(clean_phone, pin, base_url)
        return _result([
            _msg_text("⚠️ 4-இலக்க எண்களை மட்டும் அனுப்பவும்\nPlease send only 4 digits")
        ], stage="AWAIT_LOGIN_PIN")

    # ── Step 1: Name ──
    if stage == "ASK_NAME":
        if action == "btn_voice_name":
            return _result([
                _msg_text(
                    "🎤 *குரல் பதிவு அனுப்பவும்*\n\n"
                    "WhatsApp-ல் மைக் பொத்தானை அழுத்தி\n"
                    "உங்கள் பெயரைச் சொல்லவும்\n\n"
                    "Press the mic button and say your name"
                )
            ], stage="ASK_NAME")

        name = text.strip()
        if len(name) < 2:
            return _result([
                _msg_text("⚠️ தயவுசெய்து உங்கள் பெயரை அனுப்பவும்\nPlease send your name")
            ], stage="ASK_NAME")

        session["name"] = name
        session["stage"] = "ASK_PIN"
        ONBOARDING_STAGES[clean_phone] = session

        return _result([
            _msg_buttons(
                header="🔐 படி 2/3 • PIN எண் (Step 2/3)",
                body=(
                    f"✅ வணக்கம் *{name}*!\n\n"
                    "4-இலக்க ரகசிய PIN அமைக்கவும்\n"
                    "Set a 4-digit secret PIN\n\n"
                    "இது உங்கள் கணக்கைப் பாதுகாக்கும் 🔒\n"
                    "This protects your account 🔒\n\n"
                    "⌨️ PIN எண்ணை தட்டச்சு செய்யவும்\n"
                    "அல்லது இயல்பு PIN பயன்படுத்தலாம் 👇"
                ),
                buttons=[
                    {"id": "btn_set_pin_custom", "title": "⌨️ நான் அமைப்பேன்"},
                    {"id": "btn_set_pin_7890",   "title": "🔢 7890 பயன்படுத்து"},
                ],
                footer="படி 2/4 • Step 2/4"
            )
        ], stage="ASK_PIN")

    # ── Step 2: PIN ──
    if stage == "ASK_PIN":
        if action == "btn_set_pin_7890":
            pin_digits = "7890"
        elif action == "btn_set_pin_custom":
            return _result([
                _msg_text(
                    "⌨️ 4-இலக்க PIN எண்ணை தட்டச்சு செய்யவும்\n"
                    "Type your 4-digit PIN (e.g. 4567)"
                )
            ], stage="ASK_PIN")
        else:
            pin_digits = "".join([c for c in text if c.isdigit()])

        if len(pin_digits) != 4:
            return _result([
                _msg_buttons(
                    body=(
                        "⚠️ 4 எண்கள் மட்டும் அனுப்பவும்\n"
                        "Please send exactly 4 digits\n\n"
                        "எடுத்துக்காட்டு: 1234"
                    ),
                    buttons=[
                        {"id": "btn_set_pin_7890", "title": "🔢 7890 பயன்படுத்து"},
                    ]
                )
            ], stage="ASK_PIN")

        session["pin"] = pin_digits
        session["stage"] = "ASK_FAMILY"
        ONBOARDING_STAGES[clean_phone] = session

        # 8 major hub districts in Tamil Nadu (Strictly <= 10 rows for WhatsApp Cloud API compliance)
        top_districts = [
            {"id": "dist_madurai",     "title": "மதுரை",          "description": "Madurai District"},
            {"id": "dist_chennai",     "title": "சென்னை",          "description": "Chennai District"},
            {"id": "dist_coimbatore",  "title": "கோயம்புத்தூர்",   "description": "Coimbatore District"},
            {"id": "dist_trichy",      "title": "திருச்சிராப்பள்ளி", "description": "Tiruchirappalli District"},
            {"id": "dist_salem",       "title": "சேலம்",           "description": "Salem District"},
            {"id": "dist_tirunelveli", "title": "திருநெல்வேலி",     "description": "Tirunelveli District"},
            {"id": "dist_erode",       "title": "ஈரோடு",           "description": "Erode District"},
            {"id": "dist_thanjavur",   "title": "தஞ்சாவூர்",        "description": "Thanjavur District"},
        ]
        sections = [{"title": "📍 முக்கிய மாவட்டங்கள்", "rows": top_districts}]

        return _result([
            _msg_list(
                header="👨‍👩‍👧 படி 3/3 • மாவட்டம் & குடும்பம் (Step 3/3)",
                body=(
                    f"✅ PIN *{pin_digits}* அமைக்கப்பட்டது!\n\n"
                    "உங்கள் மாவட்டத்தைத் தேர்வு செய்யவும் 👇\n"
                    "(பட்டியலில் தொடவும் அல்லது மாவட்டப் பெயரை தட்டச்சு செய்யவும்)\n\n"
                    "Select your district from the list below, or simply type your district name 👇"
                ),
                button_label="📍 மாவட்டம் தேர்வு",
                sections=sections,
                footer="படி 3/3 • Step 3/3 • கடைசி படி!"
            )
        ], stage="ASK_FAMILY")

    # ── Step 3/3: Family & District ──
    if stage == "ASK_FAMILY":
        # Check action from interactive district list click
        if action.startswith("dist_"):
            dist_key = action.replace("dist_", "")
            for d in TN_DISTRICTS:
                if d[0] == dist_key:
                    session["district"] = d[1]
                    break
        else:
            # Check typed district name against all 38 TN districts
            lower_t = text.lower()
            for d in TN_DISTRICTS:
                if d[0] in lower_t or d[1].lower() in lower_t or (len(d) > 2 and d[2].lower() in lower_t):
                    session["district"] = d[1]
                    break

        # If user re-sends a 4-digit PIN while in this stage
        stripped = text.strip()
        if len(stripped) == 4 and stripped.isdigit():
            session["pin"] = stripped

        members = 4
        if action == "fam_2":
            members = 2
        elif action == "fam_4":
            members = 4
        elif action == "fam_6":
            members = 6
        else:
            nums = [int(s) for s in text.split() if s.isdigit() and len(s) <= 2]
            if nums:
                members = min(max(nums[0], 1), 20)

        name = session.get("name", "குடிமகன்")
        pin = session.get("pin", "7890")
        district = session.get("district", "Madurai")

        # Register the user
        user_data = register_new_user(
            phone=clean_phone, name=name, pin=pin,
            district=district, family_members_count=members
        )
        ONBOARDING_STAGES.pop(clean_phone, None)

        # Generate magic link
        auth_token = create_magic_auth_token(phone=clean_phone, secret_pin=pin)
        magic_url = f"{base_url}/auth/magic?token={auth_token['token']}&phone={clean_phone}"

        msgs = [
            _msg_text(
                f"🎉 *வாழ்த்துக்கள்! பதிவு வெற்றி!*\n"
                f"Congratulations! Registration complete! ✅\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"👤 *பெயர்:* {name}\n"
                f"📱 *மொபைல்:* +91 {clean_phone}\n"
                f"🔐 *PIN:* {pin}\n"
                f"📍 *மாவட்டம்:* {district}\n"
                f"👨‍👩‍👧‍👦 *குடும்பம்:* {members} பேர்\n\n"
                f"🧠 *SIA 3D Dashboard திறக்க:*\n"
                f"👉 {magic_url}\n\n"
                f"⏱️ இணைப்பு 15 நிமிடம் செல்லும்\n"
                f"🔒 முடித்ததும் *CLOSE* அனுப்பவும்"
            ),
            _build_service_menu()
        ]
        return _result(msgs, stage="COMPLETED", magic_url=magic_url, user=user_data)

    # Unknown stage – reset
    ONBOARDING_STAGES.pop(clean_phone, None)
    return _send_welcome(clean_phone)


# ══════════════════════════════════════════════════════════════════════════════
# Service action handler
# ══════════════════════════════════════════════════════════════════════════════

def _handle_service_action(
    clean_phone: str, action: str, base_url: str
) -> Dict[str, Any]:
    """Handle service-menu item selections."""
    from whatsapp_auth_manager import create_magic_auth_token, terminate_session_by_whatsapp

    user = get_user_profile(clean_phone)
    name = user.get("name", "நண்பரே") if user else "நண்பரே"

    if action == "svc_logout":
        term_res = terminate_session_by_whatsapp(clean_phone)
        return _result([
            _msg_buttons(
                header="🔒 அமர்வு மூடப்பட்டது",
                body=(
                    f"வணக்கம் *{name}*!\n\n"
                    "உங்கள் SIA இணைய அமர்வு பாதுகாப்பாக மூடப்பட்டது ✅\n"
                    "Your SIA web session has been securely terminated.\n\n"
                    "மீண்டும் பயன்படுத்த Hi SIA அனுப்பவும் 👋"
                ),
                buttons=[
                    {"id": "btn_login",    "title": "🔑 மீண்டும் நுழை"},
                    {"id": "btn_help",     "title": "❓ உதவி"},
                ],
            )
        ], stage="LOGGED_OUT")

    if action == "svc_dash":
        auth_token = create_magic_auth_token(phone=clean_phone, secret_pin=user.get("pin", "7890") if user else "7890")
        magic_url = f"{base_url}/auth/magic?token={auth_token['token']}&phone={clean_phone}"
        return _result([
            _msg_text(
                f"🧠 *SIA 3D Neural Dashboard*\n\n"
                f"👉 {magic_url}\n\n"
                f"3D Neural Brain 🧠 | Heartbeat EKG 💓 | AI Companion 🗣️\n"
                f"⏱️ 15 நிமிட இணைப்பு"
            ),
            _msg_buttons(
                body="வேறு சேவை தேவையா?\nNeed another service?",
                buttons=[
                    {"id": "btn_services", "title": "📋 சேவைகள்"},
                    {"id": "svc_logout",   "title": "🔒 வெளியேறு"},
                ],
            )
        ], stage="DASHBOARD_SENT", magic_url=magic_url)

    if action == "svc_vault":
        proofs = user.get("proofs_vault", []) if user else []
        doc_lines = []
        for p in proofs:
            status_icon = "✅" if p.get("status") in ("VERIFIED", "ACTIVE", "AUDITED") else "⏳"
            doc_lines.append(f"{status_icon} *{p.get('doc_name_ta', p.get('doc_type'))}*\n   எண்: {p.get('doc_number')} | {p.get('verified_by')}")
        docs_text = "\n".join(doc_lines) if doc_lines else "ஆவணங்கள் இல்லை"
        return _result([
            _msg_text(
                f"📄 *{name} - ஆவண பெட்டகம்*\n"
                f"Document Vault\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{docs_text}\n\n"
                f"📸 புதிய ஆவணத்தின் புகைப்படம் அனுப்பினால்\n"
                f"AI தானாக சரிபார்த்து சேர்க்கும்!\n\n"
                f"Send a photo of any document to add it"
            ),
            _msg_buttons(
                body="வேறு சேவை?",
                buttons=[{"id": "btn_services", "title": "📋 சேவைகள்"}],
            )
        ], stage="VAULT_SHOWN")

    # ── Generic service responses ──
    service_map = {
        "svc_land": (
            "🏠 *நிலம் & சொத்து சேவைகள்*\nLand & Property Services",
            "• பட்டா பெயர் மாற்றம் (₹60 மட்டுமே!)\n• சிட்டா / FMB நகல்\n• நில அளவீடு கோரிக்கை\n• EC சான்று\n\n"
            "📸 உங்கள் நில ஆவணத்தின் புகைப்படம் அனுப்பினால் AI ஆய்வு செய்யும்!\n"
            "Send a photo of your land document for AI analysis",
        ),
        "svc_ration": (
            "📋 *ரேஷன் அட்டை சேவை*\nSmart Ration Card",
            "• புதிய அட்டை விண்ணப்பம் (₹0 கட்டணம்)\n• பெயர் சேர்ப்பு / நீக்கம்\n• முகவரி மாற்றம்\n• அட்டை வகை மாற்றம்\n\n"
            "🚫 இடைத்தரகர்களிடம் ₹500-₹3000 கொடுக்க வேண்டாம்!\nDon't pay brokers!",
        ),
        "svc_aadhaar": (
            "🪪 *ஆதார் அட்டை சேவை*\nAadhaar Card",
            "• முகவரி மாற்றம் (₹50 மட்டுமே)\n• பெயர் திருத்தம்\n• மொபைல் எண் புதுப்பிப்பு\n\n"
            "🌐 myaadhaar.uidai.gov.in",
        ),
        "svc_agri": (
            "🌾 *வேளாண்மை ஆலோசனை*\nAgriculture Advisory",
            "📸 *பயிர் இலை AI ஆய்வு:*\nஉங்கள் பாதிக்கப்பட்ட பயிர் இலையின் புகைப்படம் அனுப்பினால் Meta SAM 3.1 AI நோய் கண்டறியும்!\n\n"
            "💰 *அரசு திட்டங்கள்:*\n• PM-KISAN: ₹6,000/ஆண்டு\n• சோலார் பம்ப் 70% மானியம்\n• பயிர் காப்பீடு PMFBY\n\n"
            "Send a photo of your crop leaf for AI diagnosis 🌿",
        ),
        "svc_edu": (
            "📚 *கல்வி உதவி*\nEducation Assistant",
            "• சமச்சீர் கல்வி (1-12) பாட உதவி\n• NEET UG வழிகாட்டி\n• TNPSC குரூப் 4 தயாரிப்பு\n• SWAYAM இலவச படிப்பு\n\n"
            "📖 உங்கள் கேள்வியை அனுப்பவும்\nSend your question!",
        ),
        "svc_health": (
            "💊 *மருத்துவ காப்பீடு*\nHealth Insurance",
            "• CMCHIS: ₹5 லட்சம் இலவச மருத்துவம்\n• PMJAY: ₹5 லட்சம் கூடுதல்\n• இலவச மருந்தகம்: Amma Pharmacy\n\n"
            "📋 காப்பீடு தகுதி சரிபார்க்க உங்கள் ரேஷன் அட்டை எண் அனுப்பவும்",
        ),
        "svc_rti": (
            "📝 *RTI தகவல் அறியும் உரிமை மனு*\nRight to Information",
            "• கட்டணம்: ₹10 மட்டுமே (BPL: ₹0)\n• 30 நாள் பதில் கட்டாயம்\n• அரசு செலவு, டெண்டர் விவரம் கேட்கலாம்\n\n"
            "📄 உங்கள் RTI மனுவை 1-கிளிக்கில் உருவாக்க Dashboard-ஐ திறக்கவும்",
        ),
        "svc_mla": (
            "🗳️ *MLA / MP மக்கள் கோரிக்கை மனு*\nPeople's Petition",
            "• 100% இலவசம் (₹0)\n• சாலை, குடிநீர், மின்சாரம்\n• பள்ளி, மருத்துவமனை\n• புதிய பேருந்து / ரயில் நிறுத்தம்\n\n"
            "📄 1-கிளிக்கில் மனு உருவாக்க Dashboard-ஐ திறக்கவும்",
        ),
    }

    if action in service_map:
        title, details = service_map[action]
        return _result([
            _msg_text(f"{title}\n━━━━━━━━━━━━━━━━━━━━\n\n{details}"),
            _msg_buttons(
                body="வேறு சேவை தேவையா?\nNeed another service?",
                buttons=[
                    {"id": "btn_services", "title": "📋 சேவைகள்"},
                    {"id": "svc_dash",     "title": "🧠 Dashboard"},
                    {"id": "svc_logout",   "title": "🔒 வெளியேறு"},
                ],
            )
        ], stage="SERVICE_DETAIL")

    # Fallback
    return _result([_build_service_menu()], stage="SERVICE_MENU")


# ══════════════════════════════════════════════════════════════════════════════
# Result builder
# ══════════════════════════════════════════════════════════════════════════════

def _result(messages: List[Dict[str, Any]], stage: str = "", **extra) -> Dict[str, Any]:
    """Standard return envelope."""
    return {
        "messages": messages,
        "reply": _plain_text_fallback(messages),
        "stage": stage,
        **extra,
    }
