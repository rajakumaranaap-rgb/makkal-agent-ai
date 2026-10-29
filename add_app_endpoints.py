"""
Script to add /api/meta/train-domain-models and /api/meta/orchestrate endpoints to app.py
"""

import sys

FILE_PATH = r"D:\api\makkal-agent-ai\app.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

target = """@app.post("/api/meta/export-baseten-dataset")
async def export_baseten_dataset_endpoint():
    \"\"\"
    Exports the domain Q&A dataset into standard Baseten LoRA / SFT training JSONL.
    \"\"\"
    from domain_training_engine import domain_training_engine
    res = domain_training_engine.export_baseten_fine_tuning_dataset()
    return res"""

new_endpoints = """@app.post("/api/meta/export-baseten-dataset")
async def export_baseten_dataset_endpoint():
    \"\"\"
    Exports the domain Q&A dataset into standard Baseten LoRA / SFT training JSONL.
    \"\"\"
    from domain_training_engine import domain_training_engine
    res = domain_training_engine.export_baseten_fine_tuning_dataset()
    return res


@app.post("/api/meta/train-domain-models")
async def train_domain_models_endpoint():
    \"\"\"
    Executes domain fine-tuning export and statutory alignment re-indexing.
    Re-loads all 532+ samples, generates Baseten train/eval sets, and benchmarks statutory accuracy.
    \"\"\"
    from meta_client import meta_client
    return meta_client.train_and_align_domain_models()


@app.post("/api/meta/orchestrate")
async def orchestrate_meta_models_endpoint(req: Request):
    \"\"\"
    Unified Meta Multi-Model Ensemble Orchestrator Endpoint.
    Combines SeamlessM4T (audio), SAM 3.1 (segmentation), Baseten 816B (sovereign),
    Wonder 1.0 (deep reasoning), and Spark 1.3 (fast triage) at peak performance.
    \"\"\"
    from meta_client import meta_client
    body = await req.json()
    query = body.get("query", "")
    context = body.get("context")
    preferred_model = body.get("preferred_model")
    res = meta_client.orchestrate_meta_models(
        query=query,
        context=context,
        preferred_model=preferred_model
    )
    return JSONResponse(content=res)"""

if target in content and "/api/meta/train-domain-models" not in content:
    content = content.replace(target, new_endpoints, 1)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Added /api/meta/train-domain-models and /api/meta/orchestrate to app.py")
elif "/api/meta/train-domain-models" in content:
    print("Endpoints already present in app.py")
else:
    print("Target snippet not found in app.py")
