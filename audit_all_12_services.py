import sys, os
sys.path.insert(0, r'D:\api\makkal-agent-ai')
sys.stdout.reconfigure(encoding='utf-8')

from sia_user_manager import handle_sia_whatsapp_flow

services = [
    # 1. Agri
    ("btn_menu_1_agri", "Menu 1: Agri"),
    ("btn_crop_pest", "1a: Pest Doctor"),
    ("btn_weather_rep", "1b: Weather Alert"),
    ("btn_machinery_rent", "1c: Farm Machinery"),
    
    # 2. Cattle
    ("btn_menu_2_cattle", "Menu 2: Cattle"),
    ("btn_mastitis_aid", "2a: Mastitis Aid"),
    ("btn_feed_plan", "2b: Milk Booster"),
    ("btn_vet_doc", "2c: Emergency Vet"),
    
    # 3. Store
    ("btn_menu_3_store", "Menu 3: Store"),
    ("store_order", "3a: Store Order"),
    ("store_voice", "3b: Voice Order"),
    ("store_catalog", "3c: Full Catalog"),
    
    # 4. Taxi
    ("btn_menu_4_taxi", "Menu 4: Taxi"),
    ("btn_book_taxi", "4a: Book Taxi"),
    ("btn_taxi_sos", "4b: Taxi SOS"),
    ("btn_taxi_live", "4c: Live Tracking"),
    
    # 5. Food
    ("btn_menu_5_food", "Menu 5: Food"),
    ("food_order", "5a: Food Order"),
    ("food_menu", "5b: Menu Card"),
    ("food_reg_cook", "5c: Register Cook"),
    
    # 6. eSevai
    ("btn_menu_6_patta", "Menu 6: Patta / eSevai"),
    ("svc_patta", "6a: Patta Audit"),
    ("svc_fmb", "6b: FMB Sketch"),
    ("svc_ration", "6c: Ration Card"),
    
    # 7. Education
    ("btn_menu_7_edu", "Menu 7: Education"),
    ("btn_edu_10th", "7a: Class 10"),
    ("btn_edu_12th", "7b: Class 12"),
    ("btn_cbt_quiz", "7c: CBT Quiz"),
    
    # 8. Petition
    ("btn_menu_8_mla", "Menu 8: Petition"),
    ("btn_petition_pdf", "8a: Manu PDF"),
    ("btn_pet_water", "8b: Water Petition"),
    ("btn_pet_road", "8c: Road Petition"),
    ("btn_pet_pension", "8d: Pension Petition"),
    
    # 9. Spoken English
    ("btn_menu_9_spoken", "Menu 9: Spoken English"),
    ("btn_spoken_start", "9a: Start Dialogue"),
    ("btn_spoken_interview", "9b: Job Interview"),
    ("btn_spoken_voice", "9c: Voice Coach"),
    
    # 10. Mental Health
    ("btn_menu_10_mental", "Menu 10: Mental Health"),
    ("btn_call_14416", "10a: Call 14416"),
    ("btn_calm_breath", "10b: Calm Breath"),
    ("btn_counseling", "10c: Chat Counselor"),
    
    # 11. Exam Roadmap
    ("btn_menu_11_exam", "Menu 11: Exam Roadmap"),
    ("btn_roadmap_tnpsc", "11a: TNPSC Roadmap"),
    ("btn_roadmap_neet", "11b: NEET 7.5%"),
    ("btn_roadmap_study", "11c: Free Notes"),
    
    # 12. RentO
    ("btn_menu_12_rento", "Menu 12: RentO Machinery"),
    ("btn_rent_tractor", "12a: Rent Tractor"),
    ("btn_rent_harvester", "12b: Paddy Harvester"),
    ("btn_rent_nearby", "12c: Nearby Machinery"),
]

phone = "919486335870"
base_url = "https://regulatory-stack-counter-lady.trycloudflare.com"

print(f"{'ACTION':<25} | {'DESC':<25} | {'RESULT':<10} | {'STAGE':<30} | {'BUTTONS':<40}")
print("-" * 140)

failures = []
for action_id, desc in services:
    res = handle_sia_whatsapp_flow(phone, "", base_url, msg_type="interactive", interactive_id=action_id, interactive_title="")
    if res is None:
        print(f"{action_id:<25} | {desc:<25} | {'FAILED (None)':<10} | {'FALLTHROUGH_TO_LLM':<30} | {'NONE':<40}")
        failures.append((action_id, desc))
    else:
        stage = res.get("stage", "NO_STAGE")
        msgs = res.get("messages", [])
        btns = []
        for m in msgs:
            if m.get("type") == "button":
                btns = [b.get("title", "") for b in m.get("buttons", [])]
        print(f"{action_id:<25} | {desc:<25} | {'OK':<10} | {stage:<30} | {str(btns):<40}")

print("\n" + "=" * 50)
print(f"Total tested: {len(services)}, Passed: {len(services)-len(failures)}, Failed: {len(failures)}")
if failures:
    print("Failures:")
    for f in failures:
        print(f" - {f[0]}: {f[1]}")
