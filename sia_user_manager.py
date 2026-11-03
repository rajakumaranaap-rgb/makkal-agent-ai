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

from sia_admin_and_menu_engine import (
    is_super_admin,
    get_super_admin_response,
    get_menu_guide_response,
    get_simplified_pictorial_menu,
    get_inactivity_nudge,
    get_admin_login_prompt,
    get_language_picker_prompt,
    sanitize_whatsapp_text,
    SUPER_ADMIN_PHONES
)

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

                "title": "🌾 வேளாண், கல்வி & பயணம்",

                "rows": [

                    {"id": "svc_agri",    "title": "🌾 வேளாண்மை & மானியம்", "description": "TNAU உரம், SAM 3.1 நோய், 100% பாசனம்"},

                    {"id": "svc_edu",     "title": "📚 10th டியூஷன் & கல்வி", "description": "CBSE/சமச்சீர் வீட்டுப்பாடம் & அட்டவணை"},

                    {"id": "svc_travel",  "title": "🚖 RedTaxi & சுற்றுலா",  "description": "0% Surge டாக்ஸி, ராமேஸ்வரம் யாத்திரை"},

                    {"id": "svc_health",  "title": "💊 மருத்துவ காப்பீடு",  "description": "CMCHIS அரசு மருத்துவ காப்பீடு"},

                ]

            },

            {

                "title": "🔧 கணக்கு & Dashboard",

                "rows": [

                    {"id": "svc_vault",   "title": "📄 ஆவண பெட்டகம்",     "description": "சான்றிதழ்கள் பாதுகாப்பு சேமிப்பு"},

                    {"id": "svc_dash",    "title": "🧠 3D Dashboard",       "description": "SIA Super Intelligence Portal"},

                    {"id": "svc_logout",  "title": "🔒 வெளியேறு",          "description": "பாதுகாப்பாக Session முடக்கு"},

                ]

            }

        ]

    )

def get_user_language(clean_phone: str) -> str:
    """Returns preferred language: 'ta' (Tamil script) or 'en' (English). Defaults to 'ta' on WhatsApp."""
    clean = _clean_phone(clean_phone)
    sess = ONBOARDING_STAGES.get(clean, {})
    if sess.get("language"):
        return sess["language"]
    user = get_user_profile(clean)
    if user and user.get("language"):
        return user["language"]
    return "ta"

