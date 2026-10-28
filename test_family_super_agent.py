# -*- coding: utf-8 -*-
"""
==============================================================================
Test Suite for SIA Family Super-Intelligent Agent & Meta Model Workflows
Meta AI Developer Hackathon 2026
==============================================================================
Verifies end-to-end multi-persona family guidance across:
1. Student / Child (Samacheer 1-12, TutO CBT, 80 Ambition tracks, 45 GK milestones)
2. Farmer / Parent (SAM 3.1 leaf diagnostic, Mandi rates, RentO machinery, PMFBY)
3. Elder / Senior (OAP ₹1,000 pension, KMUT ₹1,000 redressal, CMCHIS ₹5L health)
4. Citizen / Head (Patta RSO 31, Ration card, Aadhaar ₹50, RTI ₹10)
5. WhatsApp Ingress & Interactive Button Dispatches
6. Web API Endpoints & Zero Personal Name Enforcement
==============================================================================
"""

import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent))

from app import app
from family_super_agent import family_super_agent, FAMILY_STATUTORY_RULES
from tuto_testo_qbank_bridge import tuto_testo_qbank_bridge
from whatsapp_agent import process_incoming_whatsapp_message


class TestFamilySuperAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_family_persona_triage(self):
        """Verifies multi-role intent classification into 4 family personas."""
        # Student
        t_student = family_super_agent.triage_family_intent("I want to become an IAS collector")
        self.assertEqual(t_student["persona"], "student")
        self.assertEqual(t_student["sub_intent"], "ambition_mentorship")

        t_gk = family_super_agent.triage_family_intent("இன்றைய பொது அறிவு மற்றும் அறிவியல் GK")
        self.assertEqual(t_gk["persona"], "student")
        self.assertEqual(t_gk["sub_intent"], "daily_gk")

        t_cbt = family_super_agent.triage_family_intent("TNPSC பொதுத் தேர்வு மாதிரி வினாக்கள்")
        self.assertEqual(t_cbt["persona"], "student")
        self.assertEqual(t_cbt["sub_intent"], "cbt_exam")

        # Farmer
        t_leaf = family_super_agent.triage_family_intent("நெல் பயிர் இலை கருகல் நோய் மற்றும் மருந்து")
        self.assertEqual(t_leaf["persona"], "farmer")
        self.assertEqual(t_leaf["sub_intent"], "crop_diagnostic")

        t_mandi = family_super_agent.triage_family_intent("கோயம்பேடு உழவர் சந்தை தக்காளி மண்டி விலை")
        self.assertEqual(t_mandi["persona"], "farmer")
        self.assertEqual(t_mandi["sub_intent"], "mandi_prices")

        # Elder
        t_oap = family_super_agent.triage_family_intent("முதியோர் உதவித்தொகை ₹1000 பெறுவது எப்படி?")
        self.assertEqual(t_oap["persona"], "elder")
        self.assertEqual(t_oap["sub_intent"], "oap_pension")

        t_kmut = family_super_agent.triage_family_intent("கலைஞர் மகளிர் உரிமைத் தொகை நிராகரிக்கப்பட்டது")
        self.assertEqual(t_kmut["persona"], "elder")
        self.assertEqual(t_kmut["sub_intent"], "kmut_appeal")

        # Citizen
        t_patta = family_super_agent.triage_family_intent("கிரய பத்திரம் மூலம் பட்டா பெயர் மாற்றம்")
        self.assertEqual(t_patta["persona"], "citizen")
        self.assertEqual(t_patta["sub_intent"], "patta_transfer")

        t_rti = family_super_agent.triage_family_intent("தகவல் அறியும் உரிமைச் சட்டம் RTI மனு")
        self.assertEqual(t_rti["persona"], "citizen")
        self.assertEqual(t_rti["sub_intent"], "rti_petition")

    def test_02_student_ambition_and_gk_progression(self):
        """Verifies Ambition career tracks and 365 daily GK milestones."""
        tracks = tuto_testo_qbank_bridge.get_ambition_tracks()
        self.assertEqual(len(tracks), 8)
        curriculums = [t["curriculum"] for t in tracks]
        self.assertIn("JrIAS (Civil Servant)", curriculums)
        self.assertIn("JrDR (Doctor)", curriculums)
        self.assertIn("JrJudge (Justice & Law)", curriculums)
        self.assertIn("JrScientist (ISRO / Space)", curriculums)

        # Handle IAS ambition query
        res_ias = family_super_agent.handle_family_request("IAS", persona_override="student")
        self.assertEqual(res_ias["status"], "success")
        self.assertIn("JrIAS", res_ias["reply_ta"])
        self.assertIn("Meta Wonder 1.0", res_ias["reply_ta"])

        # Handle Daily GK
        res_gk = family_super_agent.handle_family_request("GK", persona_override="student")
        self.assertEqual(res_gk["status"], "success")
        self.assertIn("பொது அறிவு", res_gk["reply_ta"])

    def test_03_farmer_mandi_and_statutory_advisory(self):
        """Verifies Farmer Mandi rates and PMFBY statutory rules."""
        res_mandi = family_super_agent.handle_family_request("Mandi price", persona_override="farmer")
        self.assertEqual(res_mandi["status"], "success")
        self.assertIn("உழவர் சந்தை", res_mandi["reply_ta"])
        self.assertIn("பொன்னி", res_mandi["reply_ta"])

        res_agri = family_super_agent.handle_family_request("Agri general", persona_override="farmer")
        self.assertIn("PMFBY", res_agri["reply_ta"])
        self.assertIn("72 மணி", res_agri["reply_ta"])

    def test_04_elder_social_security_and_health(self):
        """Verifies Old Age Pension (OAP), KMUT, and CMCHIS health coverage."""
        res_oap = family_super_agent.handle_family_request("OAP Pension", persona_override="elder")
        self.assertEqual(res_oap["status"], "success")
        self.assertIn("₹1,000", res_oap["reply_ta"])
        self.assertIn("60 வயது", res_oap["reply_ta"])

        res_kmut = family_super_agent.handle_family_request("KMUT", persona_override="elder")
        self.assertIn("கோட்டாட்சியர்", res_kmut["reply_ta"])

    def test_05_whatsapp_ingress_family_routing(self):
        """Verifies WhatsApp Cloud API ingress routing for family triggers and buttons."""
        # 1. Family Hub trigger
        payload_hub = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "916381029380",
                            "type": "text",
                            "text": {"body": "FAMILY"}
                        }]
                    }
                }]
            }]
        }
        res_hub = process_incoming_whatsapp_message(payload_hub)
        self.assertEqual(res_hub["status"], "processed")
        self.assertEqual(res_hub["handler"], "family_hub_dispatcher")

        # 2. Ambition trigger (IAS)
        payload_ias = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "916381029380",
                            "type": "text",
                            "text": {"body": "IAS"}
                        }]
                    }
                }]
            }]
        }
        res_ias = process_incoming_whatsapp_message(payload_ias)
        self.assertEqual(res_ias["status"], "processed")
        self.assertEqual(res_ias["handler"], "family_student_ambition")

        # 3. Daily GK trigger
        payload_gk = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "916381029380",
                            "type": "text",
                            "text": {"body": "GK"}
                        }]
                    }
                }]
            }]
        }
        res_gk = process_incoming_whatsapp_message(payload_gk)
        self.assertEqual(res_gk["status"], "processed")
        self.assertEqual(res_gk["handler"], "family_student_gk")

        # 4. Elder Pension trigger
        payload_pension = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "916381029380",
                            "type": "text",
                            "text": {"body": "PENSION"}
                        }]
                    }
                }]
            }]
        }
        res_pension = process_incoming_whatsapp_message(payload_pension)
        self.assertEqual(res_pension["status"], "processed")
        self.assertEqual(res_pension["handler"], "family_elder_pension")

        # 5. Interactive button click (fam_farmer)
        payload_btn = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "916381029380",
                            "type": "interactive",
                            "interactive": {
                                "type": "button_reply",
                                "button_reply": {
                                    "id": "fam_farmer",
                                    "title": "🌾 உழவர் நலன்"
                                }
                            }
                        }]
                    }
                }]
            }]
        }
        res_btn = process_incoming_whatsapp_message(payload_btn)
        self.assertEqual(res_btn["status"], "processed")
        self.assertEqual(res_btn["handler"], "family_farmer_mandi")

    def test_06_fastapi_family_endpoints(self):
        """Verifies REST endpoints for Web Workstation Family Hub."""
        # Summary
        r1 = self.client.get("/api/sia/family-hub/summary")
        self.assertEqual(r1.status_code, 200)
        data1 = r1.json()
        self.assertEqual(len(data1["personas"]), 4)
        self.assertGreaterEqual(data1["total_qbank_questions"], 250)
        self.assertGreaterEqual(data1["total_ambition_lessons"], 80)
        self.assertGreaterEqual(data1["total_gk_milestones"], 45)

        # Ambition Tracks
        r2 = self.client.get("/api/sia/ambition-tracks")
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(len(r2.json()["tracks"]), 8)

        # Daily GK
        r3 = self.client.get("/api/sia/gk-daily")
        self.assertEqual(r3.status_code, 200)
        self.assertIsNotNone(r3.json().get("milestone"))

        # Elder Pension Rules
        r4 = self.client.get("/api/sia/elder-pension")
        self.assertEqual(r4.status_code, 200)
        self.assertIn("oap", r4.json()["rules"])
        self.assertIn("₹1,000", r4.json()["rules"]["oap"])

        # Query
        r5 = self.client.post("/api/sia/family-hub/query", json={"query": "Junior Doctor", "persona": "student"})
        self.assertEqual(r5.status_code, 200)
        self.assertEqual(r5.json()["persona"], "student")


if __name__ == "__main__":
    unittest.main()
