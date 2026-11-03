# -*- coding: utf-8 -*-
"""
Uploads D:\metascreens\SIA_Meta_Hackathon_2026_Judges_Demo_3Min.mp4 to Aishlee Technology YouTube Channel.
"""

import sys
import os
import json
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(r"D:\api\makkal-agent-ai")
METASCREENS_DIR = Path(r"D:\metascreens")
VIDEO_PATH = METASCREENS_DIR / "SIA_Meta_Hackathon_2026_Judges_Demo_3Min.mp4"
YOUTUBE_TOKEN_PATH = Path(r"D:\api\arcreel\projects\projects\youtube_channel_master\tokens\aishlee_tech.json")

def upload_video():
    print("=" * 70)
    print("UPLOADING 3-MINUTE JUDGES DEMO VIDEO TO AISHLEE TECHNOLOGY YOUTUBE")
    print("=" * 70)

    if not VIDEO_PATH.exists():
        raise FileNotFoundError(f"Missing video file: {VIDEO_PATH}")

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = Credentials.from_authorized_user_file(str(YOUTUBE_TOKEN_PATH), scopes)
    if not creds.valid:
        print("[*] Refreshing Aishlee Technology OAuth token...")
        creds.refresh(Request())
        with open(str(YOUTUBE_TOKEN_PATH), "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    youtube = build("youtube", "v3", credentials=creds)

    title = "SIA (Namma Ooru SuperApp) - Official 3-Minute Live App Demo | Meta AI Hackathon 2026"
    description = """SIA: Namma Ooru SuperApp (Super Intelligent Agent / மக்கள் Agent AI)
Official 3-Minute Live App Walkthrough for Meta AI Developer Hackathon 2026
Targeting: Indie Developer Track Grand Prize ($150,000 USD) & Open Weights Award ($10,000 USD)

🏛️ ABOUT THE PROJECT:
SIA is a Sovereign Multimodal Citizen Action & Civic SuperApp for Tamil Nadu's 80 million citizens.
Designed with a WhatsApp-first, zero-typing interface: citizens simply send 'Hi SIA' on WhatsApp to access 12 essential services—eliminating corrupt middlemen extortion and delivering 0% aggregator commission across civic rights, agriculture, mobility, and commerce.

🧠 META AI ARCHITECTURE & BASETEN INFRASTRUCTURE:
• Meta Muse Spark 1.3 (Llama 3.2 3B): Autonomous civic triage, statutory routing, and colloquial dialect translation.
• Meta Muse Wonder 1.0 (Llama 3.3 70B): 4-step cognitive deliberation over Tamil Nadu Revenue Standing Order 31 and K-12 education.
• Meta SAM 3.1 & SAM 2: Multimodal computer vision for deed forensic segmentation (99.8% Ashoka emblem & seal match) and crop pest detection.
• Meta Muse Voice Transcribe 1.0: Dialect-aware Tamil speech-to-text & voice concierge.
• Meta Muse Spark Open 1026: Sovereign open-weight inference fine-tuned with PEFT LoRA (Rank=16, Alpha=32) hosted on Baseten Serverless (sub-200ms latency, zero cold starts).
• Meta Llama Guard 3: Air-gapped zero-retention privacy shield compliant with India's DPDP Act 2023.
• Meta WhatsApp Cloud API (+91 6381029380): Fully interactive button cards, list drawers, and 4.1s voice-to-petition PDF pipeline.

📱 LIVE PRODUCTION ACCESS:
• Live Web Portal: https://regulatory-stack-counter-lady.trycloudflare.com/?unlocked=1
• AWS EC2 Production Host: http://52.66.255.113:8001 (Ubuntu 22.04 LTS)
• GitHub Repository: https://github.com/rajakumaranaap-rgb/makkal-agent-ai
• Official WhatsApp Hotline: +91 63810 29380 (Judge Demo PIN: 7890)

#MetaAI #MetaHackathon2026 #Llama3 #SAM2 #SAM3 #Baseten #WhatsAppCloudAPI #MakkalAgent #SIA #TamilNadu #CivicTech #AIForGood #OpenSourceAI"""

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [
                "Meta AI Hackathon 2026", "Meta AI", "Llama 3.3", "SAM 3.1", "Baseten",
                "Makkal Agent", "SIA", "Tamil Nadu", "Civic Tech", "Aishlee Technology",
                "WhatsApp Cloud API", "AI Demo", "Open Weights"
            ],
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"[*] Uploading '{VIDEO_PATH.name}' ({VIDEO_PATH.stat().st_size / (1024*1024):.2f} MB) to YouTube...")
    media = MediaFileUpload(str(VIDEO_PATH), chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()

    video_id = response.get("id")
    watch_url = f"https://youtu.be/{video_id}"
    print("\n" + "=" * 70)
    print("🎉 YOUTUBE UPLOAD SUCCESSFUL!")
    print(f"[*] Video ID:   {video_id}")
    print(f"[*] Watch URL:  {watch_url}")
    print(f"[*] Title:      {title}")
    print("=" * 70)

    # Update Readmes
    update_readmes(watch_url)
    return watch_url

def update_readmes(video_url: str):
    # 1. Update root README.md
    readme_path = ROOT_DIR / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        badge = f"\n\n[![SIA Meta Hackathon Official 3-Min Demo Video](https://img.shields.io/badge/YouTube-Watch%20Official%203--Min%20Demo%20Video-red?style=for-the-badge&logo=youtube)]({video_url})\n\n"
        if video_url not in content:
            if "# Makkal Agent AI" in content:
                content = content.replace("# Makkal Agent AI", f"# Makkal Agent AI (SIA: Namma Ooru SuperApp)\n\n> 🎥 **Official 3-Minute Meta Hackathon Demo Video:** [{video_url}]({video_url})\n" + badge, 1)
            elif "# SIA" in content:
                content = content.replace("# SIA", f"# SIA: Namma Ooru SuperApp\n\n> 🎥 **Official 3-Minute Meta Hackathon Demo Video:** [{video_url}]({video_url})\n" + badge, 1)
            else:
                content = f"> 🎥 **Official 3-Minute Meta Hackathon Demo Video:** [{video_url}]({video_url})\n" + badge + content
            readme_path.write_text(content, encoding="utf-8")
            print(f"✓ Updated root README.md: {readme_path}")

    # 2. Update D:\metascreens\README.md
    meta_readme = METASCREENS_DIR / "README.md"
    if meta_readme.exists():
        meta_content = meta_readme.read_text(encoding="utf-8")
        if video_url not in meta_content:
            meta_content = f"> 🎥 **Official 3-Minute Judges Live Demo Video:** [{video_url}]({video_url})\n\n" + meta_content
            meta_readme.write_text(meta_content, encoding="utf-8")
            print(f"✓ Updated D:\\metascreens\\README.md: {meta_readme}")

if __name__ == "__main__":
    url = upload_video()
    print(f"\nCompleted successfully! Live YouTube Link: {url}")
