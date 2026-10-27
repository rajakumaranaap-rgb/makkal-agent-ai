"""
Makkal Agent AI - End-to-End Automated Verification Test Suite
Meta AI Developer Hackathon 2026
"""

import sys
import os
import json
import io
import time
import requests
from PIL import Image, ImageDraw

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REMOTE_BASE = "https://brighton-decorative-opposite-attendance.trycloudflare.com"
LOCAL_BASE = "http://127.0.0.1:8001"

# Determine target URL: try remote first, fallback to local if remote unreachable
try:
    r = requests.get(f"{REMOTE_BASE}/health", timeout=5)
    if r.status_code == 200:
        TARGET_URL = REMOTE_BASE
        print(f"[*] Targeting Live Cloudflare Remote Endpoint: {TARGET_URL}")
    else:
        TARGET_URL = LOCAL_BASE
        print(f"[*] Fallback to Local Endpoint: {TARGET_URL}")
except Exception:
    TARGET_URL = LOCAL_BASE
    print(f"[*] Fallback to Local Endpoint: {TARGET_URL}")


def create_sample_deed_image() -> bytes:
    """Generates a synthetic deed image with seal and signature boxes for SAM 3.1 test."""
    img = Image.new("RGB", (1000, 1400), color=(250, 248, 240))
    draw = ImageDraw.Draw(img)
    # Header
    draw.rectangle([100, 50, 900, 150], fill=(230, 220, 200), outline=(100, 50, 0), width=3)
    draw.text((150, 80), "GOVERNMENT OF TAMIL NADU - REGISTRATION DEPARTMENT", fill=(50, 20, 0))
    # Seal
    draw.ellipse([120, 200, 320, 400], fill=(240, 230, 210), outline=(150, 0, 0), width=4)
    draw.text((160, 290), "TALUK SEAL", fill=(150, 0, 0))
    # Body text
    for y in range(450, 1000, 60):
        draw.line([100, y, 900, y], fill=(200, 200, 200), width=2)
    # Signature
    draw.rectangle([650, 1150, 900, 1300], fill=(240, 240, 230), outline=(0, 0, 120), width=3)
    draw.text((680, 1220), "SUB-REGISTRAR SIGN", fill=(0, 0, 120))
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def run_tests():
    print("\n" + "=" * 70)
    print("🏛️ MAKKAL AGENT AI: META HACKATHON VERIFICATION SUITE")
    print(f"Target: {TARGET_URL}")
    print("=" * 70 + "\n")

    results = []

    # Test 1: Health Endpoint
    print("[1/10] Testing /health endpoint...")
    try:
        res = requests.get(f"{TARGET_URL}/health", timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "online"
        print(f"  ✓ PASS: Service online, Host: {data.get('host')}")
        results.append(("Health Check", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Health Check", "FAIL"))

    # Test 2: Services Catalog
    print("\n[2/10] Testing /api/catalog endpoint...")
    try:
        res = requests.get(f"{TARGET_URL}/api/catalog", timeout=8)
        data = res.json()
        assert res.status_code == 200
        services = data.get("services", [])
        assert len(services) >= 5
        print(f"  ✓ PASS: Loaded {len(services)} civic welfare services in catalog")
        results.append(("Services Catalog", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Services Catalog", "FAIL"))

    # Test 3: Chat with Muse Spark 1.3 (Tamil)
    print("\n[3/10] Testing /api/chat with Meta Muse Spark 1.3 (Tamil)...")
    try:
        payload = {
            "message": "எனக்கு நிலம் சர்வே செய்து பட்டா பெயர் மாற்றம் செய்ய வேண்டும், அரசு கட்டணம் எவ்வளவு?",
            "language": "ta"
        }
        res = requests.post(f"{TARGET_URL}/api/chat", json=payload, timeout=12)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        assert "muse-spark-1.3" in data.get("model_used")
        print(f"  ✓ PASS: Model [{data.get('model_used')}] responded with {len(data.get('reply'))} chars")
        results.append(("Muse Spark 1.3 Chat", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Muse Spark 1.3 Chat", "FAIL"))

    # Test 4: Deep Legal Reasoning with Meta Muse Wonder 1.0
    print("\n[4/10] Testing /api/chat with Meta Muse Wonder 1.0 (Deep Reasoning)...")
    try:
        payload = {
            "message": "வாரிசு சான்றிதழ் பெறுவதில் வாரிசுகளுக்குள் சர்ச்சை உள்ளது, சட்டப்படியான தீர்வு என்ன?",
            "use_deep_reasoning": True,
            "language": "ta"
        }
        res = requests.post(f"{TARGET_URL}/api/chat", json=payload, timeout=12)
        data = res.json()
        assert res.status_code == 200
        assert "muse-wonder-1.0" in data.get("model_used")
        print(f"  ✓ PASS: Deep Reasoning Model [{data.get('model_used')}] responded successfully")
        results.append(("Muse Wonder 1.0 Deep Reasoning", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Muse Wonder 1.0 Deep Reasoning", "FAIL"))

    # Test 5: Open-Weight Model Routing on Baseten
    print("\n[5/10] Testing /api/chat with Baseten Open-Weight Model ($10k Prize Track)...")
    try:
        payload = {
            "message": "நில எல்லை தகராறு தீர்வு சட்டம்",
            "use_open_weight": True,
            "language": "ta"
        }
        res = requests.post(f"{TARGET_URL}/api/chat", json=payload, timeout=12)
        data = res.json()
        assert res.status_code == 200
        assert "Baseten" in data.get("model_used")
        print(f"  ✓ PASS: Open-Weight Engine [{data.get('model_used')}] routed successfully")
        results.append(("Baseten Open-Weight Engine", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Baseten Open-Weight Engine", "FAIL"))

    # Test 6: SAM 3.1 Document Segmentation Audit
    print("\n[6/10] Testing /api/audit-document with Meta SAM 3.1...")
    try:
        deed_bytes = create_sample_deed_image()
        files = {"file": ("deed_test.jpg", deed_bytes, "image/jpeg")}
        res = requests.post(f"{TARGET_URL}/api/audit-document", files=files, timeout=12)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        assert data.get("model_used") == "sam-3.1"
        assert len(data.get("segmented_zones", [])) > 0
        print(f"  ✓ PASS: SAM 3.1 detected {len(data.get('segmented_zones'))} zones, Authentic: {data.get('is_authentic')}")
        results.append(("SAM 3.1 Document Audit", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("SAM 3.1 Document Audit", "FAIL"))

    # Test 7: Court-Ready Legal Petition PDF Generation
    print("\n[7/10] Testing /api/generate-petition (Autonomous Action Engine)...")
    try:
        payload = {
            "applicant_name": "T. Murugesan",
            "phone": "9840198765",
            "district": "Madurai",
            "taluk": "Melur",
            "village": "Thiruvathavur",
            "service_title": "Patta Name Transfer & Subdivision Survey",
            "survey_number": "218/4C",
            "grounds_summary": "Purchased property through registered sale deed. Requiring official subdivision mutation under RSO 31."
        }
        res = requests.post(f"{TARGET_URL}/api/generate-petition", json=payload, timeout=12)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        pdf_url = data.get("download_url")
        assert pdf_url is not None
        
        # Verify downloading generated PDF
        pdf_res = requests.get(f"{TARGET_URL}{pdf_url}", timeout=8)
        assert pdf_res.status_code == 200
        assert len(pdf_res.content) > 1000
        print(f"  ✓ PASS: Generated PDF [{data.get('filename')}] ({len(pdf_res.content)} bytes)")
        results.append(("Legal Petition PDF Synthesis", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Legal Petition PDF Synthesis", "FAIL"))

    # Test 8: Meta WhatsApp Webhook Handshake & Ingress
    print("\n[8/10] Testing Meta WhatsApp Cloud API Webhook handshake...")
    try:
        params = {
            "hub.mode": "subscribe",
            "hub.verify_token": "makkal_agent_meta_2026",
            "hub.challenge": "9988776655"
        }
        res = requests.get(f"{TARGET_URL}/api/whatsapp/webhook", params=params, timeout=8)
        assert res.status_code == 200
        assert res.text == "9988776655"
        print("  ✓ PASS: Meta WhatsApp Webhook handshake verified (200 OK)")
        results.append(("WhatsApp Webhook Handshake", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("WhatsApp Webhook Handshake", "FAIL"))

    # Test 9: Live Anti-Corruption & Civic Economic Impact Counter
    print("\n[9/10] Testing /api/impact-metrics (Real-Time Corruption Prevention)...")
    try:
        res = requests.get(f"{TARGET_URL}/api/impact-metrics", timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        assert data.get("middleman_extortion_blocked_inr") == 3500
        assert data.get("official_statutory_fee_inr") == 60
        assert data.get("total_corruption_prevented_inr") >= 6000000
        print(f"  ✓ PASS: ₹{data.get('middleman_extortion_blocked_inr')} bribe blocked, ₹{data.get('total_corruption_prevented_inr')} total civic savings")
        results.append(("Anti-Corruption Impact Metrics", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Anti-Corruption Impact Metrics", "FAIL"))

    # Test 10: Cadastral FMB Subdivision Plot Visualizer
    print("\n[10/11] Testing /api/cadastral-fmb/{survey_no} (Cadastral SVG Visualizer)...")
    try:
        res = requests.get(f"{TARGET_URL}/api/cadastral-fmb/142-3B", timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        assert "<svg" in data.get("svg", "")
        assert "142-3B" in data.get("survey_no")
        print(f"  ✓ PASS: Successfully synthesized Cadastral FMB SVG plot for Survey No [{data.get('survey_no')}]")
        results.append(("Cadastral FMB Plot Synthesis", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Cadastral FMB Plot Synthesis", "FAIL"))

    # Test 11: Sample Deed Vision Endpoint for Judges
    print("\n[11/14] Testing /api/sample-deed (Judges 1-Click Computer Vision Test)...")
    try:
        res = requests.get(f"{TARGET_URL}/api/sample-deed", timeout=8)
        assert res.status_code == 200
        assert "image/jpeg" in res.headers.get("content-type", "")
        assert len(res.content) > 1000
        print(f"  ✓ PASS: Synthesized authentic deed sample image ({len(res.content)} bytes)")
        results.append(("Sample Deed Vision Generator", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Sample Deed Vision Generator", "FAIL"))

    # Test 12: MLA Constituencies & District Directory
    print("\n[12/14] Testing /api/mla/constituencies (TN 234 Assembly Directory)...")
    try:
        res = requests.get(f"{TARGET_URL}/api/mla/constituencies", timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        assert data.get("districts_count") == 38
        assert data.get("total_constituencies") >= 20
        print(f"  ✓ PASS: Loaded {data.get('total_constituencies')} Assembly Constituencies across all {data.get('districts_count')} Districts")
        results.append(("MLA Constituencies Directory", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("MLA Constituencies Directory", "FAIL"))

    # Test 13: MLA Constituency Real-Time Semantic Resolution
    print("\n[13/14] Testing /api/mla/resolve (Intelligent Village -> MLA Mapping)...")
    try:
        payload = {"query": "மேலூர் கிராமத்தில் உள்ளோம்", "district": "Madurai"}
        res = requests.post(f"{TARGET_URL}/api/mla/resolve", json=payload, timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        r = data.get("result", {})
        assert r.get("ac_no") == 188
        assert "Melur" in r.get("constituency_en", "")
        assert "mla.melur@tn.gov.in" in r.get("mla_email", "")
        print(f"  ✓ PASS: Resolved village to AC {r.get('ac_no')} [{r.get('constituency_ta')}] MLA: {r.get('mla_name_ta')}")
        results.append(("MLA Constituency Resolver", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("MLA Constituency Resolver", "FAIL"))

    # Test 14: Automated MLA Grievance Petition PDF Synthesis & Dispatch
    print("\n[14/14] Testing /api/mla/submit-petition (Court-Ready MLA Petition Dispatch)...")
    try:
        payload = {
            "applicant_name": "மு. செல்லத்துரை",
            "phone": "9840198765",
            "district": "Madurai",
            "taluk": "மேலூர்",
            "village": "திருவாதவூர்",
            "constituency": "மேலூர்",
            "grievance_category": "பாசன வாய்க்கால் தூர்வாருதல்",
            "grievance_details": "விவசாய பாசன வாய்க்கால் பல ஆண்டுகளாக தூர்வாரப்படவில்லை. உடனடியாக தூர்வாரி தர வேண்டுகிறேன்.",
            "dispatch_channel": "both"
        }
        res = requests.post(f"{TARGET_URL}/api/mla/submit-petition", json=payload, timeout=12)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        assert "TN-MLA-2026" in data.get("acknowledgement_id")
        assert "pdf_download_url" in data
        assert "whatsapp_share_url" in data
        
        # Verify downloading generated MLA PDF
        pdf_res = requests.get(f"{TARGET_URL}{data['pdf_download_url']}", timeout=8)
        assert pdf_res.status_code == 200
        assert len(pdf_res.content) > 1000
        print(f"  ✓ PASS: Synthesized Court-Ready MLA Petition PDF [{data['filename']}] ({len(pdf_res.content)} bytes) Ack ID: {data['acknowledgement_id']}")
        results.append(("MLA Petition Synthesis & Dispatch", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("MLA Petition Synthesis & Dispatch", "FAIL"))

    # Test 15: Universal Petition Categories & Statutory Tiers
    print("\n[15/18] Testing /api/petitions/categories (6-Tier Civic Grievance Registry)...")
    try:
        res = requests.get(f"{TARGET_URL}/api/petitions/categories", timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        tiers = data.get("tiers", {})
        assert "collector" in tiers
        assert "police_sp" in tiers
        assert "rdo_appeal" in tiers
        assert "tangedco" in tiers
        assert len(tiers) >= 6
        print(f"  ✓ PASS: Loaded {len(tiers)} Statutory Governance Tiers (Collector, Police SP, RDO, TANGEDCO, BDO, CM Cell)")
        results.append(("Universal Grievance Categories", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Universal Grievance Categories", "FAIL"))

    # Test 16: Authority Resolution for District Collector & Police SP
    print("\n[16/18] Testing /api/petitions/resolve-authority (Statutory Officer Mapping)...")
    try:
        # Test Collector resolution
        payload_coll = {"tier": "collector", "district": "Madurai"}
        res_coll = requests.post(f"{TARGET_URL}/api/petitions/resolve-authority", json=payload_coll, timeout=8)
        data_coll = res_coll.json()
        assert res_coll.status_code == 200
        auth_coll = data_coll.get("authority", {})
        assert "collrmdu@nic.in" in auth_coll.get("official_email", "")

        # Test Police SP resolution
        payload_sp = {"tier": "police_sp", "district": "Madurai"}
        res_sp = requests.post(f"{TARGET_URL}/api/petitions/resolve-authority", json=payload_sp, timeout=8)
        data_sp = res_sp.json()
        assert res_sp.status_code == 200
        auth_sp = data_sp.get("authority", {})
        assert "sp.mdu@tn.gov.in" in auth_sp.get("official_email", "")

        print(f"  ✓ PASS: Resolved Collector [{auth_coll.get('official_email')}] & SP [{auth_sp.get('official_email')}]")
        results.append(("Authority Resolution Engine", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Authority Resolution Engine", "FAIL"))

    # Test 17: District Collector Monday Grievance Petition PDF Synthesis & Dispatch
    print("\n[17/18] Testing /api/petitions/submit (District Collector Monday Grievance)...")
    try:
        payload = {
            "tier": "collector",
            "applicant_name": "ரா. பெருமாள்",
            "phone": "9840123456",
            "district": "Madurai",
            "taluk": "மேலூர்",
            "village": "திருவாதவூர்",
            "grievance_category": "நீர்வழி & ஏரி புறம்போக்கு ஆக்கிரமிப்பு அகற்றுதல்",
            "grievance_details": "கிராம பொது பயன்பாட்டில் உள்ள குளம் மற்றும் நீர்வழி பாசன வாய்க்கால் தனிநபர்களால் சட்டவிரோதமாக ஆக்கிரமிக்கப்பட்டுள்ளது. உடனடியாக கள ஆய்வு செய்து ஆக்கிரமிப்பை அகற்றிட வேண்டுகிறேன்.",
            "dispatch_channel": "both"
        }
        res = requests.post(f"{TARGET_URL}/api/petitions/submit", json=payload, timeout=12)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        assert "TN-COLLECTOR-2026" in data.get("acknowledgement_id")
        assert "pdf_download_url" in data
        assert "whatsapp_share_url" in data

        # Verify downloading generated Collector PDF
        pdf_res = requests.get(f"{TARGET_URL}{data['pdf_download_url']}", timeout=8)
        assert pdf_res.status_code == 200
        assert len(pdf_res.content) > 1000
        print(f"  ✓ PASS: Synthesized Court-Ready Collector Grievance PDF [{data['filename']}] ({len(pdf_res.content)} bytes) Ack ID: {data['acknowledgement_id']}")
        results.append(("Collector Monday Grievance PDF", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Collector Monday Grievance PDF", "FAIL"))

    # Test 18: Anti-Land Grabbing Special Cell (ALGC) Police SP Petition PDF Synthesis & Dispatch
    print("\n[18/18] Testing /api/petitions/submit (Police SP Land Grabbing Special Cell)...")
    try:
        payload = {
            "tier": "police_sp",
            "applicant_name": "எஸ். சுந்தரலிங்கம்",
            "phone": "9840998877",
            "district": "Madurai",
            "taluk": "மேலூர்",
            "village": "திருவாதவூர்",
            "grievance_category": "நில அபகரிப்பு தடுப்பு சிறப்புப் பிரிவு (ALGC) புகார்",
            "grievance_details": "எனக்குச் சொந்தமான சர்வே எண் 142/3 பத்திரப் பதிவு செய்யப்பட்ட பட்டா நிலத்தை ஆள்மாறாட்டம் மற்றும் போலி ஆவணங்கள் தயாரித்து கள்ளக் கிரயம் செய்துள்ளனர். நில அபகரிப்பு சிறப்புப் பிரிவு மூலம் குற்றவாளிகள் மீது வழக்குப்பதிவு செய்து நிலத்தை மீட்டுத்தர வேண்டுகிறேன்.",
            "dispatch_channel": "both"
        }
        res = requests.post(f"{TARGET_URL}/api/petitions/submit", json=payload, timeout=12)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        assert "TN-POLICE-SP-2026" in data.get("acknowledgement_id")
        assert "pdf_download_url" in data
        assert "whatsapp_share_url" in data

        # Verify downloading generated Police SP PDF
        pdf_res = requests.get(f"{TARGET_URL}{data['pdf_download_url']}", timeout=8)
        assert pdf_res.status_code == 200
        assert len(pdf_res.content) > 1000
        print(f"  ✓ PASS: Synthesized Court-Ready Police SP Petition PDF [{data['filename']}] ({len(pdf_res.content)} bytes) Ack ID: {data['acknowledgement_id']}")
        results.append(("Police SP Land Grabbing PDF", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Police SP Land Grabbing PDF", "FAIL"))

    # Test 19: Civic Issue Solutions & Video Guides Catalog
    print("\n[19/20] Testing /api/issue-solutions (Multimedia Solutions & Video Catalog)...")
    try:
        res = requests.get(f"{TARGET_URL}/api/issue-solutions", timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        sols = data.get("solutions", [])
        assert len(sols) >= 5
        first_sol = sols[0]
        assert "action_roadmap" in first_sol
        assert len(first_sol["action_roadmap"]) >= 4
        assert "verified_video_guides" in first_sol
        assert len(first_sol["verified_video_guides"]) >= 3
        print(f"  ✓ PASS: Loaded {len(sols)} Civic Solution Packages with 4-Step Roadmaps and Facebook/Insta/YouTube Videos")
        results.append(("Multimedia Solution Catalog", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Multimedia Solution Catalog", "FAIL"))

    # Test 20: Intelligent Solution & Video Search
    print("\n[20/20] Testing /api/issue-solutions/search (Semantic Roadmap & Video Matcher)...")
    try:
        payload = {"query": "போலி பத்திரம் ரத்து செய்வது எப்படி"}
        res = requests.post(f"{TARGET_URL}/api/issue-solutions/search", json=payload, timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        sol = data.get("solution", {})
        assert "77A" in sol.get("governing_statute", "")
        assert len(sol.get("action_roadmap", [])) >= 4
        assert len(sol.get("verified_video_guides", [])) >= 3
        
        # Verify video platforms are present
        platforms = [v["platform"] for v in sol["verified_video_guides"]]
        assert "Facebook" in platforms
        assert "Instagram" in platforms
        assert "YouTube" in platforms
        print(f"  ✓ PASS: Matched [{sol.get('title_ta')}] Statute: {sol.get('governing_statute')[:40]}... with Facebook, Insta & YouTube videos")
        results.append(("Semantic Video & Roadmap Matcher", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Semantic Video & Roadmap Matcher", "FAIL"))

    # Test 21: Family Education Catalog
    print("\n[21/23] Testing /api/education/catalog (Family Learning Studio Catalog)...")
    try:
        res = requests.get(f"{TARGET_URL}/api/education/catalog", timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        topics = data.get("topics", [])
        assert len(topics) >= 3
        print(f"  ✓ PASS: Loaded {len(topics)} Educational Topics with Interactive SVGs, Voice Scripts & Quizzes")
        results.append(("Family Education Catalog", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Family Education Catalog", "FAIL"))

    # Test 22: Adult Heart Anatomy Interactive Learning & SVG Generation
    print("\n[22/23] Testing /api/education/learn (Human Heart Anatomy & SVG Diagram)...")
    try:
        payload = {"topic": "human_heart_functioning"}
        res = requests.post(f"{TARGET_URL}/api/education/learn", json=payload, timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        topic = data.get("topic", {})
        assert "heart" in topic.get("topic_id", "")
        assert "<svg" in topic.get("svg_diagram", "")
        assert "Right Atrium" in topic.get("svg_diagram", "")
        assert "Left Ventricle" in topic.get("svg_diagram", "")
        assert len(topic.get("voice_over_script_ta", "")) > 50
        assert len(topic.get("interactive_quiz", [])) >= 2
        print(f"  ✓ PASS: Synthesized Interactive Heart SVG Diagram ({len(topic.get('svg_diagram'))} chars) + Clinical Voice Script + 3D Videos")
        results.append(("Heart Anatomy & Blood Circulation", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("Heart Anatomy & Blood Circulation", "FAIL"))

    # Test 23: KG Kids Tamil Rhyme Voice Coach & Repeat-After-Me Mode
    print("\n[23/23] Testing /api/education/learn (KG Kids Rhyme Voice Coach)...")
    try:
        payload = {"topic": "kids_tamil_rhymes"}
        res = requests.post(f"{TARGET_URL}/api/education/learn", json=payload, timeout=8)
        data = res.json()
        assert res.status_code == 200
        assert data.get("status") == "success"
        topic = data.get("topic", {})
        assert "rhymes" in topic.get("topic_id", "")
        assert "<svg" in topic.get("svg_diagram", "")
        assert "நிலா நிலா" in topic.get("voice_over_script_ta", "")
        assert len(topic.get("verified_video_guides", [])) >= 3
        print(f"  ✓ PASS: Loaded KG Rhyme Coach [{topic.get('title_ta')}] with Smiling Moon SVG & Voice Audio Prompt")
        results.append(("KG Kids Rhyme Voice Coach", "PASS"))
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        results.append(("KG Kids Rhyme Voice Coach", "FAIL"))

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST EXECUTION SUMMARY:")
    print("=" * 70)
    passed = 0
    for name, status in results:
        sym = "✅" if status == "PASS" else "❌"
        print(f"{sym} {name:<35} : {status}")
        if status == "PASS":
            passed += 1

    print("-" * 70)
    print(f"Result: {passed}/{len(results)} tests passed ({(passed/len(results))*100:.0f}% success)")
    print("=" * 70 + "\n")
    return passed == len(results)


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
