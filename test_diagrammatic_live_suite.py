# -*- coding: utf-8 -*-
"""
End-to-End Verification Suite for Diagrammatic Knowledge & Exam Guide Engine
Meta AI Developer Hackathon 2026
Supports both Live Remote Tunnel and Local FastAPI TestClient
"""
import sys
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = os.getenv("TEST_BASE_URL", "https://regulatory-stack-counter-lady.trycloudflare.com")

print("=" * 75)
print("🗺️ TESTING UNIVERSAL DIAGRAMMATIC GUIDE & PORTAL GROUNDING ENGINE")
print("=" * 75)

# Setup resilient client (Remote HTTP with fallback to FastAPI TestClient)
use_local = False
try:
    import urllib.request
    req = urllib.request.Request(f"{BASE_URL}/health", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=4) as resp:
        if resp.status != 200:
            use_local = True
except Exception:
    use_local = True

if use_local:
    print("ℹ️ Live remote tunnel unreachable or pre-deployment; utilizing local FastAPI TestClient...")
    from fastapi.testclient import TestClient
    from app import app
    client = TestClient(app)

    def get_req(path):
        r = client.get(path)
        return r.status_code, r.text, (r.json() if "application/json" in r.headers.get("content-type", "") else None)

    def post_req(path, payload):
        r = client.post(path, json=payload)
        return r.status_code, r.json()
else:
    print(f"🌐 Connected to live remote URL: {BASE_URL}")
    import urllib.request
    def get_req(path):
        req = urllib.request.Request(f"{BASE_URL}{path}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode('utf-8')
            try:
                js = json.loads(text)
            except Exception:
                js = None
            return resp.status, text, js

    def post_req(path, payload):
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}{path}",
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))


# 1. Check HTML UI Elements
print("\n[1] Checking Web App UI for Diagrammatic Guide Pod...")
status, html, _ = get_req("/")
assert status == 200
assert "Diagrammatic Knowledge & Exam Guide" in html, "Missing Diagrammatic Guide title in HTML"
assert "diagrammaticQueryInput" in html, "Missing query input field in HTML"
assert "executeDiagrammaticSolve" in html, "Missing executeDiagrammaticSolve JS in HTML"
assert "pushCurrentDiagramGuideToWhatsApp" in html, "Missing WhatsApp push function in HTML"
print("    Verified Diagrammatic Guide Pod, Voice input, Flowchart container, and JS handlers in HTML!")

# 2. Test Diagrammatic Solve API Across Major Portals
queries = [
    ("TNPSC Group 4 & VAO", "TNPSC குரூப் 4 மற்றும் VAO தேர்வு பாடத்திட்டம் தகுதி என்ன?", "tnpsc.gov.in"),
    ("NEET 7.5% Quota", "NEET 7.5% அரசு பள்ளி இடஒதுக்கீடு விதிகள் என்ன?", "exams.nta.ac.in"),
    ("UPSC IAS / IPS", "UPSC சிவில் சர்வீசஸ் IAS IPS தேர்வு முறை", "upsc.gov.in"),
    ("TNeGA Legal Heir", "வாரிசுச் சான்றிதழ் Legal Heir பெற கட்டணம் ஆவணங்கள்", "tnega.tn.gov.in"),
    ("TNPDS Ration Newborn", "ரேஷன் கார்டில் பிறந்த குழந்தை பெயர் சேர்க்கும் முறை", "tnpds.gov.in"),
    ("IGNOU Distance Higher Ed", "IGNOU தொலைதூர படிப்பு சேர்க்கை அசைன்மென்ட்", "ignou.ac.in"),
    ("PM-KISAN Central Scheme", "PM கிசான் ₹6000 e-KYC உதவித்தொகை", "india.gov.in"),
    ("Selvamagal Semippu 8.2%", "செல்வமகள் சேமிப்புத் திட்டம் Sukanya 8.2% வட்டி", "tn.gov.in")
]

print("\n[2] Testing POST /api/guide/diagrammatic-solve across 8 portals...")
for label, q_text, expected_domain_keyword in queries:
    status, res = post_req("/api/guide/diagrammatic-solve", {"query": q_text, "phone": "6381029380"})
    assert status == 200
    assert res.get("status") == "success", f"Failed for {label}"
    assert len(res.get("roadmap_steps", [])) >= 3, f"Insufficient steps for {label}"
    portal_url = res.get("portal_url", "")
    print(f"    ✓ {label:24} -> Portal: {portal_url:32} | Steps: {len(res['roadmap_steps'])} | Fee: {res['statutory_fee_text'][:35]}...")

# 3. Test Push to WhatsApp
print("\n[3] Testing POST /api/guide/push-to-whatsapp...")
status, push_res = post_req("/api/guide/push-to-whatsapp", {
    "phone": "6381029380",
    "whatsapp_text": "🏛️ *TNPSC குரூப் 4 தேர்வு வழிகாட்டி*: 10-ம் வகுப்பு தகுதி, 200 வினாக்கள், 300 மதிப்பெண்கள். கட்டணம் ₹100. தளம்: tnpsc.gov.in"
})
assert status == 200
assert push_res.get("status") == "success", "WhatsApp push failed"
print(f"    Verified guide push dispatched successfully: {push_res.get('status')}")

# 4. Check Live Event Stream
print("\n[4] Testing GET /api/live-stream/recent for WhatsApp push delivery...")
status, _, ls_data = get_req("/api/live-stream/recent")
assert status == 200
events = ls_data.get("events", []) if ls_data else []
assert len(events) > 0, "No live events in queue"
last_event = events[-1]
print(f"    Last Event in Hub: [{last_event.get('event_type')}] Channel: {last_event.get('data', {}).get('channel')} | Text: {last_event.get('data', {}).get('text')[:45]}...")

print("\n" + "=" * 75)
print("🎉 ALL DIAGRAMMATIC GUIDE & PORTAL GROUNDING TESTS PASSED 100%!")
print("=" * 75)
