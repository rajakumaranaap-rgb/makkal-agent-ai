"""
Direct FastAPI endpoint verification for Education, Mental Health, Tuition & Student Vault
"""

import sys
import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_api():
    print("=" * 65)
    print("TESTING FASTAPI EDUCATION, MENTAL HEALTH & TUITION ENDPOINTS")
    print("=" * 65)

    # 1. Spoken English
    r = client.get("/api/spoken-english/levels")
    assert r.status_code == 200
    print(f"✓ /api/spoken-english/levels: status=200, count={len(r.json()['levels'])}")

    r = client.get("/api/spoken-english/scenario/self_introduction")
    assert r.status_code == 200
    print(f"✓ /api/spoken-english/scenario/self_introduction: status=200")

    r = client.post("/api/spoken-english/assess", json={"spoken_text": "Good morning teacher how are you"})
    assert r.status_code == 200
    print(f"✓ /api/spoken-english/assess: status=200, score={r.json()['score_percentage']}%")

    # 2. Mental Health
    r = client.get("/api/mental-health/modules")
    assert r.status_code == 200
    print(f"✓ /api/mental-health/modules: status=200, count={len(r.json()['modules'])}")

    r = client.get("/api/mental-health/helplines")
    assert r.status_code == 200
    print(f"✓ /api/mental-health/helplines: status=200, helplines={len(r.json()['helplines'])}")

    r = client.post("/api/mental-health/counsel", json={"query": "தேர்வு பயமாக உள்ளது", "phone": "6381029380"})
    assert r.status_code == 200
    print(f"✓ /api/mental-health/counsel: status=200, status_key={r.json()['status']}")

    # 3. Universal Tuition
    r = client.get("/api/tuition/classes")
    assert r.status_code == 200
    print(f"✓ /api/tuition/classes: status=200, count={len(r.json()['classes'])}")

    r = client.get("/api/tuition/topic/class10_physics_electricity")
    assert r.status_code == 200
    print(f"✓ /api/tuition/topic/class10_physics_electricity: status=200")

    r = client.post("/api/tuition/solve", json={"query": "Ohm's law formula and problem", "board": "CBSE"})
    assert r.status_code == 200
    print(f"✓ /api/tuition/solve: status=200, primary_model={r.json().get('primary_model')}")

    # 4. Student Vault Profile
    r = client.get("/api/student-vault/profile?phone=6381029380")
    assert r.status_code == 200
    print(f"✓ /api/student-vault/profile: status=200, name={r.json()['profile']['student_name']}")

    print("=" * 65)
    print("ALL 10 FASTAPI ENDPOINTS RETURNED 200 OK & PASSED 100%!")
    print("=" * 65)


if __name__ == "__main__":
    test_api()
