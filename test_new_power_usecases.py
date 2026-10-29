"""
Comprehensive Test Suite for Super-Intelligent Tamil Nadu Use Cases:
1. Education Online Exam Daily Plans & WhatsApp Courses (Muse Spark Open 816B)
2. Family Day-to-Day Task Planner & Proactive Civic Reminders (WhatsApp + Web)
3. Uber / RedTaxi Travel Booking & Ride Dispatcher (Verified Driver, OTP, 0% Surge)
"""

import sys
import io
import requests

BASE_URL = "http://127.0.0.1:8001"

print("=" * 75)
print("🏆 TESTING SUPER-INTELLIGENT TAMIL NADU USE CASES")
print("=" * 75)

# ------------------------------------------------------------------------------
# 1. EDUCATION & EXAM DAILY PLANS
# ------------------------------------------------------------------------------
print("\n[1] Testing Education Courses Catalog...")
r = requests.get(f"{BASE_URL}/api/education/courses", timeout=10)
assert r.status_code == 200, f"Failed: {r.status_code}"
courses = r.json()["courses"]
print(f"    Available Courses: {len(courses)}")
for c in courses:
    print(f"    • {c['icon']} {c['title_ta']} ({c['total_days']} days)")
assert len(courses) >= 4

print("\n[2] Testing Daily Lesson Retrieval (Day 1 TNPSC)...")
r_lesson = requests.get(f"{BASE_URL}/api/education/course/tnpsc_g4/lesson/1", timeout=10)
assert r_lesson.status_code == 200
lesson_data = r_lesson.json()
print(f"    Topic: {lesson_data['topic']}")
print(f"    Quiz Questions: {len(lesson_data['lesson']['questions'])}")
assert len(lesson_data['lesson']['questions']) >= 3

print("\n[3] Testing Daily Quiz Evaluation via Meta Muse Spark Open...")
r_eval = requests.post(f"{BASE_URL}/api/education/quiz/evaluate", json={
    "course_id": "tnpsc_g4",
    "day": 1,
    "answers": {"q1": "B", "q2": "A", "q3": "B"},
    "phone": "919840012345"
}, timeout=30)
assert r_eval.status_code == 200
eval_res = r_eval.json()
print(f"    Score: {eval_res['score']} / {eval_res['total']} ({eval_res['percentage']}%)")
assert eval_res['passed'] is True

print("\n[4] Testing Personalized Study Schedule Planner...")
r_plan = requests.post(f"{BASE_URL}/api/education/study-plan", json={
    "persona": "working_aspirant",
    "target_exam": "TNPSC Group 4 & VAO",
    "daily_hours": 4
}, timeout=10)
assert r_plan.status_code == 200
plan_data = r_plan.json()
print(f"    Target: {plan_data['target_exam']}")
print(f"    Routine Slots: {len(plan_data['routine'])} time blocks")
assert len(plan_data['routine']) >= 4

# ------------------------------------------------------------------------------
# 2. FAMILY DAY-TO-DAY TASKS & PROACTIVE CIVIC ALERTS
# ------------------------------------------------------------------------------
print("\n[5] Testing Family Tasks Listing...")
r_tasks = requests.get(f"{BASE_URL}/api/family/tasks?phone=919840012345", timeout=10)
assert r_tasks.status_code == 200
tasks_data = r_tasks.json()
print(f"    Family Tasks: {len(tasks_data['tasks'])} tasks (Pending: {tasks_data['pending_count']})")
assert len(tasks_data['tasks']) >= 2

print("\n[6] Testing Adding a Family Task...")
r_add = requests.post(f"{BASE_URL}/api/family/tasks/add", json={
    "phone": "919840012345",
    "task": "TANGEDCO சோலார் பம்ப் மானியம் விண்ணப்பித்தல்",
    "category": "solar_agri",
    "assigned_to": "அப்பா",
    "due_date": "நாளைக்குள்"
}, timeout=10)
assert r_add.status_code == 200
print(f"    Add Task Response: {r_add.json()['message_ta']}")