def set_user_language(clean_phone: str, lang: str):
    """Saves language preference in-memory and in persistent user registry."""
    clean = _clean_phone(clean_phone)
    if clean in ONBOARDING_STAGES:
        ONBOARDING_STAGES[clean]["language"] = lang
    reg = load_registry()
    if clean in reg.get("users", {}):
        reg["users"][clean]["language"] = lang
        save_registry(reg)

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

    if session:
        return _handle_onboarding_step(clean_phone, text, action, session, public_base_url)

    # ────────────────────────────────────────────────────────────────────────
    #  LANGUAGE SWITCH COMMANDS ('EN', 'ENGLISH', 'TAMIL', 'தமிழ்')
    # ────────────────────────────────────────────────────────────────────────
    if action in ["LANG_EN", "EN", "ENGLISH"] or upper in ["EN", "ENGLISH", "LANG EN"]:
        set_user_language(clean_phone, "en")
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "Citizen") if u_prof else "Citizen"
        menu = get_simplified_pictorial_menu(u_name, lang="en")
        return _result([
            _msg_buttons(
                header="🇬🇧 Language Set to English",
                body=(
                    "Language set to English successfully! ✅\n\n"
                    + menu["body"]
                ),
                buttons=menu["buttons"],
                footer=menu["footer"]
            )
        ], stage="LANGUAGE_CHANGED_EN")

    if action in ["LANG_TA", "TAMIL", "தமிழ்"] or upper in ["TAMIL", "தமிழ்", "LANG TA", "TM"]:
        set_user_language(clean_phone, "ta")
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "நண்பரே") if u_prof else "நண்பரே"
        menu = get_simplified_pictorial_menu(u_name, lang="ta")
        return _result([
            _msg_buttons(
                header="🇮🇳 மொழி தமிழுக்கு மாற்றப்பட்டது",
                body=(
                    "மொழி தமிழ் வரிவடிவிற்கு வெற்றிகரமாக மாற்றப்பட்டது! ✅\n\n"
                    + menu["body"]
                ),
                buttons=menu["buttons"],
                footer=menu["footer"]
            )
        ], stage="LANGUAGE_CHANGED_TA")

    # ────────────────────────────────────────────────────────────────────────
    #  SUPER ADMIN COMMAND INTERCEPTOR (Phone: 9486335870 or PIN 7890)
    # ────────────────────────────────────────────────────────────────────────
    if action in ["ADMIN", "நிர்வாகம்", "அட்மின்", "ADMIN MENU", "ADMIN PANEL", "SUPER ADMIN"] or action.startswith("admin_"):
        if is_super_admin(clean_phone):
            admin_data = get_super_admin_response(action, public_base_url)
            return _result([
                _msg_buttons(
                    header=admin_data["header"],
                    body=admin_data["body"],
                    buttons=admin_data["buttons"],
                    footer=admin_data["footer"]
                )
            ], stage="SUPER_ADMIN_COCKPIT", magic_url=admin_data.get("magic_url"))
        else:
            lang = get_user_language(clean_phone)
            prompt = get_admin_login_prompt(lang)
            return _result([
                _msg_buttons(
                    header=prompt["header"],
                    body=prompt["body"],
                    buttons=prompt["buttons"],
                    footer=prompt["footer"]
                )
            ], stage="ADMIN_AUTH_PROMPT")

    if action.lower() in ["btn_admin_pin_7890", "admin_pin_7890"]:
        admin_data = get_super_admin_response("admin", public_base_url)
        return _result([
            _msg_buttons(
                header=admin_data["header"],
                body=admin_data["body"],
                buttons=admin_data["buttons"],
                footer=admin_data["footer"]
            )
        ], stage="SUPER_ADMIN_COCKPIT", magic_url=admin_data.get("magic_url"))

    # ────────────────────────────────────────────────────────────────────────
    #  INACTIVITY NUDGE & RE-ENGAGEMENT HANDLERS (Judging Mode)
    # ────────────────────────────────────────────────────────────────────────
    if action.lower() in ["btn_nudge_wait", "wait", "waiting", "காத்திரு", "wait 2m"] or upper in ["WAIT", "WAITING", "காத்திரு"]:
        lang = get_user_language(clean_phone)
        wait_text = (
            "✅ All right! I will gladly wait for you. Send a message anytime whenever you are ready to continue! 🙏"
            if lang == "en" else
            "✅ சரிங்க! தங்களின் வசதிக்கேற்ப காத்திருக்கிறேன். தொடர விரும்பும்போது எப்போது வேண்டுமானாலும் செய்தி அனுப்பலாம் அல்லது கீழே உள்ள மெனுவைத் தேர்ந்தெடுக்கலாம்! 🙏"
        )
        return _result([
            _msg_buttons(
                header="⏳ SIA காத்திருக்கிறது (Waiting)" if lang == "ta" else "⏳ SIA Waiting",
                body=wait_text,
                buttons=[
                    {"id": "btn_nudge_menu", "title": "🔄 முதன்மை மெனு" if lang == "ta" else "🔄 Restart Menu"},
                    {"id": "btn_nudge_close", "title": "🔒 அமர்வை முடிக்க" if lang == "ta" else "🔒 Close Session"},
                ],
                footer="SIA • Citizen First Care"
            )
        ], stage="NUDGE_WAITING")

    if action.lower() in ["btn_nudge_menu", "btn_menu_all_list", "restart_menu", "மீண்டும் தொடங்கு", "முதன்மை மெனு"] or upper in ["RESTART", "RESTART MENU", "RESET MENU", "முதன்மை மெனு"]:
        return _send_welcome(clean_phone)

    if action.lower() in ["btn_nudge_close", "close_session", "முடிக்க", "வெளியேறு"] or upper in ["CLOSE", "QUIT", "EXIT", "முடிக்க"]:
        from whatsapp_auth_manager import terminate_session_by_whatsapp
        try:
            terminate_session_by_whatsapp(clean_phone)
        except Exception:
            pass
        lang = get_user_language(clean_phone)
        close_text = (
            "🔒 *SIA Session Concluded (Closed)*\n\nYour session has been safely saved and closed. Send *Hi SIA* or *வணக்கம்* anytime to start again! 🙏"
            if lang == "en" else
            "🔒 *SIA அமர்வு நிறைவுற்றது (Session Closed)*\n\nவணக்கம்! உங்கள் அமர்வு வெற்றிகரமாக நிறைவுபெற்று பாதுகாப்பாக மூடப்பட்டது. மீண்டும் தொடர்பு கொள்ள எப்போது வேண்டுமானாலும் *Hi SIA* அல்லது *வணக்கம்* என அனுப்பலாம்! 🙏"
        )
        return _result([
            _msg_buttons(
                header="🔒 அமர்வு நிறைவுற்றது" if lang == "ta" else "🔒 Session Closed",
                body=close_text,
                buttons=[
                    {"id": "btn_nudge_menu", "title": "🌟 Hi SIA (தொடங்கு)" if lang == "ta" else "🌟 Hi SIA (Start)"},
                ],
                footer="SIA • Air-Gapped Sovereign Security"
            )
        ], stage="NUDGE_CLOSED")

    if action.lower() in ["trigger_inactivity_nudge", "nudge_inactivity", "idle_nudge"] or upper in ["IDLE", "INACTIVITY", "NUDGE"]:
        lang = get_user_language(clean_phone)
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "நண்பரே") if u_prof else "நண்பரே"
        nudge_data = get_inactivity_nudge(citizen_name=u_name, lang=lang)
        return _result([
            _msg_buttons(
                header=nudge_data["header"],
                body=nudge_data["body"],
                buttons=nudge_data["buttons"],
                footer=nudge_data["footer"]
            )
        ], stage="INACTIVITY_NUDGE")

    # ────────────────────────────────────────────────────────────────────────

    # ────────────────────────────────────────────────────────────────────────
    #  DIRECT 1-2 STEP PETITION GENERATOR & ACTIONS (Judging & Rural Illiterate Friendly)
    # ────────────────────────────────────────────────────────────────────────
    if action in [
        "btn_petition_pdf", "btn_new_petition", "btn_mla_petition", "மனு PDF", "மனு", "புதிய மனு",
        "MANU", "PETITION", "DRAFT PETITION", "DOWNLOAD PDF", "btn_pet_voice"
    ] or upper in ["மனு PDF", "மனு", "புதிய மனு", "PETITION", "MANU"]:
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "நண்பரே") if u_prof else "நண்பரே"
        lang = get_user_language(clean_phone)
        return _result([
            _msg_buttons(
                header="📜 அதிகாரப்பூர்வ மக்கள் கோரிக்கை மனு" if lang == "ta" else "📜 1-Click Official Grievance Petition",
                body=(
                    f"வணக்கம் *{u_name}*!\n\n"
                    "✍️ *எந்த பிரச்சனைக்கு மனு தயாரிக்க வேண்டும்?*\n"
                    "கீழேயுள்ள பொத்தானைத் தொடவும் அல்லது 10 விநாடி குரல் பதிவை (Voice Note) அனுப்பவும்:\n\n"
                    "• உடனடி சீல் வைக்கப்பட்ட அதிகாரப்பூர்வ PDF மனு தயாராகும்.\n"
                    "• உங்கள் தொகுதி MLA / MP-க்கு 1-கிளிக்கில் அனுப்பலாம்!"
                    if lang == "ta" else
                    f"Welcome *{u_name}*!\n\n"
                    "✍️ *What type of petition do you need?*\n"
                    "Tap a button below or send a 10-second voice note:\n\n"
                    "• Instantly generates official sealed PDF petition.\n"
                    "• 1-Click direct dispatch to your MLA/MP & Collector!"
                ),
                buttons=[
                    {"id": "btn_pet_water", "title": "💧 குடிநீர் வசதி மனு" if lang == "ta" else "💧 Drinking Water"},
                    {"id": "btn_pet_road", "title": "🛣️ சாலை & விளக்கு" if lang == "ta" else "🛣️ Road & Light"},
                    {"id": "btn_pet_pension", "title": "🏛️ முதியோர் உதவித்தொகை" if lang == "ta" else "🏛️ OAP Pension"},
                ],
                footer="SIA • 1-கிளிக் சட்டமன்ற உறுப்பினர் மனு"
            )
        ], stage="PETITION_TYPE_SELECTION")

    if action in [
        "btn_pet_water", "btn_pet_road", "btn_pet_pension", "btn_pet_patta",
        "குடிநீர் வசதி மனு", "சாலை & விளக்கு", "முதியோர் உதவித்தொகை",
        "DRINKING WATER", "ROAD & LIGHT", "OAP PENSION"
    ]:
        from mla_mp_petition_forwarder import create_and_forward_petition
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "ர. சுப்பிரமணியன்") if u_prof else "ர. சுப்பிரமணியன்"
        u_dist = u_prof.get("district", "சென்னை") if u_prof else "சென்னை"
        u_vil = u_prof.get("village", "கொளத்தூர்") if u_prof else "கொளத்தூர்"

        grievance_map = {
            "btn_pet_water": "குடிநீர் குழாய் உடைப்பு சீரமைக்க மற்றும் சீரான குடிநீர் வழங்கக் கோரும் அவசர மனு",
            "குடிநீர் வசதி மனு": "குடிநீர் குழாய் உடைப்பு சீரமைக்க மற்றும் சீரான குடிநீர் வழங்கக் கோரும் அவசர மனு",
            "btn_pet_road": "சேதமடைந்த தார்ச்சாலை சீரமைப்பு மற்றும் தெருவிளக்கு வசதி செய்யக் கோரும் அவசர மனு",
            "சாலை & விளக்கு": "சேதமடைந்த தார்ச்சாலை சீரமைப்பு மற்றும் தெருவிளக்கு வசதி செய்யக் கோரும் அவசர மனு",
            "btn_pet_pension": "முதியோர் உதவித்தொகை (OAP) வேண்டி மாவட்ட சமூகப் பாதுகாப்பு துறைக்கு விண்ணப்ப மனு",
            "முதியோர் உதவித்தொகை": "முதியோர் உதவித்தொகை (OAP) வேண்டி மாவட்ட சமூகப் பாதுகாப்பு துறைக்கு விண்ணப்ப மனு",
            "btn_pet_patta": "பட்டா மாறுதல் மற்றும் வில்லங்கச் சான்று சரிபார்ப்பு கோரும் வருவாய்த்துறை மனு",
        }
        chosen_text = grievance_map.get(action, "குடிநீர் குழாய் சீரமைப்பு மற்றும் சாலை வசதி கோரும் பொது மக்கள் மனு")

        pet_res = create_and_forward_petition(
            user_text=chosen_text,
            sender_phone=clean_phone,
            applicant_name=u_name,
            district_hint=u_dist,
            village_hint=u_vil,
            public_base_url=public_base_url
        )

        fwd_url = pet_res.get("forward_links", {}).get("whatsapp_mla_direct", "https://wa.me/919444012345")
        mla_phone = fwd_url.split("phone=")[-1].split("&")[0] if "phone=" in fwd_url else "919444012345"

        messages = []
        if pet_res.get("pdf_download_url"):
            messages.append({
                "type": "document",
                "document_url": pet_res["pdf_download_url"],
                "filename": f"SIA_Petition_{pet_res.get('tier', 'MLA')}_{pet_res.get('verification_id', 'REF')}.pdf",
                "caption": f"📄 அதிகாரப்பூர்வ மக்கள் மனு PDF ({pet_res.get('verification_id')})"
            })

        messages.append(_msg_buttons(
            header=f"✅ {pet_res.get('authority_name_ta', 'MLA')} மனு தயாராகிவிட்டது!",
            body=(
                f"• *பதிவு எண்:* `{pet_res.get('verification_id')}`\n"
                f"• *தொகுதி:* {pet_res.get('constituency_ta')} ({pet_res.get('district')} மாவட்டம்)\n"
                f"• *துறை:* {pet_res.get('category_ta')}\n"
                f"• *சட்டம்:* {pet_res.get('statute')}\n\n"
                f"📄 அதிகாரப்பூர்வ PDF மனு உங்கள் வாட்ஸ்அப்பில் பதிவேற்றப்பட்டுள்ளது!\n\n"
                f"👉 MLA வாட்ஸ்அப்பிற்கு அனுப்ப: wa.me/{mla_phone}"
            ),
            buttons=[
                {"id": "btn_petition_pdf", "title": "✍️ புதிய மனு"},
                {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
            ],
            footer="SIA • அதிகாரப்பூர்வ மக்கள் மனு"
        ))
        return _result(messages, stage="PETITION_GENERATED_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 1: CROP DISEASE DIRECT CURE ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_crop_blast_cure", "btn_crop_pest", "பூச்சி மருத்துவம்", "குலைநோய்"]:
        return _result([
            _msg_buttons(
                header="✅ நெல் குலைநோய் (Paddy Blast) TNAU இயற்கை மருந்து",
                body=(
                    "1. *சூடோமோனாஸ் ஃப்ளோரசன்ஸ்:* 2.5 கிராம்/லிட்டர் நீரில் கலந்து காலை/மாலை தெளிக்கவும்.\n"
                    "2. *யூரியா உரம்:* தற்காலிகமாக நைட்ரஜன் உரம் இடுவதை நிறுத்தவும்.\n"
                    "3. *செலவு:* ₹80 மட்டுமே (இரசாயன பூச்சிக்கொல்லி ₹1,500 மிச்சம்)!\n\n"
                    "📸 உங்கள் பயிர் இலையை படம் பிடித்து அனுப்பினால் SAM 3.1 விஷன் உடனே பரிசோதிக்கும்."
                ),
                buttons=[
                    {"id": "btn_weather_rep", "title": "🌧️ வானிலை அறிக்கை"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • TNAU இயற்கை வேளாண்மை"
            )
        ], stage="AGRI_CURE_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 2: CATTLE CARE DIRECT HERBAL CURE ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_mastitis_aid", "btn_feed_plan", "மடிநோய்", "மடிநோய் முதலுதவி"]:
        if action == "btn_feed_plan":
            return _result([
                _msg_buttons(
                    header="🥛 பால் உற்பத்தி பெருக்கும் தீவன முறை (TANUVAS)",
                    body=(
                        "• *பசுந்தீவனம்:* அசோலா (Azolla) தினமும் 1 முதல் 1.5 கிலோ.\n"
                        "• *தாது உப்பு கலவை:* தினமும் 50 கிராம் தீவனத்தில் கலக்கவும்.\n"
                        "• *சுத்தமான குடிநீர்:* தாராளமாக வழங்கவும்.\n\n"
                        "📈 பால் உற்பத்தி 15% முதல் 20% வரை உடனடியாக அதிகரிக்கும்!"
                    ),
                    buttons=[
                        {"id": "btn_mastitis_aid", "title": "🩹 மடிநோய் முதலுதவி"},
                        {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                    ],
                    footer="SIA • TANUVAS பால் பெருக்க திட்டம்"
                )
            ], stage="CATTLE_FEED_DISPATCHED")
        return _result([
            _msg_buttons(
                header="🐄 மடிவீக்க நோய் அவசர முதலுதவி (TANUVAS)",
                body=(
                    "1. சோற்றுக் கற்றாழை 250g + மஞ்சள் தூள் 60g + வெற்றிலை சுண்ணாம்பு 15g.\n"
                    "2. மிக்சியில் விழுதாக அரைத்து மடியில் தினமும் 4-5 முறை பூசவும்.\n"
                    "3. 24 மணிநேரத்தில் வீக்கம் முற்றிலும் குணமாகும்!\n\n"
                    "செலவு: ₹20 மட்டுமே (தனியார் டாக்டர் கட்டணம் ₹2,000 மிச்சம்)!"
                ),
                buttons=[
                    {"id": "btn_feed_plan", "title": "🥛 பால் பெருக்க தீவனம்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • TANUVAS கால்நடை முதலுதவி"
            )
        ], stage="CATTLE_MASTITIS_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 3: VYABAR LOCAL STORE 1-TAP ORDER ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["store_order", "btn_vyabar_quick_order", "மளிகை ஆர்டர்"]:
        return _result([
            _msg_buttons(
                header="✅ மளிகை ஆர்டர் உறுதி செய்யப்பட்டது!",
                body=(
                    "• *கடை:* சோழவந்தான் முருகன் ஸ்டோர்ஸ்\n"
                    "• *பொருட்கள்:* பொன்னி அரிசி 10kg + துவரம் பருப்பு 1kg\n"
                    "• *மொத்தத் தொகை:* ₹780 (0% கமிஷன், நேரடி கடை விலையே)\n"
                    "• *டெலிவரி:* அடுத்த 30 நிமிடங்களில் உங்கள் வீடு தேடி வரும்!\n"
                    "• *டெலிவரி OTP:* *4182*"
                ),
                buttons=[
                    {"id": "btn_vyabar_status", "title": "📦 ஆர்டர் நிலை"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • 100% உள்ளூர் வணிகம்"
            )
        ], stage="VYABAR_ORDER_CONFIRMED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 4: REDTAXI 1-TAP DISPATCH ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_book_taxi", "btn_taxi_instant_book", "ஆட்டோ புக் செய்"]:
        return _result([
            _msg_buttons(
                header="✅ ஆட்டோ முன்பதிவு உறுதியானது!",
                body=(
                    "• *ஓட்டுநர்:* S. வேலு (SIA சரிபார்க்கப்பட்ட ஓட்டுநர்)\n"
                    "• *வாகனம்:* TN 58 AZ 3522 (பஜாஜ் ஆட்டோ)\n"
                    "• *உங்கள் புறப்படும் OTP:* *6395*\n"
                    "• *கட்டணம்:* அரசு நிர்ணய கட்டணம் ₹12/கி.மீ (Rule 108)\n"
                    "• *பாதுகாப்பு:* தமிழ்நாடு காவல்துறை 112 SOS நேரடி கண்காணிப்பில் உள்ளது."
                ),
                buttons=[
                    {"id": "btn_taxi_sos", "title": "🚨 112 அவசர SOS"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • பாதுகாப்பான பயணம்"
            )
        ], stage="TAXI_BOOKING_CONFIRMED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 5: COMMUNITY KITCHEN 1-TAP ORDER ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["food_order", "btn_food_quick_order", "btn_food_meals", "btn_food_tiffin"]:
        return _result([
            _msg_buttons(
                header="🍱 வாழை இலை சாப்பாடு உறுதி செய்யப்பட்டது!",
                body=(
                    "• *உணவகம்:* அன்னலட்சுமி மகளிர் சுயஉதவிக் குழு சமையல்\n"
                    "• *விலை:* ₹60 மட்டுமே (0% கமிஷன்)\n"
                    "• *டெலிவரி:* அடுத்த 20 நிமிடங்களில் சுடச்சுட வரும்!\n"
                    "• *ஓட்டுநர்:* குமார் (OTP: *5821*)"
                ),
                buttons=[
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • மகளிர் சமுதாய சமையல்"
            )
        ], stage="FOOD_MEALS_CONFIRMED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 6: PATTA QUICK AUDIT ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_patta_quick_survey", "svc_patta", "btn_patta_audit_action"]:
        return _result([
            _msg_buttons(
                header="📑 பட்டா நில ஆவண ஆய்வு முடிவு (RSO 31)",
                body=(
                    "• *சர்வே எண்:* 142/3A (சோழவந்தான் கிராமம்)\n"
                    "• *அசோகா முத்திரை & சீல்:* 100% அதிகாரப்பூர்வமானது ✅\n"
                    "• *அரசு நிர்ணய கட்டணம்:* உட்பிரிவு ₹60 மட்டுமே!\n"
                    "• *எச்சரிக்கை:* இடைத்தரகர்களுக்கு ₹3,000-₹5,000 கொடுக்க வேண்டாம்."
                ),
                buttons=[
                    {"id": "btn_pet_water", "title": "📄 பட்டா பெயர் மாற்ற மனு"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • நில ஆவண பாதுகாப்பு"
            )
        ], stage="PATTA_SURVEY_AUDITED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 7: CBT QUIZ 1-TAP LAUNCH ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_quiz_start_now", "btn_cbt_quiz"]:
        return _result([
            _msg_buttons(
                header="🎯 TNPSC குரூப் 4 மாதிரி தேர்வு (கேள்வி 1/5)",
                body=(
                    "❓ *'அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு'*\n"
                    "இதில் பயின்று வரும் அணி எது?\n\n"
                    "சரியான விடையைத் தேர்ந்தெடுக்கவும்:"
                ),
                buttons=[
                    {"id": "btn_quiz_opt_b", "title": "B) எடுத்துக்காட்டு உவமை"},
                    {"id": "btn_quiz_opt_a", "title": "A) உவமை அணி"},
                    {"id": "btn_quiz_opt_c", "title": "C) பிறிது மொழிதல் அணி"}
                ],
                footer="SIA • சமச்சீர் கல்வி தேர்வு கூடம்"
            )
        ], stage="CBT_QUESTION_1")

    if action == "btn_quiz_opt_b":
        return _result([
            _msg_buttons(
                header="🎉 சரியான விடை! (Grade: A+)",
                body=(
                    "✅ *அருமை! 'எடுத்துக்காட்டு உவமை அணி' என்பது மிகச் சரியான விடை.*\n\n"
                    "விளக்கம்: உவமையும் உவமேயமும் தனித்தனி வாக்கியங்களாக அமைந்து உவம உருபு மறைந்து வருவது எடுத்துக்காட்டு உவமை அணி ஆகும்."
                ),
                buttons=[
                    {"id": "btn_quiz_start_now", "title": "➡️ அடுத்த கேள்வி"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • டிஜிட்டல் கல்வி"
            )
        ], stage="CBT_QUESTION_CORRECT")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 10: 4-7-8 CALMING BREATHING ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_mh_breathe", "btn_calm_breath"]:
        return _result([
            _msg_buttons(
                header="🌬️ 4-7-8 மன அமைதி மூச்சுப் பயிற்சி",
                body=(
                    "1. 4 விநாடிகள் மூச்சை உள்ளே இழுக்கவும்... 🫁\n"
                    "2. 7 விநாடிகள் மூச்சை அடக்கவும்... ⏱️\n"
                    "3. 8 விநாடிகள் மெதுவாக மூச்சை வெளியேற்றவும்... 🍃\n\n"
                    "3 முறை இதைச் செய்யவும். உங்கள் பதற்றம் தணிந்து அமைதி கிடைக்கும்!\n"
                    "📞 இலவச ஆலோசனைக்கு: *14416* (Tele-MANAS தமிழ்நாடு அரசு 24/7)"
                ),
                buttons=[
                    {"id": "btn_call_14416", "title": "📞 14416 அழைப்பு"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • Tele-MANAS அரசு மனநல மையம்"
            )
        ], stage="MH_BREATHING_GUIDED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 1: WEATHER & MACHINERY REDIRECT ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_weather_rep", "வானிலை அறிக்கை", "வானிலை", "மழை", "WEATHER"]:
        return _result([
            _msg_buttons(
                header="🌧️ 3-நாள் உள்ளூர் வானிலை அறிக்கை (TNAU Agro-Met)",
                body=(
                    "• *வானிலை முன்னறிவிப்பு:* அடுத்த 48 மணிநேரத்தில் மிதமான மழை வாய்ப்பு (65%).\n"
                    "• *விவசாய ஆலோசனை:* யூரியா/இலைவழி உரம் தெளிப்பதை 2 நாட்களுக்கு தள்ளிவைக்கவும்.\n"
                    "• *வடிகால் வசதி:* வயலில் தேங்கும் அதிகப்படியான மழைநீரை வெளியேற்ற வாய்க்கால்களை தூர்வாரவும்.\n"
                    "• *காற்று வேகம்:* மணிக்கு 14 கி.மீ (இயல்பான அளவு).\n\n"
                    "📸 உங்கள் பயிர் இலையை படம் பிடித்து அனுப்பினால் SAM 3.1 விஷன் உடனே பரிசோதிக்கும்."
                ),
                buttons=[
                    {"id": "btn_crop_blast_cure", "title": "🌾 பூச்சி மருந்து"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • TNAU பயிர் வானிலை மையம்"
            )
        ], stage="AGRI_WEATHER_REPORT")

    if action in ["btn_machinery_rent", "btn_rent_agri", "menu_agri_rent", "வாடகை இயந்திரங்கள்"]:
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "நண்பரே") if u_prof else "நண்பரே"
        lang = get_user_language(clean_phone)
        guide_data = get_menu_guide_response("12", citizen_name=u_name, lang=lang)
        if guide_data:
            return _result([
                _msg_buttons(
                    header=guide_data["header"],
                    body=guide_data["body"],
                    buttons=guide_data["buttons"],
                    footer=guide_data["footer"]
                )
            ], stage="MENU_GUIDE_12")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 2: VET DOCTOR ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_cattle_vet", "கால்நடை மருத்துவர்", "டாக்டர்", "VET"]:
        return _result([
            _msg_buttons(
                header="🩺 அரசு கால்நடை மருத்துவமனை (சோழவந்தான்)",
                body=(
                    "• *மருத்துவர்:* Dr. K. செந்தில்குமார், B.V.Sc (கால்நடை உதவி மருத்துவர்)\n"
                    "• *தொலைபேசி:* 0452-2589012 / 94431 22890\n"
                    "• *முகவரி:* அரசு கால்நடை மருந்தகம், மெயின் ரோடு, சோழவந்தான்.\n"
                    "• *இலவச சேவைகள்:* மடிநோய் தீவிர சிகிச்சை, சினை ஊசி, கோமாரி நோய் தடுப்பூசி முகாம் (காலை 8 முதல் 12 வரை).\n\n"
                    "அவசர முதலுதவிக்கு கீழே உள்ள பொத்தானைத் தொடவும் 👇"
                ),
                buttons=[
                    {"id": "btn_mastitis_aid", "title": "🩹 மடிநோய் முதலுதவி"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • அரசு கால்நடை உதவி மையம்"
            )
        ], stage="CATTLE_VET_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 3: VYABAR STATUS & MANDI PRICES ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["mandi_rates", "btn_mandi_prices", "store_deals", "மண்டி விலை", "உழவர் சந்தை"]:
        return _result([
            _msg_buttons(
                header="📊 உழவர் சந்தை நேரடி விலை நிலவரம்",
                body=(
                    "• *தக்காளி (நாட்டு):* ₹28 / கிலோ\n"
                    "• *சின்ன வெங்காயம்:* ₹45 / கிலோ\n"
                    "• *உருளைக்கிழங்கு:* ₹32 / கிலோ\n"
                    "• *பச்சை மிளகாய்:* ₹35 / கிலோ\n"
                    "• *தேங்காய்:* ₹18 / காய்\n\n"
                    "🌾 100% நேரடி உழவர் விற்பனை - இடைத்தரகர் கமிஷன் இல்லை!"
                ),
                buttons=[
                    {"id": "store_order", "title": "🛒 மளிகை ஆர்டர்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • உழவர் சந்தை நேரடி விலை"
            )
        ], stage="VYABAR_MANDI_PRICES")

    if action in ["btn_vyabar_status", "ஆர்டர் நிலை"]:
        return _result([
            _msg_buttons(
                header="📦 மளிகை ஆர்டர் நிலை (#VY-9042)",
                body=(
                    "• *நிலை:* டெலிவரிக்கு புறப்பட்டுவிட்டது (Out for Delivery)\n"
                    "• *கடை:* சோழவந்தான் முருகன் ஸ்டோர்ஸ்\n"
                    "• *டெலிவரி பார்ட்னர்:* வினோத் (Ph: 98421 11029)\n"
                    "• *வருகை நேரம்:* அடுத்த 8 நிமிடங்கள்\n"
                    "• *டெலிவரி ரகசிய OTP:* *4182*"
                ),
                buttons=[
                    {"id": "store_order", "title": "🛒 புதிய ஆர்டர்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • உள்ளூர் நேரடி டெலிவரி"
            )
        ], stage="VYABAR_ORDER_STATUS")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 4: REDTAXI AUTO / SEDAN, STATUS & RATES ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in [
        "btn_taxi_auto", "btn_taxi_sedan", "redtaxi_book", "btn_taxi_book_now",
        "btn_book_taxi", "btn_taxi_instant_book", "ஆட்டோ புக்", "கார் புக்", "சவாரி புக்"
    ]:
        is_sedan = action in ["btn_taxi_sedan", "கார் புக்"]
        driver_name = "M. கார்த்திக்" if is_sedan else "S. வேலு"
        vehicle = "ஸ்விஃப்ட் டிசையர் (TN 58 CA 7721)" if is_sedan else "பஜாஜ் மேக்ஸிமா ஆட்டோ (TN 58 AB 4092)"
        rate = "₹14 / கிமீ" if is_sedan else "₹12 / கிமீ"
        otp = "8124" if is_sedan else "6395"
        eta = "5 நிமிடங்கள்" if is_sedan else "3 நிமிடங்கள்"

        return _result([
            _msg_buttons(
                header=f"✅ {'கார்' if is_sedan else 'ஆட்டோ'} முன்பதிவு உறுதியானது!",
                body=(
                    f"• *ஓட்டுநர்:* {driver_name} (SIA சரிபார்க்கப்பட்ட ஓட்டுநர்)\n"
                    f"• *வாகனம்:* {vehicle}\n"
                    f"• *வருகை நேரம்:* {eta}\n"
                    f"• *சவாரி தொடக்க OTP:* *{otp}*\n"
                    f"• *கட்டணம்:* {rate} (0% கமிஷன், இரவு நேர கூடுதல் கட்டணம் இல்லை)!\n\n"
                    "ஓட்டுநர் தங்களை அழைக்கிறார். இனிய பயணம் அமையட்டும்!"
                ),
                buttons=[
                    {"id": "btn_taxi_rates", "title": "💰 கட்டண விவரம்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • ரெட் டாக்ஸி மக்கள் சேவை"
            )
        ], stage="REDTAXI_DISPATCHED")

    if action in ["redtaxi_status", "டாக்ஸி நிலை"]:
        return _result([
            _msg_buttons(
                header="🚖 ரெட் டாக்ஸி சவாரி நிலை",
                body=(
                    "• *சவாரி நிலை:* ஓட்டுநர் ச. வேலு தங்களை நோக்கி வந்துகொண்டிருக்கிறார்.\n"
                    "• *வருகை நேரம்:* 2 நிமிடங்கள்\n"
                    "• *வாகனம்:* பஜாஜ் ஆட்டோ (TN 58 AB 4092)\n"
                    "• *சவாரி தொடக்க OTP:* *6395*"
                ),
                buttons=[
                    {"id": "btn_taxi_auto", "title": "🛺 புதிய சவாரி"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • ரெட் டாக்ஸி நேரடி கண்காணிப்பு"
            )
        ], stage="REDTAXI_STATUS")

    if action in ["btn_taxi_rates", "redtaxi_rates", "டாக்ஸி கட்டணம்"]:
        return _result([
            _msg_buttons(
                header="💰 ரெட் டாக்ஸி வெளிப்படையான கட்டண விவரம்",
                body=(
                    "• *பஜாஜ் ஆட்டோ:* குறைந்தபட்சம் ₹40 (முதல் 1.8 கிமீ), பின் *₹12 / கிமீ*\n"
                    "• *மினி கார்:* குறைந்தபட்சம் ₹80, பின் *₹14 / கிமீ*\n"
                    "• *செடான் கார்:* குறைந்தபட்சம் ₹110, பின் *₹16 / கிமீ*\n\n"
                    "🛡️ இரவு நேர கூடுதல் கட்டணம் இல்லை, 0% சர்ஜ் (Zero Surge Commission)!"
                ),
                buttons=[
                    {"id": "btn_taxi_auto", "title": "🛺 ஆட்டோ புக் (₹12/km)"},
                    {"id": "btn_taxi_sedan", "title": "🚗 கார் புக் (₹14/km)"}
                ],
                footer="SIA • ரெட் டாக்ஸி வெளிப்படை கட்டணம்"
            )
        ], stage="REDTAXI_RATES")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 5: COMMUNITY KITCHEN MENU & COOK REGISTRATION ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["food_menu", "மெனு கார்டு", "உணவு பட்டியல்"]:
        return _result([
            _msg_buttons(
                header="📋 சமுதாய உணவக மெனு கார்டு (இன்றைய ஸ்பெஷல்)",
                body=(
                    "• *மதிய வாழை இலை சைவ சாப்பாடு:* ₹85\n"
                    "• *நாட்டுக்கோழி பாரம்பரிய சாப்பாடு:* ₹150\n"
                    "• *மல்லிகைப் பூ இட்லி சாம்பார் (4 எண்):* ₹40\n"
                    "• *மொறுமொறு நெய் ரோஸ்ட்:* ₹50\n"
                    "• *சூடான உளுந்து வடை (2 எண்):* ₹30\n\n"
                    "🛵 மகளிர் சுயஉதவிக் குழு சமையல் - 20 நிமிட விரைவு டெலிவரி!"
                ),
                buttons=[
                    {"id": "food_order", "title": "🍲 உணவு ஆர்டர்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • மக்கள் சமுதாய உணவகம்"
            )
        ], stage="COMMUNITY_FOOD_MENU")

    if action in ["food_reg_cook", "சமையல் பதிவு"]:
        return _result([
            _msg_buttons(
                header="👩‍🍳 மகளிர் சுயஉதவிக் குழு சமையல் பதிவு",
                body=(
                    "• உங்கள் வீட்டு சமையல் மூலம் தினமும் ₹800 முதல் ₹1,500 வரை வருமானம் ஈட்டலாம்!\n"
                    "• பதிவு கட்டணம்: *₹0 (முற்றிலும் இலவசம்)*.\n"
                    "• ஆர்டர் தொகை நேரடியாக உங்கள் வங்கிக் கணக்கில் வரவு வைக்கப்படும்.\n\n"
                    "பதிவு செய்ய: உங்கள் பெயர், ஊர் மற்றும் மகளிர் குழு பெயரை அனுப்பவும்."
                ),
                buttons=[
                    {"id": "food_order", "title": "🍲 உணவு ஆர்டர்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • மகளிர் சுயதொழில் முன்னேற்றம்"
            )
        ], stage="COMMUNITY_COOK_REGISTRATION")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 6: FMB SKETCH & RATION CARD ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["svc_fmb", "FMB வரைபடம்", "புல வரைபடம்"]:
        return _result([
            _msg_buttons(
                header="🌾 FMB புல வரைபட வழிகாட்டி (Field Measurement Book)",
                body=(
                    "• *இணையதளம்:* eservices.tn.gov.in/eservicesnew/land/chitta.html\n"
                    "• *அரசுக் கட்டணம்:* *₹0 (முற்றிலும் இலவசம்)*\n"
                    "• *பதிவிறக்கும் முறை:* மாவட்டம் > வட்டம் > கிராமம் > புல எண் (Survey No) உள்ளிட்டால் அதிகாரப்பூர்வ அரசு வரைபடம் உடனடியாக கிடைக்கும்.\n\n"
                    "எல்லைத் தகராறு அல்லது அளவீடு கோரிக்கைக்கு 'மனு PDF' என தட்டவும்."
                ),
                buttons=[
                    {"id": "svc_patta", "title": "📜 பட்டா ஆய்வு"},
                    {"id": "btn_petition_pdf", "title": "✍️ மனு PDF"}
                ],
                footer="SIA • நில அளவை மற்றும் நிலவரித் திட்டம்"
            )
        ], stage="ESEVAI_FMB_GUIDE")

    if action in ["svc_ration", "ரேஷன் அட்டை", "ஸ்மார்ட் கார்டு"]:
        return _result([
            _msg_buttons(
                header="🍚 ஸ்மார்ட் ரேஷன் கார்டு சேவைகள் (TNPDS)",
                body=(
                    "• *புதிய உறுப்பினர் சேர்த்தல் / நீக்கல்:* *₹0 (முற்றிலும் இலவசம்)*\n"
                    "• *குடும்பத் தலைவர் / முகவரி மாற்றம்:* *₹0 (இலவசம்)*\n"
                    "• *அதிகாரப்பூர்வ தளம்:* tnpds.gov.in\n"
                    "• *ஒப்புதல் காலம்:* தாலுகா வட்ட வழங்கல் அலுவலரால் (TSO) 15 நாட்களில் ஒப்புதல் வழங்கப்படும்.\n\n"
                    "இடைத்தரகர்களுக்கு பணம் தர வேண்டாம்!"
                ),
                buttons=[
                    {"id": "svc_patta", "title": "📜 பட்டா ஆய்வு"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • உணவு மற்றும் நுகர்வோர் பாதுகாப்பு"
            )
        ], stage="ESEVAI_RATION_GUIDE")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 7: EDUCATION CLASS 10 & 12 NOTES & QUIZ OPTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_edu_10th", "10-ஆம் வகுப்பு"]:
        return _result([
            _msg_buttons(
                header="📚 10-ஆம் வகுப்பு சமச்சீர் பாடக்குறிப்புகள்",
                body=(
                    "• *அறிவியல்:* 100+ முக்கிய வரைபடக் கேள்விகள் & விடைக் குறிப்புகள்.\n"
                    "• *கணிதம்:* அனைத்து தேற்றங்கள், சூத்திரங்கள் & வரைபடங்கள்.\n"
                    "• *தமிழ்:* அனைத்து பாடல் வரிகள், சொல்லும் பொருளும், அணிகள்.\n"
                    "• *சமூக அறிவியல்:* தமிழ்நாடு & இந்தியா வரலாற்று வரைபடங்கள்.\n\n"
                    "அனைத்து பாடக்குறிப்புகளும் இலவசமாக வாட்ஸ்அப்பில் பதிவிறக்கத் தயார்!"
                ),
                buttons=[
                    {"id": "btn_quiz_start_now", "title": "📝 மாதிரி தேர்வு"},
                    {"id": "btn_edu_12th", "title": "🧪 12-ஆம் வகுப்பு"}
                ],
                footer="SIA • சமச்சீர் கல்வி கூடம்"
            )
        ], stage="EDU_CLASS_10_NOTES")

    if action in ["btn_edu_12th", "12-ஆம் வகுப்பு"]:
        return _result([
            _msg_buttons(
                header="🧪 12-ஆம் வகுப்பு பொதுத்தேர்வு வழிகாட்டி",
                body=(
                    "• *இயற்பியல்:* 5-மதிப்பெண் வரைபட கேள்விகள் & கணக்கீடுகள்.\n"
                    "• *வேதியியல்:* முக்கிய பெயர் வினைகள் (Name Reactions) அட்டவணை.\n"
                    "• *உயிரியல்:* தாவர மற்றும் விலங்கியல் முக்கிய வரைபடங்கள்.\n"
                    "• முந்தைய 5 ஆண்டு அரசு பொதுத்தேர்வு வினாத்தாள்கள் விடைகளுடன் கிடைக்கும்!"
                ),
                buttons=[
                    {"id": "btn_quiz_start_now", "title": "📝 மாதிரி தேர்வு"},
                    {"id": "btn_edu_10th", "title": "📚 10-ஆம் வகுப்பு"}
                ],
                footer="SIA • மேனிலை கல்வி கூடம்"
            )
        ], stage="EDU_CLASS_12_NOTES")

    if action in ["btn_quiz_opt_a", "btn_quiz_opt_c"]:
        return _result([
            _msg_buttons(
                header="ℹ️ விடை வழிகாட்டல் (Answer Guidance)",
                body=(
                    "❌ தாங்கள் தேர்ந்தெடுத்த விடை தவறானது.\n\n"
                    "✅ *சரியான விடை:* *B) எடுத்துக்காட்டு உவமை அணி*\n\n"
                    "விளக்கம்: 'அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு' குறளில், 'அகரம் எழுத்துகளுக்கு தொடக்கமாக இருப்பது போல இறைவன் உலகிற்கு தொடக்கமாக இருக்கிறார்' என்ற உவம உருபு ('போல') மறைந்து வந்துள்ளதால் இது எடுத்துக்காட்டு உவமை அணி ஆகும்."
                ),
                buttons=[
                    {"id": "btn_quiz_start_now", "title": "➡️ அடுத்த கேள்வி"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • டிஜிட்டல் கல்வி"
            )
        ], stage="CBT_QUESTION_EXPLAINED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 8: MLA DETAILS ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_mla_details", "MLA விவரம்", "சட்டமன்ற உறுப்பினர்"]:
        return _result([
            _msg_buttons(
                header="🏛️ சட்டமன்ற உறுப்பினர் அலுவலக விவரம்",
                body=(
                    "• *தொகுதி:* கொளத்தூர் (சென்னை மாவட்டம்)\n"
                    "• *சட்டமன்ற உறுப்பினர்:* மாண்புமிகு திரு. மு.க. ஸ்டாலின்\n"
                    "• *அலுவலகம்:* கொளத்தூர் சட்டமன்ற உறுப்பினர் அலுவலகம், சென்னை.\n"
                    "• *தொடர்பு எண்:* 044-25501234\n"
                    "• *அதிகாரப்பூர்வ வாட்ஸ்அப்:* +91 94863 35870\n"
                    "• *மக்கள் குறைதீர்க்கும் நாள்:* ஒவ்வொரு புதன்கிழமையும்.\n\n"
                    "உடனடி மனு தயாரிக்க கீழேயுள்ள பொத்தானைத் தொடவும் 👇"
                ),
                buttons=[
                    {"id": "btn_petition_pdf", "title": "✍️ மனு PDF"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • மக்கள் பிரதிநிதி தொடர்பு"
            )
        ], stage="MLA_DETAILS_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 9: SPOKEN ENGLISH START, INTERVIEW & VOICE COACH ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_spoken_start", "btn_spoken_eng", "உரையாடல் தொடங்கு"]:
        return _result([
            _msg_buttons(
                header="🗣️ இன்றைய ஆங்கில வாக்கிய பயிற்சி (Daily Practice)",
                body=(
                    "📌 *வாக்கியம்:* \"I want to open a savings bank account.\"\n\n"
                    "📌 *தமிழ் பொருள்:* \"நான் இந்த வங்கியில் ஒரு சேமிப்புக் கணக்கு தொடங்க விரும்புகிறேன்.\"\n\n"
                    "📌 *உச்சரிப்பு வழிகாட்டி:* \"ஐ வான்ட் டு ஓபன் எ சேவிங்ஸ் பேங்க் அக்கவுன்ட்\"\n\n"
                    "🎙️ இந்த வாக்கியத்தை பேசி வாய்ஸ் நோட்டாக அனுப்பினால் Meta AI உங்கள் உச்சரிப்பை சரிபார்த்து தரும்!"
                ),
                buttons=[
                    {"id": "btn_spoken_interview", "title": "🏢 நேர்காணல் பயிற்சி"},
                    {"id": "btn_spoken_voice", "title": "🎙️ வாய்ஸ் பயிற்சி"}
                ],
                footer="SIA • வள்ளுவர் AI மொழி பயிற்றுநர்"
            )
        ], stage="SPOKEN_DAILY_PRACTICE")

    if action in ["btn_spoken_interview", "நேர்காணல் பயிற்சி"]:
        return _result([
            _msg_buttons(
                header="🏢 வேலை நேர்காணல் பயிற்சி (Job Interview Practice)",
                body=(
                    "❓ *கேள்வி:* \"Tell me about your background and experience.\"\n\n"
                    "💡 *மாதிரி பதில்:* \"Good morning Sir/Madam. My name is Subramanian. I have completed Diploma in Mechanical Engineering from Madurai. I have 2 years of practical experience in CNC machine operations. I am a disciplined and dedicated worker.\"\n\n"
                    "🎙️ இதை பேசி வாய்ஸ் நோட்டாக அனுப்பவும்!"
                ),
                buttons=[
                    {"id": "btn_spoken_start", "title": "🗣️ வாக்கிய பயிற்சி"},
                    {"id": "btn_spoken_voice", "title": "🎙️ வாய்ஸ் பயிற்சி"}
                ],
                footer="SIA • நேர்காணல் வழிகாட்டி"
            )
        ], stage="SPOKEN_INTERVIEW_PRACTICE")

    if action in ["btn_spoken_voice", "வாய்ஸ் பயிற்சி"]:
        return _result([
            _msg_buttons(
                header="🎙️ நேரடி வாய்ஸ் பயிற்சி கூடம் (Meta AI Voice Coach)",
                body=(
                    "நீங்கள் ஆங்கிலத்தில் பேச விரும்பும் எந்த ஒரு வாக்கியத்தையும் தமிழ் அல்லது ஆங்கிலத்தில் வாய்ஸ் நோட்டாக அனுப்புங்கள்.\n\n"
                    "Meta muse-voice-transcribe-1.0 உங்கள் உச்சரிப்பு, வேகம், இலக்கணத்தை ஆராய்ந்து உடனடி குரல் திருத்தத்தை வழங்கும்!"
                ),
                buttons=[
                    {"id": "btn_spoken_start", "title": "🗣️ வாக்கிய பயிற்சி"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • குரல் வழி மொழிப்பயிற்சி"
            )
        ], stage="SPOKEN_VOICE_COACH")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 10: 14416 HELPLINE CALL & COUNSELING ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_call_14416", "14416 அழைப்பு"]:
        return _result([
            _msg_buttons(
                header="📞 தமிழ்நாடு அரசு Tele-MANAS உதவி மையம்",
                body=(
                    "• *இலவச கட்டணமில்லா உதவி எண்:* *14416*\n"
                    "• *சேவை நேரம்:* 24 மணி நேரமும் (24x7)\n"
                    "• *மொழி:* தூய தமிழ் மற்றும் ஆங்கிலம்\n"
                    "• *சிறப்பு:* பயிற்சி பெற்ற மனநல மருத்துவர்கள் & உளவியல் ஆலோசகர்கள்.\n"
                    "• தேர்வு பயம், மன அழுத்தம், குடும்ப கவலைகளுக்கு 100% ரகசிய ஆலோசனை!"
                ),
                buttons=[
                    {"id": "btn_calm_breath", "title": "🧘 அமைதி பயிற்சி"},
                    {"id": "btn_counseling", "title": "💬 மனநல ஆலோசனை"}
                ],
                footer="SIA • Tele-MANAS 24x7 ஹெல்ப்லைன்"
            )
        ], stage="MH_CALL_14416_INFO")

    if action in ["btn_counseling", "மனநல ஆலோசனை"]:
        return _result([
            _msg_buttons(
                header="💬 மன அமைதிக்கான அன்பான ஆலோசனை",
                body=(
                    "வணக்கம் நண்பரே! எந்த ஒரு கடினமான சூழ்நிலையும் தற்காலிகமானதுதான். நீங்கள் தனியாக இல்லை, உங்கள் உணர்வுகளை மதிக்கிறோம்.\n\n"
                    "உள்ளத்தில் உள்ள கவலைகளை தயக்கமின்றி இங்கே பதிவிடலாம் அல்லது தமிழ்நாடு அரசின் *14416* எண்ணை அழைத்து இலவசமாக மனநல ஆலோசகரிடம் மனம் திறந்து பேசலாம். அனைத்தும் ரகசியமாக வைக்கப்படும். ❤️"
                ),
                buttons=[
                    {"id": "btn_calm_breath", "title": "🧘 அமைதி பயிற்சி"},
                    {"id": "btn_call_14416", "title": "📞 14416 அழைப்பு"}
                ],
                footer="SIA • அன்பான உளவியல் வழிகாட்டல்"
            )
        ], stage="MH_COUNSELING_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 11: TNPSC ROADMAP, NEET 7.5% QUOTA & STUDY NOTES ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_roadmap_tnpsc", "TNPSC வரைபடம்"]:
        return _result([
            _msg_buttons(
                header="🗺️ TNPSC குரூப் 4 & 2 முழுமையான தேர்வு வரைபடம்",
                body=(
                    "1. *பொதுத் தமிழ் (100 வினாக்கள் / 150 மதிப்பெண்கள்):*\n"
                    "   • பகுதி அ: இலக்கணம் (பொருத்துதல், பிரித்தெழுதுதல், அணி)\n"
                    "   • பகுதி ஆ: இலக்கியம் (திருக்குறள், கம்பராமாயணம், எட்டுத்தொகை)\n"
                    "   • பகுதி இ: தமிழ் அறிஞர்களும் தமிழ்த் தொண்டும்\n"
                    "2. *பொது அறிவு (75 வினாக்கள்) + திறனறி தேர்வு (25 வினாக்கள்):* மொத்தம் 100 வினாக்கள் / 150 மதிப்பெண்கள்.\n\n"
                    "🎯 வெற்றி இலக்கு: 175+ வினாக்கள் சரியான விடை!"
                ),
                buttons=[
                    {"id": "btn_roadmap_neet", "title": "🩺 NEET 7.5% விவரம்"},
                    {"id": "btn_roadmap_study", "title": "📖 இலவச பாடக்குறிப்பு"}
                ],
                footer="SIA • அரசுப் பணி வழிகாட்டி"
            )
        ], stage="EXAM_ROADMAP_TNPSC")

    if action in ["btn_roadmap_neet", "NEET 7.5% விவரம்"]:
        return _result([
            _msg_buttons(
                header="🩺 அரசு பள்ளி மாணவர்களுக்கான NEET 7.5% இடஒதுக்கீடு",
                body=(
                    "• *தகுதி:* 6 முதல் 12-ஆம் வகுப்பு வரை அரசுப் பள்ளிகளில் தமிழ்/ஆங்கில வழியில் படித்த மாணவர்கள்.\n"
                    "• *சலுகை:* மருத்துவக் கல்லூரி கல்விக் கட்டணம், விடுதிக் கட்டணம் முழுவதையும் அரசே ஏற்கும்!\n"
                    "• *2025 கட்-ஆஃப் மார்க்:* MBBS (480+), BDS (430+).\n"
                    "• *தேவையான சான்றிதழ்:* 6-12 அரசு பள்ளி தலைமை ஆசிரியர் Bonafide சான்றிதழ்."
                ),
                buttons=[
                    {"id": "btn_roadmap_tnpsc", "title": "🗺️ TNPSC வரைபடம்"},
                    {"id": "btn_roadmap_study", "title": "📖 இலவச பாடக்குறிப்பு"}
                ],
                footer="SIA • மருத்துவக் கல்வி இடஒதுக்கீடு"
            )
        ], stage="EXAM_ROADMAP_NEET")

    if action in ["btn_roadmap_study", "இலவச பாடக்குறிப்பு"]:
        return _result([
            _msg_buttons(
                header="📖 அரசுப் போட்டித் தேர்வு இலவச பாடக்குறிப்புகள்",
                body=(
                    "• *TNPSC பொதுத்தமிழ் 100/100 வினா வங்கி*\n"
                    "• *இந்திய அரசியலமைப்பு முக்கிய சரத்துகள் அட்டவணை*\n"
                    "• *சமச்சீர் அறிவியல் & சமூக அறிவியல் 1-வரி குறிப்புகள்*\n"
                    "• *கணிதம் குறுக்குவழி முறைகள் (Maths Shortcuts)*\n\n"
                    "அனைத்து பாடக்குறிப்புகளும் உங்கள் வாட்ஸ்அப்பில் இலவசமாக பதிவிறக்கத் தயார்!"
                ),
                buttons=[
                    {"id": "btn_roadmap_tnpsc", "title": "🗺️ TNPSC வரைபடம்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • டிஜிட்டல் நூலகம்"
            )
        ], stage="EXAM_ROADMAP_STUDY_NOTES")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 12: RENTO TRACTOR, HARVESTER & NEARBY MACHINERY ACTIONS
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_rent_tractor", "டிராக்டர் வாடகை"]:
        return _result([
            _msg_buttons(
                header="✅ டிராக்டர் வாடகை முன்பதிவு உறுதியானது!",
                body=(
                    "• *இயந்திரம்:* மஹிந்திரா 45HP டிராக்டர் + 36-பிளேடு ரோட்டவேட்டர்\n"
                    "• *உழவர் உரிமையாளர்:* பி. முருகேசன்\n"
                    "• *முகவரி:* மேலூர் மெயின் ரோடு (உங்கள் வயலிலிருந்து 2.5 கிமீ)\n"
                    "• *வாடகை:* *₹850 / மணி* (டீசல் & ஓட்டுநர் உட்பட)\n"
                    "• *தொலைபேசி:* 94432 87654\n"
                    "• 0% இடைத்தரகர் கட்டணம்! உரிமையாளர் உங்கள் வயலுக்கு வரத் தயாராக உள்ளார்."
                ),
                buttons=[
                    {"id": "btn_rent_harvester", "title": "🌾 அறுவடை இயந்திரம்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • RentO உழவர் இயந்திர மையம்"
            )
        ], stage="RENTO_TRACTOR_BOOKED")

    if action in ["btn_rent_harvester", "அறுவடை இயந்திரம்"]:
        return _result([
            _msg_buttons(
                header="✅ நெல் அறுவடை இயந்திர முன்பதிவு உறுதியானது!",
                body=(
                    "• *இயந்திரம்:* கம்பைன்ட் நெல் அறுவடை இயந்திரம் (Combined Paddy Harvester)\n"
                    "• *உழவர் உரிமையாளர்:* கே. ராமசாமி\n"
                    "• *முகவரி:* சோழவந்தான் (உங்கள் வயலிலிருந்து 3 கிமீ)\n"
                    "• *வாடகை:* *₹2,200 / மணி*\n"
                    "• *தொலைபேசி:* 98431 54321\n"
                    "• நெல் கதிர் அறுவடை, தூற்றுதல் மற்றும் சாக்கு பிடித்தல் ஒரே நேரத்தில் நடக்கும்!"
                ),
                buttons=[
                    {"id": "btn_rent_tractor", "title": "🚜 டிராக்டர் வாடகை"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • RentO உழவர் இயந்திர மையம்"
            )
        ], stage="RENTO_HARVESTER_BOOKED")

    if action in ["btn_rent_nearby", "அருகில் உள்ள கருவிகள்"]:
        return _result([
            _msg_buttons(
                header="📍 உங்கள் பகுதியில் உள்ள வாடகை உழவர் கருவிகள்",
                body=(
                    "1. 🚜 *மஹிந்திரா டிராக்டர் ரோட்டவேட்டர்:* ₹850/மணி (2.5 கிமீ, Ph: 94432 87654)\n"
                    "2. 🌾 *நெல் அறுவடை இயந்திரம்:* ₹2,200/மணி (3.0 கிமீ, Ph: 98431 54321)\n"
                    "3. ⚙️ *பவர் வீடர் (களை மெஷின்):* ₹450/மணி (1.2 கிமீ, Ph: 97891 23456)\n"
                    "4. 🔋 *சோலார் தெளிப்பான்:* ₹150/நாள் (800 மீ, Ph: 96552 34567)\n\n"
                    "நேரடி உழவர் வாடகை - இடைத்தரகர் கட்டணம் இல்லை!"
                ),
                buttons=[
                    {"id": "btn_rent_tractor", "title": "🚜 டிராக்டர் வாடகை"},
                    {"id": "btn_rent_harvester", "title": "🌾 அறுவடை இயந்திரம்"}
                ],
                footer="SIA • RentO ஹைப்பர்-லோக்கல் மையம்"
            )
        ], stage="RENTO_NEARBY_MACHINERY")

    #  INTERACTIVE QUICK MENU BUTTONS (btn_menu_1_agri, btn_menu_4_taxi, etc.)
    # ────────────────────────────────────────────────────────────────────────
    if action.startswith("btn_menu_"):
        clean_target = action.replace("btn_menu_", "").split("_")[0]
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "நண்பரே") if u_prof else "நண்பரே"
        lang = get_user_language(clean_phone)
        guide_data = get_menu_guide_response(clean_target, citizen_name=u_name, lang=lang)
        if guide_data:
            return _result([
                _msg_buttons(
                    header=guide_data["header"],
                    body=guide_data["body"],
                    buttons=guide_data["buttons"],
                    footer=guide_data["footer"]
                )
            ], stage=f"MENU_GUIDE_{clean_target}")

    # ────────────────────────────────────────────────────────────────────────
    #  PRIMARY PORTAL ACTIONS (1, 2, 3, 4)
    # ────────────────────────────────────────────────────────────────────────
    if action.lower() in ["portal_govt", "portal_commerce", "portal_finance", "portal_vault"]:
        portal_map = {
            "portal_govt": "1",
            "portal_commerce": "2",
            "portal_finance": "3",
            "portal_vault": "4"
        }
        lang = get_user_language(clean_phone)
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "நண்பரே") if u_prof else "நண்பரே"
        guide_data = get_menu_guide_response(portal_map[action.lower()], citizen_name=u_name, lang=lang)
        if guide_data:
            return _result([
                _msg_buttons(
                    header=guide_data["header"],
                    body=guide_data["body"],
                    buttons=guide_data["buttons"],
                    footer=guide_data["footer"]
                )
            ], stage=f"PORTAL_{portal_map[action.lower()]}")

    # ────────────────────────────────────────────────────────────────────────

    #  NUMBERED MENU CHOICES INTERCEPTOR (1 through 12, "1.", "1️⃣", etc.)

    # ────────────────────────────────────────────────────────────────────────

    # Map natural single-word keywords to service numbers 1-12
    KEYWORD_SERVICE_MAP = {
        # Service 1: Agri
        "பயிர்": "1", "விவசாயம்": "1", "வேளாண்மை": "1", "பூச்சி": "1", "நெல்": "1", "AGRI": "1", "AGRICULTURE": "1", "CROP": "1", "PEST": "1",
        # Service 2: Cattle
        "மாடு": "2", "கால்நடை": "2", "மடிவீக்கம்": "2", "CATTLE": "2", "COW": "2", "DAIRY": "2",
        # Service 3: Store
        "மளிகை": "3", "கடை": "3", "அரிசி": "3", "பருப்பு": "3", "STORE": "3", "KIRANA": "3", "GROCERY": "3",
        # Service 4: Taxi
        "டாக்ஸி": "4", "ஆட்டோ": "4", "கார்": "4", "TAXI": "4", "AUTO": "4", "CAB": "4", "RIDE": "4",
        # Service 5: Food
        "உணவு": "5", "சாப்பாடு": "5", "பசி": "5", "FOOD": "5", "MEALS": "5", "LUNCH": "5",
        # Service 6: Patta / eSevai
        "பட்டா": "6", "சிட்டா": "6", "இசேவை": "6", "நிலம்": "6", "PATTA": "6", "CHITTA": "6", "ESEVAI": "6",
        # Service 7: Education
        "கல்வி": "7", "பள்ளி": "7", "மாணவர்": "7", "EDUCATION": "7", "EDU": "7", "SCHOOL": "7", "STUDENT": "7",
        # Service 8: Petition
        "மனு": "8", "கோரிக்கை": "8", "MLA": "8", "MP": "8", "PETITION": "8", "MANU": "8",
        # Service 9: Spoken English
        "ஆங்கிலம்": "9", "பேச்சு": "9", "ENGLISH": "9", "SPOKEN": "9",
        # Service 10: Mental Health
        "மனநலம்": "10", "பதற்றம்": "10", "பயம்": "10", "14416": "10", "MENTAL": "10", "STRESS": "10", "CALM": "10",
        # Service 11: Exam
        "தேர்வு": "11", "TNPSC": "11", "NEET": "11", "UPSC": "11", "EXAM": "11", "ROADMAP": "11",
        # Service 12: RentO Machinery
        "டிராக்டர்": "12", "அறுவடை": "12", "இயந்திரம்": "12", "வாடகை": "12", "TRACTOR": "12", "HARVESTER": "12", "RENTO": "12", "MACHINERY": "12"
    }

    clean_num = upper.strip().rstrip(".").replace("️⃣", "")
    if clean_num in KEYWORD_SERVICE_MAP:
        clean_num = KEYWORD_SERVICE_MAP[clean_num]
    elif text in KEYWORD_SERVICE_MAP:
        clean_num = KEYWORD_SERVICE_MAP[text]

    if clean_num in [str(i) for i in range(1, 18)]:

        u_prof = get_user_profile(clean_phone)

        u_name = u_prof.get("name", "நண்பரே") if u_prof else "நண்பரே"

        lang = get_user_language(clean_phone)
        guide_data = get_menu_guide_response(clean_num, citizen_name=u_name, lang=lang)

        if guide_data:

            return _result([

                _msg_buttons(

                    header=guide_data["header"],

                    body=guide_data["body"],

                    buttons=guide_data["buttons"],

                    footer=guide_data["footer"]

                )

            ], stage=f"MENU_GUIDE_{clean_num}")

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

        "AADHAAR", "RTI", "ANS", "GOOD MORNING", "GM", "MORNING", "காலை வணக்கம்",

        "NEWS", "செய்திகள்", "செய்தி", "AIR", "வானொலி", "RADIO"

    }

    if any(upper == k or upper.startswith(k + " ") or upper.startswith(k + "-") for k in SYSTEM_COMMAND_KEYWORDS):

        return None

    if upper in ["A", "B", "C", "D"] or (len(upper) >= 3 and upper[0].isdigit() and upper[1] in "-:" and upper[2] in "ABCD"):

        return None

    contains_sia = "SIA" in upper or "சியா" in text

    if not is_user_registered(clean_phone) and any(w in upper for w in ["ACCESS", "REGISTER", "SIGNUP", "NEW", "WANT TO ACCESS"]):

        return _start_registration(clean_phone)

    # Bypass generic welcome for Good Morning and News requests

    if any(k in upper for k in ["GOOD MORNING", "GM", "காலை வணக்கம்", "NEWS", "செய்திகள்", "AIR"]):

        return None

    is_greeting = upper in [

        "HI", "HELLO", "START", "LOGIN", "MENU",

        "வணக்கம்", "ஹலோ", "ஹாய்", "SIA",

    ] or contains_sia

    if is_greeting:

        return _send_welcome(clean_phone)

    # ────────────────────────────────────────────────────────────────────────

    #  CASE 6: Service menu request

    # ────────────────────────────────────────────────────────────────────────

    if action in ("btn_services", "btn_menu", "btn_menu_restart"):
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
    """Welcome message returning the simplified pictorial menu in pure Tamil script / English."""
    lang = get_user_language(clean_phone)
    user = get_user_profile(clean_phone)
    name = user.get("name", "நண்பரே") if user else ("Citizen" if lang == "en" else "நண்பரே")
    menu = get_simplified_pictorial_menu(name, lang=lang)
    return _result([
        _msg_buttons(
            header=menu["header"],
            body=menu["body"],
            buttons=menu["buttons"],
            footer=menu["footer"]
        )
    ], stage="SIMPLIFIED_PICTORIAL_MENU")

def _start_registration(clean_phone: str) -> Dict[str, Any]:
    """Begin interactive registration by asking for language preference (Tamil script / English)."""
    ONBOARDING_STAGES[clean_phone] = {"stage": "ASK_LANGUAGE", "phone": clean_phone}
    prompt = get_language_picker_prompt()
    msgs = [
        _msg_buttons(
            header=prompt["header"],
            body=prompt["body"],
            buttons=prompt["buttons"],
            footer=prompt["footer"]
        )
    ]
    return _result(msgs, stage="ASK_LANGUAGE")

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

        # ── Step 0: Language Preference ──
    if stage == "ASK_LANGUAGE":
        lang = "ta"
        if action == "lang_en" or "english" in text.lower() or text.strip() == "2":
            lang = "en"
        elif action == "lang_ta" or "தமிழ்" in text.lower() or "tamil" in text.lower() or text.strip() == "1":
            lang = "ta"

        session["language"] = lang
        session["stage"] = "ASK_NAME"
        ONBOARDING_STAGES[clean_phone] = session
        set_user_language(clean_phone, lang)

        if lang == "en":
            return _result([
                _msg_buttons(
                    header="👤 Step 1/3 • Your Name",
                    body=(
                        "Please type your full name ⌨️\n"
                        "or send a voice note 🎤\n\n"
                        "Example: Arun Kumar"
                    ),
                    buttons=[
                        {"id": "btn_voice_name", "title": "🎤 Speak Name"},
                    ],
                    footer="Step 1/3 • Registration"
                )
            ], stage="ASK_NAME")
        else:
            return _result([
                _msg_buttons(
                    header="👤 படி 1/3 • பெயர்",
                    body=(
                        "உங்கள் முழுப் பெயரை தட்டச்சு செய்யவும் ⌨️\n"
                        "அல்லது குரல் பதிவு அனுப்பவும் 🎤\n\n"
                        "எடுத்துக்காட்டு: அருண் குமார்"
                    ),
                    buttons=[
                        {"id": "btn_voice_name", "title": "🎤 குரலில் சொல்ல"},
                    ],
                    footer="படி 1/3 • பதிவு"
                )
            ], stage="ASK_NAME")

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

    if action == "svc_patta":

        return _result([

            _msg_text(

                "📜 *பட்டா மாறுதல் வழிகாட்டி (RSO 31 / TNeGA)*\n\n"

                "• *உட்பிரிவு இல்லாத பட்டா:* முற்றிலும் ₹0 இலவசம்!\n"

                "• *உட்பிரிவு உள்ள பட்டா:* ₹60 அரசு கட்டணம் மட்டுமே.\n"

                "• *தேவையானவை:* கிரய பத்திரம், வில்லங்க சான்று (EC), ஆதார்.\n\n"

                "⚠️ இடைத்தரகர்களுக்கு ₹3,000 - ₹5,000 கொடுக்காதீர்கள்!\n"

                f"🌐 நேரடி நில வரைபடம் & பத்திரம் சரிபார்க்க: {base_url}"

            )

        ], stage="SVC_PATTA_EXP")

    if action == "svc_ration":

        return _result([

            _msg_text(

                "🍚 *ஸ்மார்ட் குடும்ப அட்டை வழிகாட்டி (TNePDS)*\n\n"

                "• புதிய அட்டை விண்ணப்பம்: ₹0 இலவசம்\n"

                "• பெயர் சேர்த்தல் / நீக்குதல்: ₹0 இலவசம்\n"

                "• முகவரி மாற்றம்: ₹0 இலவசம் (ஆதார் OTP உடன்)\n\n"

                "உணவுப் பொருள் விநியோக குறைபாடுகளுக்கு 1967 எண்ணில் புகாரளிக்கலாம்."

            )

        ], stage="SVC_RATION_EXP")

    if action == "svc_kmut":

        return _result([

            _msg_text(

                "🌸 *கலைஞர் மகளிர் உரிமைத் திட்டம் (மாதம் ₹1,000)*\n\n"

                "• ஆண்டு குடும்ப வருமானம் ₹2.5 லட்சத்திற்குள் இருக்க வேண்டும்.\n"

                "• 5 ஏக்கர் நன்செய் அல்லது 10 ஏக்கர் புன்செய் நிலத்திற்குள் இருக்க வேண்டும்.\n"

                "• குடும்ப மின் பயன்பாடு ஆண்டுக்கு 3,600 யூனிட்டிற்குள் இருக்க வேண்டும்.\n"

                "• பணம் நேரடியாக உங்கள் வங்கி கணக்கில் வரவு வைக்கப்படும்!"

            )

        ], stage="SVC_KMUT_EXP")

    if action in ("svc_mla_petition", "svc_mp_petition", "svc_sample_petition"):

        return _result([

            _msg_text(

                "📝 *குறைதீர்ப்பு மனு தயாரிப்பு வழிகாட்டி*\n\n"

                "உங்கள் கிராமம் அல்லது பகுதி குறைகளை நேரடியாக எழுதி அல்லது குரல் பதிவாக அனுப்பவும்:\n"

                "எ.கா: `சோழவந்தான் மெயின் ரோட்டில் குடிநீர் குழாய் உடைப்பு மனு`\n\n"

                "உடனடியாக சீல் வைக்கப்பட்ட அதிகாரப்பூர்வ மனு PDF வடிவில் உங்கள் வாட்ஸ்அப்பிற்கு வரும்!"

            )

        ], stage="SVC_PETITION_EXP")

    if action in ("svc_tuition", "svc_homework", "svc_diagram"):

        return _result([

            _msg_text(

                "📚 *பள்ளி கல்வி & டியூஷன் வழிகாட்டி*\n\n"

                "உங்கள் வகுப்பு மற்றும் பாடத்தை அனுப்பவும்:\n"

                "• `10-ம் வகுப்பு அறிவியல் மனித இதயம் வரைபடம்`\n"

                "• `12-ம் வகுப்பு கணிதம் Differential Calculus உதவி`\n"

                "உடனடி விளக்கக் குறிப்புகள் மற்றும் வரைபடங்கள் வழங்கப்படும்!"

            )

        ], stage="SVC_TUITION_EXP")

    if action in ("svc_tnpsc", "svc_neet", "svc_cbt_cert"):

        return _result([

            _msg_text(

                "🎯 *போட்டித் தேர்வுகள் (CBT) வழிகாட்டி*\n\n"

                "மாதிரி தேர்வு எழுத தலைப்பை அனுப்பவும்:\n"

                "• `TNPSC குரூப் 4 திருக்குறள் மாதிரி தேர்வு`\n"

                "• `NEET Biology Cell Division 5 questions test`\n"

                "உடனடி கவுண்டவுன் தேர்வும், 60% மேல் மதிப்பெண் பெற்றால் சான்றிதழும் வழங்கப்படும்!"

            )

        ], stage="SVC_EXAMS_EXP")

    if action in ("svc_bike", "svc_tractor", "svc_labor"):

        return _result([

            _msg_text(

                "🛵 *ஹைப்பர்-லோக்கல் வாடகை (0% கமிஷன்)*\n\n"

                "உங்கள் 6-இலக்க பின்கோடுடன் தேவை அனுப்பவும்:\n"

                "• `625214 பைக் வேணும்`\n"

                "• `613001 நெல் அறுவடை இயந்திரம்`\n"

                "• `641001 கொத்தனார் ஆட்கள் வேண்டும்`\n"

                "அருகிலுள்ள சரிபார்க்கப்பட்ட தொழிலாளி உடனடியாக ஒதுக்கப்படுவார்!"

            )

        ], stage="SVC_RENTALS_EXP")

    if action in ("svc_gold", "svc_stocks", "svc_invest"):

        return _result([

            _msg_text(

                "🪙 *நேரடி தங்கம் விலை (Live Gold Rate)*\n\n"

                "• 1 பவுன் (8 கிராம்): *₹1,01,800+* (1.02 லட்சம் - நேரடி சந்தை!)\n"

                "• 10 கிராம் 24K: *₹1,27,250+* (1.27 லட்சம்)\n"

                "• NIFTY 50: *24,350+* | SENSEX: *80,100+*\n\n"

                "நீண்ட கால முதலீட்டுக்கு Sovereign Gold Bond (SGB) அல்லது NIFTY Index Fund சிறந்தது."

            )

        ], stage="SVC_GOLD_EXP")

    if action in ("svc_reels", "svc_new_video", "svc_shorts"):

        return _result([

            _msg_text(

                "🎬 *ArcReel 45s வைரல் வீடியோக்கள்*\n\n"

                "தற்போதைய ட்ரெண்டிங் வீடியோக்கள் தயாராக உள்ளன:\n"

                "• தங்கம் விலை வரலாறு காணாத உச்சம் (> 1 லட்சம் பவுன்)\n"

                "• ஹோசூர் AI தொழிற்சாலை & நேரடி வாய்ப்புகள்\n\n"

                f"🌐 இணையத்தில் வீடியோக்களைப் பார்க்க: {base_url}"

            )

        ], stage="SVC_REELS_EXP")

    if action in ("reg_driver", "reg_machinery", "reg_labor"):

        return _result([

            _msg_text(

                "🤝 *கூட்டாளர் பதிவு வழிகாட்டி (0% கமிஷன்)*\n\n"

                "சுயதொழில் பதிவு செய்ய கீழ்கண்ட முறையில் அனுப்பவும்:\n"

                "`பதிவு [தொழில்] [பெயர்] [வாகனம்] [பின்கோடு] [தொலைபேசி]`\n\n"

                "எ.கா: `பதிவு ஓட்டுநர் ரமேஷ் பைக் 625214 9840112233`\n"

                "பதிவு செய்தவுடன் உங்கள் எண் உடனடியாக சரிபார்க்கப்படும்!"

            )

        ], stage="SVC_PARTNER_REG_EXP")

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

    if action == "svc_travel":

        from travel_booking_engine import format_whatsapp_travel_menu

        m = format_whatsapp_travel_menu()

        return _result([

            _msg_buttons(

                header=m["header_text"],

                body=m["body_text"],

                buttons=m["buttons"],

                footer=m["footer_text"]

            )

        ], stage="TRAVEL_MENU")

    if action == "svc_edu":

        from universal_tuition_engine import format_whatsapp_tuition_menu

        m = format_whatsapp_tuition_menu()

        return _result([

            _msg_buttons(

                header=m["header_text"],

                body=m["body_text"],

                buttons=m["buttons"],

                footer=m["footer_text"]

            )

        ], stage="TUITION_MENU")

    if action == "svc_agri":

        from agriculture_engine import format_whatsapp_agri_menu

        m = format_whatsapp_agri_menu()

        return _result([

            _msg_buttons(

                header=m["header_text"],

                body=m["body_text"],

                buttons=m["buttons"],

                footer=m["footer_text"]

            )

        ], stage="AGRI_MENU")

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

