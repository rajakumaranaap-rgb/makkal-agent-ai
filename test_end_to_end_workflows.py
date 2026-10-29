import sys
import os
import json
import traceback
from pathlib import Path

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
print("SIA MAKKAL AGENT AI — END-TO-END COMPREHENSIVE WORKFLOW TEST SUITE")
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
# TEST 1: Travel & RedTaxi Zero-Surge Booking Engine
# ==============================================================================
def test_travel_engine():
    import travel_booking_engine as tbe

    # 1. Fare calculation
    fare = tbe.calculate_ride_fare("Madurai", "Rameswaram", vehicle_id="sedan", trip_type="one_way")
    assert fare["status"] == "success", "Fare calculation status not success"
    assert fare["distance_km"] == 175, f"Expected 175 km, got {fare['distance_km']}"
    assert fare["fare_breakdown"]["surge_percentage"] == 0, "Surge pricing must be 0%"
    assert fare["fare_breakdown"]["total_fare"] > 0, "Total fare must be > 0"

    # 2. Execute ride booking
    ride = tbe.execute_ride_booking(
        phone="6381029380",
        customer_name="அருண் குமார்",
        origin="Madurai Junction",
        destination="Rameswaram Temple",
        vehicle_id="sedan"
    )
    assert ride["status"] == "confirmed", "Ride booking status not confirmed"
    assert len(ride["ride_otp"]) == 4, "Ride OTP must be 4 digits"
    assert "TN" in ride["vehicle_plate"], "Vehicle plate must have TN RTO registration"
    assert "112" in ride["whatsapp_card"], "Must include 112 SOS protection"

    # 3. Fleet and temple packages
    fleet = tbe.get_fleet_catalog()
    assert len(fleet) >= 4, "Must have at least 4 fleet tiers"
    pkgs = tbe.get_temple_packages()
    assert len(pkgs) >= 4, "Must have at least 4 temple packages"

    # 4. WhatsApp formatters
    wa_menu = tbe.format_whatsapp_travel_menu()
    assert "buttons" in wa_menu and len(wa_menu["buttons"]) == 3
    wa_list = tbe.format_whatsapp_temple_list()
    assert len(wa_list["sections"][0]["rows"]) >= 4

run_test("Travel & RedTaxi Zero-Surge Booking Engine", test_travel_engine)

# ==============================================================================
# TEST 2: Universal Tuition, 10th CBSE Homework Solver & Study Planner
# ==============================================================================
def test_tuition_engine():
    import universal_tuition_engine as ute

    # 1. Ohm's Law physics problem
    sol_ohm = ute.solve_homework_submission(
        query_text="Calculate current if potential difference is 220V and resistance is 44 ohms",
        class_id="class_10",
        curriculum="CBSE",
        subject="Physics"
    )
    assert sol_ohm["status"] == "success"
    assert "V = I" in sol_ohm["formula_used"]
    assert len(sol_ohm["steps"]) >= 4
    assert "தண்ணீர் குழாயில்" in sol_ohm["tamil_analogy"]

    wa_msg = ute.format_whatsapp_homework_response(sol_ohm)
    assert "வீட்டுப்பாட தீர்வு" in wa_msg
    assert "220" in wa_msg or "V" in wa_msg

    # 2. Quadratic Equation math problem
    sol_quad = ute.solve_homework_submission(
        query_text="Solve quadratic equation x^2 - 5x + 6 = 0",
        class_id="class_10",
        curriculum="CBSE",
        subject="Mathematics"
    )
    assert "ax² + bx + c = 0" in sol_quad["formula_used"] or "x =" in sol_quad["formula_used"]

    # 3. Daily Study Schedule (Pomodoro 25/5)
    plan = ute.get_daily_student_study_plan(class_id="class_10", curriculum="CBSE")
    assert len(plan["daily_schedule"]) == 5
    assert any("Pomodoro" in r for r in plan["golden_study_rules"])

    plan_wa = ute.format_whatsapp_study_plan_message(class_id="class_10", curriculum="CBSE")
    assert "பொதுத் தேர்வு தினசரி படிப்பு அட்டவணை" in plan_wa

run_test("Universal Tuition, 10th CBSE Homework Solver & Study Planner", test_tuition_engine)

# ==============================================================================
# TEST 3: Agriculture & Farmer Welfare Agronomy Engine
# ==============================================================================
def test_agriculture_engine():
    import agriculture_engine as age

    # 1. TNAU weed and fertilizer protocol for Turmeric
    adv_turmeric = age.get_tnau_agronomy_advisory("turmeric")
    assert "Pendimethalin" in adv_turmeric["weed_control"]["chemical_ta"]
    assert "Nano DAP" in adv_turmeric["foliar_nutrition"]["product_ta"]
    assert "100%" in adv_turmeric["grains_subsidy"]["irrigation_subsidy_ta"]

    # 2. Paddy protocol
    adv_paddy = age.get_tnau_agronomy_advisory("paddy")
    assert "Pendimethalin" in adv_paddy["weed_control"]["chemical_ta"]

    # 3. Mandi Price Board
    mandi = age.get_all_mandi_prices()
    assert len(mandi["markets"]) >= 4

    # 4. WhatsApp Menus
    wa_menu = age.format_whatsapp_agri_menu()
    assert len(wa_menu["buttons"]) == 3
    wa_crops = age.format_whatsapp_agri_crops_list()
    assert len(wa_crops["sections"][0]["rows"]) >= 4

