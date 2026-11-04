# -*- coding: utf-8 -*-
"""
SIA (Super Intelligent Agent) Comprehensive Verification Suite
Meta AI Developer Hackathon 2026
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fastapi.testclient import TestClient
from app import app
from sia_user_manager import (
    handle_sia_whatsapp_flow,
    is_user_registered,
    get_user_profile,
    register_new_user,
    add_proof_document,
    SIA_OFFICIAL_NUMBER
)
from whatsapp_agent import process_incoming_whatsapp_message


class TestSIAArchitecture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.base_url = "http://localhost:8001"

    def test_01_sia_official_cell_number(self):
        """Verifies that SIA official cell number is configured as 6381029380."""
        self.assertEqual(SIA_OFFICIAL_NUMBER, "6381029380")
        self.assertTrue(is_user_registered("6381029380"))
        user = get_user_profile("6381029380")
        self.assertIsNotNone(user)
        self.assertEqual(user["pin"], "7890")

    def test_02_whatsapp_hi_sia_flow_registered_citizen(self):
        """Verifies sending 'Hi SIA' from registered number triggers greeting & menu/PIN."""
        res = handle_sia_whatsapp_flow(
            sender_phone="6381029380",
            message_text="Hi SIA",
            public_base_url=self.base_url
        )
        self.assertIsNotNone(res)
        self.assertTrue(res.get("stage") in ["SIMPLIFIED_PICTORIAL_MENU", "registered_ask_pin", "AWAIT_LOGIN_PIN"])
        self.assertIn("SIA", res["reply"])

    def test_03_whatsapp_pin_verification_and_magic_link(self):
        """Verifies sending correct PIN yields authenticated 1-Click Magic Dashboard Link."""
        res = handle_sia_whatsapp_flow(
            sender_phone="6381029380",
            message_text="PIN 7890",
            public_base_url=self.base_url
        )
        self.assertIsNotNone(res)
        self.assertEqual(res.get("status"), "authenticated")
        self.assertIn("/auth/magic?token=", res.get("magic_url", ""))
        self.assertIn("3D Neural Brain", res["reply"])
        self.assertIn("Live Biometric Heartbeat", res["reply"])

    def test_04_whatsapp_new_citizen_3step_onboarding(self):
        """Verifies full conversational registration via WhatsApp for unregistered numbers."""
        from sia_user_manager import load_registry, save_registry
        test_phone = "9840998877"

        # Ensure clean state for unregistered flow test
        reg = load_registry()
        if test_phone in reg.get("users", {}):
            del reg["users"][test_phone]
            save_registry(reg)

        # Step 1: User says 'Hi SIA' -> SIA prompts for Language or Name
        s1 = handle_sia_whatsapp_flow(test_phone, "Hi SIA, I want to access SIA", self.base_url)
        self.assertIn(s1["stage"], ["ASK_LANGUAGE", "ASK_NAME"])
        
        # Step 1b: User chooses Tamil if asked for language
        if s1["stage"] == "ASK_LANGUAGE":
            s1 = handle_sia_whatsapp_flow(test_phone, "தமிழ்", self.base_url)
            self.assertEqual(s1["stage"], "ASK_NAME")
            self.assertIn("படி 1/3", s1["reply"])

        # Step 2: User sends Name -> SIA prompts for PIN
        s2 = handle_sia_whatsapp_flow(test_phone, "கார்த்திக் ராஜா", self.base_url)
        self.assertEqual(s2["stage"], "ASK_PIN")
        self.assertIn("படி 2/3", s2["reply"])

        # Step 3: User sends 4-digit PIN -> SIA prompts for Family details
        s3 = handle_sia_whatsapp_flow(test_phone, "4321", self.base_url)
        self.assertEqual(s3["stage"], "ASK_FAMILY")
        self.assertIn("படி 3/3", s3["reply"])

        # Step 4: User sends District & Members -> SIA creates profile & sends 1-Click Magic Link
        s4 = handle_sia_whatsapp_flow(test_phone, "மதுரை, 4 உறுப்பினர்கள்", self.base_url)
        self.assertEqual(s4["stage"], "COMPLETED")
        self.assertIn("/auth/magic?token=", s4["magic_url"])
        self.assertTrue(is_user_registered(test_phone))

        user = get_user_profile(test_phone)
        self.assertEqual(user["name"], "கார்த்திக் ராஜா")
        self.assertEqual(user["pin"], "4321")
        self.assertEqual(user["district"], "Madurai")

    def test_05_proofs_vault_crud(self):
        """Verifies storing and retrieving citizen proofs in the SIA Digital Vault."""
        add_res = add_proof_document(
            phone="6381029380",
            doc_type="10th Samacheer Kalvi Marksheet",
            doc_number="TNSB-SSLC-849201",
            verified_by="Llama 3.2 Vision"
        )
        self.assertEqual(add_res["status"], "success")
        
        user = get_user_profile("6381029380")
        vault_types = [doc["doc_type"] for doc in user["proofs_vault"]]
        self.assertIn("10th Samacheer Kalvi Marksheet", vault_types)

    def test_06_sia_api_endpoints(self):
        """Verifies REST API endpoints for user profile, proofs, and WhatsApp simulator."""
        # 1. Profile
        r1 = self.client.get("/api/sia/user-profile/6381029380")
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r1.json()["user"]["phone"], "6381029380")

        # 2. Add Proof
        r2 = self.client.post("/api/sia/add-proof", json={
            "phone": "6381029380",
            "doc_type": "Income Certificate",
            "doc_number": "REV-INC-2026-99"
        })
        self.assertEqual(r2.status_code, 200)

        # 3. WhatsApp Sim
        r3 = self.client.post("/api/sia/whatsapp-sim", json={
            "sender_phone": "6381029380",
            "message_text": "Hi SIA"
        })
        self.assertEqual(r3.status_code, 200)
        self.assertIn("SIA", r3.json()["result"]["reply"])

        # 4. Heartbeat telemetry
        r4 = self.client.get("/api/sia/heartbeat-stats")
        self.assertEqual(r4.status_code, 200)
        self.assertEqual(r4.json()["bpm"], 76)

    def test_07_sia_web_dashboard_visual_elements(self):
        """Verifies the UI renders the 3D Neural Brain, Heartbeat EKG, and Talking Avatar elements."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.text
        self.assertIn("SIA (Super Intelligent Agent)", html)
        self.assertIn("neuralBrainCanvas", html)
        self.assertIn("heartbeatEkgCanvas", html)
        self.assertIn("talkingAvatarCanvas", html)
        self.assertIn("siaLiveSubtitle", html)
        self.assertIn("proofsVaultModal", html)
        self.assertIn("whatsAppSimModal", html)
        self.assertIn("6381029380", html)


if __name__ == "__main__":
    unittest.main()
