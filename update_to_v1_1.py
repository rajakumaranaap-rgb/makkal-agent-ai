# -*- coding: utf-8 -*-
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

root = r"D:\api\makkal-agent-ai"

# 1. Update app.py
app_path = os.path.join(root, "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    app_c = f.read()

app_c = app_c.replace('version="1.0 (Stable Beta Release)"', 'version="1.1 (Stable Production Release)"')
app_c = app_c.replace('"version": "1.0 (Stable Beta Release)"', '"version": "1.1 (Stable Production Release)"')
with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_c)
print("✓ app.py updated to v1.1")

# 2. Update sia_ui_template.py
ui_path = os.path.join(root, "sia_ui_template.py")
with open(ui_path, "r", encoding="utf-8") as f:
    ui_c = f.read()

ui_c = ui_c.replace("v1.0 Stable Beta", "v1.1 Stable Production")
with open(ui_path, "w", encoding="utf-8") as f:
    f.write(ui_c)
print("✓ sia_ui_template.py updated to v1.1 Stable Production")

# 3. Update simulate_enduser_uat.py
uat_path = os.path.join(root, "simulate_enduser_uat.py")
if os.path.exists(uat_path):
    with open(uat_path, "r", encoding="utf-8") as f:
        uat_c = f.read()
    uat_c = uat_c.replace("1.0 (Stable Beta Release)", "1.1 (Stable Production Release)")
    uat_c = uat_c.replace("v1.0 Stable Beta", "v1.1 Stable Production")
    with open(uat_path, "w", encoding="utf-8") as f:
        f.write(uat_c)
    print("✓ simulate_enduser_uat.py updated to v1.1")

# 4. Update README.md
readme_path = os.path.join(root, "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    readme_c = f.read()

# Update release badge
readme_c = readme_c.replace("badge/Release-v2.5%20(Production%20Live)-10B981.svg", "badge/Release-v1.1%20(Production%20Live)-10B981.svg")
readme_c = readme_c.replace("badge/Release-v1.0%20(Stable%20Beta)-10B981.svg", "badge/Release-v1.1%20(Production%20Live)-10B981.svg")

# Ensure the new video link is featured prominently at the very top
yt_url = "https://youtu.be/nvkdHhOqRUw"
top_banner = f"""> 🎥 **Official 3-Minute Live App Walkthrough Demo Video (Google Flow HD):** [{yt_url}]({yt_url})

[![SIA Meta Hackathon Official 3-Min Live Demo Video](https://img.shields.io/badge/YouTube-Watch%20Official%203--Min%20Live%20Demo-red?style=for-the-badge&logo=youtube)]({yt_url})
"""

# Update top of README if not already there
if yt_url not in readme_c:
    if "# 🏛️ SIA" in readme_c:
        parts = readme_c.split("# 🏛️ SIA", 1)
        readme_c = top_banner + "\n# 🏛️ SIA" + parts[1]

# Also ensure table has the top row for Google Flow HD
table_row = f"| 🌟 **Official 3-Minute Live Screen Recording Demo (Google Flow HD)** | 1080p Full HD (2:40) | [**Watch on YouTube: youtu.be/nvkdHhOqRUw**]({yt_url}) | **The Definitive Hackathon Live Demo:** Lossless Google Flow 1080p live captures! Zero-password login, dual-sync WhatsApp workstation, and complete demonstrations across all sovereign services + Baseten Meta Model APIs. |\n"

if "| Demo Video Track |" in readme_c and "nvkdHhOqRUw" not in readme_c.split("| Demo Video Track |")[1]:
    marker = "| :--- | :--- | :--- | :--- |\n"
    readme_c = readme_c.replace(marker, marker + table_row)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme_c)
print("✓ README.md updated to v1.1 and latest YouTube video")
