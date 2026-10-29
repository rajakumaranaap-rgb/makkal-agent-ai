# -*- coding: utf-8 -*-
"""
Adds diagrammatic guide endpoints to app.py.
"""
import sys

def main():
    path = "D:/api/makkal-agent-ai/app.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_endpoints = '''

# ==============================================================================
# 🗺️ 7. UNIVERSAL DIAGRAMMATIC ROADMAP & GOVERNMENT PORTAL GUIDE ENDPOINTS
# ==============================================================================

@app.post("/api/guide/diagrammatic-solve")
async def diagrammatic_solve_endpoint(req: Request):
    """
    Parses any voice or text query into an innovative diagrammatic step-by-step
    visual roadmap with verified government portal URLs, fee locks, and document checklists.
    """
    from diagrammatic_guide_engine import solve_diagrammatic_guide
    body = await req.json()
    query = body.get("query", "")
    phone = body.get("phone", "6381029380")
    res = solve_diagrammatic_guide(query_text=query, phone=phone)
    return JSONResponse(content=res)


@app.post("/api/guide/push-to-whatsapp")
async def push_guide_to_whatsapp_endpoint(req: Request):
    """
    Pushes a formatted diagrammatic roadmap guide and legal/syllabus details
    directly to the citizen's WhatsApp chat (+1 555-019-2834 / recipient phone).
    """
    from whatsapp_agent import send_whatsapp_message
    from live_message_hub import live_hub
    body = await req.json()
    phone = body.get("phone", "6381029380")
    text = body.get("whatsapp_text", "")
    
    if not text:
        return JSONResponse(content={"status": "error", "message": "No message text provided"}, status_code=400)
    
    res = send_whatsapp_message(to_number=phone, text=text)
    if live_hub:
        live_hub.publish_event(
            event_type="wa_outgoing",
            data={"text": text, "type": "text", "channel": "guide_push"},
            sender=phone
        )
    return JSONResponse(content={"status": "success", "delivery": res})
'''

    if "/api/guide/diagrammatic-solve" not in content:
        content += new_endpoints
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Added diagrammatic guide endpoints to app.py")
    else:
        print("Endpoints already present in app.py")

if __name__ == "__main__":
    main()
