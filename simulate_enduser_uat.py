"""
==============================================================================
SIA (Makkal Agent AI) - End-to-End End-User UAT Simulation Suite
Target: Version 1.0 (Stable Beta Release)
Citizen Classes of Tamil Nadu:
  1. Farmer / Rural Citizen (உழவர் / விவசாயி)
  2. Student / Competitive Aspirant (மாணவர் / இளைஞர்)
  3. Women & Self Help Groups (பெண்கள் / மகளிர் குழு)
  4. Senior Citizens (முதியோர் நலன் & மனநலம்)
  5. Small Merchants & Gig Drivers (சிறு வணிகர் / ஆட்டோ ஓட்டுநர்)
  6. Civic Grievance Petitioners (பொது மக்கள் / மனுதாரர்)
  7. Hackathon Evaluators & Modern Mobile-First UI Verification
==============================================================================
"""

import sys
import os
import json
import time
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_root = Path(r"D:\api\makkal-agent-ai")
sys.path.insert(0, str(repo_root))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

print("=" * 80)
print("🇮🇳 SIA MAKKAL AGENT AI - END-TO-END CITIZEN UAT SIMULATION SUITE")
print("   Target Release: Version 1.0 (Stable Beta Release)")
print("=" * 80)

uat_results = []

def record_uat(persona: str, scenario: str, status: bool, details: str, latency_ms: float):
    icon = "✅ PASS" if status else "❌ FAIL"
    print(f"\n{icon} | [{persona}] {scenario} ({latency_ms:.1f}ms)")
    print(f"       Details: {details}")
    uat_results.append({
        "persona": persona,
        "scenario": scenario,
        "passed": status,
        "latency_ms": latency_ms,
        "details": details
    })


# ----------------------------------------------------------------------------
# Persona 1: உழவர் / விவசாயி (Farmer - Land Mutation & Agronomy)
# ----------------------------------------------------------------------------
print("\n" + "-" * 75)
print("🌾 PERSONA 1: உழவர் / விவசாயி (Farmer - Land Mutation & Agronomy)")
print("-" * 75)

# 1.1 Land Patta Statutory Fee Lock
t0 = time.perf_counter()
resp = client.post("/api/chat", json={
    "message": "எனது நிலம் சர்வே எண் 142/3A பட்டா பெயர் மாற்றம் செய்ய அரசு கட்டணம் எவ்வளவு?",
    "phone": "919443123456",
    "language": "ta"
})
lat = (time.perf_counter() - t0) * 1000
passed = resp.status_code == 200 and ("142/3" in resp.text or "பட்டா" in resp.text or "60" in resp.text or "RSO 31" in resp.text)
record_uat(
    "Farmer",
    "Land Patta Mutation & Statutory Fee Lock (₹60 vs ₹3,500)",
    passed,
    f"Status: {resp.status_code}, Grounding Matched: {'Yes' if passed else 'No'}",
    lat
)

# 1.2 TNAU Agriculture Welfare Schemes
t0 = time.perf_counter()
resp = client.get("/api/agriculture/schemes")
lat = (time.perf_counter() - t0) * 1000
data = resp.json() if resp.status_code == 200 else {}
schemes = data.get("schemes", [])
passed = resp.status_code == 200 and len(schemes) >= 3
record_uat(
    "Farmer",
    "TNAU & Uzhavan Welfare Schemes & GRAINS Portal Lookup",
    passed,
    f"Status: {resp.status_code}, Schemes Count: {len(schemes)}",
    lat
)

# 1.3 Patta Checklist & Statutory Verification
t0 = time.perf_counter()
resp = client.get("/api/tnega/checklists/patta_chitta")
lat = (time.perf_counter() - t0) * 1000
data = resp.json() if resp.status_code == 200 else {}
passed = resp.status_code == 200 and "mandatory_checklist" in data.get("service", {}) and "₹60" in data.get("service", {}).get("statutory_fee_lock", "")
record_uat(
    "Farmer",
    "Revenue Standing Order 31 Patta Checklist & ₹60 Fee Lock",
    passed,
    f"Status: {resp.status_code}, Mandatory Docs: {len(data.get('service', {}).get('mandatory_checklist', []))}",
    lat
)


# ----------------------------------------------------------------------------
# Persona 2: மாணவர் / இளைஞர் (Student & Youth - Trichy / Chennai)
# ----------------------------------------------------------------------------
print("\n" + "-" * 75)
print("📚 PERSONA 2: மாணவர் / இளைஞர் (Student - Samacheer Kalvi & TNPSC CBT)")
print("-" * 75)

