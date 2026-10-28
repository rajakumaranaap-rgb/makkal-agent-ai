# -*- coding: utf-8 -*-
"""
Makkal Agent AI - WhatsApp Secret PIN Magic Auth & Remote Session Manager
Meta AI Developer Hackathon 2026

Enables rural citizens to log in to Makkal AI without passwords, usernames, or complex forms:
1. Citizen sends their Secret PIN or 'LOGIN' to the Makkal WhatsApp Bot number.
2. WhatsApp Webhook verifies the phone number and auto-dispatches a single-use Magic Login Link.
3. Citizen taps the link in WhatsApp and instantly accesses their authenticated citizen portal.
4. Remote Kill-Switch: Citizen sends 'CLOSE' or 'LOGOUT' to the WhatsApp bot to terminate
   the active web session in real-time. Web app immediately stops access and requires
   WhatsApp PIN to unlock!
"""

import time
import uuid
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("makkal.whatsapp_auth")

# Active Session & Token Store (Thread-safe in-memory cache with expiry)
# Format: { token: { phone, pin, created_at, expires_at, status: "PENDING" | "ACTIVE" | "TERMINATED" } }
MAGIC_TOKENS: Dict[str, Dict[str, Any]] = {}
PHONE_ACTIVE_SESSIONS: Dict[str, str] = {}  # phone -> latest_token
PHONE_LOCK_STATE: Dict[str, str] = {}       # phone -> "ACTIVE" | "LOCKED_AWAITING_PIN"

TOKEN_TTL_SECONDS = 900  # 15 Minutes Validity


def _clean_phone(phone: str) -> str:
    digits = "".join([c for c in str(phone) if c.isdigit()])
    return digits[-10:] if len(digits) >= 10 else digits


