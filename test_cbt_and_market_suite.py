"""
==============================================================================
Makkal Agent AI - CBT Exam Generator & Boto Market Intelligence Test Suite
==============================================================================
Validates:
1. Dynamic CBT Exam Synthesis & Active Session Registry
2. Automated Evaluation Engine & Verifiable SVG Certificate of Excellence
3. Diagrammatic Study Notes Engine (Mermaid Diagrams & Conceptual Frameworks)
4. Boto Market Intelligence Bridge (Institutional Equities, F&O Strategies, Crypto Tax)
5. WhatsApp Agent Conversational & Button Ingress Triggers
6. FastAPI REST Endpoints (/api/exam/* and /api/market/*)
==============================================================================
"""

import os
import sys
import json
from typing import Dict, Any

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

from cbt_exam_and_notes_engine import (
    create_custom_cbt_exam,
    evaluate_cbt_exam,
    generate_skill_certificate_svg,
    generate_topic_study_notes,
    format_whatsapp_cbt_invite,
    ACTIVE_EXAM_SESSIONS
)
from boto_market_intelligence_bridge import (
    get_boto_market_snapshot,
    query_boto_recommendations,
    BOTO_EQUITY_UNIVERSE,
    BOTO_FNO_STRATEGIES,
    BOTO_CRYPTO_RADAR
)
import whatsapp_agent as wa
from fastapi.testclient import TestClient
from app import app


