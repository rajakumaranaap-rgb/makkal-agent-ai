import subprocess
import requests
import json
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:8001"
OUTPUT_DIR = Path(r"D:\api\makkal-agent-ai\demo_video_assets\screenshots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def capture(url, output_png, wait_sec=2):
    print(f"[*] Capturing: {output_png.name} from {url}...")
    cmd = [
        CHROME_EXE,
        "--headless=new",
        "--window-size=1920,1080",
        "--hide-scrollbars",
        f"--screenshot={output_png}",
        url
    ]
    subprocess.run(cmd, check=True)
    time.sleep(wait_sec)
    if output_png.exists():
        print(f"    [✓] Generated: {output_png.name} ({output_png.stat().st_size / 1024:.1f} KB)")
    else:
        print(f"    ❌ Failed to generate: {output_png.name}")

# 1. Landing Page
capture(f"{BASE_URL}/", OUTPUT_DIR / "01_landing_ingress_page.png")

# 2. Get Sandbox token for authenticated citizen
r = requests.post(f"{BASE_URL}/api/auth/sandbox-session")
data = r.json()
token = data.get("token")
print(f"[*] Acquired Sandbox Token: {token}")

# 3. Authenticated Citizen Dashboard
magic_url = f"{BASE_URL}/auth/magic?token={token}"
capture(magic_url, OUTPUT_DIR / "03_authenticated_citizen_workstation.png", wait_sec=3)
