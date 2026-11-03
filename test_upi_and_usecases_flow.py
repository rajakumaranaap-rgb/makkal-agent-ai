import sys
sys.stdout.reconfigure(encoding='utf-8')

from sia_user_manager import handle_sia_whatsapp_flow

test_phone = "+919876543210"
base_url = "https://example.com"

scenarios = [
    # ── Service 1: Crop Cures with UPI ──
    ("Svc 1 Blast UPI", "btn_crop_blast", "AGRI_CURE_DISPATCHED", "80.00", ["btn_upi_paid_agri", "btn_cod_agri"]),
    ("Svc 1 Armyworm UPI", "btn_crop_armyworm", "AGRI_ARMYWORM_DISPATCHED", "110.00", ["btn_upi_paid_agri", "btn_cod_agri"]),
    ("Svc 1 Blight UPI", "btn_crop_blight", "AGRI_BLIGHT_DISPATCHED", "95.00", ["btn_upi_paid_agri", "btn_cod_agri"]),

    # ── Service 2: Cattle Care with UPI ──
    ("Svc 2 Mastitis Kit UPI", "btn_mastitis_aid", "CATTLE_MASTITIS_DISPATCHED", "45.00", ["btn_upi_paid_cattle", "btn_cod_cattle"]),
    ("Svc 2 Feed Pack UPI", "btn_feed_plan", "CATTLE_FEED_DISPATCHED", "120.00", ["btn_upi_paid_cattle", "btn_cod_cattle"]),

    # ── Service 3: Vyabar Grocery Kits with UPI ──
    ("Svc 3 Rice Kit UPI", "btn_store_rice_kit", "VYABAR_RICE_KIT_CONFIRMED", "450.00", ["btn_upi_paid_store", "btn_cod_store"]),
    ("Svc 3 Oil Kit UPI", "btn_store_oil_kit", "VYABAR_OIL_KIT_CONFIRMED", "380.00", ["btn_upi_paid_store", "btn_cod_store"]),
    ("Svc 3 Monthly Kit UPI", "btn_store_monthly_kit", "VYABAR_MONTHLY_KIT_CONFIRMED", "1200.00", ["btn_upi_paid_store", "btn_cod_store"]),

    # ── Service 4: RedTaxi with UPI ──
    ("Svc 4 Auto Ride UPI", "btn_taxi_auto", "TAXI_AUTO_CONFIRMED", "60.00", ["btn_upi_paid_taxi", "btn_cod_taxi"]),
    ("Svc 4 Mini Car UPI", "btn_taxi_mini", "TAXI_MINI_CONFIRMED", "140.00", ["btn_upi_paid_taxi", "btn_cod_taxi"]),
    ("Svc 4 Sedan AC UPI", "btn_taxi_sedan", "TAXI_SEDAN_CONFIRMED", "250.00", ["btn_upi_paid_taxi", "btn_cod_taxi"]),

    # ── Service 5: Community Kitchen with UPI ──
    ("Svc 5 Veg Meals UPI", "btn_food_veg", "FOOD_VEG_CONFIRMED", "65.00", ["btn_upi_paid_food", "btn_cod_food"]),
    ("Svc 5 Nonveg Meals UPI", "btn_food_nonveg", "FOOD_NONVEG_CONFIRMED", "140.00", ["btn_upi_paid_food", "btn_cod_food"]),
    ("Svc 5 Hot Tiffin UPI", "btn_food_tiffin", "FOOD_TIFFIN_CONFIRMED", "40.00", ["btn_upi_paid_food", "btn_cod_food"]),

    # ── Service 6: Patta Subdivision Challan UPI ──
    ("Svc 6 Subdiv Challan UPI", "btn_patta_subdiv", "PATTA_SUBDIV_INFO", "60.00", ["btn_upi_paid_patta", "btn_pet_patta"]),

    # ── Service 12: RentO Farm Machinery Advance Token UPI ──
    ("Svc 12 Rotavator Advance UPI", "btn_tractor_rotavator", "RENTO_ROTAVATOR_CONFIRMED", "100.00", ["btn_upi_paid_rento", "btn_cod_rento"]),
    ("Svc 12 Cultivator Advance UPI", "btn_tractor_cultivator", "RENTO_CULTIVATOR_CONFIRMED", "100.00", ["btn_upi_paid_rento", "btn_cod_rento"]),
    ("Svc 12 Trailer Advance UPI", "btn_tractor_trailer", "RENTO_TRAILER_CONFIRMED", "100.00", ["btn_upi_paid_rento", "btn_cod_rento"]),

    # ── Universal Payment Verifications ──
    ("UPI Payment Verified (Agri)", "btn_upi_paid_agri", "UPI_PAYMENT_VERIFIED", None, ["btn_order_status", "btn_menu_all_list"]),
    ("UPI Payment Verified (Store)", "btn_upi_paid_store", "UPI_PAYMENT_VERIFIED", None, ["btn_order_status", "btn_menu_all_list"]),
    ("UPI Payment Verified (Food)", "btn_upi_paid_food", "UPI_PAYMENT_VERIFIED", None, ["btn_order_status", "btn_menu_all_list"]),
    ("UPI Payment Verified (Generic)", "btn_upi_paid", "UPI_PAYMENT_VERIFIED", None, ["btn_order_status", "btn_menu_all_list"]),
    ("COD Registered (Store)", "btn_cod_store", "COD_PAYMENT_REGISTERED", None, ["btn_order_status", "btn_menu_all_list"]),
    ("COD Registered (Food)", "btn_cod_food", "COD_PAYMENT_REGISTERED", None, ["btn_order_status", "btn_menu_all_list"]),
    ("Order Status Tracking", "btn_order_status", "ORDER_STATUS_CHECK", None, ["btn_menu_all_list"]),
]

