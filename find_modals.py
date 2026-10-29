import re

with open(r"D:\api\makkal-agent-ai\sia_ui_template.py", "r", encoding="utf-8") as f:
    text = f.read()

modals = re.findall(r'id=["\']([a-zA-Z0-9_]*Modal)["\']', text)
print("Modals found in sia_ui_template.py:", set(modals))
