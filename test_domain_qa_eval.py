# -*- coding: utf-8 -*-
"""
Makkal Agent AI - Meta Model Domain Training & QA Benchmark Test Suite
Meta AI Developer Hackathon 2026

Verifies:
1. Domain Training Dataset Curation (100+ High-Yield Samples).
2. Multi-Model Target Allocation (Spark 1.3, Wonder 1.0, SAM 3.1).
3. Baseten Open-Weight LoRA/SFT Fine-Tuning Dataset Export.
4. Automated Statutory Accuracy, Pedagogical Completeness & Anti-Middleman Scoring.
5. Live FastAPI Endpoints (/api/meta/training-metrics & /api/meta/evaluate-qa).
"""

import sys
import os
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from fastapi.testclient import TestClient
from app import app
from domain_training_engine import domain_training_engine

client = TestClient(app)

print("=" * 70)
print("MAKKAL AGENT AI - META MODEL DOMAIN TRAINING & QA BENCHMARK SUITE")
print("=" * 70)

# 1. Dataset Integrity & Volume Test
print("\n[1] Testing Domain Training Dataset Volume & Schema Integrity...")
stats = domain_training_engine.get_dataset_statistics()
assert stats["total_samples"] >= 100, f"Expected at least 100 samples, got {stats['total_samples']}"
print(f"    ✓ Total Verified Samples: {stats['total_samples']}")
print(f"    ✓ Estimated Token Volume: {stats['estimated_tokens']} tokens")
print(f"    ✓ Average Chars / Sample: {stats['avg_chars_per_sample']} chars")
assert len(stats["domains"]) >= 10, f"Expected rich domain coverage, got {len(stats['domains'])} domains"
print(f"    ✓ Granular Domain Verticals: {len(stats['domains'])} categories covered")

# 2. Multi-Model Target Allocation Test
print("\n[2] Testing Meta Model Architecture Specialization...")
model_dist = stats["meta_model_distribution"]
assert "muse-spark-1.3" in model_dist, "Missing Meta Spark 1.3 allocations"
assert "muse-wonder-1.0" in model_dist, "Missing Meta Wonder 1.0 allocations"
print(f"    ✓ Meta Spark 1.3 (Conversational Triage): {model_dist['muse-spark-1.3']} samples")
print(f"    ✓ Meta Wonder 1.0 (Deep Pedagogical Reasoning): {model_dist['muse-wonder-1.0']} samples")
print(f"    ✓ Pedagogical Traces Samples: {stats['pedagogical_traces_samples']}")

# 3. Baseten Fine-Tuning Dataset Export Test
print("\n[3] Testing Baseten LoRA / SFT Open-Weight Export Pipeline...")
export_res = domain_training_engine.export_baseten_fine_tuning_dataset()
assert export_res["status"] == "success"
assert export_res["train_samples"] >= 70, f"Expected >=70 train samples, got {export_res['train_samples']}"
assert export_res["eval_samples"] >= 15, f"Expected >=15 eval samples, got {export_res['eval_samples']}"

train_p = Path(export_res["train_file"])
eval_p = Path(export_res["eval_file"])
assert train_p.exists() and train_p.stat().st_size > 10000, "Train file missing or too small"
assert eval_p.exists() and eval_p.stat().st_size > 2000, "Eval file missing or too small"
print(f"    ✓ Exported Train Set: {export_res['train_samples']} samples ({train_p.stat().st_size / 1024:.1f} KB)")
print(f"    ✓ Exported Eval Set:  {export_res['eval_samples']} samples ({eval_p.stat().st_size / 1024:.1f} KB)")
print(f"    ✓ Target Open-Weight Model: {export_res['target_open_weight_model']}")

# 4. In-Context Grounding Retrieval & Anti-Middleman Rule Verification
print("\n[4] Testing Statutory Grounding Retrieval & Anti-Middleman Locks...")
g_patta = domain_training_engine.get_domain_grounding_prompt("உட்பிரிவு இல்லாத பட்டா மாறுதல் கட்டணம் எவ்வளவு?")
assert "₹0" in g_patta or "இலவசம்" in g_patta, "Missing ₹0 fee lock in patta grounding"
assert "STATUTORY REGIONAL GROUNDING DIRECTIVE" in g_patta
print("    ✓ Grounding correctly injected ₹0 fee lock for patta without subdivision")

