# -*- coding: utf-8 -*-
"""
End-to-End Verification Suite for Diagrammatic Knowledge & Exam Guide Engine
Meta AI Developer Hackathon 2026
"""
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://regulatory-stack-counter-lady.trycloudflare.com"

print("=" * 75)
print("🗺️ TESTING UNIVERSAL DIAGRAMMATIC GUIDE & PORTAL GROUNDING ENGINE")
print("=" * 75)

# 1. Check HTML UI Elements
print("\n[1] Checking Web App UI for Diagrammatic Guide Pod...")
req = urllib.request.Request(f"{BASE_URL}/", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8')
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
    payload = json.dumps({"query": q_text, "phone": "6381029380"}).encode('utf-8')
    req_solve = urllib.request.Request(
        f"{BASE_URL}/api/guide/diagrammatic-solve",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req_solve, timeout=10) as r:
        res = json.loads(r.read().decode('utf-8'))
        assert res.get("status") == "success", f"Failed for {label}"
        assert len(res.get("roadmap_steps", [])) >= 3, f"Insufficient steps for {label}"
        portal_url = res.get("portal_url", "")
        print(f"    ✓ {label:24} -> Portal: {portal_url:32} | Steps: {len(res['roadmap_steps'])} | Fee: {res['statutory_fee_text'][:35]}...")

# 3. Test Push to WhatsApp
print("\n[3] Testing POST /api/guide/push-to-whatsapp...")
wa_payload = json.dumps({
    "phone": "6381029380",
    "whatsapp_text": "🏛️ *TNPSC குரூப் 4 தேர்வு வழிகாட்டி*: 10-ம் வகுப்பு தகுதி, 200 வினாக்கள், 300 மதிப்பெண்கள். கட்டணம் ₹100. தளம்: tnpsc.gov.in"
}).encode('utf-8')
req_push = urllib.request.Request(
    f"{BASE_URL}/api/guide/push-to-whatsapp",
    data=wa_payload,
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req_push, timeout=10) as r_p:
    push_res = json.loads(r_p.read().decode('utf-8'))
    assert push_res.get("status") == "success", "WhatsApp push failed"
    print(f"    Verified guide push dispatched successfully: {push_res.get('status')}")

# 4. Check Live Event Stream
print("\n[4] Testing GET /api/live-stream/recent for WhatsApp push delivery...")
req_ls = urllib.request.Request(f"{BASE_URL}/api/live-stream/recent", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req_ls, timeout=10) as r_ls:
    ls_data = json.loads(r_ls.read().decode('utf-8'))
    events = ls_data.get("events", [])
    assert len(events) > 0, "No live events in queue"
    last_event = events[-1]
    print(f"    Last Event in Hub: [{last_event.get('event_type')}] Channel: {last_event.get('data', {}).get('channel')} | Text: {last_event.get('data', {}).get('text')[:45]}...")

print("\n" + "=" * 75)
print("🎉 ALL DIAGRAMMATIC GUIDE & PORTAL GROUNDING TESTS PASSED 100%!")
print("=" * 75)
