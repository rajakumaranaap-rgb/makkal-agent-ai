# -*- coding: utf-8 -*-
"""
Instruments whatsapp_agent.py with live_message_hub event publishing.
"""
import sys

def main():
    path = "D:/api/makkal-agent-ai/whatsapp_agent.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add live_hub import and helper if not present
    if "from live_message_hub import live_hub" not in content:
        import_hook = "from family_daily_planner import ("
        helper_code = '''try:
    from live_message_hub import live_hub
except Exception:
    live_hub = None

def _publish_live_event(event_type: str, data: Dict[str, Any], sender: str = "6381029380", model: str = "muse-spark-open-1026"):
    if live_hub:
        try:
            live_hub.publish_event(event_type=event_type, data=data, sender=sender, model=model)
        except Exception as e:
            logger.debug(f"[LIVE HUB] Publish failed: {e}")

'''
        content = content.replace(import_hook, helper_code + import_hook, 1)
        print("Added live_hub import and helper")

    # 2. Add publish in send_whatsapp_message
    hook_send = 'def send_whatsapp_message(to_number: str, text: str) -> Dict[str, Any]:\n    """\n    Sends an outbound text message to a citizen via Meta WhatsApp Cloud API.\n    """'
    pub_send = '''def send_whatsapp_message(to_number: str, text: str) -> Dict[str, Any]:
    """
    Sends an outbound text message to a citizen via Meta WhatsApp Cloud API.
    """
    clean_to = "".join([c for c in str(to_number) if c.isdigit()])
    _publish_live_event("wa_outgoing", {"text": text, "type": "text"}, sender=clean_to or "6381029380")'''
    if '_publish_live_event("wa_outgoing", {"text": text, "type": "text"}' not in content:
        content = content.replace(hook_send, pub_send, 1)
        print("Instrumented send_whatsapp_message")

    # 3. Add publish in send_whatsapp_button_message
    hook_btn = 'def send_whatsapp_button_message(\n    to_number: str,\n    body_text: str,\n    buttons: list,\n    header_text: str = "",\n    footer_text: str = "",\n) -> Dict[str, Any]:'
    pub_btn = '''def send_whatsapp_button_message(
    to_number: str,
    body_text: str,
    buttons: list,
    header_text: str = "",
    footer_text: str = "",
) -> Dict[str, Any]:
    clean_to = "".join([c for c in str(to_number) if c.isdigit()])
    _publish_live_event(
        "wa_outgoing",
        {
            "text": body_text,
            "buttons": [b.get("title") for b in buttons[:3]],
            "button_objs": buttons[:3],
            "header": header_text,
            "footer": footer_text,
            "type": "button"
        },
        sender=clean_to or "6381029380"
    )'''
    if '"button_objs": buttons[:3]' not in content:
        content = content.replace(hook_btn, pub_btn, 1)
        print("Instrumented send_whatsapp_button_message")

    # 4. Add publish in send_whatsapp_list_message
    hook_list = 'def send_whatsapp_list_message(\n    to_number: str,\n    body_text: str,\n    button_label: str,\n    sections: list,\n    header_text: str = "",\n    footer_text: str = "",\n) -> Dict[str, Any]:'
    pub_list = '''def send_whatsapp_list_message(
    to_number: str,
    body_text: str,
    button_label: str,
    sections: list,
    header_text: str = "",
    footer_text: str = "",
) -> Dict[str, Any]:
    clean_to = "".join([c for c in str(to_number) if c.isdigit()])
    _rows = []
    for _s in sections:
        _rows.extend(_s.get("rows", []))
    _publish_live_event(
        "wa_outgoing",
        {
            "text": body_text,
            "button_label": button_label,
            "sections": sections,
            "rows": _rows,
            "header": header_text,
            "footer": footer_text,
            "type": "list"
        },
        sender=clean_to or "6381029380"
    )'''
    if '"rows": _rows' not in content:
        content = content.replace(hook_list, pub_list, 1)
        print("Instrumented send_whatsapp_list_message")

    # 5. Add publish in process_incoming_whatsapp_message
    hook_incoming = 'logger.info(f"[WA INTERACTIVE] type={itype} id={interactive_id} title={interactive_title}")'
    pub_incoming = '''logger.info(f"[WA INTERACTIVE] type={itype} id={interactive_id} title={interactive_title}")
        _publish_live_event(
            "wa_incoming",
            {
                "text": user_text if msg_type in ("text", "interactive") else f"[{msg_type} message]",
                "msg_type": msg_type,
                "interactive_id": interactive_id,
                "interactive_title": interactive_title
            },
            sender=sender_phone
        )'''
    if '"interactive_title": interactive_title' not in content:
        content = content.replace(hook_incoming, pub_incoming, 1)
        print("Instrumented process_incoming_whatsapp_message")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print("SUCCESS: whatsapp_agent.py updated with live_hub instrumentation!")

if __name__ == "__main__":
    main()
