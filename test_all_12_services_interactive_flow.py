import sys
sys.stdout.reconfigure(encoding='utf-8')

from sia_user_manager import handle_sia_whatsapp_flow

test_phone = "+919876543210"
base_url = "https://example.com"

test_scenarios = [
    # ── Service 1: Crop Pest Selection & Blast Bio-Cure ──
    ("Service 1 Choice Prompt", "btn_crop_pest", "AGRI_CROP_PEST_SELECTION", ["btn_crop_blast", "btn_crop_armyworm", "btn_crop_blight"]),
    ("Service 1 Blast Cure", "btn_crop_blast", "AGRI_CURE_DISPATCHED", ["btn_crop_pest", "btn_menu_all_list"]),
    ("Service 1 Armyworm Cure", "btn_crop_armyworm", "AGRI_ARMYWORM_DISPATCHED", ["btn_crop_pest", "btn_menu_all_list"]),
    ("Service 1 Blight Cure", "btn_crop_blight", "AGRI_BLIGHT_DISPATCHED", ["btn_crop_pest", "btn_menu_all_list"]),

    # ── Service 2: Cattle Mastitis Herbal Aid ──
    ("Service 2 Mastitis Cure", "btn_mastitis_aid", "CATTLE_MASTITIS_DISPATCHED", ["btn_feed_plan", "btn_menu_all_list"]),
    ("Service 2 Milk Booster", "btn_feed_plan", "CATTLE_FEED_DISPATCHED", ["btn_mastitis_aid", "btn_menu_all_list"]),
    ("Service 2 Emergency Vet", "btn_vet_doc", "CATTLE_VET_DISPATCHED", ["btn_mastitis_aid", "btn_menu_all_list"]),

    # ── Service 3: Vyabar Local Store Kit Selection & Confirmation ──
    ("Service 3 Choice Prompt", "store_order", "VYABAR_KIT_SELECTION", ["btn_store_rice_kit", "btn_store_oil_kit", "btn_store_monthly_kit"]),
    ("Service 3 Rice Kit Confirm", "btn_store_rice_kit", "VYABAR_RICE_KIT_CONFIRMED", ["store_order", "btn_menu_all_list"]),
    ("Service 3 Oil Kit Confirm", "btn_store_oil_kit", "VYABAR_OIL_KIT_CONFIRMED", ["store_order", "btn_menu_all_list"]),
    ("Service 3 Monthly Kit Confirm", "btn_store_monthly_kit", "VYABAR_MONTHLY_KIT_CONFIRMED", ["btn_vyabar_status", "btn_menu_all_list"]),

    # ── Service 4: RedTaxi Vehicle Selection & Dispatch ──
    ("Service 4 Choice Prompt", "btn_book_taxi", "TAXI_CHOOSE_SELECTION", ["btn_taxi_auto", "btn_taxi_mini", "btn_taxi_sedan"]),
    ("Service 4 Auto Confirm", "btn_taxi_auto", "TAXI_AUTO_CONFIRMED", ["btn_taxi_sos", "btn_menu_all_list"]),
    ("Service 4 Mini Confirm", "btn_taxi_mini", "TAXI_MINI_CONFIRMED", ["btn_taxi_sos", "btn_menu_all_list"]),
    ("Service 4 Sedan Confirm", "btn_taxi_sedan", "TAXI_SEDAN_CONFIRMED", ["btn_taxi_sos", "btn_menu_all_list"]),

    # ── Service 5: Community Kitchen Food Selection & Orders ──
    ("Service 5 Choice Prompt", "food_order", "FOOD_CHOOSE_SELECTION", ["btn_food_veg", "btn_food_nonveg", "btn_food_tiffin"]),
    ("Service 5 Veg Meals Confirm", "btn_food_veg", "FOOD_VEG_CONFIRMED", ["food_order", "btn_menu_all_list"]),
    ("Service 5 Nonveg Confirm", "btn_food_nonveg", "FOOD_NONVEG_CONFIRMED", ["food_order", "btn_menu_all_list"]),
    ("Service 5 Tiffin Confirm", "btn_food_tiffin", "FOOD_TIFFIN_CONFIRMED", ["food_order", "btn_menu_all_list"]),

    # ── Service 6: Patta Audit & Subdivision Options ──
    ("Service 6 Choice Prompt", "svc_patta", "PATTA_SURVEY_AUDITED", ["btn_patta_non_subdiv", "btn_patta_subdiv", "btn_pet_patta"]),
    ("Service 6 Non-Subdiv Guide", "btn_patta_non_subdiv", "PATTA_NON_SUBDIV_INFO", ["btn_pet_patta", "btn_menu_all_list"]),
    ("Service 6 Subdiv Guide", "btn_patta_subdiv", "PATTA_SUBDIV_INFO", ["btn_pet_patta", "btn_menu_all_list"]),
    ("Service 6 Patta Petition PDF", "btn_pet_patta", "PETITION_GENERATED_DISPATCHED", ["btn_petition_pdf", "btn_menu_all_list"]),

    # ── Service 7: CBT Quiz Subject Selection & Questions ──
    ("Service 7 Subject Prompt", "btn_cbt_quiz", "CBT_SUBJECT_SELECTION", ["btn_cbt_tamil", "btn_cbt_science", "btn_cbt_physics"]),
    ("Service 7 Tamil Question", "btn_cbt_tamil", "CBT_QUESTION_1", ["btn_quiz_opt_b", "btn_quiz_opt_a", "btn_quiz_opt_c"]),
    ("Service 7 Tamil Correct", "btn_quiz_opt_b", "CBT_QUESTION_CORRECT", ["btn_cbt_quiz", "btn_menu_all_list"]),
    ("Service 7 Science Question", "btn_cbt_science", "CBT_QUESTION_SCIENCE", ["btn_quiz_sci_opt_b", "btn_quiz_sci_opt_a", "btn_quiz_sci_opt_c"]),
    ("Service 7 Science Correct", "btn_quiz_sci_opt_b", "CBT_QUESTION_CORRECT", ["btn_cbt_quiz", "btn_menu_all_list"]),
    ("Service 7 Physics Question", "btn_cbt_physics", "CBT_QUESTION_PHYSICS", ["btn_quiz_phy_opt_b", "btn_quiz_phy_opt_a", "btn_quiz_phy_opt_c"]),
    ("Service 7 Physics Correct", "btn_quiz_phy_opt_b", "CBT_QUESTION_CORRECT", ["btn_cbt_quiz", "btn_menu_all_list"]),

    # ── Service 8: Constituency Petition Direct Creation ──
    ("Service 8 Water Petition", "btn_pet_water", "PETITION_GENERATED_DISPATCHED", ["btn_petition_pdf", "btn_menu_all_list"]),
    ("Service 8 Road Petition", "btn_pet_road", "PETITION_GENERATED_DISPATCHED", ["btn_petition_pdf", "btn_menu_all_list"]),
    ("Service 8 Pension Petition", "btn_pet_pension", "PETITION_GENERATED_DISPATCHED", ["btn_petition_pdf", "btn_menu_all_list"]),

    # ── Service 9: Spoken English Studio ──
    ("Service 9 Daily Dialogue", "btn_spoken_start", "SPOKEN_DAILY_PRACTICE", ["btn_spoken_interview", "btn_spoken_voice"]),
    ("Service 9 Job Interview", "btn_spoken_interview", "SPOKEN_INTERVIEW_PRACTICE", ["btn_spoken_start", "btn_spoken_voice"]),
    ("Service 9 Voice Coach", "btn_spoken_voice", "SPOKEN_VOICE_COACH", ["btn_spoken_start", "btn_menu_all_list"]),

    # ── Service 10: Student Mental Health & Tele-MANAS ──
    ("Service 10 Call 14416", "btn_call_14416", "MH_CALL_14416_INFO", ["btn_calm_breath", "btn_counseling"]),
    ("Service 10 Calm Breathing", "btn_calm_breath", "MH_BREATHING_GUIDED", ["btn_call_14416", "btn_menu_all_list"]),
    ("Service 10 Counselor Chat", "btn_counseling", "MH_COUNSELING_DISPATCHED", ["btn_calm_breath", "btn_call_14416"]),

    # ── Service 11: Exam Roadmap Free Notes Selection ──
    ("Service 11 Notes Prompt", "btn_roadmap_study", "EXAM_ROADMAP_NOTES_SELECTION", ["btn_notes_tamil", "btn_notes_maths", "btn_notes_science"]),
    ("Service 11 Tamil Notes", "btn_notes_tamil", "EXAM_NOTES_TAMIL_DELIVERED", ["btn_roadmap_study", "btn_menu_all_list"]),
    ("Service 11 Maths Formulas", "btn_notes_maths", "EXAM_NOTES_MATHS_DELIVERED", ["btn_roadmap_study", "btn_menu_all_list"]),
    ("Service 11 Science Facts", "btn_notes_science", "EXAM_NOTES_SCIENCE_DELIVERED", ["btn_roadmap_study", "btn_menu_all_list"]),

    # ── Service 12: RentO Farm Machinery Attachment Selection ──
    ("Service 12 Implement Prompt", "btn_rent_tractor", "RENTO_TRACTOR_SELECTION", ["btn_tractor_rotavator", "btn_tractor_cultivator", "btn_tractor_trailer"]),
    ("Service 12 Rotavator Confirm", "btn_tractor_rotavator", "RENTO_ROTAVATOR_CONFIRMED", ["btn_rent_tractor", "btn_menu_all_list"]),
    ("Service 12 Cultivator Confirm", "btn_tractor_cultivator", "RENTO_CULTIVATOR_CONFIRMED", ["btn_rent_tractor", "btn_menu_all_list"]),
    ("Service 12 Trailer Confirm", "btn_tractor_trailer", "RENTO_TRAILER_CONFIRMED", ["btn_rent_tractor", "btn_menu_all_list"]),
]

