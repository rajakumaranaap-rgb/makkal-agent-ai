from whatsapp_agent import process_incoming_whatsapp_message

def make_payload(text):
    return {
        'entry': [{
            'changes': [{
                'value': {
                    'messages': [{
                        'from': '919840012345',
                        'type': 'text',
                        'text': {'body': text}
                    }]
                }
            }]
        }]
    }

print("=== Test 1: COURSE ===")
r1 = process_incoming_whatsapp_message(make_payload("COURSE"))
print("Handler:", r1.get("handler"), "| Status:", r1.get("status"))

print("\n=== Test 2: TASKS ===")
r2 = process_incoming_whatsapp_message(make_payload("TASKS"))
print("Handler:", r2.get("handler"), "| Status:", r2.get("status"))

print("\n=== Test 3: BRIEFING ===")
r3 = process_incoming_whatsapp_message(make_payload("BRIEFING"))
print("Handler:", r3.get("handler"), "| Status:", r3.get("status"))

print("\n=== Test 4: TAXI BOOKING ===")
r4 = process_incoming_whatsapp_message(make_payload("கார் முன்பதிவு மதுரை to ராமேஸ்வரம்"))
print("Handler:", r4.get("handler"), "| Status:", r4.get("status"))

print("\n[SUCCESS] All WhatsApp webhook handlers executed without errors!")
