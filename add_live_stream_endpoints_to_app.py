# -*- coding: utf-8 -*-
"""
Adds live_stream SSE endpoints and upgrades whatsapp-sim endpoint in app.py.
"""
import sys

def main():
    path = "D:/api/makkal-agent-ai/app.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add StreamingResponse to imports
    if "StreamingResponse" not in content:
        content = content.replace(
            "from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, PlainTextResponse, Response",
            "from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, PlainTextResponse, Response, StreamingResponse"
        )
        print("Added StreamingResponse to imports")

    # 2. Upgrade whatsapp-sim endpoint
    old_sim_hook = '''@app.post("/api/sia/whatsapp-sim")
async def whatsapp_sim_endpoint(payload: Dict[str, Any]):
    """Simulates interactive WhatsApp message interaction with SIA (Cell: 6381029380)."""
    sender_phone = payload.get("sender_phone", SIA_OFFICIAL_NUMBER)
    message_text = payload.get("message_text", "Hi SIA")
    msg_type = payload.get("msg_type", "text")
    interactive_id = payload.get("interactive_id", "")
    interactive_title = payload.get("interactive_title", "")
    res = handle_sia_whatsapp_flow(
        sender_phone, message_text, PUBLIC_BASE_URL,
        msg_type=msg_type,
        interactive_id=interactive_id,
        interactive_title=interactive_title,
    )
    if not res:
        res = {"reply": f"SIA received: {message_text}"}
    return {"status": "success", "result": res}'''

    new_sim_code = '''@app.post("/api/sia/whatsapp-sim")
async def whatsapp_sim_endpoint(payload: Dict[str, Any]):
    """
    Simulates interactive WhatsApp message interaction with SIA (Cell: 6381029380).
    Runs the FULL multi-agent pipeline (Spoken English, Mental Health 14416, Universal Tuition,
    Patta, RedTaxi, Baseten Muse Spark Open) and broadcasts events live to the Web UI via SSE.
    """
    import time
    from whatsapp_agent import process_incoming_whatsapp_message, handle_sia_whatsapp_flow, SIA_OFFICIAL_NUMBER, PUBLIC_BASE_URL

    sender_phone = payload.get("sender_phone", SIA_OFFICIAL_NUMBER)
    message_text = payload.get("message_text", "Hi SIA")
    msg_type = payload.get("msg_type", "text")
    interactive_id = payload.get("interactive_id", "")
    interactive_title = payload.get("interactive_title", "")

    # Construct standard Meta WhatsApp Cloud API Webhook payload
    sim_msg: Dict[str, Any] = {
        "from": sender_phone,
        "id": f"sim_msg_{int(time.time()*1000)}",
        "timestamp": str(int(time.time())),
        "type": msg_type,
    }
    if msg_type == "text":
        sim_msg["text"] = {"body": message_text}
    elif msg_type == "interactive":
        sim_msg["interactive"] = {
            "type": "button_reply",
            "button_reply": {"id": interactive_id, "title": interactive_title or message_text}
        }

    wa_webhook_payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "WHATSAPP_SIM_ENTRY",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {"display_phone_number": "15550192834", "phone_number_id": "1213113635214047"},
                    "messages": [sim_msg]
                },
                "field": "messages"
            }]
        }]
    }

    # Execute full multi-agent processing pipeline
    res = process_incoming_whatsapp_message(wa_webhook_payload)
    return {"status": "success", "result": res}


# ==============================================================================
# ⚡ 6. REAL-TIME SERVER-SENT EVENTS (SSE) LIVE STREAM ENDPOINTS
# ==============================================================================

@app.get("/api/live-stream/events")
async def live_stream_events_endpoint(client_id: str = "web_user"):
    """Server-Sent Events (SSE) real-time event stream syncing WhatsApp with Web App."""
    from live_message_hub import live_hub
    return StreamingResponse(
        live_hub.event_generator(client_id=client_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/api/live-stream/recent")
async def get_recent_live_events_endpoint(limit: int = 50):
    """Returns recent live stream events for initial page hydration."""
    from live_message_hub import live_hub
    return {"status": "success", "events": live_hub.get_recent_events(limit=limit)}


@app.post("/api/live-stream/clear")
async def clear_live_events_endpoint():
    """Clears live stream history for judge demo reset."""
    from live_message_hub import live_hub
    live_hub.clear()
    return {"status": "success", "message": "Live event stream cleared"}'''

    if "/api/live-stream/events" not in content:
        content = content.replace(old_sim_hook, new_sim_code, 1)
        print("Replaced whatsapp_sim_endpoint and added live-stream SSE endpoints")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print("SUCCESS: app.py updated successfully!")

if __name__ == "__main__":
    main()
