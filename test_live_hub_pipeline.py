# -*- coding: utf-8 -*-
import sys
sys.path.append("D:/api/makkal-agent-ai")
sys.stdout.reconfigure(encoding="utf-8")

from live_message_hub import live_hub
from whatsapp_agent import process_incoming_whatsapp_message

def test_pipeline():
    live_hub.clear()
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "SIM_ENTRY",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {"display_phone_number": "15550192834", "phone_number_id": "1213113635214047"},
                    "messages": [{
                        "from": "6381029380",
                        "id": "sim_patta_1",
                        "timestamp": "123",
                        "type": "text",
                        "text": {"body": "பட்டா மாறுதல் RSO 31 வழிகாட்டுதல்"}
                    }]
                },
                "field": "messages"
            }]
        }]
    }

    res = process_incoming_whatsapp_message(payload)
    print("Result handler / status:", res)
    events = live_hub.get_recent_events()
    print("Live Hub Events Count:", len(events))
    for i, e in enumerate(events):
        print(f"Event #{i+1}: [{e['event_type']}] from {e['sender']} -> {e['data'].get('text', '')[:60]}")

if __name__ == "__main__":
    test_pipeline()
