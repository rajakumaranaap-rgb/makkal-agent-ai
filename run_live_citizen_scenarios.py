# -*- coding: utf-8 -*-
"""
Live Citizen Scenario Demonstration & Verification
Hits the live AWS EC2 Production server via Cloudflare HTTPS Tunnel:
URL: https://regulatory-stack-counter-lady.trycloudflare.com
"""

import sys
import json
import time
import urllib.request
from typing import Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://regulatory-stack-counter-lady.trycloudflare.com"

def api_post(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=35) as resp:
        return json.loads(resp.read().decode("utf-8"))

def api_get(endpoint: str) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=35) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_scenarios():
    print("=" * 75)
    print("🇮🇳 SIA MAKKAL AGENT AI — LIVE PRODUCTION CITIZEN SCENARIOS TEST")
    print(f"Target: {BASE_URL}")
    print("=" * 75)

    # --------------------------------------------------------------------------
    # SCENARIO 1: FARMER (உழவர் - தஞ்சாவூர் / மதுரை)
    # --------------------------------------------------------------------------
    print("\n" + "🌾" * 30)
    print("SCENARIO 1: உழவர் (Farmer) - நிலப் பட்டா மாறுதல் & அறுவடை இயந்திர வாடகை")
    print("🌾" * 30)
    
    print("\n[Step 1.1] Baseten 816B Open-Weights சட்டப்பூர்வ பட்டா கட்டண ஆலோசனை...")
    farmer_query = {
        "message": "எனக்கு நிலம் சர்வே செய்து கிரய பட்டா பெயர் மாற்றம் செய்ய வேண்டும், அரசு கட்டணம் எவ்வளவு? இடைத்தரகர் ரூ.3500 கேட்கிறார்.",
        "use_open_weight": True,
        "language": "ta"
    }
    chat_res = api_post("/api/chat", farmer_query)
    print(f"  • AI மாதிரி: {chat_res.get('model_used')}")
    print(f"  • பதிலின் சுருக்கம் (Snippet):")
    reply = chat_res.get("reply", "")
    for line in reply.split("\n")[:8]:
        if line.strip():
            print(f"    {line.strip()}")
    assert chat_res.get("status") == "success"

    print("\n[Step 1.2] உழவர் அறுவடை இயந்திரம் வாடகைக்கு தேடுதல் (தஞ்சாவூர் 613001)...")
    search_res = api_post("/api/hyperlocal/pincode-lookup", {
        "pincode": "613001",
        "category": "agriculture"
    })
    print(f"  • கண்டறியப்பட்ட மாவட்டம்: {search_res.get('district')} ({search_res.get('area_ta')})")
    providers = search_res.get("providers", [])
    print(f"  • பதிவுசெய்யப்பட்ட உழவர் சேவை வழங்குநர்கள்: {len(providers)} நபர்கள்")
    for p in providers[:2]:
        print(f"    🚜 {p.get('name')} — {p.get('service')} (கட்டணம்: ₹{p.get('rate_per_unit')}/hr | போன்: {p.get('phone')})")
    assert len(providers) > 0

    print("\n[Step 1.3] உழவர் அறுவடை இயந்திரம் நேரடி முன்பதிவு & UPI கட்டண சீட்டு...")
    target_prov = providers[0]
    book_payload = {
        "provider_id": target_prov.get("provider_id"),
        "customer_name": "முத்துசாமி உழவர்",
        "customer_phone": "9842100222",
        "units": 3,
        "notes": "தஞ்சாவூர் வயல் அறுவடைக்கு உடனடி தேவை"
    }
    book_res = api_post("/api/hyperlocal/book", book_payload)
    b = book_res.get("booking", {})
    print(f"  • முன்பதிவு எண் (Order ID): {b.get('order_id')}")
    print(f"  • பணி தொடக்க OTP: {b.get('otp')}")
    print(f"  • மொத்தக் கட்டணம்: ₹{b.get('total_amount')}")
    print(f"  • GPay UPI கட்டண இணைப்பு: {b.get('upi_pay_url')}")
    assert b.get("status") == "confirmed"
    print("  ✅ SCENARIO 1 PASSED: உழவர் உரிமைகள் பாதுகாக்கப்பட்டு அறுவடை இயந்திரம் முன்பதிவு செய்யப்பட்டது!")

    # --------------------------------------------------------------------------
    # SCENARIO 2: STUDENT (மாணவர் - TNPSC தேர்வு வழிகாட்டி & CBT தேர்வு)
    # --------------------------------------------------------------------------
    print("\n" + "📚" * 30)
    print("SCENARIO 2: மாணவர் (Student) - TNPSC குரூப் 4 வரைபட வழிகாட்டி & ஆன்லைன் தேர்வு")
    print("📚" * 30)

    print("\n[Step 2.1] அதிகாரப்பூர்வ TNPSC போர்டல் வழிகாட்டி & படிமுறை வரைபடம்...")
    guide_res = api_post("/api/guide/diagrammatic-solve", {
        "query": "TNPSC குரூப் 4 மற்றும் VAO தேர்வு பாடத்திட்டம் தகுதி என்ன?",
        "phone": "6381029380"
    })
    print(f"  • போர்டல் இணைப்பு: {guide_res.get('portal_url')}")
    print(f"  • அதிகாரப்பூர்வ கட்டணம்: {guide_res.get('statutory_fee_text')}")
    print(f"  • வழிகாட்டுதல் படிகள் ({len(guide_res.get('roadmap_steps', []))} Steps):")
    for s in guide_res.get("roadmap_steps", [])[:3]:
        print(f"    👉 படி {s.get('step')}: {s.get('title')} ({s.get('domain')})")
    assert guide_res.get("status") == "success"

    print("\n[Step 2.2] TutO QBank மூலம் உடனடி ஆன்லைன் மாதிரித் தேர்வு உருவாக்கம்...")
    exam_res = api_post("/api/exam/generate", {
        "topic": "TNPSC Group 4 General Tamil & Indian Polity",
        "num_questions": 3,
        "language": "bilingual",
        "student_name": "கார்த்திகா மாணவி",
        "student_phone": "9840223344"
    })
    session = exam_res.get("session") or exam_res
    token = session.get("token") or exam_res.get("exam_token")
    questions = session.get("questions") or exam_res.get("questions", [])
    print(f"  • தேர்வு டோக்கன்: {token}")
    print(f"  • வினாக்கள் எண்ணிக்கை: {len(questions)}")
    if questions:
        q1 = questions[0].get("question_ta") or questions[0].get("question")
        print(f"  • மாதிரி வினா 1: {q1}")

    print("\n[Step 2.3] தேர்வை எழுதி சமர்ப்பித்து உடனடி திறன் சான்றிதழ் பெறுதல்...")
    submit_res = api_post("/api/exam/submit", {
        "token": token,
        "exam_token": token,
        "student_name": "கார்த்திகா மாணவி",
        "student_phone": "9840223344",
        "answers": {"1": "A", "2": "B", "3": "A"},
        "time_spent_secs": 95
    })
    result_data = submit_res.get("result") or submit_res
    score = result_data.get("score") if result_data.get("score") is not None else result_data.get("correct_count")
    total = result_data.get("total") if result_data.get("total") is not None else result_data.get("total_questions")
    pct = result_data.get("percentage") if result_data.get("percentage") is not None else result_data.get("score_percentage")
    cert_hash = result_data.get("certificate_hash") or result_data.get("verification_hash")
    raw_cert_url = result_data.get("certificate_url") or f"/api/exam/certificate/{cert_hash}"
    cert_full_url = raw_cert_url if str(raw_cert_url).startswith("http") else f"{BASE_URL}{raw_cert_url}"

    print(f"  • மதிப்பெண்: {score} / {total} ({pct}%)")
    print(f"  • தகுதி நிலை (Grade): {result_data.get('grade')}")
    print(f"  • அதிகாரப்பூர்வ சான்றிதழ் எண்: {cert_hash}")
    print(f"  • சரிபார்ப்பு இணைய இணைப்பு: {cert_full_url}")
    assert submit_res.get("status") == "success"
    print("  ✅ SCENARIO 2 PASSED: மாணவருக்கான தேர்வு வழிகாட்டி மற்றும் சான்றிதழ் வழங்கப்பட்டது!")

    # --------------------------------------------------------------------------
    # SCENARIO 3: CITIZEN ON WHATSAPP (வாட்ஸ்அப் நேரடி ஜிபிஎஸ் & ஓட்டுநர் சேவை)
    # --------------------------------------------------------------------------
    print("\n" + "📱" * 30)
    print("SCENARIO 3: வாட்ஸ்அப் குடிமக்கள் - ஜிபிஎஸ் இருப்பிடம் & பைக் டாக்சி ஆர்டர்")
    print("📱" * 30)

    print("\n[Step 3.1] வாட்ஸ்அப் மூலம் GPS இருப்பிடம் பகிர்தல் (Live Location Pin Drop)...")
    loc_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "1213113635214047",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {"display_phone_number": "15550284488", "phone_number_id": "1213113635214047"},
                    "contacts": [{"profile": {"name": "Madurai Citizen"}, "wa_id": "919840889900"}],
                    "messages": [{
                        "from": "919840889900",
                        "id": f"wamid.LIVE_{int(time.time())}",
                        "timestamp": str(int(time.time())),
                        "type": "location",
                        "location": {
                            "latitude": 9.9195,
                            "longitude": 78.1193,
                            "name": "Madurai Meenakshi Amman Temple",
                            "address": "South Chithirai Street, Madurai 625001"
                        }
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    loc_resp = api_post("/api/whatsapp/webhook", loc_payload)
    print(f"  • வாட்ஸ்அப் வரவேற்பு நிலை: {loc_resp.get('status')}")
    wa_details = loc_resp.get("details", {})
    print(f"  • கண்டறியப்பட்ட மாவட்டம்: {wa_details.get('location', {}).get('district')} ({wa_details.get('location', {}).get('area_ta')})")
    print(f"  • ஒதுக்கப்பட்ட பின்கோடு: {wa_details.get('location', {}).get('pincode')}")

    print("\n[Step 3.2] வாட்ஸ்அப் வழி பைக் டாக்சி சவாரி கோரிக்கை (600082 கொளத்தூர்)...")
    bike_text_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "1213113635214047",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {"display_phone_number": "15550284488", "phone_number_id": "1213113635214047"},
                    "contacts": [{"profile": {"name": "Chennai Citizen"}, "wa_id": "919840112233"}],
                    "messages": [{
                        "from": "919840112233",
                        "id": f"wamid.BIKE_{int(time.time())}",
                        "timestamp": str(int(time.time())),
                        "type": "text",
                        "text": {"body": "600082 கொளத்தூர் பைக் டாக்சி புக் செய்ய வேண்டும் ஜிபே UPI செலுத்துகிறேன்"}
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    bike_resp = api_post("/api/whatsapp/webhook", bike_text_payload)
    print(f"  • வாட்ஸ்அப் வரவேற்பு நிலை: {bike_resp.get('status')}")
    print(f"  • கையாளுபவர் (Handler): {bike_resp.get('details', {}).get('handler')}")
    reply_wa = bike_resp.get("details", {}).get("reply", "")
    for line in reply_wa.split("\n")[:6]:
        if line.strip():
            print(f"    {line.strip()}")
    assert bike_resp.get("status") == "received"
    print("  ✅ SCENARIO 3 PASSED: வாட்ஸ்அப் ஜிபிஎஸ் மற்றும் பைக் டாக்சி நேரடி ஒதுக்கீடு வெற்றிகரமாக முடிந்தது!")

    print("\n" + "=" * 75)
    print("🎉 ALL 3 LIVE CITIZEN PRODUCTION SCENARIOS FULLY VERIFIED ON AWS CLOUDFLARE!")
    print("=" * 75)

if __name__ == "__main__":
    run_scenarios()
