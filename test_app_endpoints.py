"""
FastAPI TestClient verification for Makkal Agent AI Regional Grounding Endpoints.
"""

import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

PROJECT_DIR = Path("D:/api/makkal-agent-ai")
sys.path.insert(0, str(PROJECT_DIR))

from app import app


class TestAppRegionalEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_tnega_services_endpoint(self):
        resp = self.client.get("/api/tnega/services")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertGreaterEqual(len(data["services"]), 4)

    def test_02_tnega_checklist_endpoint(self):
        resp = self.client.get("/api/tnega/checklists/patta_chitta")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("mandatory_checklist", data["service"])
        self.assertIn("₹60", data["service"]["statutory_fee_lock"])

    def test_03_tnega_verify_bundle_endpoint(self):
        payload = {
            "service_id": "patta_chitta",
            "uploaded_doc_codes": ["sale_deed", "previous_patta", "encumbrance_certificate", "aadhaar_card"]
        }
        resp = self.client.post("/api/tnega/verify-documents", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["audit"]["is_ready_for_esevai"])
        self.assertEqual(data["audit"]["readiness_percentage"], 100)

    def test_04_llama_vision_endpoint(self):
        resp = self.client.post("/api/vision/llama-audit", data={"service_target": "patta_chitta", "is_sample": "true"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("llama_vision_audit", data)
        self.assertTrue(data["llama_vision_audit"]["extracted_entities"]["has_official_seal"])

    def test_05_samacheer_homework_endpoint(self):
        payload = {
            "question": "நியூட்டனின் இயக்க விதிகள் யாவை?",
            "standard": 10,
            "subject": "science"
        }
        resp = self.client.post("/api/samacheer-kalvi/homework", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("இயக்க விதிகள்", data["textbook_unit"])

    def test_06_samacheer_quiz_endpoint(self):
        payload = {"standard": 10, "subject": "science"}
        resp = self.client.post("/api/samacheer-kalvi/quiz", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total_questions"], 5)

    def test_07_regional_agri_advisory_endpoint(self):
        resp = self.client.get("/api/agriculture/regional-advisory?crop=turmeric")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("Pendimethalin", data["advisory"]["weed_control"]["chemical_ta"])
        self.assertIn("Nano DAP", data["advisory"]["foliar_nutrition"]["product_ta"])

    def test_08_seamless_speech_endpoint(self):
        payload = {"text": "வணக்கம்! பட்டா மாறுதல் செய்ய என்ன ஆவணங்கள் தேவை?", "region": "madurai"}
        resp = self.client.post("/api/speech/seamless-synthesize", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("வணக்கம் அண்ணே!", data["speech"]["spoken_tamil"])
        self.assertIn("Vanakkam anne!", data["speech"]["colloquial_tanglish"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
