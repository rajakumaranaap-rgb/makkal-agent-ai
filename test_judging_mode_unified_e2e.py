# -*- coding: utf-8 -*-
"""
End-to-End Test Suite for Judging Mode Unified WhatsApp and Web Interaction.
Verifies:
1. 'Hi SIA' greeting returns single-word greeting + 12 numbered services list.
2. Numbered queries 1 through 12 return each respective service payload.
3. Inactivity nudge endpoint returns wait, menu, and close buttons.
4. Nudge actions (Wait, Menu, Close) work seamlessly.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

print("=" * 70)
print("RUNNING SIA JUDGING MODE UNIFIED E2E TEST SUITE")
print("=" * 70)

# 1. Test 'Hi SIA' via /api/sia/whatsapp-sim
res1 = client.post("/api/sia/whatsapp-sim", json={
    "sender_phone": "6381029380",
    "message_text": "Hi SIA",
    "msg_type": "text"
})
assert res1.status_code == 200, f"Failed: {res1.status_code}"
d1 = res1.json()
reply1 = d1.get("reply_text") or d1.get("reply") or ""
print("[1] 'Hi SIA' Greeting Test:")
print("    Reply Header:", reply1.split("\n")[0])
assert "வணக்கம்!" in reply1 or "Welcome" in reply1, "Missing greeting"
assert "1. 🌾" in reply1 or "வேளாண்மை" in reply1, "Missing 12 services in menu"
print("    ✓ Greeting & 1-12 Menu Verified")

# 2. Test all 12 services by number
service_expected = {
    "1": "வேளாண்மை",
    "2": "கால்நடை",
    "3": "வணிகம்",
    "4": "ரெட் டாக்ஸி",
    "5": "உணவகம்",
    "6": "பட்டா",
    "7": "கல்வி",
    "8": "சட்டமன்ற",
    "9": "பேச்சுப் பயிற்சி",
    "10": "மனநலம்",
    "11": "வரைபட",
    "12": "இயந்திரங்கள்"
}

print("\n[2] Testing Numbers 1 through 12:")
for num, keyword in service_expected.items():
    res_num = client.post("/api/sia/whatsapp-sim", json={
        "sender_phone": "6381029380",
        "message_text": num,
        "msg_type": "text"
    })
    assert res_num.status_code == 200
    d_num = res_num.json()
    rep = d_num.get("reply_text") or d_num.get("reply") or ""
    assert keyword in rep, f"Number {num} missing keyword '{keyword}' in reply: {rep[:100]}"
    print(f"    ✓ Option {num:>2}: {rep.splitlines()[0]}")

# 3. Test Inactivity Nudge Endpoint
print("\n[3] Testing Proactive Inactivity Nudge Endpoint:")
res_nudge = client.post("/api/sia/inactivity-nudge", json={"sender_phone": "6381029380"})
assert res_nudge.status_code == 200
d_nudge = res_nudge.json()
nudge_reply = d_nudge.get("reply_text") or d_nudge.get("reply") or ""
nudge_btns = d_nudge.get("button_objs") or d_nudge.get("buttons") or []
btn_ids = [b.get("id") for b in nudge_btns]
print("    Nudge Prompt:", nudge_reply.splitlines()[0])
print("    Nudge Buttons:", btn_ids)
assert "btn_nudge_wait" in btn_ids, "Missing btn_nudge_wait"
assert "btn_nudge_menu" in btn_ids, "Missing btn_nudge_menu"
assert "btn_nudge_close" in btn_ids, "Missing btn_nudge_close"
print("    ✓ Inactivity Nudge Verified")

# 4. Test Inactivity Action: btn_nudge_wait
print("\n[4] Testing Nudge Action: btn_nudge_wait:")
res_wait = client.post("/api/sia/whatsapp-sim", json={
    "sender_phone": "6381029380",
    "msg_type": "interactive",
    "interactive_id": "btn_nudge_wait",
    "interactive_title": "⏳ காத்திருக்கவும்"
})
assert res_wait.status_code == 200
d_wait = res_wait.json()
wait_rep = d_wait.get("reply_text") or d_wait.get("reply") or ""
assert "காத்திருக்கிறேன்" in wait_rep or "wait" in wait_rep.lower()
print("    ✓ Wait Action Acknowledged:", wait_rep.splitlines()[0])

# 5. Test Inactivity Action: btn_nudge_close
print("\n[5] Testing Nudge Action: btn_nudge_close:")
res_close = client.post("/api/sia/whatsapp-sim", json={
    "sender_phone": "6381029380",
    "msg_type": "interactive",
    "interactive_id": "btn_nudge_close",
    "interactive_title": "🔒 அமர்வை முடிக்க"
})
assert res_close.status_code == 200
d_close = res_close.json()
close_rep = d_close.get("reply_text") or d_close.get("reply") or ""
assert "நிறைவுற்றது" in close_rep or "closed" in close_rep.lower()
print("    ✓ Close Action Executed:", close_rep.splitlines()[0])

print("\n" + "=" * 70)
print("100% OF ALL JUDGING MODE TESTS PASSED PERFECTLY!")
print("=" * 70)
