"""
Comprehensive test suite for Spoken English, Student Mental Health, Universal Tuition, and Dual Sync
"""

import sys
import json
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spoken_english_coach import (
    get_all_english_levels,
    get_scenario_details,
    format_whatsapp_english_menu,
    format_scenario_practice_message,
    evaluate_spoken_sentence
)
from student_mental_health_coach import (
    get_all_wellbeing_modules,
    get_statutory_helplines,
    format_whatsapp_mental_health_menu,
    format_wellbeing_module_message,
    format_emergency_helpline_message,
    handle_empathetic_counseling_query
)
from universal_tuition_engine import (
    get_all_tuition_classes,
    get_tuition_topic_by_id,
    format_whatsapp_tuition_menu,
    format_whatsapp_class_topics_list,
    format_tuition_lesson_card
)
from student_learning_vault import (
    get_student_profile,
    record_spoken_english_practice,
    record_mental_health_checkin,
    record_tuition_quiz_attempt
)
from whatsapp_agent import process_incoming_whatsapp_message


def run_tests():
    print("=" * 65)
    print("TESTING SPOKEN ENGLISH, MENTAL HEALTH & TUITION ENGINE")
    print("=" * 65)

    # 1. Spoken English Tests
    levels = get_all_english_levels()
    print(f"✓ Spoken English levels loaded: {len(levels)} levels")
    assert len(levels) == 4, f"Expected 4 levels, got {len(levels)}"

    sc_detail = get_scenario_details("self_introduction")
    assert sc_detail is not None, "self_introduction scenario not found!"
    print(f"✓ Scenario found: {sc_detail['scenario']['title_ta']}")

    eval_res = evaluate_spoken_sentence("I am having two brothers and myself Ramesh.")
    print(f"✓ Speech assessment: score={eval_res['score_percentage']}%, corrections={len(eval_res['corrections'])}")
    assert len(eval_res["corrections"]) >= 1, "Expected Tanglish corrections!"

    # 2. Mental Health Tests
    mh_modules = get_all_wellbeing_modules()
    print(f"✓ Mental Health modules loaded: {len(mh_modules)} modules")
    assert len(mh_modules) == 4, f"Expected 4 modules, got {len(mh_modules)}"

    helplines = get_statutory_helplines()
    print(f"✓ Crisis helplines verified: {len(helplines)} helplines (14416 confirmed)")
    assert any("14416" in h["number"] for h in helplines), "14416 Helpline must be present!"

    counsel_res = handle_empathetic_counseling_query("தேர்வுக்கு படிக்க பயமாக உள்ளது, என்ன செய்வது?")
    print(f"✓ Counseling query handled: status={counsel_res['status']}, module={counsel_res.get('matched_module')}")
    assert counsel_res["status"] == "counseling_provided", "Expected counseling_provided!"

    crisis_res = handle_empathetic_counseling_query("எனக்கு தற்கொலை எண்ணம் வருகிறது காப்பாற்றுங்கள்")
    print(f"✓ Crisis intercept verified: is_crisis={crisis_res['is_crisis']}")
    assert crisis_res["is_crisis"] is True, "Crisis must be intercepted!"

    # 3. Universal Tuition Tests
    tuition_classes = get_all_tuition_classes()
    print(f"✓ Tuition classes loaded: {len(tuition_classes)} class levels (Primary to Higher Sec)")
    assert len(tuition_classes) == 4, f"Expected 4 levels, got {len(tuition_classes)}"

    topic = get_tuition_topic_by_id("class10_physics_electricity")
    assert topic is not None, "class10_physics_electricity not found!"
    print(f"✓ Tuition topic verified: {topic['topic']['title_ta']}")

    lesson_msg = format_tuition_lesson_card("class10_physics_electricity")
    assert "V = IR" in lesson_msg, "Ohm's law formula must be in lesson card!"
    print("✓ Tuition lesson card formatted with step-by-step breakdown & quiz")

    # 4. Student Vault Dual Sync Tests
    p = get_student_profile("916381029380")
    print(f"✓ Student Vault Profile loaded: {p['student_name']}, Spoken streak: {p['spoken_english']['streak_days']}")
    
    rec_sp = record_spoken_english_practice("916381029380", "self_introduction", score=90, channel="WhatsApp")
    assert "self_introduction" in rec_sp["spoken_english"]["completed_scenarios"]
    print("✓ Spoken English practice recorded in vault")

    rec_mh = record_mental_health_checkin("916381029380", mood="peaceful", channel="Web")
    assert rec_mh["mental_health"]["latest_mood"] == "peaceful"
    print("✓ Mental Health mood check-in recorded in vault")

    rec_tu = record_tuition_quiz_attempt("916381029380", "class10_physics_electricity", is_correct=True, score_pct=100.0)
    assert "class10_physics_electricity" in rec_tu["tuition_progress"]["completed_topics"]
    print("✓ Tuition quiz attempt recorded in vault")

    # 5. WhatsApp Ingress Trigger Tests
    wa_spoken_payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "btn_spoken_eng", "title": "🗣️ Spoken English"}
                        }
                    }]
                }
            }]
        }]
    }
    wa_spoken_res = process_incoming_whatsapp_message(wa_spoken_payload)
    print(f"✓ WhatsApp Spoken English button ingress: handler={wa_spoken_res.get('handler')}")
    assert wa_spoken_res.get("handler") == "spoken_english_coach"

    wa_mh_payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "mh_exam", "title": "🎯 தேர்வு பயம்"}
                        }
                    }]
                }
            }]
        }]
    }
    wa_mh_res = process_incoming_whatsapp_message(wa_mh_payload)
    print(f"✓ WhatsApp Mental Health button ingress: handler={wa_mh_res.get('handler')}")
    assert wa_mh_res.get("handler") == "student_mental_health_coach"

    wa_tu_payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "tui_cls_high", "title": "⚡ வகுப்பு 9 - 10"}
                        }
                    }]
                }
            }]
        }]
    }
    wa_tu_res = process_incoming_whatsapp_message(wa_tu_payload)
    print(f"✓ WhatsApp Universal Tuition button ingress: handler={wa_tu_res.get('handler')}")
    assert wa_tu_res.get("handler") == "universal_tuition_engine"

    print("=" * 65)
    print("ALL 12 EDUCATION, MENTAL HEALTH & TUITION TESTS PASSED 100%!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