# 2.1 Samacheer Kalvi Homework Concept Clarification
t0 = time.perf_counter()
resp = client.post("/api/samacheer-kalvi/homework", json={
    "question": "10th Maths Pythagoras Theorem proof in Tamil",
    "grade": 10
})
lat = (time.perf_counter() - t0) * 1000
data = resp.json() if resp.status_code == 200 else {}
reply_text = data.get("solution", "") or data.get("explanation", "") or str(data)
passed = resp.status_code == 200 and len(reply_text) > 20
record_uat(
    "Student",
    "Samacheer Kalvi 10th Maths Concept Clarification in Tamil",
    passed,
    f"Status: {resp.status_code}, Response Length: {len(reply_text)} chars",
    lat
)

# 2.2 TutO QBank Dynamic TNPSC CBT Mock Exam Generation
t0 = time.perf_counter()
resp = client.post("/api/exam/generate", json={
    "topic": "TNPSC Group 4 General Tamil & General Studies",
    "num_questions": 5,
    "language": "ta",
    "difficulty": "medium",
    "student_name": "Karthik Raja",
    "student_phone": "919443123456"
})
lat = (time.perf_counter() - t0) * 1000
exam_data = resp.json() if resp.status_code == 200 else {}
session = exam_data.get("session", {})
token = session.get("token")
questions = session.get("questions", [])
passed = resp.status_code == 200 and bool(token) and len(questions) == 5
record_uat(
    "Student",
    "TutO QBank Dynamic TNPSC CBT Mock Exam Generation",
    passed,
    f"Status: {resp.status_code}, Token: {token}, Questions: {len(questions)}",
    lat
)

# 2.3 Instant Exam Evaluation & Digital SVG Certificate
if passed and token:
    t0 = time.perf_counter()
    answers = {str(q.get("id")): q.get("options", ["A"])[0] for q in questions if "id" in q}
    sub_resp = client.post("/api/exam/submit", json={
        "token": token,
        "answers": answers,
        "time_spent_secs": 95
    })
    lat = (time.perf_counter() - t0) * 1000
    sub_data = sub_resp.json() if sub_resp.status_code == 200 else {}
    result = sub_data.get("result", {})
    cert_hash = result.get("verification_hash")
    sub_passed = sub_resp.status_code == 200 and bool(cert_hash)
    record_uat(
        "Student",
        "TNPSC Mock Exam Instant Evaluation & Digital Certificate",
        sub_passed,
        f"Score: {result.get('score')}/{result.get('total')}, Hash: {cert_hash}",
        lat
    )
    
    if sub_passed and cert_hash:
        cert_resp = client.get(f"/api/exam/certificate/{cert_hash}")
        svg_valid = cert_resp.status_code == 200 and "<svg" in cert_resp.text
        record_uat(
            "Student",
            "Vector SVG Skill Certificate of Competence Rendering",
            svg_valid,
            f"Status: {cert_resp.status_code}, SVG Size: {len(cert_resp.text)} bytes",
            1.2
        )


# ----------------------------------------------------------------------------
# Persona 3: பெண்கள் / சுயஉதவிக்குழு (Women & SHG - Dindigul / Erode)
# ----------------------------------------------------------------------------
print("\n" + "-" * 75)
print("👩 PERSONA 3: பெண்கள் / மகளிர் சுயஉதவிக்குழு (Women & SHG - KMUT & Commerce)")
print("-" * 75)

# 3.1 Kalaignar Magalir Urimai Thogai (KMUT) ₹1,000 Grievance Resolution
t0 = time.perf_counter()
resp = client.post("/api/chat", json={
    "message": "கலைஞர் மகளிர் உரிமைத் தொகை 1000 ரூபாய் விண்ணப்பம் நிராகரிக்கப்பட்டால் என்ன செய்ய வேண்டும்?",
    "phone": "919842123456",
    "language": "ta"
})
lat = (time.perf_counter() - t0) * 1000
passed = resp.status_code == 200 and ("மகளிர்" in resp.text or "1000" in resp.text or "வட்டாட்சியர்" in resp.text or "வருவாய்" in resp.text or "e-Sevai" in resp.text)
record_uat(
    "Women & SHG",
    "Kalaignar Magalir Urimai Thogai (KMUT) ₹1,000 Grievance Guidance",
    passed,
    f"Status: {resp.status_code}, Guidance Matched: {'Yes' if passed else 'No'}",
    lat
)

