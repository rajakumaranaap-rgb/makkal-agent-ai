"""
Script to safely wire Regional Grounding Directive endpoints into app.py.
"""

from pathlib import Path

app_path = Path("D:/api/makkal-agent-ai/app.py")
text = app_path.read_text(encoding="utf-8")

if "get_tnau_agronomy_advisory" in text:
    print("app.py already has regional grounding endpoints.")
    exit(0)

# 1. Update imports
target_import = "from modal_sam_agri_bridge import modal_sam_agri_bridge"
new_imports = """from modal_sam_agri_bridge import modal_sam_agri_bridge

# Tamil Nadu Civic & Regional Grounding Directive Imports
import tnega_civic_engine
from llama_vision_auditor import scan_document_with_llama_vision
from seamless_speech_engine import generate_regional_bilingual_voice, REGIONAL_INTONATION_PROFILES
from agriculture_engine import (
    get_tnau_agronomy_advisory,
    get_grains_subsidy_guidance,
    TNAU_AGRONOMY_REGISTRY
)
from family_education_engine import (
    solve_samacheer_homework,
    generate_samacheer_quiz,
    SAMACHEER_KALVI_CURRICULUM_DB
)"""

assert target_import in text, f"Could not find {target_import} in app.py"
text = text.replace(target_import, new_imports, 1)

# 2. Add API endpoints right before the root HTML endpoint
target_root = '@app.get("/", response_class=HTMLResponse)'
if target_root not in text:
    target_root = "@app.get('/', response_class=HTMLResponse)"

assert target_root in text, f"Could not find root route in app.py"

endpoints_code = '''# ==============================================================================
# TAMIL NADU CIVIC & REGIONAL GROUNDING DIRECTIVE API ENDPOINTS
# ==============================================================================

@app.get("/static/speech_audio/{filename}")
async def get_speech_audio_endpoint(filename: str):
    path = Path("D:/api/makkal-agent-ai/static/speech_audio") / filename
    if path.exists():
        return FileResponse(path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio file not found")


@app.get("/api/tnega/services")
async def get_tnega_services_endpoint():
    """Returns catalog of TNeGA civic services with statutory fee locks (blocking middlemen)."""
    return {"status": "success", "services": tnega_civic_engine.get_all_tnega_services()}


@app.get("/api/tnega/checklists/{service_id}")
async def get_tnega_checklist_endpoint(service_id: str):
    """Returns mandatory documentation checklist and step-by-step workflow for a TNeGA service."""
    res = tnega_civic_engine.get_tnega_service_checklist(service_id)
    if "error" in res:
        raise HTTPException(status_code=404, detail=res["error"])
    return {"status": "success", "service": res}


@app.post("/api/tnega/verify-documents")
async def verify_tnega_documents_endpoint(payload: Dict[str, Any]):
    """Cross-checks citizen's uploaded document list against mandatory TNeGA checklist."""
    service_id = payload.get("service_id", "patta_chitta")
    doc_codes = payload.get("uploaded_doc_codes", [])
    res = tnega_civic_engine.validate_citizen_document_bundle(service_id, doc_codes)
    return {"status": "success", "audit": res}


@app.post("/api/vision/llama-audit")
async def llama_vision_audit_endpoint(
    file: Optional[UploadFile] = File(None),
    service_target: str = Form("patta_chitta"),
    is_sample: bool = Form(False)
):
    """
    Scans citizen documents (Patta, Deed, Ration Card, Aadhaar, Bonafide) using Meta Llama 3.2 Vision.
    Performs local entity extraction, Ashoka seal checking, and cross-references TNeGA service checklists.
    """
    if file and not is_sample:
        content_bytes = await file.read()
        filename = file.filename or "uploaded_doc.jpg"
    else:
        sample_path = Path("D:/api/makkal-agent-ai/static/sample_patta_deed.jpg")
        if sample_path.exists():
            content_bytes = sample_path.read_bytes()
        else:
            content_bytes = b"sample_citizen_document_bytes"
        filename = "sample_patta_deed.jpg"

    audit_result = scan_document_with_llama_vision(
        image_bytes=content_bytes,
        service_target=service_target,
        filename=filename
    )
    return {"status": "success", "llama_vision_audit": audit_result}


@app.get("/api/samacheer-kalvi/curriculum")
async def get_samacheer_curriculum_endpoint():
    """Returns Tamil Nadu State Board Samacheer Kalvi curriculum across Standards 1 to 12."""
    return {"status": "success", "curriculum": SAMACHEER_KALVI_CURRICULUM_DB}


@app.post("/api/samacheer-kalvi/homework")
async def solve_samacheer_homework_endpoint(payload: Dict[str, Any]):
    """Solves homework questions mapped to TNSB Samacheer Kalvi textbooks with bilingual reasoning."""
    question = payload.get("question", "")
    standard = int(payload.get("standard", 10))
    subject = payload.get("subject", "science")
    res = solve_samacheer_homework(question=question, standard=standard, subject=subject)
    return res


@app.post("/api/samacheer-kalvi/quiz")
async def get_samacheer_quiz_endpoint(payload: Dict[str, Any]):
    """Generates 5 adaptive multiple choice questions aligned with Samacheer Kalvi board exams."""
    standard = int(payload.get("standard", 10))
    subject = payload.get("subject", "science")
    topic = payload.get("topic")
    res = generate_samacheer_quiz(standard=standard, subject=subject, topic_hint=topic)
    return res


@app.get("/api/agriculture/regional-advisory")
async def get_regional_agri_advisory_endpoint(crop: str = Query("turmeric"), query_type: str = Query("all")):
    """Returns TNAU verified agronomy guidelines (Pendimethalin, Nano DAP, Bio-inputs) and GRAINS subsidies."""
    res = get_tnau_agronomy_advisory(crop, query_type=query_type)
    return {"status": "success", "advisory": res}


@app.post("/api/speech/seamless-synthesize")
async def synthesize_seamless_speech_endpoint(payload: Dict[str, Any]):
    """
    Synthesizes expressive spoken audio using Meta SeamlessM4T v2 architecture with regional intonations
    (Madurai, Kongu, Nellai, Chennai) and bilingual Tamil / Tanglish output.
    """
    text = payload.get("text", "வணக்கம்! மக்கள் ஏஜென்ட் உங்களுக்கு உதவ தயாராக உள்ளது.")
    region = payload.get("region", "madurai")
    res = generate_regional_bilingual_voice(text=text, region=region)
    return {"status": "success", "speech": res}

\n''' + target_root

text = text.replace(target_root, endpoints_code, 1)

app_path.write_text(text, encoding="utf-8")
print("SUCCESSFULLY PATCHED app.py!")
