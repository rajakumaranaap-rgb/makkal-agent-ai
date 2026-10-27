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
    print("[1/8] Testing /health endpoint...")
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
    print("\n[2/8] Testing /api/catalog endpoint...")
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
    print("\n[3/8] Testing /api/chat with Meta Muse Spark 1.3 (Tamil)...")
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
    print("\n[4/8] Testing /api/chat with Meta Muse Wonder 1.0 (Deep Reasoning)...")
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
    print("\n[5/8] Testing /api/chat with Baseten Open-Weight Model ($10k Prize Track)...")
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
    print("\n[6/8] Testing /api/audit-document with Meta SAM 3.1...")
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
    print("\n[7/8] Testing /api/generate-petition (Autonomous Action Engine)...")
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
    print("\n[8/8] Testing Meta WhatsApp Cloud API Webhook handshake...")
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
