# -*- coding: utf-8 -*-
with open("D:/api/makkal-agent-ai/whatsapp_agent.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '''        # ── Extract interactive reply data (button clicks / list selections) ──
        interactive_id = ""
        interactive_title = ""
        if msg_type == "interactive":
            interactive_data = msg.get("interactive", {})
            itype = interactive_data.get("type", "")
            if itype == "button_reply":
                br = interactive_data.get("button_reply", {})
                interactive_id = br.get("id", "")
                interactive_title = br.get("title", "")
                user_text = interactive_title
            elif itype == "list_reply":
                lr = interactive_data.get("list_reply", {})
                interactive_id = lr.get("id", "")
                interactive_title = lr.get("title", "")
                user_text = interactive_title
            logger.info(f"[WA INTERACTIVE] type={itype} id={interactive_id} title={interactive_title}")
        _publish_live_event(
            "wa_incoming",
            {
                "text": user_text if msg_type in ("text", "interactive") else f"[{msg_type} message]",
                "msg_type": msg_type,
                "interactive_id": interactive_id,
                "interactive_title": interactive_title
            },
            sender=sender_phone
        )

        if msg_type in ("text", "interactive"):
            if msg_type == "text":
                user_text = msg.get("text", {}).get("body", "").strip()'''

replacement = '''        # ── Extract interactive reply data (button clicks / list selections) ──
        interactive_id = ""
        interactive_title = ""
        user_text = ""
        if msg_type == "interactive":
            interactive_data = msg.get("interactive", {})
            itype = interactive_data.get("type", "")
            if itype == "button_reply":
                br = interactive_data.get("button_reply", {})
                interactive_id = br.get("id", "")
                interactive_title = br.get("title", "")
                user_text = interactive_title
            elif itype == "list_reply":
                lr = interactive_data.get("list_reply", {})
                interactive_id = lr.get("id", "")
                interactive_title = lr.get("title", "")
                user_text = interactive_title
            logger.info(f"[WA INTERACTIVE] type={itype} id={interactive_id} title={interactive_title}")
        elif msg_type == "text":
            user_text = msg.get("text", {}).get("body", "").strip()

        _publish_live_event(
            "wa_incoming",
            {
                "text": user_text if msg_type in ("text", "interactive") else f"[{msg_type} message]",
                "msg_type": msg_type,
                "interactive_id": interactive_id,
                "interactive_title": interactive_title
            },
            sender=sender_phone
        )

        if msg_type in ("text", "interactive"):'''

# Normalize newlines for match
target_norm = target.replace("\r\n", "\n")
text_norm = text.replace("\r\n", "\n")

if target_norm in text_norm:
    text_norm = text_norm.replace(target_norm, replacement.replace("\r\n", "\n"), 1)
    with open("D:/api/makkal-agent-ai/whatsapp_agent.py", "w", encoding="utf-8") as f:
        f.write(text_norm)
    print("SUCCESS: Fixed user_text order in whatsapp_agent.py")
else:
    print("WARNING: target_norm not found")
