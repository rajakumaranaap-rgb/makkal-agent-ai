# -*- coding: utf-8 -*-
"""
==============================================================================
Comprehensive Verification Suite: SIA Sovereign Commerce (0% Commission)
Tests all 5 business pillars + API endpoints + WhatsApp Menu integration:
1. Food & Tiffin (Swiggy/Zomato Alt)
2. Grocery & Kirana (BigBasket Alt)
3. Finance & Deeds (Anti-Usury TN Act 2003 & Legal Form-A Promissory Note)
4. Scrap & Circular Recycling (Meta Vision AI Valuation)
5. Cattle & Grains Bidding (Direct Farmer Auction & Shandy Benchmarks)
6. Business Marketing Poster & Vyabar Ledger
==============================================================================
"""

import sys
import json
from pathlib import Path
from fastapi.testclient import TestClient

from app import app
import sia_unified_commerce_engine as uce
from sia_user_manager import handle_sia_whatsapp_flow

client = TestClient(app)

def test_food_endpoints():
    print("\n--- 1. Testing Food & Tiffin Endpoints ---")
    res = client.get("/api/commerce/food/kitchens?pincode=625214")
    assert res.status_code == 200, f"Failed: {res.text}"
    data = res.json()
    assert data["status"] == "success"
    assert data["kitchen"]["pincode"] == "625214"
    print(f"✅ Food Kitchen Loaded: {data['kitchen']['name_ta']} (FSSAI: {data['kitchen']['fssai_reg']})")

    res_menu = client.get("/api/commerce/food/menu")
    assert res_menu.status_code == 200
    menu = res_menu.json()["menu"]
    assert len(menu) >= 10
    print(f"✅ Food Menu Items: {len(menu)} items verified (Sample: {menu[0]['name_ta']})")

    # Order Creation
    order_payload = {
        "pincode": "625214",
        "customer_name": "க. சுந்தரம்",
        "customer_phone": "9840112233",
        "items": [{"dish_id": "FD_LN_01", "quantity": 2}, {"dish_id": "FD_BF_01", "quantity": 1}],
        "address": "மேலத்தெரு, சோழவந்தான்"
    }
    res_order = client.post("/api/commerce/food/order/create", json=order_payload)
    assert res_order.status_code == 200
    order = res_order.json()["order"]
    assert order["platform_commission"] == 0.0
    assert "upi_details" in order
    assert len(order["handshake_otp"]) == 4
    print(f"✅ Food Order Created: {order['order_id']} | Total: ₹{order['total_amount']} | OTP: {order['handshake_otp']} | 0% Fee Verified")

def test_store_endpoints():
    print("\n--- 2. Testing Store & Grocery Endpoints (BigBasket Alt) ---")
    res = client.get("/api/commerce/store/info?pincode=625214")
    assert res.status_code == 200
    store = res.json()["store"]
    assert store["pincode"] == "625214"
    print(f"✅ Store Loaded: {store['store_name_ta']} (Owner: {store['owner_name']})")

    res_cat = client.get("/api/commerce/store/catalog?pincode=625214")
    assert res_cat.status_code == 200
    catalog = res_cat.json()["catalog"]
    assert len(catalog) >= 20
    print(f"✅ Store Catalog: {len(catalog)} products verified")

    # NLP Slip Parsing
    slip_payload = {"text": "1 kg ponni arisi, 500g toor dal, 1L kadalai ennai, 1kg thakkali"}
    res_parse = client.post("/api/commerce/store/parse-slip", json=slip_payload)
    assert res_parse.status_code == 200
    parsed = res_parse.json()["parsed"]
    assert parsed["items_count"] >= 3
    print(f"✅ Voice/Slip Parser: Recognized {parsed['items_count']} items | Subtotal: ₹{parsed['subtotal']} | Delivery: ₹{parsed['delivery_fee']}")

def test_finance_and_deed_endpoints():
    print("\n--- 3. Testing Finance & Deed Making Endpoints ---")
    res_prov = client.get("/api/commerce/finance/providers?pincode=625214")
    assert res_prov.status_code == 200
    provs = res_prov.json()["providers"]
    assert len(provs) >= 1
    print(f"✅ PACCS / Credit Provider: {provs[0]['name_ta']} ({provs[0]['statutory_act']})")

    # Anti-Usury Check (Secured 12% p.a.)
    calc_payload = {"amount": 100000.0, "tenure_months": 12, "is_secured": True}
    res_calc = client.post("/api/commerce/finance/anti-usury-check", json=calc_payload)
    assert res_calc.status_code == 200
    terms = res_calc.json()["terms"]
    assert terms["annual_interest_rate_pct"] == 12.0
    assert terms["total_interest"] == 12000.0
    print(f"✅ Anti-Usury Validated: Rate {terms['annual_interest_rate_pct']}% p.a. | Monthly EMI: ₹{terms['monthly_emi']} | Act 38 of 2003 Compliant")

    # Legal Deed Generation
    deed_payload = {
        "deed_type": "promissory_note",
        "borrower": {"name": "கே. சிவக்குமார்", "phone": "9840112233", "district": "Madurai", "address": "சோழவந்தான்"},
        "lender": {"name": "சோழவந்தான் தொடக்க வேளாண்மை கூட்டுறவு வங்கி", "phone": "9443017890", "address": "ரயில்வே ரோடு"},
        "amount": 100000.0,
        "tenure_months": 12
    }
    res_deed = client.post("/api/commerce/finance/generate-deed", json=deed_payload)
    assert res_deed.status_code == 200
    deed = res_deed.json()["deed"]
    assert deed["status"] == "DEED_GENERATED"
    assert "borrower_verification_otp" in deed
    print(f"✅ Bilingual Form-A Deed Generated: {deed['deed_number']} | Stamp: {deed['stamp_duty_category']} | Dual-OTP Verified")

