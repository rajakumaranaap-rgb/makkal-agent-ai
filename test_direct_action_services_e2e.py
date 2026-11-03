# -*- coding: utf-8 -*-
"""
==============================================================================
Test Suite: Ultra-Simplified Direct Action Services & Petition Flow Verification
==============================================================================
Tests that illiterate & rural citizens get direct, 1-2 step responses without
irrelevant text dumps or confusing menus.
==============================================================================
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(r"D:\api\makkal-agent-ai")
sys.path.insert(0, str(ROOT_DIR))

from sia_user_manager import handle_sia_whatsapp_flow

TEST_PHONE = "916381029380"
BASE_URL = "https://regulatory-stack-counter-lady.trycloudflare.com"

def run_tests():
    print("=" * 70)
    print("RUNNING DIRECT ACTION SERVICES & PETITION TEST SUITE")
    print("=" * 70)

    # 1. Test Service 8 Menu response
    res_s8 = handle_sia_whatsapp_flow(TEST_PHONE, "8", BASE_URL)
    assert res_s8 is not None, "Service 8 should return a valid response"
    msg_s8 = res_s8["messages"][0]
    print(f"✓ Test 1: Service 8 Menu Title: {msg_s8.get('header')}")
    buttons_s8 = [b["id"] for b in msg_s8.get("buttons", [])]
    print(f"   Buttons: {buttons_s8}")
    assert "btn_pet_water" in buttons_s8 or "btn_pet_road" in buttons_s8, "Service 8 must offer direct petition choices"

    # 2. Test tapping '📄 மனு PDF' (btn_petition_pdf)
    res_pdf_menu = handle_sia_whatsapp_flow(TEST_PHONE, "📄 மனு PDF", BASE_URL, interactive_id="btn_petition_pdf")
    assert res_pdf_menu is not None, "btn_petition_pdf should be handled directly"
    msg_pm = res_pdf_menu["messages"][0]
    print(f"\n✓ Test 2: 'மனு PDF' Button Prompt: {msg_pm.get('header')}")
    print(f"   Prompt Text:\n   {msg_pm.get('body')[:150]}...")
    pm_buttons = [b["id"] for b in msg_pm.get("buttons", [])]
    print(f"   Buttons: {pm_buttons}")
    assert "btn_pet_water" in pm_buttons, "Must offer direct water petition"
    assert "btn_pet_road" in pm_buttons, "Must offer direct road petition"

    # 3. Test tapping 'btn_pet_water' (Instant PDF Generation & Dispatch)
    print("\n✓ Test 3: Tapping 'btn_pet_water' -> Instant PDF Generation...")
    res_water = handle_sia_whatsapp_flow(TEST_PHONE, "💧 குடிநீர் வசதி மனு", BASE_URL, interactive_id="btn_pet_water")
    assert res_water is not None, "btn_pet_water should return petition response"
    messages_w = res_water.get("messages", [])
    print(f"   Total Messages Dispatched: {len(messages_w)}")
    
    # Check document message
    doc_msg = next((m for m in messages_w if m.get("type") == "document"), None)
    btn_msg = next((m for m in messages_w if m.get("type") == "button"), None)
    
    assert doc_msg is not None, "Must dispatch document (PDF) message"
    print(f"   📄 Dispatched Document URL: {doc_msg.get('document_url')}")
    print(f"   Filename: {doc_msg.get('filename')}")
    
    assert btn_msg is not None, "Must dispatch button confirmation"
    print(f"   Header: {btn_msg.get('header')}")
    print(f"   Confirmation Body:\n   {btn_msg.get('body')[:160]}...")

    # 4. Test Service 1 (Crop Disease Direct Cure)
    print("\n✓ Test 4: Tapping 'btn_crop_blast_cure' (Instant TNAU Bio-Cure)...")
    res_crop = handle_sia_whatsapp_flow(TEST_PHONE, "நெல் குலைநோய் மருந்து", BASE_URL, interactive_id="btn_crop_blast_cure")
    assert res_crop is not None
    msg_crop = res_crop["messages"][0]
    print(f"   Header: {msg_crop.get('header')}")
    print(f"   Cure Body:\n   {msg_crop.get('body')[:150]}...")
    assert "சூடோமோனாஸ்" in msg_crop.get("body", ""), "Must contain bio-cure"

    # 5. Test Service 2 (Cattle Care Mastitis First Aid)
    print("\n✓ Test 5: Tapping 'btn_mastitis_aid' (Instant Mastitis Herbal Remedy)...")
    res_cattle = handle_sia_whatsapp_flow(TEST_PHONE, "மடிநோய் முதலுதவி", BASE_URL, interactive_id="btn_mastitis_aid")
    assert res_cattle is not None
    msg_cattle = res_cattle["messages"][0]
    print(f"   Header: {msg_cattle.get('header')}")
    print(f"   Remedy Body:\n   {msg_cattle.get('body')[:150]}...")
    assert "கற்றாழை" in msg_cattle.get("body", ""), "Must contain aloe vera herbal remedy"

    # 6. Test Service 4 (RedTaxi 1-Tap Booking)
    print("\n✓ Test 6: Tapping 'btn_taxi_instant_book' (Instant RedTaxi Dispatch)...")
    res_taxi = handle_sia_whatsapp_flow(TEST_PHONE, "ஆட்டோ புக் செய்க", BASE_URL, interactive_id="btn_taxi_instant_book")
    assert res_taxi is not None
    msg_taxi = res_taxi["messages"][0]
    print(f"   Header: {msg_taxi.get('header')}")
    print(f"   Taxi Body:\n   {msg_taxi.get('body')[:150]}...")
    assert "6395" in msg_taxi.get("body", ""), "Must contain OTP 6395"

    # 7. Test Service 7 (CBT 5-Minute Quiz)
    print("\n✓ Test 7: Tapping 'btn_quiz_start_now' (Instant 1-Click Quiz)...")
    res_quiz = handle_sia_whatsapp_flow(TEST_PHONE, "5-நிமிட மாதிரி தேர்வு", BASE_URL, interactive_id="btn_quiz_start_now")
    assert res_quiz is not None
    msg_quiz = res_quiz["messages"][0]
    print(f"   Header: {msg_quiz.get('header')}")
    print(f"   Question:\n   {msg_quiz.get('body')[:100]}...")
    assert "அகர முதல" in msg_quiz.get("body", ""), "Must launch question 1"

    print("\n" + "=" * 70)
    print("🎉 ALL 7 DIRECT ACTION & ILLITERATE-FRIENDLY TESTS PASSED 100%!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
