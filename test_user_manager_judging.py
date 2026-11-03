# -*- coding: utf-8 -*-
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sia_user_manager import handle_sia_whatsapp_flow

test_phone = "6381029380"
base_url = "https://regulatory-stack-counter-lady.trycloudflare.com"

# 1. Test Greeting "Hi SIA"
res_greeting = handle_sia_whatsapp_flow(test_phone, "Hi SIA", base_url)
assert res_greeting is not None, "Failed greeting Hi SIA"
msg_0 = res_greeting["messages"][0]
print("Greeting Result:", msg_0.get("header"), "| Buttons:", len(msg_0.get("buttons", [])))
assert "வணக்கம்!" in msg_0.get("header", "")
assert len(msg_0.get("buttons", [])) == 3

# 2. Test Numbered Option "1" (Agri)
res_1 = handle_sia_whatsapp_flow(test_phone, "1", base_url)
assert res_1 is not None, "Failed option 1"
msg_1 = res_1["messages"][0]
print("Option 1 Result:", msg_1.get("header"))
assert "வேளாண்மை" in msg_1.get("header", "")

# 3. Test Numbered Option "4" (RedTaxi)
res_4 = handle_sia_whatsapp_flow(test_phone, "4", base_url)
assert res_4 is not None, "Failed option 4"
msg_4 = res_4["messages"][0]
print("Option 4 Result:", msg_4.get("header"))
assert "ரெட் டாக்ஸி" in msg_4.get("header", "")

# 4. Test Numbered Option "8" (MLA Petition)
res_8 = handle_sia_whatsapp_flow(test_phone, "8", base_url)
assert res_8 is not None, "Failed option 8"
msg_8 = res_8["messages"][0]
print("Option 8 Result:", msg_8.get("header"))
assert "சட்டமன்ற" in msg_8.get("header", "")

# 5. Test Button Click "btn_menu_8_mla"
res_btn_8 = handle_sia_whatsapp_flow(test_phone, "8. MLA Petition", base_url, msg_type="interactive", interactive_id="btn_menu_8_mla")
assert res_btn_8 is not None, "Failed button click btn_menu_8_mla"
print("Button 8 Result:", res_btn_8["messages"][0].get("header"))

# 6. Test Inactivity Trigger "trigger_inactivity_nudge"
res_nudge = handle_sia_whatsapp_flow(test_phone, "", base_url, msg_type="interactive", interactive_id="trigger_inactivity_nudge")
assert res_nudge is not None, "Failed trigger_inactivity_nudge"
msg_nudge = res_nudge["messages"][0]
print("Inactivity Nudge:", msg_nudge.get("header"), "| Buttons:", [b["id"] for b in msg_nudge.get("buttons", [])])
assert "btn_nudge_wait" in [b["id"] for b in msg_nudge.get("buttons", [])]

# 7. Test Nudge Action "btn_nudge_wait"
res_wait = handle_sia_whatsapp_flow(test_phone, "Wait", base_url, msg_type="interactive", interactive_id="btn_nudge_wait")
assert res_wait is not None, "Failed btn_nudge_wait"
print("Nudge Wait Result:", res_wait["messages"][0].get("header"))

print("ALL USER MANAGER JUDGING MODE TESTS PASSED SUCCESSFULLY!")
