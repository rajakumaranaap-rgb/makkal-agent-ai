import sys
import os
import json
import traceback

# Force UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, r"D:\api\makkal-agent-ai")

# Safe mock for reportlab if missing locally
try:
    import reportlab
except ImportError:
    import types
    reportlab = types.ModuleType("reportlab")
    lib = types.ModuleType("reportlab.lib")
    pagesizes = types.ModuleType("reportlab.lib.pagesizes")
    pagesizes.letter = (612, 792)
    pagesizes.A4 = (595, 842)
    colors = types.ModuleType("reportlab.lib.colors")
    colors.HexColor = lambda c: c
    colors.black = "black"
    colors.white = "white"
    platypus = types.ModuleType("reportlab.platypus")
    class MockDoc:
        def __init__(self, *args, **kwargs): pass
        def build(self, story): pass
    platypus.SimpleDocTemplate = MockDoc
    platypus.Paragraph = lambda t, s: t
    platypus.Spacer = lambda w, h: (w, h)
    platypus.Table = lambda data, **kwargs: data
    platypus.TableStyle = lambda styles: styles
    platypus.KeepTogether = lambda x: x
    platypus.HRFlowable = lambda *args, **kwargs: None
    styles = types.ModuleType("reportlab.lib.styles")
    class MockStyleSheet(dict):
        def add(self, s): pass
    styles.getSampleStyleSheet = lambda: MockStyleSheet()
    styles.ParagraphStyle = lambda *args, **kwargs: {}
    pdfgen = types.ModuleType("reportlab.pdfgen")
    canvas = types.ModuleType("reportlab.pdfgen.canvas")
    canvas.Canvas = lambda *args, **kwargs: None

    sys.modules["reportlab"] = reportlab
    sys.modules["reportlab.lib"] = lib
    sys.modules["reportlab.lib.pagesizes"] = pagesizes
    sys.modules["reportlab.lib.colors"] = colors
    sys.modules["reportlab.platypus"] = platypus
    sys.modules["reportlab.lib.styles"] = styles
    sys.modules["reportlab.pdfgen"] = pdfgen
    sys.modules["reportlab.pdfgen.canvas"] = canvas

print("=" * 80)
print("SIA MAKKAL AGENT AI — DAILY NEWS & AIR ALL INDIA RADIO TEST SUITE")
print("Target: Meta AI Developer Hackathon 2026 ($150,000 Grand Prize)")
print("=" * 80)

failures = []
passes = []

def run_test(name, fn):
    print(f"\n▶ Testing: {name} ...", end=" ")
    try:
        fn()
        passes.append(name)
        print("✅ PASSED")
    except Exception as e:
        failures.append((name, str(e)))
        print(f"❌ FAILED: {e}")
        traceback.print_exc()

# ==============================================================================
# TEST 1: Daily News Bulletin Structure (10 TN + 5 IN + 3 WD)
# ==============================================================================
def test_daily_news_bulletin_structure():
    import daily_news_air_engine as dne

    b = dne.get_daily_news_bulletin()
    assert b["status"] == "success"
    assert b["total_news_count"] == 18, f"Expected 18 news items, got {b['total_news_count']}"
    assert b["tamil_nadu_news_count"] == 10, f"Expected 10 TN news, got {b['tamil_nadu_news_count']}"
    assert b["india_news_count"] == 5, f"Expected 5 India news, got {b['india_news_count']}"
    assert b["world_news_count"] == 3, f"Expected 3 World news, got {b['world_news_count']}"
    assert "2026" in b["date_tamil"] or len(b["date_tamil"]) > 5

    # Check AIR Metadata
    assert "newsonair.gov.in" in b["air_broadcast"]["official_portal"]
    assert "Akashvani" in b["air_broadcast"]["station_name"] or "வானொலி" in b["air_broadcast"]["station_name"]

run_test("Daily News Bulletin Structure (10 TN + 5 IN + 3 WD)", test_daily_news_bulletin_structure)