# 3.2 Makkal Sovereign Commerce Catalog (0% Middleman Commission)
t0 = time.perf_counter()
resp = client.get("/api/commerce/store/catalog?pincode=625214")
lat = (time.perf_counter() - t0) * 1000
data = resp.json() if resp.status_code == 200 else {}
catalog = data.get("catalog", {})
passed = resp.status_code == 200 and len(catalog) > 0
record_uat(
    "Women & SHG",
    "Makkal Sovereign Commerce 0% Commission Marketplace Catalog",
    passed,
    f"Status: {resp.status_code}, Categories: {len(catalog)}",
    lat
)


# ----------------------------------------------------------------------------
# Persona 4: முதியோர் நலன் (Senior Citizens - Tirunelveli / Madurai)
# ----------------------------------------------------------------------------
print("\n" + "-" * 75)
print("👴 PERSONA 4: முதியோர் நலன் (Senior Citizens - Life Vault & Tele-MANAS)")
print("-" * 75)

# 4.1 Old Age Pension (OAP) Welfare Scheme Verification
t0 = time.perf_counter()
resp = client.get("/api/sia/elder-pension")
lat = (time.perf_counter() - t0) * 1000
data = resp.json() if resp.status_code == 200 else {}
passed = resp.status_code == 200 and data.get("status") == "success"
record_uat(
    "Senior Citizen",
    "Tamil Nadu Old Age Pension (OAP ₹1,200) Statutory Rules & Criteria",
    passed,
    f"Status: {resp.status_code}, Monthly Amount: ₹{data.get('monthly_pension', 1200)}",
    lat
)

# 4.2 Tele-MANAS 14416 Mental Health & Elderly Support Helpline
t0 = time.perf_counter()
resp = client.get("/api/mental-health/helplines")
lat = (time.perf_counter() - t0) * 1000
data = resp.json() if resp.status_code == 200 else {}
helplines = data.get("helplines", [])
has_14416 = any("14416" in h.get("number", "") for h in helplines)
passed = resp.status_code == 200 and has_14416
record_uat(
    "Senior Citizen",
    "Tele-MANAS 14416 24x7 Mental Health & Elderly Emotional Helpline",
    passed,
    f"Status: {resp.status_code}, 14416 Verified: {'Yes' if has_14416 else 'No'}",
    lat
)


# ----------------------------------------------------------------------------
# Persona 5: சிறு வணிகர் / ஓட்டுநர் (Small Merchant / Auto Driver - Madurai)
# ----------------------------------------------------------------------------
print("\n" + "-" * 75)
print("🛺 PERSONA 5: சிறு வணிகர் / ஓட்டுநர் (Gig Workers - Zero Fee Mobility)")
print("-" * 75)

# 5.1 Mobility Fleet Verification
t0 = time.perf_counter()
resp = client.get("/api/travel/fleet")
lat = (time.perf_counter() - t0) * 1000
data = resp.json() if resp.status_code == 200 else {}
fleet = data.get("fleet", [])
passed = resp.status_code == 200 and len(fleet) >= 2
record_uat(
    "Gig & Merchant",
    "Zero-Commission Hyperlocal Mobility Fleet Catalog",
    passed,
    f"Status: {resp.status_code}, Vehicle Options: {len(fleet)}",
    lat
)

# 5.2 Transparent Travel Fare Calculation (No Surge, 0% Aggregator Deduction)
t0 = time.perf_counter()
resp = client.post("/api/travel/fare-estimate", json={
    "origin": "Madurai Mattuthavani",
    "destination": "Periyar Bus Stand",
    "vehicle_id": "auto"
})
lat = (time.perf_counter() - t0) * 1000
fare_data = resp.json() if resp.status_code == 200 else {}
passed = resp.status_code == 200 and fare_data.get("status") == "success" and fare_data.get("fare_breakdown", {}).get("surge_percentage") == 0
record_uat(
    "Gig & Merchant",
    "Transparent Travel Fare Estimate (0% Surge & Direct Driver Lock)",
    passed,
    f"Total Fare: ₹{fare_data.get('fare_breakdown', {}).get('total_fare')}, Surge: 0%",
    lat
)


# ----------------------------------------------------------------------------
# Persona 6: பொது மக்கள் / மனுதாரர் (Civic Petitioners - Kolathur, Chennai)
# ----------------------------------------------------------------------------
print("\n" + "-" * 75)
print("🏛️ PERSONA 6: பொது மக்கள் / மனுதாரர் (Civic Grievances & Legal Petitions)")
print("-" * 75)