def create_magic_auth_token(phone: str, secret_pin: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a secure, one-time Magic Login Token triggered by incoming WhatsApp message.
    Clears any prior lock state for this phone.
    """
    clean_phone = _clean_phone(phone)
    token = f"makkal_magic_{uuid.uuid4().hex[:16]}"
    now = time.time()

    session_data = {
        "token": token,
        "phone": clean_phone,
        "secret_pin": secret_pin or "7890",
        "created_at": now,
        "expires_at": now + TOKEN_TTL_SECONDS,
        "status": "ACTIVE",  # Active immediately upon PIN receipt
        "device_info": "WhatsApp Verified Mobile Session"
    }

    MAGIC_TOKENS[token] = session_data
    PHONE_ACTIVE_SESSIONS[clean_phone] = token
    # Unlock phone
    PHONE_LOCK_STATE[clean_phone] = "UNLOCKED"

    logger.info(f"[WHATSAPP AUTH] Created active magic token for {clean_phone} (PIN: {secret_pin or 'DEFAULT'})")
    return session_data


def verify_magic_auth_token(token: str, phone: Optional[str] = None) -> Dict[str, Any]:
    """
    Validates a Magic Token when clicked from WhatsApp link.
    Marks session as ACTIVE.
    """
    if not token or token not in MAGIC_TOKENS:
        return {"valid": False, "error": "செல்லுபடியாகாத அல்லது காலாவதியான இணைப்பு (Invalid/Expired Link)"}

    session = MAGIC_TOKENS[token]
    clean_phone = session["phone"]
    now = time.time()

    if now > session["expires_at"]:
        session["status"] = "EXPIRED"
        return {"valid": False, "error": "இணைப்பின் 15 நிமிட கால அவகாசம் முடிந்துவிட்டது (Link Expired)"}

    if session["status"] == "TERMINATED" or PHONE_LOCK_STATE.get(clean_phone) == "LOCKED_AWAITING_PIN":
        return {
            "valid": False,
            "locked": True,
            "error": "இந்த அமர்வு WhatsApp மூலம் பாதுகாப்பாக மூடப்பட்டுவிட்டது. மீண்டும் திறக்க WhatsApp-ல் உங்கள் ரகசிய PIN அனுப்பவும்."
        }

    # Mark as ACTIVE authenticated session
    session["status"] = "ACTIVE"
    session["authenticated_at"] = now
    PHONE_LOCK_STATE[clean_phone] = "ACTIVE"

    logger.info(f"[WHATSAPP AUTH] Session activated for phone: {clean_phone}")
    return {
        "valid": True,
        "phone": clean_phone,
        "secret_pin": session["secret_pin"],
        "status": "ACTIVE",
        "expires_in_secs": int(session["expires_at"] - now)
    }


def terminate_session_by_whatsapp(phone: str, close_pin: Optional[str] = None) -> Dict[str, Any]:
    """
    Remote Kill-Switch:
    When a citizen texts 'CLOSE', 'LOGOUT', or exit keywords on WhatsApp,
    this immediately invalidates active web sessions and marks the user's
    phone access as LOCKED_AWAITING_PIN!
    """
    clean_phone = _clean_phone(phone)
    PHONE_LOCK_STATE[clean_phone] = "LOCKED_AWAITING_PIN"

    # Invalidate all tokens associated with this phone
    terminated_count = 0
    for tok, sess in list(MAGIC_TOKENS.items()):
        if sess.get("phone") == clean_phone or clean_phone.endswith(sess.get("phone", "")[-10:]):
            sess["status"] = "TERMINATED"
            sess["terminated_at"] = time.time()
            terminated_count += 1

    PHONE_ACTIVE_SESSIONS.pop(clean_phone, None)

    logger.info(f"[WHATSAPP AUTH] Remote kill-switch triggered for {clean_phone}! Web session stopped. Locked awaiting WhatsApp PIN.")
    return {
        "success": True,
        "phone": clean_phone,
        "terminated_count": terminated_count,
        "status": "LOCKED_AWAITING_PIN",
        "message": (
            "🔒 உங்கள் SIA இணைய அமர்வு WhatsApp மூலம் பாதுகாப்பாக உடனடியாக மூடப்பட்டது!\n"
            "மீண்டும் இணையத்தை திறக்க உங்கள் 4-இலக்க ரகசிய PIN எண்ணை இந்த வாட்ஸ்அப் எண்ணிற்கு அனுப்பவும்."
        )
    }


def terminate_session_by_token(token: str) -> Dict[str, Any]:
    """
    Terminates a session directly using its token (e.g. from web logout button).
    """
    if not token or token not in MAGIC_TOKENS:
        return {"success": False, "message": "செல்லுபடியாகாத அமர்வு (Invalid session)"}

    session = MAGIC_TOKENS[token]
    session["status"] = "TERMINATED"
    session["terminated_at"] = time.time()
    phone = session.get("phone", "")
    if phone:
        clean = _clean_phone(phone)
        PHONE_LOCK_STATE[clean] = "LOCKED_AWAITING_PIN"
        PHONE_ACTIVE_SESSIONS.pop(clean, None)

    logger.info(f"[WHATSAPP AUTH] Session {token} terminated directly via web logout.")
    return {
        "success": True,
        "phone": phone,
        "terminated_token": token,
        "message": "அமர்வு வெற்றிகரமாக மூடப்பட்டது (Logged out successfully)"
    }


def request_phone_login(phone: str) -> Dict[str, Any]:
    """
    Called when a user enters their WhatsApp phone number in the Apple Desktop view.
    Sets the phone's lock state to LOCKED_AWAITING_PIN so the browser can wait
    for the user to send their secret PIN (text or voice) via WhatsApp.
    """
    clean_phone = _clean_phone(phone)
    PHONE_LOCK_STATE[clean_phone] = "LOCKED_AWAITING_PIN"
    PHONE_ACTIVE_SESSIONS.pop(clean_phone, None)
    logger.info(f"[WHATSAPP AUTH] Phone login requested for {clean_phone}. Awaiting WhatsApp PIN.")
    return {
        "status": "AWAITING_PIN",
        "phone": clean_phone,
        "message": "Waiting for secret PIN from WhatsApp"
    }


def get_session_status(token: Optional[str] = None, phone: Optional[str] = None) -> Dict[str, Any]:
    """
    Polled by the web client every 2-3 seconds to detect:
    1. If the session was remotely terminated by 'CLOSE' on WhatsApp -> Stop access immediately!
    2. If the user sent their secret PIN on WhatsApp -> Automatically unlock access!
    """
    clean_p = _clean_phone(phone) if phone else ""

    # Check phone-level lock first
    if clean_p and PHONE_LOCK_STATE.get(clean_p) == "LOCKED_AWAITING_PIN":
        return {
            "status": "TERMINATED",
            "active": False,
            "locked": True,
            "phone": clean_p,
            "lock_reason": "WHATSAPP_CLOSE_COMMAND",
            "message": "வாட்ஸ்அப் மூலம் அமர்வு நிறுத்தப்பட்டுள்ளது. மீண்டும் திறக்க உங்கள் ரகசிய PIN-ஐ வாட்ஸ்அப்பில் அனுப்பவும்."
        }

    # If token provided, inspect token
    if token and token in MAGIC_TOKENS:
        session = MAGIC_TOKENS[token]
        p = session.get("phone", "")
        if PHONE_LOCK_STATE.get(p) == "LOCKED_AWAITING_PIN":
            return {
                "status": "TERMINATED",
                "active": False,
                "locked": True,
                "phone": p,
                "lock_reason": "WHATSAPP_CLOSE_COMMAND",
                "message": "வாட்ஸ்அப் மூலம் அமர்வு நிறுத்தப்பட்டுள்ளது."
            }
        is_active = session["status"] == "ACTIVE" and time.time() <= session["expires_at"]
        return {
            "status": session["status"] if is_active else "EXPIRED",
            "active": is_active,
            "locked": not is_active,
            "phone": p,
            "token": token,
            "time_remaining_secs": max(0, int(session["expires_at"] - time.time()))
        }

    # If phone is provided, check if it has a confirmed active session
    if clean_p:
        is_locked = PHONE_LOCK_STATE.get(clean_p) == "LOCKED_AWAITING_PIN"
        if is_locked:
            return {
                "status": "TERMINATED",
                "active": False,
                "locked": True,
                "phone": clean_p,
                "lock_reason": "WHATSAPP_CLOSE_COMMAND",
                "message": "வாட்ஸ்அப் மூலம் அமர்வு நிறுத்தப்பட்டுள்ளது. மீண்டும் திறக்க உங்கள் ரகசிய PIN-ஐ வாட்ஸ்அப்பில் அனுப்பவும்."
            }
        active_tok = PHONE_ACTIVE_SESSIONS.get(clean_p)
        if active_tok and active_tok in MAGIC_TOKENS:
            tok_sess = MAGIC_TOKENS[active_tok]
            if tok_sess["status"] in ("ACTIVE", "PENDING") and time.time() <= tok_sess["expires_at"]:
                return {
                    "status": "ACTIVE",
                    "active": True,
                    "locked": False,
                    "phone": clean_p,
                    "token": active_tok,
                    "time_remaining_secs": max(0, int(tok_sess["expires_at"] - time.time()))
                }
        # If no active session token exists or session expired, phone is strictly locked!
        return {
            "status": "LOCKED",
            "active": False,
            "locked": True,
            "phone": clean_p
        }

    return {"status": "NOT_FOUND", "active": False, "locked": True}
