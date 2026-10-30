# -*- coding: utf-8 -*-
"""
Comprehensive Test Suite for SIA Universal Master AI Assistant & Services Directory.
Validates:
1. Master services catalog has all 12 domains populated.
2. format_whatsapp_master_menu creates compliant WhatsApp button message.
3. Triage on greetings ('வணக்கம்', 'ஹலோ', 'help', 'சேவைகள்') returns master guide.
4. Triage on domain queries (rental, tuition, cbt, mla, vault, share market, agri, partner, mental health).
5. Open-ended queries correctly invoke Meta AI model guidance.
6. FastAPI REST endpoints (/api/assistant/guide, /api/assistant/triage, /api/chat).
7. Full WhatsApp Ingress via process_incoming_whatsapp_message.
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(r"D:\api\makkal-agent-ai")))

from universal_master_assistant import (
    universal_assistant,
    format_whatsapp_master_menu,
    format_text_master_menu,
    SIA_MASTER_SERVICES,
    UNIVERSAL_SYSTEM_PROMPT
)

class TestUniversalMasterAssistantSuite(unittest.TestCase):
    def test_01_catalog_and_domains(self):
        """Verify master catalog has 12 domains populated with metadata."""
        self.assertEqual(len(SIA_MASTER_SERVICES), 12, "Must have exactly 12 master service domains")
        expected_domains = {
            "civic_governance", "mla_mp_petitions", "school_tuition", "competitive_exams",
            "smart_agriculture", "hyperlocal_rentals", "partner_registration", "citizen_life_vault",
            "share_market_boto", "daily_news_air", "spoken_english_mental_health", "entertainment_posters"
        }
        actual_domains = set(s["id"] for s in SIA_MASTER_SERVICES)
        self.assertEqual(expected_domains, actual_domains)
        print(f"[PASS] test_01: All 12 master domains verified in catalog!")

    def test_02_whatsapp_master_menu_format(self):
        """Verify interactive WhatsApp button menu formatting."""
        menu = format_whatsapp_master_menu()
        self.assertIn("body_text", menu)
        self.assertIn("buttons", menu)
        self.assertLessEqual(len(menu["buttons"]), 3, "WhatsApp button message allows max 3 buttons")
        self.assertIn("1️⃣", menu["body_text"])
        self.assertIn("12", menu["body_text"])
        print("[PASS] test_02: Interactive WhatsApp master menu verified!")

    def test_03_greetings_triage(self):
        """Verify greetings trigger the master guide menu."""
        greetings = ["வணக்கம்", "ஹலோ", "help", "சேவைகள்", "services", "menu", "வழிகாட்டி"]
        for g in greetings:
            res = universal_assistant["triage"](g)
            self.assertEqual(res["status"], "success")
            self.assertEqual(res["type"], "master_menu", f"Greeting '{g}' must return master_menu")
            self.assertIn("SIA", res["message"])
        print("[PASS] test_03: Greetings correctly trigger master guide menu!")

    def test_04_domain_queries_triage(self):
        """Verify domain queries return targeted action steps."""
        test_queries = [
            ("பைக் எப்படி புக் பண்ணனும்?", "hyperlocal_rentals"),
            ("10-ஆம் வகுப்பு அறிவியல் வரைபடம்", "school_tuition"),
            ("TNPSC குரூப் 4 மாதிரி தேர்வு", "competitive_exams"),
            ("MLA-க்கு மனு எழுதணும்", "mla_mp_petitions"),
            ("என் வரவு செலவு கணக்கு விவரம்", "citizen_life_vault"),
            ("RELIANCE பங்கு நிலவரம்", "share_market_boto"),
            ("பயிர் இலை கருகல் நோய் மருந்து", "smart_agriculture"),
            ("நான் ஒரு ஓட்டுநர் எப்படி பதிவு செய்வது?", "partner_registration"),
            ("எனக்கு தேர்வு பயம் மன அழுத்தம்", "spoken_english_mental_health")
        ]

        for q, expected_domain in test_queries:
            res = universal_assistant["triage"](q)
            self.assertEqual(res["status"], "success")
            self.assertEqual(res["type"], "domain_guidance", f"Query '{q}' must return domain_guidance")
            self.assertEqual(res["domain_id"], expected_domain, f"Query '{q}' expected domain {expected_domain}, got {res.get('domain_id')}")
            self.assertIn("Next Action", res["message"])
        print("[PASS] test_04: Domain queries return targeted action steps!")

    def test_05_meta_ai_open_ended_counsel(self):
        """Verify open-ended questions invoke Meta AI model guidance."""
        open_query = "குடும்பத்தின் அமைதிக்கும் குழந்தைகளின் எதிர்கால சேமிப்புக்கும் என்ன வழி?"
        res = universal_assistant["triage"](open_query)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["type"], "meta_ai_counsel")
        self.assertIn("SIA", res["message"])
        print("[PASS] test_05: Open-ended query returns Meta AI model counsel!")

    def test_06_fastapi_assistant_endpoints(self):
        """Verify FastAPI REST endpoints /api/assistant/guide and /api/assistant/triage."""
        from fastapi.testclient import TestClient
        from app import app

        client = TestClient(app)

        # 1. GET /api/assistant/guide
        r1 = client.get("/api/assistant/guide")
        self.assertEqual(r1.status_code, 200)
        d1 = r1.json()
        self.assertEqual(d1["status"], "success")
        self.assertEqual(d1["total_domains"], 12)

        # 2. POST /api/assistant/triage
        r2 = client.post("/api/assistant/triage", json={"query": "வணக்கம் என்னென்ன சேவைகள் உள்ளன?"})
        self.assertEqual(r2.status_code, 200)
        d2 = r2.json()
        self.assertEqual(d2["type"], "master_menu")

        # 3. POST /api/chat with universal assistant
        r3 = client.post("/api/chat", json={
            "message": "SIA மூலம் என்னால் என்னவெல்லாம் செய்ய முடியும்?",
            "language": "ta"
        })
        self.assertEqual(r3.status_code, 200)
        d3 = r3.json()
        self.assertIn("reply", d3)
        print("[PASS] test_06: REST API endpoints /api/assistant/guide, triage, and /api/chat functional!")

    def test_07_full_whatsapp_ingress(self):
        """Verify full WhatsApp ingress webhook handles greetings with interactive buttons."""
        from whatsapp_agent import process_incoming_whatsapp_message

        # 1. Greeting message
        payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "916381029380",
                            "id": "wamid.test_master",
                            "type": "text",
                            "text": {"body": "வணக்கம் உதவி தேவை"}
                        }]
                    }
                }]
            }]
        }
        res = process_incoming_whatsapp_message(payload)
        self.assertEqual(res["status"], "processed")
        self.assertEqual(res["handler"], "universal_master_guide")

        # 2. Interactive button click for rentals
        btn_payload = {
            "entry": [{
                "changes": [{
                    "value": {
                        "messages": [{
                            "from": "916381029380",
                            "id": "wamid.test_btn_rentals",
                            "type": "interactive",
                            "interactive": {
                                "type": "button_reply",
                                "button_reply": {"id": "menu_rentals", "title": "🛵 பைக் / வாடகை"}
                            }
                        }]
                    }
                }]
            }]
        }
        btn_res = process_incoming_whatsapp_message(btn_payload)
        self.assertEqual(btn_res["status"], "processed")
        self.assertEqual(btn_res["handler"], "universal_master_guide")
        print("[PASS] test_07: Full WhatsApp Ingress verified for text and interactive menu buttons!")

if __name__ == "__main__":
    unittest.main()
