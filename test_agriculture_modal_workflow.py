"""
==============================================================================
Test Suite: Makkal Agent AI - Agriculture, Modal GPU & Farmer Welfare
==============================================================================
"""

import io
import sys
import unittest
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from agriculture_engine import (
    get_crop_diseases_list,
    get_all_mandi_prices,
    get_farmer_schemes,
    get_modal_architecture_info
)
from modal_sam_agri_bridge import modal_sam_agri_bridge
from action_executor import action_executor
from meta_client import meta_client
from whatsapp_agent import handle_text_query, process_incoming_whatsapp_message


class TestAgricultureModalWorkflow(unittest.TestCase):

    def test_01_crop_disease_directory(self):
        """Validates Tamil Nadu crop diseases catalog and TNAU rules."""
        crops = get_crop_diseases_list()
        self.assertGreaterEqual(len(crops), 4)
        crop_keys = [c["crop_key"] for c in crops]
        self.assertIn("paddy", crop_keys)
        self.assertIn("sugarcane", crop_keys)
        self.assertIn("banana", crop_keys)
        self.assertIn("cotton", crop_keys)
        print("  ✓ Test 01 Passed: Crop disease catalog verified with TNAU rules.")

    def test_02_mandi_price_board(self):
        """Validates live Uzhavar Sandhai and APMC mandi price boards."""
        mandi = get_all_mandi_prices()
        self.assertIn("markets", mandi)
        market_ids = [m["market_id"] for m in mandi["markets"]]
        self.assertIn("koyambedu_chennai", market_ids)
        self.assertIn("paravai_madurai", market_ids)
        self.assertIn("thanjavur_paddy_mandi", market_ids)
        print("  ✓ Test 02 Passed: Mandi prices board returns active markets & commodities.")

    def test_03_farmer_schemes_directory(self):
        """Validates farmer welfare schemes (PM-KISAN, Free Power, PMFBY)."""
        schemes = get_farmer_schemes()
        scheme_ids = [s["id"] for s in schemes]
        self.assertIn("pm_kisan", scheme_ids)
        self.assertIn("tn_free_electricity", scheme_ids)
        self.assertIn("pmfby_crop_insurance", scheme_ids)
        self.assertIn("pm_kusum_solar_pump", scheme_ids)
        print("  ✓ Test 03 Passed: Farmer welfare schemes verified.")

    def test_04_modal_sam_vision_bridge(self):
        """Validates SAM 3.1 leaf lesion segmentation on Modal Serverless GPU bridge."""
        dummy_leaf = b"sample_crop_leaf_binary_content"
        res = modal_sam_agri_bridge.analyze_crop_leaf(
            image_bytes=dummy_leaf,
            crop_hint="paddy",
            filename="paddy_leaf.jpg"
        )
        self.assertEqual(res["status"], "success")
        self.assertIn("Pyricularia oryzae", res["disease_name_ta"])
        self.assertGreater(res["infected_area_pct"], 0)
        self.assertIn("overlay_image_base64", res)
        self.assertTrue(res["overlay_image_base64"].startswith("data:image/jpeg;base64,"))
        self.assertIn("spoken_audio_script_ta", res)
        print("  ✓ Test 04 Passed: Modal SAM 3.1 lesion segmentation & overlay generated.")

    def test_05_modal_architecture_metadata(self):
        """Validates Modal serverless GPU manifest, scale-to-zero stats, and cost reduction."""
        modal_info = get_modal_architecture_info()
        self.assertEqual(modal_info["framework"], "Modal Serverless Python (modal.com)")
        self.assertIn("A10G", modal_info["gpu_target"])
        self.assertEqual(modal_info["scale_to_zero_delay_seconds"], 60)
        self.assertIn("4GB", modal_info["user_problem_solved"])
        print("  ✓ Test 05 Passed: Modal serverless GPU architecture manifest validated.")

    def test_06_crop_loss_petition_pdf(self):
        """Validates generation of official court-ready Crop Loss Compensation Petition PDF."""
        pdf_path = action_executor.generate_crop_loss_petition_pdf(
            farmer_name="க. சுப்பிரமணியன்",
            phone="9840012345",
            district="Madurai",
            taluk="Vadipatti",
            village="Sholavandan",
            survey_number="84/2B",
            crop_name="நெல் (Paddy IR20)",
            affected_acres="2.5",
            damage_cause="குலை நோய் மற்றும் தொடர் கனமழை",
            severity_pct="23.4%",
            estimated_loss_rs="45,000",
            meta_verification_id="AGRI-TEST-2026"
        )
        self.assertTrue(pdf_path.exists())
        self.assertGreater(pdf_path.stat().st_size, 3000)
        print(f"  ✓ Test 06 Passed: Official Crop Loss Petition PDF generated ({pdf_path.stat().st_size} bytes).")

    def test_07_meta_client_agri_reasoning_trace(self):
        """Validates Meta Muse Wonder 1.0 cognitive reasoning trace for crop queries."""
        steps = meta_client.generate_reasoning_trace("பயிர் குலை நோய் மற்றும் நிவாரணம்", language="ta")
        self.assertEqual(len(steps), 5)
        self.assertEqual(steps[0]["status"], "SAM_SEGMENTED")
        self.assertEqual(steps[2]["status"], "PRIVACY_SECURED")
        self.assertEqual(steps[4]["status"], "ACTION_DISPATCHED")
        print("  ✓ Test 07 Passed: Meta Muse Wonder 1.0 5-step cognitive agronomic trace verified.")

    def test_08_whatsapp_agri_triage(self):
        """Validates WhatsApp triage for agriculture, mandi prices, and crop leaf photo."""
        reply = handle_text_query("விவசாய பயிர் நோய் மற்றும் உழவர் சந்தை விலை", sender_phone="919840012345")
        self.assertIn("Modal", reply)
        self.assertIn("PM-KISAN", reply)
        self.assertIn("உழவர் சந்தை", reply)

        # Simulate incoming leaf photo
        sample_wa_payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "919840012345",
                            "type": "image",
                            "id": "wa_leaf_msg_001",
                            "image": {
                                "id": "leaf_media_999",
                                "caption": "நெல் பயிர் இலை காய்ந்து விட்டது என்ன பண்றது"
                            }
                        }]
                    }
                }]
            }]
        }
        ingress_res = process_incoming_whatsapp_message(sample_wa_payload)
        self.assertEqual(ingress_res["status"], "processed")
        self.assertTrue(ingress_res["reply_dispatched"])
        print("  ✓ Test 08 Passed: WhatsApp agro-advisory triage and photo ingress verified.")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌾 RUNNING MAKKAL AGENT AI - AGRICULTURE & MODAL TEST SUITE")
    print("=" * 60)
    unittest.main()
