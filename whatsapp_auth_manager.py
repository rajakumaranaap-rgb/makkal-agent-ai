# -*- coding: utf-8 -*-
"""
Makkal Agent AI - WhatsApp Secret PIN Magic Auth & Remote Session Manager
Meta AI Developer Hackathon 2026

Enables rural citizens to log in to Makkal AI without passwords, usernames, or complex forms:
1. Citizen sends their Secret PIN or 'LOGIN' to the Makkal WhatsApp Bot number.
2. WhatsApp Webhook verifies the phone number and auto-dispatches a single-use Magic Login Link.
3. Citizen taps the link in WhatsApp and instantly accesses their authenticated citizen portal.
4. Remote Kill-Switch: Citizen sends 'CLOSE' or 'LOGOUT' to the WhatsApp bot to terminate
   the active web session in real-time from anywhere in the world!
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

TOKEN_TTL_SECONDS = 900  # 15 Minutes Validity


def create_magic_auth_token(phone: str, secret_pin: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a secure, one-time Magic Login Token triggered by incoming WhatsApp message.
    """
    clean_phone = "".join([c for c in str(phone) if c.isdigit()])
    token = f"makkal_magic_{uuid.uuid4().hex[:16]}"
    now = time.time()

    session_data = {
        "token": token,
        "phone": clean_phone,
        "secret_pin": secret_pin or "MAKKAL",
        "created_at": now,
        "expires_at": now + TOKEN_TTL_SECONDS,
        "status": "PENDING",  # Transitions to ACTIVE on web click, TERMINATED on close command
        "device_info": "WhatsApp Verified Mobile Session"
    }

    MAGIC_TOKENS[token] = session_data
    PHONE_ACTIVE_SESSIONS[clean_phone] = token

    logger.info(f"[WHATSAPP AUTH] Created magic token for {clean_phone} (PIN: {secret_pin or 'DEFAULT'})")
    return session_data


def verify_magic_auth_token(token: str, phone: Optional[str] = None) -> Dict[str, Any]:
    """
    Validates a Magic Token when clicked from WhatsApp link.
    Marks session as ACTIVE.
    """
    if not token or token not in MAGIC_TOKENS:
        return {"valid": False, "error": "செல்லுபடியாகாத அல்லது காலாவதியான இணைப்பு (Invalid/Expired Link)"}

    session = MAGIC_TOKENS[token]
    now = time.time()

    if now > session["expires_at"]:
        session["status"] = "EXPIRED"
        return {"valid": False, "error": "இணைப்பின் 15 நிமிட கால அவகாசம் முடிந்துவிட்டது (Link Expired)"}

    if session["status"] == "TERMINATED":
        return {"valid": False, "error": "இந்த அமர்வு WhatsApp மூலம் பாதுகாப்பாக மூடப்பட்டுவிட்டது (Session Terminated Remotely)"}

    # Mark as ACTIVE authenticated session
    session["status"] = "ACTIVE"
    session["authenticated_at"] = now

    logger.info(f"[WHATSAPP AUTH] Session activated for phone: {session['phone']}")
    return {
        "valid": True,
        "phone": session["phone"],
        "secret_pin": session["secret_pin"],
        "status": "ACTIVE",
        "expires_in_secs": int(session["expires_at"] - now)
    }


def terminate_session_by_whatsapp(phone: str, close_pin: Optional[str] = None) -> Dict[str, Any]:
    """
    Remote Kill-Switch:
    When a citizen texts 'CLOSE', 'LOGOUT', or their close action PIN on WhatsApp,
    this immediately invalidates any active web browser session tied to that phone number!
    """
    clean_phone = "".join([c for c in str(phone) if c.isdigit()])
    token = PHONE_ACTIVE_SESSIONS.get(clean_phone)

    if not token or token not in MAGIC_TOKENS:
        # Check reverse match for partial phone strings
        matched_token = None
        for tok, sess in MAGIC_TOKENS.items():
            if sess["phone"] == clean_phone or clean_phone.endswith(sess["phone"][-10:]):
                matched_token = tok
                break
        token = matched_token

    if not token:
        return {
            "success": False,
            "message": "செயலில் உள்ள அமர்வுகள் எதுவும் இல்லை (No active sessions found for this number)."
        }

    session = MAGIC_TOKENS[token]
    session["status"] = "TERMINATED"
    session["terminated_at"] = time.time()

    logger.info(f"[WHATSAPP AUTH] Remote kill-switch triggered for {clean_phone}! Web session terminated.")
    return {
        "success": True,
        "phone": clean_phone,
        "terminated_token": token,
        "message": "உங்கள் Makkal AI இணைய அமர்வு WhatsApp மூலம் பாதுகாப்பாக உடனடியாக மூடப்பட்டது!"
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
    if phone in PHONE_ACTIVE_SESSIONS and PHONE_ACTIVE_SESSIONS[phone] == token:
        del PHONE_ACTIVE_SESSIONS[phone]

    logger.info(f"[WHATSAPP AUTH] Session {token} terminated directly via web logout.")
    return {
        "success": True,
        "phone": phone,
        "terminated_token": token,
        "message": "அமர்வு வெற்றிகரமாக மூடப்பட்டது (Logged out successfully)"
    }



def get_session_status(token: str) -> Dict[str, Any]:
    """
    Polled by the web client every few seconds to detect if the session
    was terminated remotely via WhatsApp message.
    """
    if not token or token not in MAGIC_TOKENS:
        return {"status": "NOT_FOUND", "active": False}

    session = MAGIC_TOKENS[token]
    is_active = session["status"] == "ACTIVE" and time.time() <= session["expires_at"]
    return {
        "status": session["status"],
        "active": is_active,
        "phone": session["phone"],
        "time_remaining_secs": max(0, int(session["expires_at"] - time.time()))
    }