def run_unit_tests():
    print("=" * 80)
    print("SIA MAKKAL AGENT AI — CBT EXAMS & BOTO SHARE MARKET TEST SUITE")
    print("Target: Meta AI Developer Hackathon 2026 ($150,000 Grand Prize)")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # 1. CBT EXAM GENERATOR & EVALUATION ENGINE
    # --------------------------------------------------------------------------
    print("\n[1/5] Testing Dynamic CBT Exam Generator & Session Registry...")
    exam = create_custom_cbt_exam(
        topic="Indian Constitution Fundamental Rights",
        num_questions=5,
        language="bilingual",
        difficulty="UPSC Civil Services",
        student_name="Sundar Pichai",
        student_phone="9840123456"
    )
    print(f"  ✅ Generated Exam Token: {exam['token']}")
    print(f"     Topic: {exam['topic']} | Qty: {len(exam['questions'])} | Time: {exam['time_limit_mins']} mins")
    print(f"     Secure Link: {exam['exam_url']}")
    assert len(exam['questions']) == 5, f"Expected 5 questions, got {len(exam['questions'])}"
    assert exam['token'] in ACTIVE_EXAM_SESSIONS

    q1 = exam['questions'][0]
    assert "options_ta" in q1 and "options_en" in q1
    assert q1['correct_option'] in ["A", "B", "C", "D"]

    # --------------------------------------------------------------------------
    # 2. EVALUATION & SVG CERTIFICATE ENGINE
    # --------------------------------------------------------------------------
    print("\n[2/5] Testing CBT Evaluation Engine & Verifiable SVG Certificate...")
    user_answers = {str(q['q_id']): q['correct_option'] for q in exam['questions']}
    eval_result = evaluate_cbt_exam(
        exam_token=exam['token'],
        answers=user_answers,
        time_spent_secs=95
    )
    print(f"  ✅ Evaluated Score: {eval_result['correct_count']}/{eval_result['total_questions']} ({eval_result['score_percentage']}%)")
    print(f"     Grade: {eval_result['grade']}")
    print(f"     Verification Hash: {eval_result['verification_hash']}")
    assert eval_result['score_percentage'] == 100.0
    assert "A+" in eval_result['grade']
    assert "SIA-CERT-" in eval_result['verification_hash']

    cert_svg = generate_skill_certificate_svg(eval_result)
    assert "<svg" in cert_svg and "</svg>" in cert_svg
    assert "Sundar Pichai" in cert_svg
    assert eval_result['verification_hash'] in cert_svg
    print(f"  ✅ Official SVG Certificate Generated ({len(cert_svg)} bytes)")

    # --------------------------------------------------------------------------
    # 3. TOPIC STUDY NOTES & MERMAID DIAGRAM ENGINE
    # --------------------------------------------------------------------------
    print("\n[3/5] Testing Topic Study Notes with Mermaid Diagrams...")
    notes = generate_topic_study_notes(
        topic="Snell's Law and Optics",
        target_exam="Class 12 CBSE & NEET"
    )
    print(f"  ✅ Generated Notes for: {notes['topic']} ({notes['target_exam']})")
    assert "mermaid" in notes['notes_ta']
    assert "graph" in notes['notes_ta']

    # --------------------------------------------------------------------------
    # 4. BOTO QUANT MARKET INTELLIGENCE BRIDGE
    # --------------------------------------------------------------------------
    print("\n[4/5] Testing Boto Quant Market Intelligence Bridge...")
    snapshot = get_boto_market_snapshot()
    print(f"  ✅ Market Status: {snapshot['status']} | NIFTY Spot: ₹{snapshot['nifty_spot']} | PCR: {snapshot['nifty_pcr']}")
    print(f"     Equities: {len(snapshot['equities'])} | F&O: {len(snapshot['fno_setups'])} | Crypto: {len(snapshot['crypto_radar'])}")
    assert len(snapshot['equities']) >= 5
    assert "SEBI" in snapshot['sebi_disclaimer_ta']

    eq_advice = query_boto_recommendations("RELIANCE")
    print(f"  ✅ Stock Advisory: {eq_advice['symbol']} - Entry: ₹{eq_advice['data']['entry']} | SL: ₹{eq_advice['data']['sl']} | T1: ₹{eq_advice['data']['t1']}")
    assert "SEBI" in eq_advice['formatted_message']

    fno_advice = query_boto_recommendations("NIFTY FNO OPTION")
    print(f"  ✅ F&O Strategy: {fno_advice['data']['strategy_name']} ({fno_advice['data']['buy_leg']})")
    assert "SEBI" in fno_advice['formatted_message']

    crypto_advice = query_boto_recommendations("CRYPTO BITCOIN BTC")
    print(f"  ✅ Crypto Radar: {crypto_advice['asset']} - Strategy: {crypto_advice['data']['delta_strategy']}")
    assert "115BBH" in crypto_advice['formatted_message']

    # --------------------------------------------------------------------------
    # 5. FASTAPI REST ENDPOINTS & WHATSAPP INGRESS
    # --------------------------------------------------------------------------
    print("\n[5/5] Testing FastAPI Endpoints & WhatsApp Ingress...")
    client = TestClient(app)

    # 5.1 POST /api/exam/generate
    r_gen = client.post("/api/exam/generate", json={
        "topic": "Polity Governance",
        "num_questions": 5,
        "difficulty": "Hard",
        "language": "bilingual",
        "student_name": "Test Aspirant"
    })
    assert r_gen.status_code == 200, f"Error: {r_gen.text}"
    gen_data = r_gen.json()
    assert gen_data["status"] == "success"
    cbt_token = gen_data["session"]["token"]
    print(f"  ✅ POST /api/exam/generate -> Token: {cbt_token}")

    # 5.2 GET /api/exam/{token}
    r_get = client.get(f"/api/exam/{cbt_token}")
    assert r_get.status_code == 200
    assert r_get.json()["status"] == "success"
    print(f"  ✅ GET /api/exam/{cbt_token} -> Exam Questions Loaded")

    # 5.3 POST /api/exam/submit
    r_sub = client.post("/api/exam/submit", json={
        "token": cbt_token,
        "answers": {"1": "A", "2": "A", "3": "A", "4": "A", "5": "A"},
        "time_spent_secs": 80
    })
    assert r_sub.status_code == 200
    sub_data = r_sub.json()
    assert sub_data["status"] == "success"
    cert_hash = sub_data["result"]["verification_hash"]
    print(f"  ✅ POST /api/exam/submit -> Evaluated Grade: {sub_data['result']['grade']}")

    # 5.4 GET /api/exam/certificate/{hash_id}
    r_cert = client.get(f"/api/exam/certificate/{cert_hash}")
    assert r_cert.status_code == 200
    assert "image/svg+xml" in r_cert.headers.get("content-type", "")
    print(f"  ✅ GET /api/exam/certificate/{cert_hash} -> Official SVG Certificate Rendered")

    # 5.5 POST /api/exam/notes
    r_notes = client.post("/api/exam/notes", json={
        "topic": "Gravitation and Kepler Laws",
        "exam_type": "Class 11 Physics & JEE"
    })
    assert r_notes.status_code == 200
    assert r_notes.json()["status"] == "success"
    print(f"  ✅ POST /api/exam/notes -> Diagrammatic Notes Generated")

    # 5.6 GET /api/market/snapshot
    r_snap = client.get("/api/market/snapshot")
    assert r_snap.status_code == 200
    assert r_snap.json()["status"] == "success"
    print(f"  ✅ GET /api/market/snapshot -> Quant Snapshot OK")

    # 5.7 POST /api/market/query
    r_mquery = client.post("/api/market/query", json={"query": "RELIANCE"})
    assert r_mquery.status_code == 200
    assert r_mquery.json()["status"] == "success"
    print(f"  ✅ POST /api/market/query -> Boto Analysis for RELIANCE OK")

    # 5.8 WhatsApp Ingress for EXAM
    wa_payload_exam = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "919840123456",
                        "type": "text",
                        "text": {"body": "EXAM Polity 5"}
                    }]
                }
            }]
        }]
    }
    wa_res_exam = wa.handle_whatsapp_ingress(wa_payload_exam)
    assert wa_res_exam.get("status") in ["processed", "success"]
    print(f"  ✅ WhatsApp Ingress 'EXAM Polity 5' -> Handled Successfully")

    # 5.9 WhatsApp Ingress for SHARE
    wa_payload_share = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "919840123456",
                        "type": "text",
                        "text": {"body": "SHARE RELIANCE"}
                    }]
                }
            }]
        }]
    }
    wa_res_share = wa.handle_whatsapp_ingress(wa_payload_share)
    assert wa_res_share.get("status") in ["processed", "success"]
    print(f"  ✅ WhatsApp Ingress 'SHARE RELIANCE' -> Handled Successfully")

    print("\n" + "=" * 80)
    print("🏆 ALL CBT EXAMS & BOTO SHARE MARKET TESTS PASSED AT 100% SUCCESS!")
    print("================================================================================")


if __name__ == "__main__":
    run_unit_tests()
