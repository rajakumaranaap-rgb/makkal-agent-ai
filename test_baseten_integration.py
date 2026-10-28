import sys
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

print("[1] Testing GET /api/baseten/benchmark...")
r_bench = client.get('/api/baseten/benchmark')
assert r_bench.status_code == 200, f"Benchmark failed: {r_bench.status_code}"
bench_data = r_bench.json()['benchmark']
print(f"    Status: {bench_data['status']}")
print(f"    Provider: {bench_data['provider']}")
print(f"    Latency: {bench_data['latency_ms']} ms")
print(f"    Quota: {bench_data['tpm_quota']}")
print(f"    Sovereignty: {bench_data['data_sovereignty']}")

print("[2] Testing POST /api/chat with use_open_weight=True...")
r_chat = client.post('/api/chat', json={
    'message': 'எனது நிலம் சர்வே எண் 142/3A பட்டா மாறுதல்',
    'use_open_weight': True,
    'use_deep_reasoning': True,
    'language': 'ta'
})
assert r_chat.status_code == 200, f"Chat failed: {r_chat.status_code}"
chat_data = r_chat.json()
print(f"    Model Used: {chat_data['model_used']}")
print(f"    Reasoning Steps: {len(chat_data.get('reasoning_steps') or [])} steps")
assert "Baseten Sovereign Edge" in chat_data['reply']
print("    Verified Baseten Sovereign badge in assistant reply!")

print("[3] Testing GET / (HTML UI verification)...")
r_ui = client.get('/')
assert r_ui.status_code == 200
html = r_ui.text
assert 'id="basetenToggle"' in html, "Missing basetenToggle in HTML"
assert 'id="basetenBenchBtn"' in html, "Missing basetenBenchBtn in HTML"
assert 'baseten_sovereign' in html, "Missing baseten_sovereign demo tour in HTML"
assert 'function runBasetenBenchmark' in html, "Missing runBasetenBenchmark in JS"
print("    All Baseten UI controls, toggles, badges, and JS functions verified in HTML!")

print("\n[SUCCESS] All Baseten Sovereign Edge integration tests passed flawlessly!")
