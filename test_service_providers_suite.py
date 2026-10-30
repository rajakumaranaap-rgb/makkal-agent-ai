# -*- coding: utf-8 -*-
"""
Comprehensive Test Suite for SIA Service Providers Registry & Pincode Dispatch Hub.
Validates:
1. Default 25+ partner population and category coverage.
2. Partner self-registration via register_new_partner.
3. Proximity search by district & pincode across Tamil Nadu.
4. Direct hire request generation with OTP and zero-commission UPI link.
5. Conversational WhatsApp queries (625214 பைக், 613001 அறுவடை, 641001 கொத்தனார், பதிவு...).
6. FastAPI REST endpoints (/api/providers/list, /api/providers/register, /api/providers/hire).
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(r"D:\api\makkal-agent-ai")))

from sia_service_providers_registry import (
    load_providers_registry,
    save_providers_registry,
    register_new_partner,
    search_service_providers,
    create_provider_hire_request,
    process_provider_query_conversational,
    DEFAULT_SERVICE_PROVIDERS
)

class TestServiceProvidersRegistry(unittest.TestCase):
    def setUp(self):
        self.providers = load_providers_registry()

    def test_01_default_population_and_categories(self):
        """Verify default 25+ partners and full category coverage."""
        self.assertGreaterEqual(len(self.providers), 25, "Must have at least 25 pre-populated partners")
        
        categories = set(p["category"] for p in self.providers)
        expected_cats = {"mobility", "agri_machinery", "gig_labor", "education", "farm_labor"}
        for ec in expected_cats:
            self.assertIn(ec, categories, f"Category {ec} must be present in default providers")
        
        districts = set(p["district"] for p in self.providers)
        expected_districts = {"Madurai", "Thanjavur", "Coimbatore", "Chennai", "Tiruchirappalli", "Salem", "Dindigul"}
        for ed in expected_districts:
            self.assertIn(ed, districts, f"District {ed} must have registered service providers")
        print(f"[PASS] test_01: Found {len(self.providers)} providers across {len(districts)} districts!")

    def test_02_partner_self_registration(self):
        """Verify partner self-registration dynamically persists to registry."""
        res = register_new_partner(
            name="முத்துவேல் (Muthuvel)",
            phone="9876501234",
            category="mobility",
            service_key="car_sedan",
            pincode="625218",
            vehicle_or_equipment="Maruti Dzire Tour (TN-58-CD-9988)",
            rate_card="அடிப்படை ₹100 + ₹13/கி.மீ",
            upi_id="muthuvel.tour@okhdfcbank"
        )
        self.assertEqual(res["status"], "success")
        self.assertIn("provider_id", res)
        
        # Verify in loaded list
        updated_list = load_providers_registry()
        found = any(p["phone"] == "9876501234" for p in updated_list)
        self.assertTrue(found, "Newly registered partner must be persisted in registry")
        print(f"[PASS] test_02: Partner self-registration successful for ID {res['provider_id']}")

    def test_03_proximity_search_pincode_and_category(self):
        """Verify proximity search returns targeted results by pincode and category."""
        # Search Madurai Sholavandan bike (625214)
        bikes = search_service_providers(category="mobility", service_key="bike", pincode="625214")
        self.assertGreaterEqual(len(bikes), 1)
        self.assertEqual(bikes[0]["pincode"], "625214")

        # Search Thanjavur Harvester (613001)
        harvesters = search_service_providers(category="agri_machinery", service_key="harvester", pincode="613001")
        self.assertGreaterEqual(len(harvesters), 1)
        self.assertIn("அறுவடை", harvesters[0]["service_title_ta"])

        # Search Coimbatore Mason (641001)
        masons = search_service_providers(category="gig_labor", service_key="mason", pincode="641001")
        self.assertGreaterEqual(len(masons), 1)
        self.assertIn("கொத்தனார்", masons[0]["service_title_ta"])
        print("[PASS] test_03: Proximity search verified for mobility, agri, and artisans across pincodes!")

    def test_04_direct_hire_dispatch_and_otp(self):
        """Verify hire request produces 4-digit OTP, direct phone, WhatsApp link, and UPI deep link."""
        providers = load_providers_registry()
        p = providers[0]
        hire_res = create_provider_hire_request(p["provider_id"], customer_phone="9840112233", notes="Emergency booking")
        
        self.assertEqual(hire_res["status"], "success")
        self.assertEqual(len(str(hire_res["otp"])), 4, "OTP must be a 4-digit security code")
        self.assertTrue(hire_res["whatsapp_chat_url"].startswith("https://wa.me/"))
        self.assertTrue(hire_res["upi_payment_link"].startswith("upi://pay"))
        self.assertIn("booking_id", hire_res)
        print(f"[PASS] test_04: Hire request created with OTP {hire_res['otp']} (Booking ID: {hire_res['booking_id']})")

    def test_05_conversational_whatsapp_queries(self):
        """Verify natural language query parsing via process_provider_query_conversational."""
        test_queries = [
            ("625214 பைக் வேணும்", "SIA சரிபார்க்கப்பட்ட"),
            ("613001 நெல் அறுவடை இயந்திரம் வாடகைக்கு", "சுந்தரமூர்த்தி"),
            ("641001 கொத்தனார் ஆட்கள் வேண்டும்", "ஆறுமுகம்"),
            ("625001 10-ஆம் வகுப்பு கணிதம் டியூஷன் ஆசிரியர்", "மீனாட்சி"),
            ("600028 நீட் தேர்வு வழிகாட்டி", "செந்தில்"),
            ("பதிவு ஓட்டுநர் பாலு பைக் 625214 9840998877", "வெற்றிகரமாக முடிந்தது")
        ]

        for query, expected_snippet in test_queries:
            reply = process_provider_query_conversational("6381029380", query)
            self.assertIsNotNone(reply, f"Query '{query}' must return a response")
            reply_str = reply.get("message", "") if isinstance(reply, dict) else str(reply)
            self.assertIn(expected_snippet, reply_str, f"Reply for '{query}' must contain '{expected_snippet}'")
        print("[PASS] test_05: Conversational WhatsApp queries correctly dispatched and answered!")

    def test_06_fastapi_rest_endpoints(self):
        """Verify REST API integration in FastAPI app."""
        from fastapi.testclient import TestClient
        from app import app
        
        client = TestClient(app)
        
        # 1. GET /api/providers/list
        r1 = client.get("/api/providers/list?pincode=625214")
        self.assertEqual(r1.status_code, 200)
        d1 = r1.json()
        self.assertEqual(d1["status"], "success")
        self.assertGreaterEqual(len(d1["providers"]), 1)
        
        # 2. POST /api/providers/register
        r2 = client.post("/api/providers/register", json={
            "name": "எஸ். வேலு (S. Velu)",
            "phone": "9894011223",
            "category": "mobility",
            "service_key": "auto",
            "pincode": "625214",
            "vehicle_or_equipment": "Bajaj RE Auto (TN-58-AZ-3322)",
            "rate_card": "அரசு மீட்டர்கட்டணம்",
            "upi_id": "velu.auto@sbi"
        })
        self.assertEqual(r2.status_code, 200)
        d2 = r2.json()
        self.assertEqual(d2["status"], "success")
        new_id = d2["provider_id"]
        
        # 3. POST /api/providers/hire
        r3 = client.post("/api/providers/hire", json={
            "provider_id": new_id,
            "customer_phone": "6381029380"
        })
        self.assertEqual(r3.status_code, 200)
        d3 = r3.json()
        self.assertEqual(d3["status"], "success")
        self.assertEqual(len(str(d3["otp"])), 4)
        print("[PASS] test_06: REST API endpoints /api/providers/list, register, and hire fully functional!")

if __name__ == "__main__":
    unittest.main()