run_test("Agriculture & Farmer Welfare Agronomy Engine", test_agriculture_engine)

# ==============================================================================
# TEST 4: WhatsApp Agent Ingress & Service Router Integration
# ==============================================================================
def test_whatsapp_agent_ingress():
    import whatsapp_agent as wa

    # 1. Simulate button click for Travel RedTaxi
    payload_travel = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "btn_taxi_sedan", "title": "🚘 RedTaxi / கார்"}
                        }
                    }]
                }
            }]
        }]
    }
    res_travel = wa.handle_whatsapp_ingress(payload_travel)
    assert res_travel.get("status") == "processed", f"Expected processed, got {res_travel}"
    assert res_travel.get("handler") == "travel_booking_engine", f"Handler mismatch: {res_travel.get('handler')}"

    # 2. Simulate button click for Agri Sowing Calendar
    payload_agri = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "btn_agri_sow", "title": "📅 சாகுபடி காலண்டர்"}
                        }
                    }]
                }
            }]
        }]
    }
    res_agri = wa.handle_whatsapp_ingress(payload_agri)
    assert res_agri.get("status") == "processed"
    assert res_agri.get("handler") == "agriculture_agronomy_engine"

    # 3. Simulate button click for 10th Student Study Plan
    payload_study = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "916381029380",
                        "type": "interactive",
                        "interactive": {
                            "type": "button_reply",
                            "button_reply": {"id": "tui_study_plan", "title": "📅 படிப்பு அட்டவணை"}
                        }
                    }]
                }
            }]
        }]
    }
    res_study = wa.handle_whatsapp_ingress(payload_study)
    assert res_study.get("status") == "processed"
    assert res_study.get("handler") == "tuition_daily_study_plan"

run_test("WhatsApp Agent Ingress & Interactive Router", test_whatsapp_agent_ingress)

# ==============================================================================
# TEST 5: FastAPI Endpoints Verification via TestClient
# ==============================================================================
def test_fastapi_endpoints():
    from fastapi.testclient import TestClient
    from app import app

    client = TestClient(app)

    # 1. Tuition Homework Solve Endpoint
    r1 = client.post("/api/tuition/homework-solve", json={
        "query_text": "Find resistance when V=100V and I=5A",
        "class_id": "class_10",
        "curriculum": "CBSE",
        "subject": "Physics"
    })
    assert r1.status_code == 200, f"Status: {r1.status_code}"
    data1 = r1.json()
    assert data1["status"] == "success"
    assert "V = I" in data1["formula_used"]

    # 2. Tuition Study Plan Endpoint
    r2 = client.get("/api/tuition/daily-study-plan?class_id=class_10&curriculum=CBSE")
    assert r2.status_code == 200
    data2 = r2.json()
    assert len(data2["daily_schedule"]) == 5

    # 3. Travel Book Ride Endpoint
    r3 = client.post("/api/travel/book-ride", json={
        "origin": "Coimbatore",
        "destination": "Ooty",
        "vehicle_id": "suv",
        "phone": "6381029380"
    })
    assert r3.status_code == 200
    data3 = r3.json()
    assert data3["status"] == "confirmed"
    assert len(data3["ride_otp"]) == 4

    # 4. Travel Fleet Endpoint
    r4 = client.get("/api/travel/fleet")
    assert r4.status_code == 200
    assert len(r4.json()["fleet"]) >= 4

    # 5. Agri TNAU Advisory Endpoint
    r5 = client.post("/api/agri/tnau-advisory", json={"crop_key": "turmeric"})
    assert r5.status_code == 200
    assert "Pendimethalin" in r5.json()["weed_control"]["chemical_ta"]

    # 6. Diagrammatic Solve Endpoint
    r6 = client.post("/api/guide/diagrammatic-solve", json={"query": "TNPSC Group 4 தேர்வு வினாத்தாள்"})
    assert r6.status_code == 200
    assert r6.json()["status"] == "success"
    assert len(r6.json()["roadmap_steps"]) >= 3

run_test("FastAPI Endpoints Verification", test_fastapi_endpoints)

print("\n" + "=" * 80)
print(f"RESULTS: {len(passes)} PASSED, {len(failures)} FAILED")
print("=" * 80)
if failures:
    for name, err in failures:
        print(f"  ❌ {name}: {err}")
    sys.exit(1)
else:
    print("🏆 ALL WORKFLOWS PASSED AT 100% STATUTORY PRECISION!")
