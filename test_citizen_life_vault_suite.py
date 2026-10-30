"""
==============================================================================
Makkal Agent AI - Citizen Sovereign Life Vault & Personal Databases Test Suite
==============================================================================
Validates:
1. All 7 Sovereign Life Vault Pillars:
   - Accounts (Daily In/Outs Ledger & Balance)
   - Contacts DB (Personal & Emergency Services)
   - Proofs DB (Citizen Sovereign Gov Document Vault)
   - Needs & Welfare Tracker (Auto-matching with TN schemes)
   - Diary (Reflections & Mood Tracking)
   - Plans & Goals (Milestones & Targets)
   - Family Bio & PIN-Protected Secret Vault
2. WhatsApp Conversational "Ask and Get" Natural Ingress
3. FastAPI REST Endpoints (/api/vault/*)
==============================================================================
"""

import os
import sys
import json
from typing import Dict, Any

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, r"D:\api\makkal-agent-ai")

# Safe mock for reportlab if missing locally
try:
    import reportlab
except ImportError:
    import types
    reportlab = types.ModuleType("reportlab")
    lib = types.ModuleType("reportlab.lib")
    pagesizes = types.ModuleType("reportlab.lib.pagesizes")
    pagesizes.letter = (612, 792)
    pagesizes.A4 = (595, 842)
    colors = types.ModuleType("reportlab.lib.colors")
    colors.HexColor = lambda c: c
    colors.black = "black"
    colors.white = "white"
    platypus = types.ModuleType("reportlab.platypus")
    class MockDoc:
        def __init__(self, *args, **kwargs): pass
        def build(self, story): pass
    platypus.SimpleDocTemplate = MockDoc
    platypus.Paragraph = lambda t, s: t
    platypus.Spacer = lambda w, h: (w, h)
    platypus.Table = lambda data, **kwargs: data
    platypus.TableStyle = lambda styles: styles
    platypus.KeepTogether = lambda x: x
    platypus.HRFlowable = lambda *args, **kwargs: None
    styles = types.ModuleType("reportlab.lib.styles")
    class MockStyleSheet(dict):
        def add(self, s): pass
    styles.getSampleStyleSheet = lambda: MockStyleSheet()
    styles.ParagraphStyle = lambda *args, **kwargs: {}
    pdfgen = types.ModuleType("reportlab.pdfgen")
    canvas = types.ModuleType("reportlab.pdfgen.canvas")
    canvas.Canvas = lambda *args, **kwargs: None

    sys.modules["reportlab"] = reportlab
    sys.modules["reportlab.lib"] = lib
    sys.modules["reportlab.lib.pagesizes"] = pagesizes
    sys.modules["reportlab.lib.colors"] = colors
    sys.modules["reportlab.platypus"] = platypus
    sys.modules["reportlab.lib.styles"] = styles
    sys.modules["reportlab.pdfgen"] = pdfgen
    sys.modules["reportlab.pdfgen.canvas"] = canvas

from citizen_life_vault_engine import (
    get_or_initialize_user_vault,
    add_account_entry,
    get_accounts_summary,
    add_contact_entry,
    search_contacts,
    get_user_proofs,
    add_user_need,
    add_diary_entry,
    add_plan_entry,
    get_family_bio,
    unlock_secret_vault,
    process_life_vault_conversational_query
)
import whatsapp_agent as wa
from fastapi.testclient import TestClient
from app import app

TEST_PHONE = "6381029380"

