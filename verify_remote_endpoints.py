import requests
import json
import sys

BASE = "http://127.0.0.1:8001"

print("=" * 70)
print("SIA MAKKAL AGENT AI — REMOTE EC2 LIVE ENDPOINTS VERIFICATION")
print("=" * 70)

# 1. Health
r_health = requests.get(f"{BASE}/health")
print("1. Health Endpoint:", r_health.status_code, r_health.json().get("status"))
assert r_health.status_code == 200

# 2. Travel Fleet
r_fleet = requests.get(f"{BASE}/api/travel/fleet")
print("2. Travel Fleet:", r_fleet.status_code, f"{len(r_fleet.json()['fleet'])} tiers")
assert r_fleet.status_code == 200

# 3. Travel Ride Booking (Zero-Surge & 4-digit OTP)
r_ride = requests.post(f"{BASE}/api/travel/book-ride", json={
    "origin": "Coimbatore Junction",
    "destination": "Ooty Botanical Garden",
    "vehicle_id": "suv",
    "phone": "6381029380"
})
ride_data = r_ride.json()
print("3. Travel Ride Booking:", r_ride.status_code, "OTP:", ride_data.get("ride_otp"), "Plate:", ride_data.get("vehicle_plate"), "Fare: ₹", ride_data.get("total_fare"))
assert r_ride.status_code == 200 and len(ride_data.get("ride_otp")) == 4

# 4. Temple Pilgrimage Packages
r_temple = requests.get(f"{BASE}/api/travel/temple-packages")
print("4. Temple Packages:", r_temple.status_code, f"{len(r_temple.json()['packages'])} circuits")
assert r_temple.status_code == 200

# 5. 10th Student Homework Solver
r_hw = requests.post(f"{BASE}/api/tuition/homework-solve", json={
    "query_text": "Find current when V=220 and R=44",
    "class_id": "class_10",
    "curriculum": "CBSE",
    "subject": "Physics"
})
hw_data = r_hw.json()
print("5. 10th CBSE Homework Solve:", r_hw.status_code, "Topic:", hw_data.get("topic_name"))
assert r_hw.status_code == 200 and "V = I" in hw_data.get("formula_used")

# 6. 10th Student Daily Study Plan (Pomodoro)
r_plan = requests.get(f"{BASE}/api/tuition/daily-study-plan?class_id=class_10&curriculum=CBSE")
plan_data = r_plan.json()
print("6. 10th Daily Study Plan:", r_plan.status_code, f"{len(plan_data.get('daily_schedule', []))} slots")
assert r_plan.status_code == 200

# 7. Agriculture TNAU Weed & Fertilizer Advisory
r_agri = requests.post(f"{BASE}/api/agri/tnau-advisory", json={"crop_key": "turmeric"})
agri_data = r_agri.json()
print("7. TNAU Agri Advisory:", r_agri.status_code, "Weed Chemical:", agri_data.get("weed_control", {}).get("chemical_ta", "")[:35])
assert r_agri.status_code == 200

# 8. 100% Drip Irrigation Subsidy
r_sub = requests.get(f"{BASE}/api/agri/grains-subsidy?crop_key=paddy")
print("8. GRAINS 100% Subsidy:", r_sub.status_code)
assert r_sub.status_code == 200

# 9. Diagrammatic Roadmap Solve
r_diag = requests.post(f"{BASE}/api/guide/diagrammatic-solve", json={"query": "TNPSC Group 4 தேர்வு வினாத்தாள்"})
diag_data = r_diag.json()
print("9. Diagrammatic Roadmap Solve:", r_diag.status_code, "Steps:", len(diag_data.get("roadmap_steps", [])))
assert r_diag.status_code == 200

print("=" * 70)
print("🏆 ALL 9 LIVE PRODUCTION ENDPOINTS VERIFIED ON AWS EC2 SUCCESSFULLY!")
print("=" * 70)