passed = 0
failed = 0

print("=" * 80)
print("  AUDITING ALL 12 SERVICES INTERACTIVE MULTI-CHOICE ARCHITECTURE")
print("=" * 80)

for name, action_input, expected_stage, expected_buttons in test_scenarios:
    res = handle_sia_whatsapp_flow(
        sender_phone=test_phone,
        message_text="",
        public_base_url=base_url,
        msg_type="interactive",
        interactive_id=action_input
    )
    if not res:
        print(f"  [FAIL] {name:32} -> No response returned")
        failed += 1
        continue

    actual_stage = res.get("stage", "UNKNOWN")
    messages = res.get("messages", [])

    actual_buttons = []
    title_len_ok = True
    for m in messages:
        for b in m.get("buttons", []):
            bid = b.get("id")
            btitle = b.get("title", "")
            actual_buttons.append(bid)
            if len(btitle) > 20:
                print(f"  [ERROR] Button title exceeds 20 chars: '{btitle}' ({len(btitle)} chars)")
                title_len_ok = False

    # Stage check
    stage_match = (actual_stage == expected_stage)
    # Buttons check
    buttons_match = all(eb in actual_buttons for eb in expected_buttons)

    if stage_match and buttons_match and title_len_ok:
        passed += 1
        print(f"  [PASS] {name:32} -> stage={actual_stage:30} buttons={len(actual_buttons)}")
    else:
        failed += 1
        print(f"  [FAIL] {name:32}")
        print(f"         Expected: stage={expected_stage}, buttons={expected_buttons}")
        print(f"         Actual:   stage={actual_stage}, buttons={actual_buttons}")

print("=" * 80)
print(f"RESULT: {passed}/{len(test_scenarios)} PASSED ({passed*100/len(test_scenarios):.1f}%), {failed} FAILED")
print("=" * 80)
if failed == 0:
    print("ALL 12 SERVICES PERFECTLY OPTIMIZED! 100% WhatsApp Compliant.")
