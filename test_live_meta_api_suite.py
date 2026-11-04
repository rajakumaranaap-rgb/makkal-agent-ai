"""
Live verification script for Meta Model API & Domain Training endpoints on FastAPI server
"""

import sys
import json
import requests
from test_client_helper import get_test_client

requests, BASE_URL = get_test_client("http://127.0.0.1:8001")

def test_endpoints():
    print("=" * 60)
    print("TESTING LIVE MAKKAL AGENT AI ENDPOINTS")
    print("=" * 60)

    # 1. Training Metrics
    r = requests.get(f"{BASE_URL}/api/meta/training-metrics")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    print(f"✓ /api/meta/training-metrics: status={data.get('status')}, total_samples={data.get('total_samples')}, tokens={data.get('estimated_tokens'):,}")

    # 2. Train Domain Models
    r = requests.post(f"{BASE_URL}/api/meta/train-domain-models")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    train_data = r.json()
    print(f"✓ /api/meta/train-domain-models: status={train_data.get('status')}, statutory_acc={train_data.get('statutory_accuracy_benchmark', {}).get('overall_score')}%")

    # 3. Multi-Model Orchestrate (TNPSC Exam)
    payload = {"query": "TNPSC குரூப் 4 தேர்வு முறை மற்றும் அரசியலமைப்பு முகப்புரை முக்கியத்துவம் என்ன?"}
    r = requests.post(f"{BASE_URL}/api/meta/orchestrate", json=payload)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    res = r.json()
    print(f"✓ /api/meta/orchestrate (TNPSC): primary={res.get('primary_model')}, pipeline={' -> '.join(res.get('pipeline', []))}, latency={res.get('latency_ms')}ms")

    # 4. Multi-Model Orchestrate (RedTaxi)
    payload = {"query": "RedTaxi மூலம் செடான் கார் முன்பதிவு கட்டணம் என்ன? 0% சர்ஜ் உத்திரவாதம்"}
    r = requests.post(f"{BASE_URL}/api/meta/orchestrate", json=payload)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    res = r.json()
    print(f"✓ /api/meta/orchestrate (RedTaxi): primary={res.get('primary_model')}, pipeline={' -> '.join(res.get('pipeline', []))}, latency={res.get('latency_ms')}ms")

    # 5. Multi-Model Orchestrate (Family TANGEDCO)
    payload = {"query": "TANGEDCO 100 யூனிட் இலவச மின்சார திட்டம் மற்றும் ரேஷன் கடை பொருட்கள் விலை"}
    r = requests.post(f"{BASE_URL}/api/meta/orchestrate", json=payload)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    res = r.json()
    print(f"✓ /api/meta/orchestrate (Family): primary={res.get('primary_model')}, pipeline={' -> '.join(res.get('pipeline', []))}, latency={res.get('latency_ms')}ms")

    # 6. Baseten Live Benchmark
    r = requests.get(f"{BASE_URL}/api/baseten/benchmark")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    baseten_data = r.json()
    print(f"✓ /api/baseten/benchmark: status={baseten_data.get('status')}, throughput={baseten_data.get('tokens_per_second')} tps, tpm={baseten_data.get('tpm_quota')}")

    print("=" * 60)
    print("ALL 6 LIVE ENDPOINTS RETURNED STATUS 200 OK & 100% PASS!")
    print("=" * 60)

if __name__ == "__main__":
    test_endpoints()