g_rti = domain_training_engine.get_domain_grounding_prompt("RTI மனு கட்டணம் எவ்வளவு?")
assert "₹10" in g_rti, "Missing ₹10 fee lock in RTI grounding"
print("    ✓ Grounding correctly injected ₹10 fee lock for RTI petitions")

# 5. Automated Response Evaluation & Scoring Test
print("\n[5] Testing Automated Response Evaluation Engine...")
mock_patta_reply = (
    "நிலப் பட்டா மாறுதல் செய்ய அரசு கட்டணம்: உட்பிரிவு இல்லாத பட்டா ₹0 (இலவசம்), "
    "உட்பிரிவு உள்ள பட்டா ₹60 மட்டுமே. புரோக்கர்கள் அல்லது இடைத்தரகர்கள் கேட்கும் லஞ்சத்தை கொடுக்க வேண்டாம்."
)
eval_patta = domain_training_engine.evaluate_response(mock_patta_reply, "உட்பிரிவு இல்லாத பட்டா கட்டணம் எவ்வளவு?")
assert eval_patta["passed"] is True, f"Evaluation failed: {eval_patta}"
assert eval_patta["metrics"]["statutory_fee_accuracy"] == 100
assert eval_patta["metrics"]["anti_middleman_warning"] == 100
print(f"    ✓ Patta Evaluation Score: {eval_patta['overall_score']}/100 (Fee Accuracy: 100%, Anti-Middleman: 100%)")

mock_wonder_reply = (
    "நியூட்டனின் இயக்க விதிகள்: படிமுறை விளக்கம் மற்றும் சூத்திரம் F = m * a. "
    "அரசு தேர்வு குறிப்பு: விடைத்தாளில் முக்கிய சொற்களை எழுதவும்."
)
eval_wonder = domain_training_engine.evaluate_response(mock_wonder_reply, "நியூட்டனின் இயக்க விதி என்ன?")
assert eval_wonder["passed"] is True
assert eval_wonder["metrics"]["pedagogical_clarity"] == 100
print(f"    ✓ Wonder 1.0 Pedagogical Deliberation Score: {eval_wonder['overall_score']}/100")

# 6. Live FastAPI Endpoints Verification
print("\n[6] Testing Live API Endpoints (/api/meta/training-metrics & /api/meta/evaluate-qa)...")
r_metrics = client.get("/api/meta/training-metrics")
assert r_metrics.status_code == 200, f"Failed /api/meta/training-metrics: {r_metrics.status_code}"
m_data = r_metrics.json()
assert m_data["status"] == "ready"
assert m_data["total_samples"] >= 100
print(f"    ✓ GET /api/meta/training-metrics: {m_data['total_samples']} samples verified")

r_eval = client.post("/api/meta/evaluate-qa", json={
    "query": "உட்பிரிவு உள்ள பட்டா மாறுதல் அரசு கட்டணம் எவ்வளவு?",
    "reply": "உட்பிரிவு உள்ள பட்டா மாறுதல் செய்ய அதிகாரப்பூர்வ அரசு கட்டணம் ₹60 மட்டுமே. இடைத்தரகர்களைத் தவிர்க்கவும்."
})
assert r_eval.status_code == 200
eval_data = r_eval.json()
assert eval_data["passed"] is True
print(f"    ✓ POST /api/meta/evaluate-qa: Score {eval_data['overall_score']}/100 (Passed: {eval_data['passed']})")

r_export = client.post("/api/meta/export-baseten-dataset")
assert r_export.status_code == 200
exp_data = r_export.json()
assert exp_data["status"] == "success"
print(f"    ✓ POST /api/meta/export-baseten-dataset: {exp_data['train_samples']} train + {exp_data['eval_samples']} eval records")

print("\n" + "=" * 70)
print("[SUCCESS] ALL META MODEL DOMAIN TRAINING & QA BENCHMARKS VERIFIED 100%!")
print("=" * 70)