def run_vault_test_suite():
    print("=" * 80)
    print("SIA MAKKAL AGENT AI — CITIZEN SOVEREIGN LIFE VAULT TEST SUITE")
    print("Target: Meta AI Developer Hackathon 2026 ($150,000 Grand Prize)")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # 1. ACCOUNTS LEDGER (Daily In & Outs)
    # --------------------------------------------------------------------------
    print("\n[1/7] Testing Accounts Ledger (Daily In & Outs / வரவு செலவு)...")
    res_exp = add_account_entry(TEST_PHONE, "EXPENSE", 450.0, "Food / மளிகை", "மளிகைக் கடை காய்கறிகள்")
    assert res_exp["status"] == "success"
    assert res_exp["entry"]["amount"] == 450.0

    res_inc = add_account_entry(TEST_PHONE, "INCOME", 2000.0, "Farm / விவசாயம்", "நெல் விற்பனை முன் தொகைப் பணம்")
    assert res_inc["status"] == "success"
    assert res_inc["entry"]["amount"] == 2000.0

    summary = get_accounts_summary(TEST_PHONE)
    print(f"  ✅ Accounts Ledger OK: Total Income=₹{summary['total_income']} | Total Expense=₹{summary['total_expense']} | Balance=₹{summary['net_balance']}")
    assert summary["net_balance"] > 0
    assert summary["entries_count"] >= 2

    # --------------------------------------------------------------------------
    # 2. CONTACTS DB (Personal & Emergency Services)
    # --------------------------------------------------------------------------
    print("\n[2/7] Testing Contacts DB (தொடர்புகள்)...")
    res_cnt = add_contact_entry(
        TEST_PHONE,
        name="செல்வம் டிராக்டர் (Selvam Tractor)",
        role="Tractor / உழவு இயந்திரம்",
        contact_phone="9842109876",
        location="வாடிப்பட்டி",
        notes="ஏக்கருக்கு ₹1,200 உழவு கட்டணம்"
    )
    assert res_cnt["status"] == "success"
    
    # Search
    doc_contacts = search_contacts(TEST_PHONE, "doctor")
    assert len(doc_contacts) > 0
    print(f"  ✅ Contacts DB OK: Found {len(doc_contacts)} doctor contact(s): {doc_contacts[0]['name']} ({doc_contacts[0]['phone']})")

    # --------------------------------------------------------------------------
    # 3. PROOFS DB (Sovereign Gov Document Vault)
    # --------------------------------------------------------------------------
    print("\n[3/7] Testing Proofs DB (அரசு ஆவணப் பெட்டகம்)...")
    masked_proofs = get_user_proofs(TEST_PHONE, unmask_with_pin=None)
    assert len(masked_proofs) >= 3
    # Check that aadhaar is masked
    aadhaar_doc = next((p for p in masked_proofs if "aadhaar" in p["id"]), None)
    assert aadhaar_doc is not None
    assert "XXXX" in aadhaar_doc["display_number"]
    print(f"  ✅ Masked Proofs OK: {aadhaar_doc['doc_name_ta']} -> {aadhaar_doc['display_number']}")

    unmasked_proofs = get_user_proofs(TEST_PHONE, unmask_with_pin="7890")
    aadhaar_unmasked = next((p for p in unmasked_proofs if "aadhaar" in p["id"]), None)
    assert "5482" in aadhaar_unmasked["display_number"]
    print(f"  ✅ Unmasked Proof with PIN OK: {aadhaar_unmasked['display_number']}")

    # --------------------------------------------------------------------------
    # 4. NEEDS & WELFARE TRACKER
    # --------------------------------------------------------------------------
    print("\n[4/7] Testing Needs Tracker & Welfare Scheme Matcher (தேவைகள்)...")
    res_need = add_user_need(TEST_PHONE, "2 மூட்டை உரம் தேவை", category="Agriculture", urgency="Urgent")
    assert res_need["status"] == "success"
    need = res_need["need"]
    print(f"  ✅ Need Logged: '{need['title']}' -> Matched Scheme: {need['matched_scheme']}")
    assert "PACCS" in need["matched_scheme"] or "கூட்டுறவு" in need["matched_scheme"]

    # --------------------------------------------------------------------------
    # 5. DIARY & JOURNAL
    # --------------------------------------------------------------------------
    print("\n[5/7] Testing Personal Diary & Mood Tracker (நாட்குறிப்பு)...")
    res_dry = add_diary_entry(TEST_PHONE, "இன்று ஊர் பெரியவர்களுடன் ஆலோசித்து புதிய நீர் பாசன திட்டம் தொடங்கினோம்.", mood="Happy / மகிழ்ச்சி 😊")
    assert res_dry["status"] == "success"
    print(f"  ✅ Diary Entry OK: Date={res_dry['diary_entry']['date']} | Mood={res_dry['diary_entry']['mood']}")

    # --------------------------------------------------------------------------
    # 6. PLANS & GOALS
    # --------------------------------------------------------------------------
    print("\n[6/7] Testing Plans & Goals Board (எதிர்காலத் திட்டங்கள்)...")
    res_pln = add_plan_entry(TEST_PHONE, "மகளுக்கு ஸ்கூட்டர் வாங்க முன்பணம் சேமிப்பு", category="Finance", target_date="2026-12-15", priority="High")
    assert res_pln["status"] == "success"
    print(f"  ✅ Plan Created: '{res_pln['plan']['title']}' | Target: {res_pln['plan']['target_date']}")

    # --------------------------------------------------------------------------
    # 7. FAMILY BIO & PIN-PROTECTED SECRET VAULT
    # --------------------------------------------------------------------------
    print("\n[7/7] Testing Family Bio & PIN-Protected Secret Vault (குடும்பம் & ரகசியம்)...")
    family = get_family_bio(TEST_PHONE)
    assert len(family) >= 3
    print(f"  ✅ Family Bio OK: {len(family)} family members tracked. Sample: {family[0]['name']} (Blood: {family[0]['blood_group']})")

    # Secret Vault: Wrong PIN
    wrong_unlock = unlock_secret_vault(TEST_PHONE, "0000")
    assert wrong_unlock["unlocked"] is False
    print("  ✅ Secret Vault Protected: Access DENIED for invalid PIN.")

    # Secret Vault: Correct PIN
    correct_unlock = unlock_secret_vault(TEST_PHONE, "7890")
    assert correct_unlock["unlocked"] is True
    assert len(correct_unlock["items"]) >= 2
    print(f"  ✅ Secret Vault UNLOCKED with PIN: {len(correct_unlock['items'])} confidential records revealed safely.")

    # --------------------------------------------------------------------------
    # 8. CONVERSATIONAL WHATSAPP INGRESS ("ASK AND GET")
    # --------------------------------------------------------------------------
    print("\n[8/9] Testing WhatsApp Conversational Natural Ingress Flows...")
    
    # 8.1 Expense Voice/Text
    wa_res1 = process_life_vault_conversational_query(TEST_PHONE, "செலவு 250 டீ மற்றும் டிபன்")
    assert wa_res1["status"] == "processed"
    assert "250" in wa_res1["message"]
    print(f"  ✅ WhatsApp Expense Logged OK")

    # 8.2 Balance Query
    wa_res2 = process_life_vault_conversational_query(TEST_PHONE, "என் வரவு செலவு கணக்கு நிலை என்ன?")
    assert wa_res2["status"] == "processed"
    assert "கையிருப்பு மீதி" in wa_res2["message"]
    print(f"  ✅ WhatsApp Balance Query OK")

    # 8.3 Doctor Contact Query
    wa_res3 = process_life_vault_conversational_query(TEST_PHONE, "டாக்டர் போன் நம்பர் என்ன?")
    assert wa_res3["status"] == "processed"
    assert "9840123456" in wa_res3["message"]
    print(f"  ✅ WhatsApp Doctor Contact Query OK")

    # 8.4 Secret Vault Unlock
    wa_res4 = process_life_vault_conversational_query(TEST_PHONE, "ரகசிய பெட்டகம் 7890")
    assert wa_res4["status"] == "processed"
    assert "திறக்கப்பட்டது" in wa_res4["message"]
    print(f"  ✅ WhatsApp Secret Vault Unlocked OK")

    # --------------------------------------------------------------------------
    # 9. FASTAPI REST ENDPOINTS
    # --------------------------------------------------------------------------
    print("\n[9/9] Testing FastAPI REST Endpoints (/api/vault/*)...")
    client = TestClient(app)

    # 9.1 GET /api/vault/{phone}
    r_get = client.get(f"/api/vault/{TEST_PHONE}")
    assert r_get.status_code == 200, f"Error: {r_get.text}"
    v_data = r_get.json()
    assert v_data["status"] == "success"
    assert "accounts_ledger" in v_data["vault"]
    assert "contacts_db" in v_data["vault"]
    assert "proofs_vault" in v_data["vault"]
    assert "family_bio" in v_data["vault"]
    print(f"  ✅ GET /api/vault/{TEST_PHONE} -> 200 OK")

    # 9.2 POST /api/vault/accounts
    r_acc = client.post("/api/vault/accounts", json={
        "phone": TEST_PHONE,
        "type": "EXPENSE",
        "amount": 180.0,
        "category": "Food",
        "description": "மதிய உணவு"
    })
    assert r_acc.status_code == 200
    print(f"  ✅ POST /api/vault/accounts -> 200 OK")

    # 9.3 POST /api/vault/unlock-secret
    r_sec = client.post("/api/vault/unlock-secret", json={
        "phone": TEST_PHONE,
        "pin": "7890"
    })
    assert r_sec.status_code == 200
    assert r_sec.json()["unlocked"] is True
    print(f"  ✅ POST /api/vault/unlock-secret -> 200 OK (Unlocked)")

    # 9.4 WhatsApp Ingress via whatsapp_agent
    wa_payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "91" + TEST_PHONE,
                        "type": "text",
                        "text": {"body": "வரவு செலவு கணக்கு"}
                    }]
                }
            }]
        }]
    }
    wa_ing_res = wa.handle_whatsapp_ingress(wa_payload)
    assert wa_ing_res.get("status") in ["processed", "success"]
    print(f"  ✅ Full WhatsApp Ingress via handle_whatsapp_ingress -> 200 Processed")

    print("\n" + "=" * 80)
    print("🏆 ALL CITIZEN SOVEREIGN LIFE VAULT TESTS PASSED AT 100% SUCCESS!")
    print("================================================================================")


if __name__ == "__main__":
    run_vault_test_suite()