print("\n[7] Testing Completing a Family Task...")
r_done = requests.post(f"{BASE_URL}/api/family/tasks/complete", json={
    "phone": "919840012345",
    "task_index": 1
}, timeout=10)
assert r_done.status_code == 200
print(f"    Completed Task Status: {r_done.json()['status']}")

print("\n[8] Testing Proactive Civic Alerts (TANGEDCO, TNPDS, KMUT, PHC)...")
r_alerts = requests.get(f"{BASE_URL}/api/family/civic-alerts", timeout=10)
assert r_alerts.status_code == 200
alerts = r_alerts.json()["alerts"]
print(f"    Active Civic Alerts: {len(alerts)}")
for a in alerts:
    print(f"    • {a['icon']} {a['title_ta']} ({a['category']})")
assert len(alerts) >= 4

print("\n[9] Testing Daily Family Morning Briefing Synthesizer...")
r_brief = requests.get(f"{BASE_URL}/api/family/daily-briefing?phone=919840012345&name=முத்துக்குமார்", timeout=10)
assert r_brief.status_code == 200
brief_data = r_brief.json()
print(f"    Briefing Date: {brief_data['date']}")
assert len(brief_data['whatsapp_briefing']) > 100

# ------------------------------------------------------------------------------
# 3. UBER / REDTAXI TRAVEL BOOKING & DISPATCH ENGINE
# ------------------------------------------------------------------------------
print("\n[10] Testing Vehicle Fleet Catalog...")
r_fleet = requests.get(f"{BASE_URL}/api/travel/fleet", timeout=10)
assert r_fleet.status_code == 200
fleet = r_fleet.json()["fleet"]
print(f"    Fleet Tiers: {len(fleet)}")
for f in fleet:
    print(f"    • {f['icon']} {f['name_ta']} (Base: ₹{f['base_fare']} | Per Km: ₹{f['per_km']})")
assert len(fleet) >= 5

print("\n[11] Testing Transparent Fare Calculator (Zero Surge Guarantee)...")
r_fare = requests.post(f"{BASE_URL}/api/travel/fare-estimate", json={
    "origin": "Madurai Junction",
    "destination": "Rameswaram Temple",
    "vehicle_id": "suv",
    "trip_type": "one_way"
}, timeout=10)
assert r_fare.status_code == 200
fare_data = r_fare.json()
print(f"    Distance: {fare_data['distance_km']} km | Hours: {fare_data['estimated_hours']} hrs")
print(f"    Total Fare: ₹{fare_data['fare_breakdown']['total_fare']:,} (Surge: {fare_data['fare_breakdown']['surge_percentage']}%)")
assert fare_data['fare_breakdown']['surge_percentage'] == 0

print("\n[12] Testing RedTaxi / Uber Ride Booking & Verified Driver Allocation...")
r_book = requests.post(f"{BASE_URL}/api/travel/book-ride", json={
    "phone": "919840012345",
    "customer_name": "முத்துக்குமார்",
    "origin": "Madurai Meenakshi Temple",
    "destination": "Rameswaram Agni Theertham",
    "vehicle_id": "sedan",
    "trip_type": "round_trip",
    "pickup_time": "காலை 06:00 மணி"
}, timeout=10)
assert r_book.status_code == 200
book_res = r_book.json()
print(f"    Booking ID: {book_res['booking_id']}")
print(f"    Ride Start OTP: {book_res['ride_otp']}")
print(f"    Assigned Driver: {book_res['driver']['name_ta']} ({book_res['driver']['badge']})")
print(f"    Vehicle Plate: {book_res['vehicle_plate']}")
print(f"    Total Fare: ₹{book_res['total_fare']:,}")
assert book_res['status'] == "confirmed"
assert len(book_res['ride_otp']) == 4

print("\n" + "=" * 75)
print("🎉 [SUCCESS] ALL 12 SUPER-INTELLIGENT TAMIL NADU USE CASE TESTS PASSED!")
print("=" * 75)
