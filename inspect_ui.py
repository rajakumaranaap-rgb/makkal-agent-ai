with open(r"D:\api\makkal-agent-ai\sia_ui_template.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "travelModal" in l:
        print(f"travelModal at line {i+1}: {l.strip()[:60]}")
    if "basetenSovereignModal" in l:
        print(f"basetenSovereignModal at line {i+1}: {l.strip()[:60]}")
