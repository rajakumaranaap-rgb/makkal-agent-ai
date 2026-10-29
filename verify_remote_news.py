import requests
import json
import sys

BASE = "http://127.0.0.1:8001"

print("=" * 70)
print("SIA MAKKAL AGENT AI — REMOTE EC2 LIVE NEWS & AIR RADIO VERIFICATION")
print("=" * 70)

# 1. Health
r_h = requests.get(f"{BASE}/health")
print("1. Health Endpoint:", r_h.status_code, r_h.json().get("status"))
assert r_h.status_code == 200

# 2. Daily News Bulletin
r_news = requests.get(f"{BASE}/api/news/daily-bulletin")
news_data = r_news.json()
print("2. Daily Bulletin Endpoint:", r_news.status_code)
print(f"   Date: {news_data.get('date_tamil')}")
print(f"   Total: {news_data.get('total_news_count')} (TN: {news_data.get('tamil_nadu_news_count')}, IN: {news_data.get('india_news_count')}, WD: {news_data.get('world_news_count')})")
assert r_news.status_code == 200
assert news_data.get("tamil_nadu_news_count") == 10
assert news_data.get("india_news_count") == 5
assert news_data.get("world_news_count") == 3

# 3. AIR Akashvani Audio Endpoint
r_air = requests.get(f"{BASE}/api/news/air-audio")
air_data = r_air.json()
print("3. AIR Audio Endpoint:", r_air.status_code)
print(f"   Station: {air_data.get('air_metadata', {}).get('station_name')}")
print(f"   Portal: {air_data.get('air_metadata', {}).get('official_portal')}")
assert r_air.status_code == 200
assert "newsonair.gov.in" in air_data.get("air_metadata", {}).get("official_portal", "")

# 4. WhatsApp Ingress Trigger for 'Good morning SIA'
from whatsapp_agent import handle_whatsapp_ingress
payload_gm = {
    "entry": [{
        "changes": [{
            "value": {
                "messages": [{
                    "from": "916381029380",
                    "type": "text",
                    "text": {"body": "Good morning SIA! இன்றைய முக்கிய செய்திகள்"}
                }]
            }
        }]
    }]
}
res_gm = handle_whatsapp_ingress(payload_gm)
print("4. WhatsApp Ingress (Good Morning):", res_gm.get("status"), "Handler:", res_gm.get("handler"), "Total News:", res_gm.get("total_news"))
assert res_gm.get("status") == "processed"
assert res_gm.get("handler") == "daily_news_full_briefing"
assert res_gm.get("total_news") == 18

# 5. WhatsApp Ingress Trigger for 'btn_news_air'
payload_air = {
    "entry": [{
        "changes": [{
            "value": {
                "messages": [{
                    "from": "916381029380",
                    "type": "interactive",
                    "interactive": {
                        "type": "button_reply",
                        "button_reply": {"id": "btn_news_air", "title": "🎙️ AIR வானொலி ஒலி"}
                    }
                }]
            }
        }]
    }]
}
res_air = handle_whatsapp_ingress(payload_air)
print("5. WhatsApp Ingress (btn_news_air):", res_air.get("status"), "Handler:", res_air.get("handler"))
assert res_air.get("status") == "processed"
assert res_air.get("handler") == "daily_news_air_audio"

print("=" * 70)
print("🏆 ALL LIVE EC2 DAILY NEWS & AIR ALL INDIA RADIO CHECKS PASSED 100%!")
print("=" * 70)