# ==============================================================================
# TEST 2: WhatsApp Formatting & Interactive Menus
# ==============================================================================
def test_whatsapp_formatting():
    import daily_news_air_engine as dne

    msg = dne.format_whatsapp_news_briefing(user_name="செந்தில் குமார்")
    assert "செந்தில் குமார்" in msg
    assert "காலை வணக்கம்" in msg
    assert "தமிழ்நாடு முக்கிய 10 செய்திகள்" in msg
    assert "இந்திய தேசிய 5 முக்கிய செய்திகள்" in msg
    assert "உலக முக்கிய 3 செய்திகள்" in msg
    assert "newsonair.gov.in" in msg

    menu = dne.format_whatsapp_news_menu()
    assert len(menu["buttons"]) == 3
    assert any(b["id"] == "btn_news_air" for b in menu["buttons"])

    air_card = dne.format_air_audio_news_card()
    assert "07:15 AM" in air_card or "07:15 மணி" in air_card
    assert "newsonair.gov.in" in air_card

run_test("WhatsApp Formatting & Interactive Menus", test_whatsapp_formatting)

# ==============================================================================
# TEST 3: WhatsApp Ingress Good Morning & AIR Radio Triggers
# ==============================================================================
def test_whatsapp_ingress_triggers():
    import whatsapp_agent as wa

    # 1. User says "Good morning SIA! 오늘의 뉴스"
    payload_gm = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "text",
                        "text": {"body": "Good morning SIA! இன்றைய செய்திகள்"}
                    }]
                }
            }]
        }]
    }
    res_gm = wa.handle_whatsapp_ingress(payload_gm)
    assert res_gm.get("status") == "processed", f"Expected processed, got {res_gm}"
    assert res_gm.get("handler") == "daily_news_full_briefing", f"Handler mismatch: {res_gm.get('handler')}"
    assert res_gm.get("total_news") == 18

    # 2. User clicks "btn_news_air"
    payload_air = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "btn_news_air", "title": "🎙️ AIR வானொலி ஒலி"}
                        }
                    }]
                }
            }]
        }]
    }
    res_air = wa.handle_whatsapp_ingress(payload_air)
    assert res_air.get("status") == "processed"
    assert res_air.get("handler") == "daily_news_air_audio"

    # 3. User clicks "btn_news_tn"
    payload_tn = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "btn_news_tn", "title": "🏛️ தமிழ்நாடு மட்டும்"}
                        }
                    }]
                }
            }]
        }]
    }
    res_tn = wa.handle_whatsapp_ingress(payload_tn)
    assert res_tn.get("status") == "processed"
    assert res_tn.get("handler") == "daily_news_tamil_nadu_top10"

run_test("WhatsApp Ingress Good Morning & AIR Radio Triggers", test_whatsapp_ingress_triggers)

# ==============================================================================
# TEST 4: FastAPI Endpoints Verification
# ==============================================================================
def test_fastapi_news_endpoints():
    from fastapi.testclient import TestClient
    from app import app

    client = TestClient(app)

    # 1. Daily Bulletin Endpoint
    r1 = client.get("/api/news/daily-bulletin")
    assert r1.status_code == 200, f"Status: {r1.status_code}"
    data1 = r1.json()
    assert data1["status"] == "success"
    assert data1["total_news_count"] == 18
    assert len(data1["tamil_nadu_news"]) == 10
    assert len(data1["india_news"]) == 5
    assert len(data1["world_news"]) == 3

    # 2. AIR Audio Endpoint
    r2 = client.get("/api/news/air-audio")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["status"] == "success"
    assert "newsonair.gov.in" in data2["air_metadata"]["official_portal"]

    # 3. Push to WhatsApp Endpoint
    r3 = client.post("/api/news/push-to-whatsapp", json={
        "phone": "6381029380",
        "user_name": "அருண் குமார்"
    })
    assert r3.status_code == 200
    assert r3.json()["status"] == "success"

run_test("FastAPI News Endpoints Verification", test_fastapi_news_endpoints)

print("\n" + "=" * 80)
print(f"RESULTS: {len(passes)} PASSED, {len(failures)} FAILED")
print("=" * 80)
if failures:
    for name, err in failures:
        print(f"  ❌ {name}: {err}")
    sys.exit(1)
else:
    print("🏆 ALL DAILY NEWS & AIR RADIO TESTS PASSED AT 100% STATUTORY PRECISION!")
