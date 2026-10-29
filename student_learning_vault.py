"""
==============================================================================
Makkal Agent AI - Student Learning & Wellbeing State Vault (Dual Sync Bridge)
==============================================================================
Target: Meta AI Developer Hackathon 2026 ($150,000 Track)
Role:
Synchronizes Spoken English practice, Mental Health wellbeing check-ins,
and Universal Tuition quiz progress between Meta WhatsApp and Web App in real time.
==============================================================================
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger("makkal.student_vault")

VAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "student_learning_vault.json")


def _load_vault() -> Dict[str, Any]:
    if not os.path.exists(VAULT_PATH):
        return {}
    try:
        with open(VAULT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading student vault: {e}")
        return {}


def _save_vault(vault: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
    with open(VAULT_PATH, "w", encoding="utf-8") as f:
        json.dump(vault, f, ensure_ascii=False, indent=2)


def get_student_profile(phone: str) -> Dict[str, Any]:
    """Retrieves student learning profile with defaults."""
    clean_phone = "".join([c for c in str(phone) if c.isdigit()]) or "919840012345"
    vault = _load_vault()

    if clean_phone not in vault:
        vault[clean_phone] = {
            "phone": clean_phone,
            "student_name": "செல்வன் / செல்வி (Student Scholar)",
            "grade_level": "10th Standard (State Board / CBSE)",
            "spoken_english": {
                "current_level": "level_2_student",
                "completed_scenarios": ["daily_greetings"],
                "total_practice_count": 4,
                "latest_fluency_score": 85,
                "streak_days": 3
            },
            "mental_health": {
                "latest_mood": "calm",
                "checkin_count": 2,
                "completed_breathing_sessions": 3,
                "last_checkin_timestamp": datetime.now().isoformat()
            },
            "tuition_progress": {
                "board": "Tamil Nadu State Board & CBSE",
                "completed_topics": ["class10_physics_electricity", "primary_math_multiplication"],
                "quizzes_taken": 3,
                "average_quiz_score_pct": 92.0
            },
            "last_active_channel": "WhatsApp"
        }
        _save_vault(vault)

    return vault[clean_phone]


def record_spoken_english_practice(phone: str, scenario_id: str, score: int, channel: str = "WhatsApp") -> Dict[str, Any]:
    """Records a completed spoken English session."""
    clean_phone = "".join([c for c in str(phone) if c.isdigit()]) or "919840012345"
    vault = _load_vault()
    prof = get_student_profile(clean_phone)

    if scenario_id not in prof["spoken_english"]["completed_scenarios"]:
        prof["spoken_english"]["completed_scenarios"].append(scenario_id)

    prof["spoken_english"]["total_practice_count"] += 1
    prof["spoken_english"]["latest_fluency_score"] = score
    prof["spoken_english"]["streak_days"] = min(30, prof["spoken_english"]["streak_days"] + 1)
    prof["last_active_channel"] = channel

    vault[clean_phone] = prof
    _save_vault(vault)
    return prof


def record_mental_health_checkin(phone: str, mood: str, session_type: str = "breathing", channel: str = "WhatsApp") -> Dict[str, Any]:
    """Records a mental health mindfulness session."""
    clean_phone = "".join([c for c in str(phone) if c.isdigit()]) or "919840012345"
    vault = _load_vault()
    prof = get_student_profile(clean_phone)

    prof["mental_health"]["latest_mood"] = mood
    prof["mental_health"]["checkin_count"] += 1
    prof["mental_health"]["completed_breathing_sessions"] += 1
    prof["mental_health"]["last_checkin_timestamp"] = datetime.now().isoformat()
    prof["last_active_channel"] = channel

    vault[clean_phone] = prof
    _save_vault(vault)
    return prof


def record_tuition_quiz_attempt(phone: str, topic_id: str, is_correct: bool, score_pct: float, channel: str = "WhatsApp") -> Dict[str, Any]:
    """Records tuition quiz completion."""
    clean_phone = "".join([c for c in str(phone) if c.isdigit()]) or "919840012345"
    vault = _load_vault()
    prof = get_student_profile(clean_phone)

    if topic_id not in prof["tuition_progress"]["completed_topics"]:
        prof["tuition_progress"]["completed_topics"].append(topic_id)

    old_quizzes = prof["tuition_progress"]["quizzes_taken"]
    old_avg = prof["tuition_progress"]["average_quiz_score_pct"]
    new_quizzes = old_quizzes + 1
    new_avg = round(((old_avg * old_quizzes) + score_pct) / new_quizzes, 1)

    prof["tuition_progress"]["quizzes_taken"] = new_quizzes
    prof["tuition_progress"]["average_quiz_score_pct"] = new_avg
    prof["last_active_channel"] = channel

    vault[clean_phone] = prof
    _save_vault(vault)
    return prof


if __name__ == "__main__":
    p = get_student_profile("6381029380")
    print("Student Profile loaded:", p["student_name"], "Streak:", p["spoken_english"]["streak_days"])