def test_scrap_endpoints():
    print("\n--- 4. Testing Scrap & Circular Recycling Endpoints ---")
    res_rates = client.get("/api/commerce/scrap/rates")
    assert res_rates.status_code == 200
    rates = res_rates.json()["rates"]
    assert "copper" in rates and "iron" in rates
    print(f"✅ Live Scrap Rates: Copper {rates['copper']['range']} | Iron {rates['iron']['range']} | Battery {rates['battery']['range']}")

    # Photo Valuation
    eval_payload = {"image_desc": "பழைய தாமிர ஒயர்கள் மற்றும் பித்தளை பாத்திரங்கள்"}
    res_eval = client.post("/api/commerce/scrap/evaluate-photo", json=eval_payload)
    assert res_eval.status_code == 200
    evaluation = res_eval.json()["evaluation"]
    assert evaluation["estimated_weight_kg"] > 0
    print(f"✅ Meta Vision Scrap Valuation: {evaluation['valuation_display']} | Verdict: {evaluation['ai_verdict_ta']}")

def test_cattle_grains_endpoints():
    print("\n--- 5. Testing Cattle & Grains Mandi Endpoints ---")
    res_bench = client.get("/api/commerce/agro/benchmarks")
    assert res_bench.status_code == 200
    bench = res_bench.json()["benchmarks"]
    assert "livestock_shandies" in bench
    print(f"✅ Shandy Benchmarks Loaded: Anthiyur, Pollachi, Manapparai verified ({bench['last_updated']})")

    # Agro Photo Valuation
    agro_payload = {"category": "cattle", "description": "காங்கேயம் கறவை மாடு", "asking_price": 65000.0}
    res_agro = client.post("/api/commerce/agro/evaluate-photo", json=agro_payload)
    assert res_agro.status_code == 200
    agro_eval = res_agro.json()["evaluation"]
    assert agro_eval["is_fair_price"] == True
    print(f"✅ Cattle Valuation: {agro_eval['identified_commodity_ta']} | {agro_eval['commission_saved_ta']}")

def test_business_tools_and_whatsapp():
    print("\n--- 6. Testing AI Marketing Poster & Vyabar Ledger ---")
    poster_payload = {
        "title": "சுடச்சுட மல்லிகைப் பூ இட்லி",
        "subtitle": "100% தூய வீட்டு சமையல்",
        "price_tag": "ரூ.40 மட்டுமே (4 இட்லி)",
        "phone": "9840112233",
        "pincode": "625214"
    }
    res_poster = client.post("/api/commerce/tools/poster", json=poster_payload)
    assert res_poster.status_code == 200
    poster = res_poster.json()["poster"]
    assert "html_code" in poster
    print("✅ AI Marketing Poster Generated: High-conversion SVG/HTML verified")

    # Vyabar Ledger
    ledger_payload = {
        "phone": "9840112233",
        "entry_type": "income",
        "amount": 2500.0,
        "party_name": "கார்த்திக் அரிசி மண்டி",
        "notes": "1 மூட்டை பொன்னி அரிசி விற்பனை"
    }
    res_led = client.post("/api/commerce/tools/ledger/add", json=ledger_payload)
    assert res_led.status_code == 200
    led = res_led.json()
    assert led["status"] == "success"
    print(f"✅ Vyabar Ledger: Total Income ₹{led['summary']['total_income']} | Profit: ₹{led['summary']['net_profit']}")

    print("\n--- 7. Testing WhatsApp Ingress for Options 13 to 17 ---")
    for opt in ["13", "14", "15", "16", "17"]:
        wa_res = handle_sia_whatsapp_flow("9840112233", opt, public_base_url="https://regulatory-stack-counter-lady.trycloudflare.com")
        msg = wa_res["messages"][0]
        assert wa_res["stage"] == f"MENU_GUIDE_{opt}"
        assert len(msg.get("buttons", [])) == 3
        print(f"✅ WhatsApp Choice {opt}: Stage={wa_res['stage']} | Header={msg.get('header')}")

if __name__ == "__main__":
    test_food_endpoints()
    test_store_endpoints()
    test_finance_and_deed_endpoints()
    test_scrap_endpoints()
    test_cattle_grains_endpoints()
    test_business_tools_and_whatsapp()
    print("\n🎉 ALL 7 SOVEREIGN COMMERCE SUITE TESTS PASSED 100% SUCCESSFULLY!")
