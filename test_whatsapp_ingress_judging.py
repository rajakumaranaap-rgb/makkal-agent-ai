# -*- coding: utf-8 -*-
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from whatsapp_agent import process_incoming_whatsapp_message

def make_payload(text="", interactive_id="", interactive_title=""):
    msg = {
        "from": "6381029380",
        "id": "test_wamid_123",
        "timestamp": "1730617000"
    }
    if interactive_id:
        msg["type"] = "interactive"
        msg["interactive"] = {
            "type": "button_reply",
            "button_reply": {"id": interactive_id, "title": interactive_title or "Click"}
        }
    else:
        msg["type"] = "text"
        msg["text"] = {"body": text}
    
    return {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [msg]
                }
            }]
        }]
    }

# 1. Test "hi sia"
p1 = make_payload(text="hi sia")
r1 = process_incoming_whatsapp_message(p1)
print("WA Ingress 'hi sia': status =", r1.get("status"), "| stage =", r1.get("stage"))
assert "வணக்கம்!" in r1.get("reply", "") or "வணக்கம்!" in r1.get("reply_text", "")

# 2. Test "1"
p2 = make_payload(text="1")
r2 = process_incoming_whatsapp_message(p2)
print("WA Ingress '1': status =", r2.get("status"), "| stage =", r2.get("stage"))
assert "வேளாண்மை" in r2.get("reply", "") or "வேளாண்மை" in r2.get("reply_text", "")

# 3. Test Inactivity Nudge Button
p3 = make_payload(interactive_id="trigger_inactivity_nudge", interactive_title="Simulate Inactivity")
r3 = process_incoming_whatsapp_message(p3)
print("WA Ingress Inactivity Nudge: status =", r3.get("status"), "| stage =", r3.get("stage"))
assert "காத்திருக்கிறீர்களா" in r3.get("reply", "") or "காத்திருக்கிறீர்களா" in r3.get("reply_text", "")

print("ALL WHATSAPP INGRESS TESTS PASSED SUCCESSFULLY!")
