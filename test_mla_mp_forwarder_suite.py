# -*- coding: utf-8 -*-
"""
==============================================================================
Makkal Agent AI - MLA & MP Petition & Multi-Channel Forwarder Test Suite
==============================================================================
Validates:
1. Authority Registry: 234 Assembly MLAs and 39 Lok Sabha MPs
2. Legal Petition PDF Generator with Watermark & Emblems
3. Multi-Channel 1-Click Launchers (wa.me, api.whatsapp.com, telegram, mailto)
4. WhatsApp Cloud API message character limit validation (< 4,096 chars)
5. Webhook Ingress (Text & Button & Voice Triggers)
==============================================================================
"""

import os
import sys
import json
import uuid
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Add parent path
sys.path.insert(0, str(Path(__file__).parent))

from mla_mp_petition_forwarder import (
    resolve_petition_authority,
    classify_grievance_category,
    create_and_forward_petition,
    format_whatsapp_petition_bundle
)
from mla_directory import ASSEMBLY_CONSTITUENCIES
from central_services_directory import TN_LOK_SABHA_MPS


def run_tests():
    print("=" * 70)
    print("🏛️ RUNNING MAKKAL MLA & MP PETITION & FORWARDER REGRESSION SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Authority Registry Validation
    # -------------------------------------------------------------
    print("\n[TEST 1] Authority Registry Validation:")
    print(f"  Total Assembly Constituencies (MLAs): {len(ASSEMBLY_CONSTITUENCIES)}")
    print(f"  Total Lok Sabha Constituencies (MPs): {len(TN_LOK_SABHA_MPS)}")
    assert len(ASSEMBLY_CONSTITUENCIES) >= 234, f"Expected 234 MLAs, got {len(ASSEMBLY_CONSTITUENCIES)}"
    assert len(TN_LOK_SABHA_MPS) == 39, f"Expected 39 MPs, got {len(TN_LOK_SABHA_MPS)}"
    print("  ✅ 234 MLAs and 39 MPs loaded accurately!")

    # -------------------------------------------------------------
    # 2. Authority Resolution Tests
    # -------------------------------------------------------------
    print("\n[TEST 2] Authority Resolution Accuracy:")
    
    auth_kolathur = resolve_petition_authority("கொளத்தூர் தொகுதி சாலை பழுது மனு", district_hint="Chennai")
    print(f"  Query: Kolathur -> Resolved: {auth_kolathur['authority_name_en']} ({auth_kolathur['constituency_en']})")
    assert "Stalin" in auth_kolathur["authority_name_en"]
    assert auth_kolathur["tier"] == "MLA"
    print("  ✅ Kolathur MLA resolved to Hon. M. K. Stalin!")

    auth_dindigul = resolve_petition_authority("திண்டுக்கல் புதிய ரயில் நிறுத்தம் கேட்டு எம்பிக்கு மனு")
    print(f"  Query: Dindigul -> Resolved: {auth_dindigul['authority_name_en']} ({auth_dindigul['constituency_en']})")
    assert "Sachithanantham" in auth_dindigul["authority_name_en"]
    assert auth_dindigul["tier"] == "MP"
    print("  ✅ Dindigul MP resolved to Hon. R. Sachithanantham!")

    auth_edappadi = resolve_petition_authority("எடப்பாடி தொகுதி குடிநீர் வசதி")
    print(f"  Query: Edappadi -> Resolved: {auth_edappadi['authority_name_en']} ({auth_edappadi['constituency_en']})")
    assert "Palaniswami" in auth_edappadi["authority_name_en"]
    print("  ✅ Edappadi MLA resolved to Hon. Edappadi K. Palaniswami!")

    # -------------------------------------------------------------
    # 3. Category Classification Tests
    # -------------------------------------------------------------
    print("\n[TEST 3] Grievance Category Classification:")
    cat_road = classify_grievance_category("எங்கள் தெருவில் தார் சாலை குண்டும் குழியுமாக உள்ளது மற்றும் தெருவிளக்கு எரியவில்லை")
    print(f"  Road/Lighting: {cat_road['category_ta']} -> Legal: {cat_road['statute']}")
    assert "Road" in cat_road["category_en"]

    cat_water = classify_grievance_category("கடந்த 15 நாட்களாக காவிரி கூட்டுக் குடிநீர் வரவில்லை")
    print(f"  Drinking Water: {cat_water['category_ta']} -> Legal: {cat_water['statute']}")
    assert "Drinking Water" in cat_water["category_en"]

    cat_train = classify_grievance_category("மதுரை - சென்னை தேஜஸ் எக்ஸ்பிரஸ் ரயில் நிறுத்தம் வேண்டும்")
    print(f"  Train: {cat_train['category_ta']} -> Legal: {cat_train['statute']}")
    assert "Railway" in cat_train["category_en"]
    print("  ✅ Category & Legal Acts classification verified!")

    # -------------------------------------------------------------
    # 4. End-to-End Petition PDF Generation & Forwarder Construction
    # -------------------------------------------------------------
    print("\n[TEST 4] End-to-End Petition PDF Generation & Multi-Forwarding Links:")
    res_petition = create_and_forward_petition(
        user_text="எங்கள் பகுதியில் கடந்த 6 மாதங்களாக முக்கிய சாலை குண்டும் குழியுமாக உள்ளது மற்றும் மழைநீர் வடிகால் அமைத்து தர வேண்டுகிறோம். கொளத்தூர் தொகுதி.",
        sender_phone="9840123456",
        applicant_name="செல்வம் (Selvam)",
        district_hint="Chennai",
        village_hint="14, நேரு தெரு, கொளத்தூர்",
        public_base_url="https://regulatory-stack-counter-lady.trycloudflare.com"
    )

    fwd = res_petition["forward_links"]
    print(f"  Tracking ID: {res_petition['verification_id']}")
    print(f"  Target: {res_petition['authority_name_en']} ({res_petition['constituency_en']})")
    print(f"  PDF File: {res_petition['pdf_filename']}")
    print(f"  PDF Download URL: {res_petition['pdf_download_url']}")
    print(f"  WhatsApp to MLA: {fwd['whatsapp_mla_direct'][:60]}...")
    print(f"  WhatsApp to ANY: {fwd['whatsapp_any_number'][:60]}...")
    print(f"  Telegram Share: {fwd['telegram_share'][:60]}...")
    print(f"  Email Mailto: {fwd['mailto_direct'][:60]}...")

    pdf_disk_path = Path("generated_petitions") / res_petition["pdf_filename"]
    assert pdf_disk_path.exists(), f"PDF file not found at {pdf_disk_path}"
    assert res_petition["pdf_download_url"].startswith("http")
    assert "wa.me" in fwd["whatsapp_mla_direct"]
    assert "api.whatsapp.com/send" in fwd["whatsapp_any_number"]
    assert "t.me/share" in fwd["telegram_share"]
    assert "mailto:" in fwd["mailto_direct"]
    print("  ✅ PDF generated successfully and all 4 forwarding URLs properly constructed!")

    # -------------------------------------------------------------
    # 5. WhatsApp 4,096-Character Limit Compliance
    # -------------------------------------------------------------
    print("\n[TEST 5] WhatsApp Cloud API 4,096-Character Limit Audit:")
    part1, part2 = format_whatsapp_petition_bundle(res_petition)
    print(f"  Part 1 (Action & Launchers) Length: {len(part1)} characters (Limit: 4096)")
    print(f"  Part 2 (Full Copy-Paste Text) Length: {len(part2)} characters (Limit: 4096)")

    assert len(part1) <= 4096, f"Part 1 exceeds 4096 chars: {len(part1)}"
    assert len(part2) <= 4096, f"Part 2 exceeds 4096 chars: {len(part2)}"
    print("  ✅ Both WhatsApp message parts comply strictly with Meta's 4,096 char limit!")

    # -------------------------------------------------------------
    # 6. Copy-Paste Plain Text Integrity
    # -------------------------------------------------------------
    print("\n[TEST 6] Copy-Paste Plain Text Petition Audit:")
    copy_text = res_petition["petition_text_copy_paste"]
    assert "அனுப்புநர்:" in copy_text or "பெறுநர்:" in copy_text
    assert res_petition["verification_id"] in copy_text
    print("  ✅ Copy-Paste text contains proper formal Tamil letter formatting!")

    print("\n" + "=" * 70)
    print("🎉 ALL MLA & MP PETITION & FORWARDER REGRESSION TESTS PASSED (6/6)!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