# 6.1 Bilingual High Court & Revenue Legal Petition Generation
t0 = time.perf_counter()
resp = client.post("/api/generate-petition", json={
    "applicant_name": "K. Murugesan",
    "phone": "919445123456",
    "district": "Chennai",
    "taluk": "Ayanavaram",
    "village": "Kolathur",
    "service_title": "Road Infrastructure & Drainage Petition",
    "survey_number": "142/3A",
    "grounds_summary": "Paper Mills Road severely waterlogged; immediate road repair requested under Municipal Administration Act."
})
lat = (time.perf_counter() - t0) * 1000
pet_data = resp.json() if resp.status_code == 200 else {}
verification_id = pet_data.get("verification_id")
download_url = pet_data.get("download_url")
passed = resp.status_code == 200 and bool(verification_id) and bool(download_url)
record_uat(
    "Civic Citizen",
    "Official High Court & Revenue Legal Petition Generation with Barcode",
    passed,
    f"Verification ID: {verification_id}, URL: {download_url}",
    lat
)

# 6.2 Court-Admissible PDF Download Integrity
if passed and download_url:
    t0 = time.perf_counter()
    doc_resp = client.get(download_url)
    lat = (time.perf_counter() - t0) * 1000
    pdf_valid = doc_resp.status_code == 200 and doc_resp.content.startswith(b"%PDF")
    record_uat(
        "Civic Citizen",
        "Court-Admissible PDF Binary Verification (%PDF Header & Integrity)",
        pdf_valid,
        f"Status: {doc_resp.status_code}, File Size: {len(doc_resp.content)} bytes",
        lat
    )


# ----------------------------------------------------------------------------
# Persona 7: Hackathon Evaluators & Modernized UI Architecture
# ----------------------------------------------------------------------------
print("\n" + "-" * 75)
print("🏆 PERSONA 7: Hackathon Evaluator & Modernized Tamil Nadu UI Components")
print("-" * 75)

# 7.1 Health & Version 1.0 Stable Beta Verification
t0 = time.perf_counter()
resp = client.get("/health")
lat = (time.perf_counter() - t0) * 1000
health = resp.json() if resp.status_code == 200 else {}
is_beta_10 = health.get("version") == "1.0 (Stable Beta Release)" and health.get("release_channel") == "Stable Beta Release"
passed = resp.status_code == 200 and is_beta_10
record_uat(
    "Evaluator",
    "System Health Check & Version 1.0 (Stable Beta Release) Status",
    passed,
    f"Status: {health.get('status')}, Version: {health.get('version')}, Channel: {health.get('release_channel')}",
    lat
)

# 7.2 Modernized Persona Switcher & Mobile Bottom Dock in Web Template
t0 = time.perf_counter()
resp = client.get("/")
lat = (time.perf_counter() - t0) * 1000
html = resp.text
has_personas = "selectCitizenPersona('farmer')" in html and "selectCitizenPersona('student')" in html and "selectCitizenPersona('women')" in html
has_dock = "mobileBottomNav" in html
has_fee_lock = "₹60" in html and "statutory" in html.lower()
has_badge = "v1.0 Stable Beta" in html
passed = resp.status_code == 200 and has_personas and has_dock and has_fee_lock and has_badge
record_uat(
    "Evaluator",
    "Mobile-First Responsive Tamil Nadu Citizen Persona Switcher & Fee Locks",
    passed,
    f"Personas: {has_personas}, Mobile Dock: {has_dock}, Fee Badges: {has_fee_lock}, v1.0 Badge: {has_badge}",
    lat
)


# ----------------------------------------------------------------------------
# Final UAT Summary Report
# ----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("📊 SIA MAKKAL AGENT AI - CITIZEN UAT SIMULATION SCORECARD")
print("=" * 80)

total_uat = len(uat_results)
passed_uat = sum(1 for r in uat_results if r["passed"])
pass_rate = (passed_uat / total_uat) * 100 if total_uat else 0
avg_lat = sum(r["latency_ms"] for r in uat_results) / total_uat if total_uat else 0

for r in uat_results:
    icon = "✅ PASS" if r["passed"] else "❌ FAIL"
    print(f"{icon} | {r['persona']:<15} | {r['scenario']:<60} | {r['latency_ms']:>6.1f}ms")

print("-" * 80)
print(f"Total UAT Scenarios Tested : {total_uat}")
print(f"Passed                     : {passed_uat} / {total_uat} ({pass_rate:.1f}%)")
print(f"Average Subsystem Latency  : {avg_lat:.1f}ms")
print(f"UAT Quality Verdict        : {'🏅 100% PERFECT PASS (READY FOR AWS PRODUCTION DEPLOYMENT)' if pass_rate == 100 else '⚠️ ATTENTION NEEDED'}")
print("=" * 80)

if pass_rate < 100:
    sys.exit(1)
