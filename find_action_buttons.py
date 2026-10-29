import sys, re

sys.stdout.reconfigure(encoding='utf-8')
with open(r"D:\api\makkal-agent-ai\sia_ui_template.py", "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
for i, l in enumerate(lines):
    if "openTravelModal" in l:
        print(f"Line {i+1}: {l.strip()[:80]}")
    if "openFamilyHubModal" in l or "openTestoModal" in l:
        print(f"Line {i+1}: {l.strip()[:80]}")
