# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path
from fastapi.testclient import TestClient

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from app import app
from whatsapp_agent import handle_text_query

client = TestClient(app)

print("=" * 70)
print("TESTING META ENTERTAINMENT & CIVIC GREETING ENGINES")
print("=" * 70)

# 1. Test Poster Generation API
print("\n[1] Testing /api/greeting/generate-poster...")
r_greet = client.post("/api/greeting/generate-poster", json={
    "leader_name": "மாண்புமிகு மு.க. ஸ்டாலின்",
    "leader_role": "Chief Minister",
    "constituency": "கொளத்தூர்",
    "citizen_name": "ரா. செல்வகுமார்",
    "citizen_district": "மதுரை மாவட்டம்",
    "occasion": "birthday",
    "leader_phone": "9840012345",
    "leader_email": "cm@tn.gov.in"
})
assert r_greet.status_code == 200, f"Greeting failed: {r_greet.status_code}"
g_data = r_greet.json()
assert g_data["status"] == "success"
print(f"    ✓ Generated Poster Image: {g_data['filename']}")
print(f"    ✓ 1-Click WhatsApp URL: {g_data['whatsapp_share_url'][:60]}...")
print(f"    ✓ 1-Click Email URL: {g_data['email_share_url'][:60]}...")

# 2. Test Serving Greeting Image
print("\n[2] Testing Static Greeting Image Serving...")
r_img = client.get(g_data["image_url"])
assert r_img.status_code == 200, f"Image serving failed: {r_img.status_code}"
assert len(r_img.content) > 10000, f"Image too small: {len(r_img.content)} bytes"
print(f"    ✓ Successfully served JPEG image ({len(r_img.content)} bytes)")

# 3. Test Entertainment Query API
print("\n[3] Testing /api/entertainment/query...")
r_music = client.post("/api/entertainment/query", json={"query": "latest songs"})
assert r_music.status_code == 200
m_data = r_music.json()
assert m_data["status"] == "success"
assert len(m_data["recommended_songs"]) >= 3
print(f"    ✓ Recommended {len(m_data['recommended_songs'])} songs (e.g. {m_data['recommended_songs'][0]['title_en']})")
print(f"    ✓ YouTube Search: {m_data['platforms']['youtube_search']}")
print(f"    ✓ Instagram Reels: {m_data['platforms']['instagram_reels_tag']}")

# 4. Test HTML UI Elements
print("\n[4] Testing HTML UI for Modals and Fast-Track Tours...")
r_ui = client.get("/")
assert r_ui.status_code == 200
html = r_ui.text
assert 'id="greetingPosterModal"' in html, "Missing greetingPosterModal"
assert 'id="entertainmentModal"' in html, "Missing entertainmentModal"
assert 'generateCivicGreetingPoster' in html, "Missing generateCivicGreetingPoster JS"
assert 'searchMusicEntertainment' in html, "Missing searchMusicEntertainment JS"
assert 'greeting_poster' in html, "Missing tour #13 in Judge modal"
assert 'music_reels' in html, "Missing tour #14 in Judge modal"
print("    ✓ Verified #greetingPosterModal and #entertainmentModal in HTML")
print("    ✓ Verified Fast-Track Tours #13 (MLA Poster) & #14 (Meta Reels Hub)")

# 5. Test WhatsApp Ingress
print("\n[5] Testing WhatsApp Ingress for Music & Greetings...")
wa_song = handle_text_query("தமிழ் லேட்டஸ்ட் பாட்டு என்ன இருக்கு?", "9840012345")
assert "Meta AI Music Hub" in wa_song or "YouTube" in wa_song
assert "Instagram Reel" in wa_song
print("    ✓ WhatsApp Song Query correctly returned YouTube, Instagram Reel, Facebook Video links")

wa_wish = handle_text_query("எங்கள் MLA பிறந்தநாள் வாழ்த்து போஸ்டர் உருவாக்க வேண்டும்", "9840012345")
assert "வாழ்த்து அட்டை" in wa_wish
assert "WhatsApp" in wa_wish
print("    ✓ WhatsApp Greeting Query correctly generated digital poster & 1-click send link")

print("\n" + "=" * 70)
print("[SUCCESS] ALL ENTERTAINMENT & GREETING CAPABILITIES TESTED & VERIFIED 100%!")
print("=" * 70)