passed = 0
failed = 0

print("=" * 85)
print("  AUDITING FULL SPECTRUM LOCAL SERVICES WITH 1-CLICK UPI & QR CODE FLOW")
print("=" * 85)

for name, action_id, expected_stage, expected_amt, expected_buttons in scenarios:
    res = handle_sia_whatsapp_flow(
        sender_phone=test_phone,
        message_text="",
        public_base_url=base_url,
        msg_type="interactive",
        interactive_id=action_id
    )
    if not res:
        print(f"  [FAIL] {name:32} -> No response returned")
        failed += 1
        continue

    actual_stage = res.get("stage", "UNKNOWN")
    messages = res.get("messages", [])
    
    stage_ok = (actual_stage == expected_stage)
    
    actual_buttons = []
    has_upi_link = False
    has_qr_url = False
    amt_match = True

    for m in messages:
        body = m.get("body", "")
        if "upi://pay?pa=" in body:
            has_upi_link = True
        if "https://api.qrserver.com/v1/create-qr-code" in body:
            has_qr_url = True
        if expected_amt and (f"₹{expected_amt}" not in body and expected_amt not in body):
            amt_match = False
        for b in m.get("buttons", []):
            actual_buttons.append(b.get("id"))

    buttons_ok = all(eb in actual_buttons for eb in expected_buttons)

    # For payment scenarios: ensure UPI link and QR URL are both present
    upi_ok = True
    if expected_amt:
        upi_ok = has_upi_link and has_qr_url and amt_match

    if stage_ok and buttons_ok and upi_ok:
        passed += 1
        print(f"  [PASS] {name:32} -> stage={actual_stage:30} upi={has_upi_link} qr={has_qr_url}")
    else:
        failed += 1
        print(f"  [FAIL] {name:32}")
        print(f"         stage_ok={stage_ok} (act={actual_stage}, exp={expected_stage})")
        print(f"         buttons_ok={buttons_ok} (act={actual_buttons}, exp={expected_buttons})")
        print(f"         upi_ok={upi_ok} (has_upi={has_upi_link}, has_qr={has_qr_url}, amt={expected_amt})")

print("=" * 85)
print(f"RESULT: {passed}/{len(scenarios)} PASSED ({passed*100/len(scenarios):.1f}%), {failed} FAILED")
print("=" * 85)
