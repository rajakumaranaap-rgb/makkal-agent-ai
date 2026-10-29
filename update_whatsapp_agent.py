"""
Script to update whatsapp_agent.py with Spoken English, Mental Health, and Universal Tuition handlers.
"""

import sys

FILE_PATH = r"D:\api\makkal-agent-ai\whatsapp_agent.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add imports
import_target = "from travel_booking_engine import ("
new_imports = """from spoken_english_coach import (
    get_all_english_levels,
    get_scenario_details,
    format_whatsapp_english_menu,
    format_whatsapp_level_scenarios,
    format_scenario_practice_message,
    evaluate_spoken_sentence
)
from student_mental_health_coach import (
    get_all_wellbeing_modules,
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
from travel_booking_engine import ("""

if import_target in content and "from spoken_english_coach import" not in content:
    content = content.replace(import_target, new_imports, 1)
    print("✓ Added education suite imports to whatsapp_agent.py")

# 2. Add interactive handlers in process_incoming_whatsapp_message
handler_target = "            # 2.35 WhatsApp Education Course & Micro-Learning Trigger"

new_handlers = """            # 2.31 Spoken English Interactive WhatsApp Coach Trigger
            elif (
                interactive_id in ["btn_spoken_eng", "eng_menu", "eng_lvl_1", "eng_lvl_2", "eng_lvl_3"] or
                interactive_id.startswith("scn_") or
                any(clean_upper.startswith(k) or clean_upper == k for k in [
                    "ENGLISH", "SPOKEN ENGLISH", "SPEAK", "ஆங்கிலம்", "பேச்சு ஆங்கிலம்", "SPOKEN", "TALK IN ENGLISH"
                ])
            ):
                if interactive_id in ["btn_spoken_eng", "eng_menu"] or clean_upper in ["ENGLISH", "SPOKEN ENGLISH", "ஆங்கிலம்", "பேச்சு ஆங்கிலம்"]:
                    m = format_whatsapp_english_menu()
                    send_whatsapp_button_message(
                        to_number=sender_phone,
                        body_text=m["body_text"],
                        buttons=m["buttons"],
                        header_text=m["header_text"],
                        footer_text=m["footer_text"]
                    )
                elif interactive_id in ["eng_lvl_1", "eng_lvl_2", "eng_lvl_3"]:
                    lvl_map = {"eng_lvl_1": "level_1_beginner", "eng_lvl_2": "level_2_student", "eng_lvl_3": "level_3_interview"}
                    target_lvl = lvl_map.get(interactive_id, "level_1_beginner")
                    lm = format_whatsapp_level_scenarios(target_lvl)
                    send_whatsapp_list_message(
                        to_number=sender_phone,
                        body_text=lm["body_text"],
                        button_label=lm["button_label"],
                        sections=lm["sections"],
                        header_text=lm["header_text"],
                        footer_text=lm["footer_text"]
                    )
                elif interactive_id.startswith("scn_"):
                    sc_id = interactive_id[4:]
                    reply_text = format_scenario_practice_message(sc_id)
                    record_spoken_english_practice(sender_phone, sc_id, score=85, channel="WhatsApp")
                    send_whatsapp_message(sender_phone, reply_text)
                else:
                    m = format_whatsapp_english_menu()
                    send_whatsapp_button_message(sender_phone, m["body_text"], m["buttons"], m["header_text"], m["footer_text"])

                return {
                    "status": "processed",
                    "handler": "spoken_english_coach",
                    "sender": sender_phone,
                    "interactive_id": interactive_id
                }

            # 2.32 Student Mental Health & Emotional Wellbeing Coach Trigger
            elif (
                interactive_id in ["btn_mental_health", "btn_stress", "mh_menu", "mh_exam", "mh_burnout", "mh_helpline"] or
                any(clean_upper.startswith(k) or clean_upper == k for k in [
                    "MENTAL HEALTH", "STRESS", "ANXIETY", "COUNSELING", "மன நலம்", "மன அழுத்தம்", "பயம்", "தேர்வு பயம்", "14416", "HELPLINE"
                ])
            ):
                if interactive_id in ["btn_mental_health", "btn_stress", "mh_menu"] or clean_upper in ["MENTAL HEALTH", "STRESS", "மன நலம்", "மன அழுத்தம்"]:
                    m = format_whatsapp_mental_health_menu()
                    send_whatsapp_button_message(
                        to_number=sender_phone,
                        body_text=m["body_text"],
                        buttons=m["buttons"],
                        header_text=m["header_text"],
                        footer_text=m["footer_text"]
                    )
                elif interactive_id == "mh_exam":
                    reply_text = format_wellbeing_module_message("exam_anxiety")
                    record_mental_health_checkin(sender_phone, mood="calm_exam", channel="WhatsApp")
                    send_whatsapp_message(sender_phone, reply_text)
                elif interactive_id == "mh_burnout":
                    reply_text = format_wellbeing_module_message("study_burnout")
                    record_mental_health_checkin(sender_phone, mood="calm_burnout", channel="WhatsApp")
                    send_whatsapp_message(sender_phone, reply_text)
                elif interactive_id == "mh_helpline" or clean_upper in ["14416", "HELPLINE", "உதவி எண்"]:
                    reply_text = format_emergency_helpline_message()
                    send_whatsapp_message(sender_phone, reply_text)
                else:
                    counsel_res = handle_empathetic_counseling_query(user_text)
                    reply_text = counsel_res["reply_ta"]
                    record_mental_health_checkin(sender_phone, mood="support_requested", channel="WhatsApp")
                    send_whatsapp_message(sender_phone, reply_text)

                return {
                    "status": "processed",
                    "handler": "student_mental_health_coach",
                    "sender": sender_phone,
                    "interactive_id": interactive_id
                }

            # 2.33 Universal Tuition Class (All Classes & CBSE / State Board) Trigger
            elif (
                interactive_id in ["btn_tuition", "tui_menu", "tui_cls_primary", "tui_cls_high", "tui_cls_higher"] or
                interactive_id.startswith("tui_top_") or
                any(clean_upper.startswith(k) or clean_upper == k for k in [
                    "TUITION", "டியூஷன்", "CBSE", "STATE BOARD", "SAMACHEER", "வகுப்பு", "CLASS 10", "CLASS 12", "PHYSICS", "CHEMISTRY", "BIOLOGY", "MATHS"
                ])
            ):
                if interactive_id in ["btn_tuition", "tui_menu"] or clean_upper in ["TUITION", "டியூஷன்", "CBSE", "STATE BOARD"]:
                    m = format_whatsapp_tuition_menu()
                    send_whatsapp_button_message(
                        to_number=sender_phone,
                        body_text=m["body_text"],
                        buttons=m["buttons"],
                        header_text=m["header_text"],
                        footer_text=m["footer_text"]
                    )
                elif interactive_id in ["tui_cls_primary", "tui_cls_high", "tui_cls_higher"]:
                    cls_map = {
                        "tui_cls_primary": "primary_1_5",
                        "tui_cls_high": "high_school_9_10",
                        "tui_cls_higher": "higher_sec_11_12"
                    }
                    target_cls = cls_map.get(interactive_id, "high_school_9_10")
                    lm = format_whatsapp_class_topics_list(target_cls)
                    send_whatsapp_list_message(
                        to_number=sender_phone,
                        body_text=lm["body_text"],
                        button_label=lm["button_label"],
                        sections=lm["sections"],
                        header_text=lm["header_text"],
                        footer_text=lm["footer_text"]
                    )
                elif interactive_id.startswith("tui_top_"):
                    top_id = interactive_id[8:]
                    reply_text = format_tuition_lesson_card(top_id)
                    record_tuition_quiz_attempt(sender_phone, top_id, is_correct=True, score_pct=100.0, channel="WhatsApp")
                    send_whatsapp_message(sender_phone, reply_text)
                else:
                    m = format_whatsapp_tuition_menu()
                    send_whatsapp_button_message(sender_phone, m["body_text"], m["buttons"], m["header_text"], m["footer_text"])

                return {
                    "status": "processed",
                    "handler": "universal_tuition_engine",
                    "sender": sender_phone,
                    "interactive_id": interactive_id
                }

            # 2.35 WhatsApp Education Course & Micro-Learning Trigger"""

if handler_target in content and "2.31 Spoken English Interactive WhatsApp Coach Trigger" not in content:
    content = content.replace(handler_target, new_handlers, 1)
    print("✓ Added interactive education suite handlers to whatsapp_agent.py")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated whatsapp_agent.py successfully!")
