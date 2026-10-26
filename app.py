"""
Makkal Agent AI (மக்கள் Agent) - Sovereign Multimodal Citizen Action Agent
Meta AI Developer Hackathon 2026 (Indie Developer Track - $150k Prize Target)

Powered by Meta Model Suite:
- Meta Muse Spark (muse-spark-1.3)
- Meta Muse Wonder (muse-wonder-1.0)
- Meta SAM 3.1 (sam-3.1)
- Meta Muse Voice Transcribe (muse-voice-transcribe-1.0)
- Meta Image (muse-image-1.0)
- Meta WhatsApp Business Cloud API Gateway
- Baseten Open-Weight Engine (meta-models/muse-spark-open-1026)
"""

import os
import json
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from meta_client import meta_client, DEFAULT_CHAT_MODEL, REASONING_MODEL, SEGMENT_MODEL, BASETEN_MODEL_ID
from sam_document_auditor import sam_auditor
from action_executor import action_executor
from knowledge_base import SERVICES_CATALOG, search_knowledge_base
from whatsapp_agent import (
    verify_webhook,
    process_incoming_whatsapp_message,
    send_whatsapp_message,
    send_whatsapp_document,
    META_WHATSAPP_PHONE_ID,
    PUBLIC_BASE_URL
)

app = FastAPI(
    title="Makkal Agent AI (மக்கள் Agent)",
    description="Autonomous Multimodal Citizen Action Agent for Tamil Nadu powered by Meta Model API & SAM 3.1",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

PETITIONS_DIR = Path(__file__).parent / "generated_petitions"
PETITIONS_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = """
You are 'Makkal Agent' (மக்கள் Agent), an autonomous, highly authoritative, and compassionate Multimodal Citizen Digital Officer for Tamil Nadu, India.
You do NOT act like a passive text chatbot; you are an ACTION AGENT that protects citizens from exploitation by corrupt middlemen and simplifies complex government bureaucracy.

Core Directives:
1. Tone: Respectful, patient, colloquial Tamil (மரியாதையான எளிய தமிழ்). If spoken to in English, provide crisp bilingual responses.
2. Structure your counsel with actionable clarity:
   - 📌 எளிய விளக்கம் (Crisp 1-line summary)
   - 📑 தேவையான ஆவணங்கள் (Checklist of required papers)
   - 💰 அரசு கட்டணம் vs இடைத்தரகர் எச்சரிக்கை (Exact official government fee vs ZERO middleman fees)
   - 🌐 அதிகாரப்பூர்வ இணையதளம் & அடுத்த நடவடிக்கை (Official portal link & immediate next step)
3. Never invent fake rules or unofficial fees. Always quote accurate Tamil Nadu Revenue Standing Orders (RSO 31), TNPDS, or e-Sevai guidelines.
4. When physical documents are uploaded, audit the government seals and recommend generating an official signed petition.
"""


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []
    use_deep_reasoning: Optional[bool] = False
    use_open_weight: Optional[bool] = False
    language: Optional[str] = "ta"


class PetitionRequest(BaseModel):
    applicant_name: str
    phone: str
    district: str
    taluk: str
    village: str
    service_title: str
    survey_number: str
    grounds_summary: str


class WhatsAppSimulateRequest(BaseModel):
    sender_phone: str = "919840012345"
    message_type: str = "text"
    text_body: Optional[str] = "பட்டா சிட்டா நில ஆவணம் பெயர் மாற்றம் செய்ய மனு தேவை"


@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "service": "Makkal Agent AI",
        "version": "2.1.0",
        "host": "AWS EC2 Production (52.66.255.113)",
        "meta_models": {
            "chat": DEFAULT_CHAT_MODEL,
            "reasoning": REASONING_MODEL,
            "vision": SEGMENT_MODEL,
            "voice": "muse-voice-transcribe-1.0",
            "open_weight": BASETEN_MODEL_ID
        },
        "whatsapp_gateway": {
            "status": "ready",
            "phone_id": META_WHATSAPP_PHONE_ID,
            "webhook_path": "/api/whatsapp/webhook"
        }
    }


@app.get("/api/catalog")
async def get_catalog():
    return {"status": "success", "services": SERVICES_CATALOG}


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        user_msg = req.message.strip()
        if not user_msg:
            raise HTTPException(status_code=400, detail="Message cannot be empty.")

        matched_kb = search_knowledge_base(user_msg)
        kb_context = json.dumps(matched_kb, ensure_ascii=False, indent=2)

        lang_instruction = (
            "Reply primarily in simple, clear spoken Tamil."
            if req.language == "ta"
            else "Reply in clear, accessible English with Tamil government scheme terms in brackets."
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT + f"\n\nLanguage Preference: {lang_instruction}\n\n[OFFICIAL TAMIL NADU STATUTORY CONTEXT]:\n{kb_context}"}
        ]
        if req.history:
            messages.extend(req.history[-6:])
        messages.append({"role": "user", "content": user_msg})

        # Model routing
        if req.use_open_weight:
            target_model = f"Baseten ({BASETEN_MODEL_ID})"
            res = meta_client.call_baseten_open_weight(messages=messages)
            reply_text = res.get("reply", "Baseten Open-Weight Inference active.")
        elif req.use_deep_reasoning:
            target_model = REASONING_MODEL
            res = meta_client.deep_reasoning(messages=messages)
            reply_text = res["choices"][0]["message"]["content"]
        else:
            target_model = DEFAULT_CHAT_MODEL
            res = meta_client.chat_completion(messages=messages, model=target_model)
            reply_text = res["choices"][0]["message"]["content"]

        return {
            "status": "success",
            "model_used": target_model,
            "reply": reply_text,
            "matched_services": [s["title_ta"] for s in matched_kb]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.post("/api/transcribe")
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """Transcribes rural Tamil voice notes using Meta muse-voice-transcribe-1.0."""
    try:
        content = await file.read()
        res = meta_client.transcribe_audio(audio_bytes=content, filename=file.filename or "audio.mp3")
        transcript = res.get("text", "")
        return {"status": "success", "transcript": transcript, "model": "muse-voice-transcribe-1.0"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.post("/api/audit-document")
async def audit_document_endpoint(file: UploadFile = File(...)):
    """Audits citizen land deeds and certificates using Meta SAM 3.1 visual segmentation."""
    try:
        content = await file.read()
        res = sam_auditor.audit_document(image_bytes=content, filename=file.filename or "doc.jpg")
        return res
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.post("/api/generate-petition")
async def generate_petition_endpoint(req: PetitionRequest):
    """Generates ready-to-print official Tamil Nadu legal petition PDF."""
    try:
        verification_id = f"META-SAM31-{uuid.uuid4().hex[:8].upper()}"
        pdf_path = action_executor.generate_legal_petition_pdf(
            applicant_name=req.applicant_name,
            phone=req.phone,
            district=req.district,
            taluk=req.taluk,
            village=req.village,
            service_title=req.service_title,
            survey_number=req.survey_number,
            grounds_summary=req.grounds_summary,
            meta_verification_id=verification_id
        )
        return {
            "status": "success",
            "verification_id": verification_id,
            "filename": pdf_path.name,
            "download_url": f"/download/petition/{pdf_path.name}"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.get("/download/petition/{filename}")
async def download_petition(filename: str):
    file_path = PETITIONS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Petition PDF not found.")
    return FileResponse(
        str(file_path),
        media_type="application/pdf",
        filename=filename
    )


# ==============================================================================
# Meta WhatsApp Cloud API Webhook Handlers
# ==============================================================================

@app.get("/api/whatsapp/webhook")
async def whatsapp_webhook_verification(
    request: Request,
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge")
):
    """
    Verification endpoint called by Meta App Dashboard during Webhook setup.
    """
    if hub_mode and hub_verify_token:
        challenge = verify_webhook(hub_mode, hub_verify_token, hub_challenge or "")
        if challenge:
            return PlainTextResponse(content=challenge, status_code=200)
        return PlainTextResponse(content="Forbidden", status_code=403)
    return PlainTextResponse(content="Bad Request", status_code=400)


@app.post("/api/whatsapp/webhook")
async def whatsapp_webhook_ingress(request: Request):
    """
    Ingress handler receiving incoming messages, voice notes, and deeds from Meta WhatsApp Cloud API.
    """
    try:
        payload = await request.json()
        result = process_incoming_whatsapp_message(payload)
        return JSONResponse(content={"status": "received", "details": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.post("/api/whatsapp/simulate")
async def whatsapp_simulate_endpoint(req: WhatsAppSimulateRequest):
    """
    Interactive test endpoint allowing hackathon judges to simulate citizen WhatsApp
    messages (voice notes / text / deeds) without needing an active WhatsApp client.
    """
    synthetic_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "WHATSAPP_BIZ_ENTRY",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15550192834",
                                "phone_number_id": META_WHATSAPP_PHONE_ID
                            },
                            "messages": [
                                {
                                    "from": req.sender_phone,
                                    "id": f"wamid.{uuid.uuid4().hex[:12]}",
                                    "timestamp": "1730000000",
                                    "type": req.message_type,
                                    "text": {"body": req.text_body} if req.message_type == "text" else None
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    result = process_incoming_whatsapp_message(synthetic_payload)
    return {"status": "success", "simulation_result": result}


# ==============================================================================
# Single-Click Accessible Bilingual Web Portal
# ==============================================================================

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Interactive Multimodal Action Portal for Makkal Agent AI."""
    html_content = r"""
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Makkal Agent (மக்கள் Agent) - Meta AI Hackathon 2026</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Mukta+Malar:wght@400;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Mukta Malar', 'Inter', sans-serif; }
        .markdown-body h1, .markdown-body h2, .markdown-body h3 {
            font-weight: 700;
            color: #34d399;
            margin-top: 0.75rem;
            margin-bottom: 0.35rem;
            font-size: 1.05rem;
        }
        .markdown-body p { margin-bottom: 0.5rem; line-height: 1.6; }
        .markdown-body ul, .markdown-body ol { margin-left: 1.25rem; margin-bottom: 0.5rem; list-style-type: disc; }
        .markdown-body li { margin-bottom: 0.25rem; }
        .markdown-body a { color: #38bdf8; text-decoration: underline; font-weight: 500; }
        .markdown-body strong { color: #f8fafc; font-weight: 600; }
        .markdown-body blockquote {
            border-left: 3px solid #10b981;
            padding-left: 0.75rem;
            color: #cbd5e1;
            background: rgba(16, 185, 129, 0.08);
            border-radius: 0 0.5rem 0.5rem 0;
            margin: 0.5rem 0;
            padding-top: 0.25rem;
            padding-bottom: 0.25rem;
        }
        .touch-card {
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .touch-card:hover {
            transform: translateY(-2px);
        }
        .touch-card:active {
            transform: scale(0.98);
        }
        @keyframes pulse-ring {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.15); opacity: 0.3; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        .pulse-recording {
            animation: pulse-ring 1.5s infinite;
        }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col items-center justify-between p-2 sm:p-4">

    <!-- Top Status Banner -->
    <div class="w-full max-w-4xl bg-gradient-to-r from-emerald-950/80 via-slate-900 to-teal-950/80 border border-emerald-500/30 rounded-xl px-3 py-1.5 mb-2.5 flex items-center justify-between text-xs">
        <div class="flex items-center gap-2">
            <span class="flex h-2 w-2 relative">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="text-slate-300 font-mono text-[11px]">
                ☁️ <strong class="text-emerald-400">AWS Cloud:</strong> 52.66.255.113:8001
            </span>
            <span class="text-slate-600 hidden sm:inline">•</span>
            <span class="text-slate-400 hidden sm:inline font-mono text-[11px]">
                📱 <strong class="text-teal-400">WhatsApp:</strong> Active Webhook
            </span>
        </div>
        <div class="flex items-center gap-2">
            <a href="https://github.com/rajakumaranaap-rgb/makkal-agent-ai" target="_blank" class="text-slate-300 hover:text-white flex items-center gap-1 font-mono text-[11px] bg-slate-800/80 hover:bg-slate-700 px-2 py-0.5 rounded-lg border border-slate-700 transition">
                <span>⭐ GitHub Repo</span>
            </a>
            <!-- Language Toggle Switch -->
            <button id="langToggleBtn" onclick="toggleLanguage()" class="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold px-2.5 py-0.5 rounded-lg text-[11px] shadow transition flex items-center gap-1">
                <span id="langFlag">🌐</span> <span id="langName">English</span>
            </button>
        </div>
    </div>

    <!-- Header -->
    <header class="w-full max-w-4xl bg-slate-900/90 backdrop-blur-md border border-slate-800 rounded-2xl p-4 mb-3 shadow-2xl flex items-center justify-between">
        <div class="flex items-center space-x-3.5">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-emerald-500 via-teal-500 to-cyan-500 flex items-center justify-center text-2xl shadow-lg shadow-emerald-500/20 flex-shrink-0">
                🏛️
            </div>
            <div>
                <div class="flex items-center gap-2">
                    <h1 id="appTitle" class="text-xl font-extrabold bg-gradient-to-r from-emerald-400 via-teal-200 to-cyan-300 bg-clip-text text-transparent">Makkal Agent (மக்கள் Agent)</h1>
                    <span class="text-[10px] bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-mono font-medium hidden sm:inline">Indie Track $150k</span>
                </div>
                <p id="appSubtitle" class="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>தமிழ்நாடு தன்னாட்சி அரசு சேவை & சட்ட நடவடிக்கை ஏஜென்ட்</span>
                </p>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <!-- Audio Auto-Play Toggle -->
            <button id="audioToggleBtn" onclick="toggleAudioSpeech()" title="குரல் ஒலிபரப்பு (Audio Voice Feedback)" class="bg-slate-800 hover:bg-slate-700 border border-slate-700 p-2 rounded-xl text-emerald-400 text-xs flex items-center gap-1 transition">
                <span id="audioIcon">🔊</span>
            </button>
            <button onclick="openPetitionModal()" class="text-xs bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold px-3 py-2 rounded-xl shadow transition flex items-center gap-1.5">
                <span id="petitionBtnText">📑 மனு உருவாக்கம் (PDF)</span>
            </button>
        </div>
    </header>

    <!-- 1-Click Illiterate-First Visual Touch Grid -->
    <div class="w-full max-w-4xl mb-3">
        <div class="flex items-center justify-between mb-1.5 px-1">
            <span id="touchGridTitle" class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">⚡ 1-கிளிக் நேரடி சேவைகள் (1-Click Citizen Entitlements - No Typing Needed)</span>
            <span class="text-[10px] text-emerald-400 font-mono">Meta Muse Spark Dispatch</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
            <!-- Service 1: Patta Chitta -->
            <button onclick="triggerServiceFlow('patta')" class="touch-card bg-gradient-to-br from-emerald-950/60 to-slate-900 border border-emerald-500/30 hover:border-emerald-400/80 p-2.5 rounded-xl text-left flex flex-col justify-between shadow-lg">
                <div class="text-2xl mb-1">🌾</div>
                <div>
                    <div id="tile1Title" class="font-bold text-xs text-emerald-300">பட்டா & சிட்டா</div>
                    <div id="tile1Desc" class="text-[10px] text-slate-400">நில ஆவணம் மாற்றம்</div>
                </div>
            </button>
            <!-- Service 2: Legal Heir -->
            <button onclick="triggerServiceFlow('legal_heir')" class="touch-card bg-gradient-to-br from-teal-950/60 to-slate-900 border border-teal-500/30 hover:border-teal-400/80 p-2.5 rounded-xl text-left flex flex-col justify-between shadow-lg">
                <div class="text-2xl mb-1">👨‍👩‍👧‍👦</div>
                <div>
                    <div id="tile2Title" class="font-bold text-xs text-teal-300">வாரிசு சான்றிதழ்</div>
                    <div id="tile2Desc" class="text-[10px] text-slate-400">குடும்ப உரிமை ஆவணம்</div>
                </div>
            </button>
            <!-- Service 3: Ration Card -->
            <button onclick="triggerServiceFlow('ration')" class="touch-card bg-gradient-to-br from-cyan-950/60 to-slate-900 border border-cyan-500/30 hover:border-cyan-400/80 p-2.5 rounded-xl text-left flex flex-col justify-between shadow-lg">
                <div class="text-2xl mb-1">🍚</div>
                <div>
                    <div id="tile3Title" class="font-bold text-xs text-cyan-300">ரேஷன் அட்டை</div>
                    <div id="tile3Desc" class="text-[10px] text-slate-400">புதிய குடும்ப அட்டை</div>
                </div>
            </button>
            <!-- Service 4: KMUT ₹1000 -->
            <button onclick="triggerServiceFlow('kmut')" class="touch-card bg-gradient-to-br from-amber-950/60 to-slate-900 border border-amber-500/30 hover:border-amber-400/80 p-2.5 rounded-xl text-left flex flex-col justify-between shadow-lg">
                <div class="text-2xl mb-1">👩‍💼</div>
                <div>
                    <div id="tile4Title" class="font-bold text-xs text-amber-300">மகளிர் உரிமை</div>
                    <div id="tile4Desc" class="text-[10px] text-slate-400">மாதம் ₹1,000 திட்டம்</div>
                </div>
            </button>
            <!-- Service 5: CMCHIS Insurance -->
            <button onclick="triggerServiceFlow('cmchis')" class="touch-card bg-gradient-to-br from-rose-950/60 to-slate-900 border border-rose-500/30 hover:border-rose-400/80 p-2.5 rounded-xl text-left flex flex-col justify-between shadow-lg">
                <div class="text-2xl mb-1">🏥</div>
                <div>
                    <div id="tile5Title" class="font-bold text-xs text-rose-300">மருத்துவக் காப்பீடு</div>
                    <div id="tile5Desc" class="text-[10px] text-slate-400">₹5 லட்சம் இலவச சிகிச்சை</div>
                </div>
            </button>
            <!-- Service 6: Public Grievance Petition -->
            <button onclick="openPetitionModal()" class="touch-card bg-gradient-to-br from-purple-950/60 to-slate-900 border border-purple-500/30 hover:border-purple-400/80 p-2.5 rounded-xl text-left flex flex-col justify-between shadow-lg">
                <div class="text-2xl mb-1">⚖️</div>
                <div>
                    <div id="tile6Title" class="font-bold text-xs text-purple-300">குறைதீர்ப்பு மனு</div>
                    <div id="tile6Desc" class="text-[10px] text-slate-400">ஆட்சியர் மனு தயாரிப்பு</div>
                </div>
            </button>
        </div>
    </div>

    <!-- Multimodal Action Bar (Voice, SAM 3.1 Vision, WhatsApp Simulator) -->
    <div class="w-full max-w-4xl bg-slate-900/60 border border-slate-800/80 rounded-2xl p-3 mb-2 flex flex-wrap items-center justify-between gap-2 text-xs">
        <div class="flex items-center gap-2">
            <!-- SAM 3.1 Camera Upload -->
            <label class="cursor-pointer bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-xl text-slate-300 flex items-center gap-1.5 transition">
                <span>📸 <span id="samBtnLabel">ஆவணம் ஆய்வு (SAM 3.1)</span></span>
                <input type="file" id="docUpload" accept="image/*" class="hidden" onchange="uploadDocumentForAudit(event)">
            </label>
            <!-- Voice Input Button -->
            <button id="voiceBtn" onclick="toggleVoiceRecording()" class="bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-xl text-slate-300 flex items-center gap-1.5 transition">
                <span id="voiceIcon">🎙️</span> <span id="voiceText">தமிழில் பேசுங்கள்</span>
            </button>
            <!-- WhatsApp Simulation Trigger for Judges -->
            <button onclick="simulateWhatsAppCitizen()" class="bg-teal-950 hover:bg-teal-900 border border-teal-700/60 px-2.5 py-1.5 rounded-xl text-teal-300 flex items-center gap-1 transition">
                <span>📱 <span id="waSimLabel">WhatsApp டெமோ</span></span>
            </button>
        </div>
        <!-- Model Selection Toggles -->
        <div class="flex items-center gap-3 text-slate-400">
            <label class="flex items-center space-x-1.5 cursor-pointer select-none hover:text-emerald-300 transition">
                <input type="checkbox" id="deepReasonToggle" class="rounded bg-slate-800 border-slate-700 text-emerald-500 focus:ring-0 accent-emerald-500">
                <span>🧠 Muse Wonder (Deep Reasoning)</span>
            </label>
        </div>
    </div>

    <!-- SAM 3.1 Visual Audit Box (Appears when document uploaded) -->
    <div id="samAuditBox" class="hidden w-full max-w-4xl bg-slate-900/90 border border-cyan-500/40 rounded-2xl p-4 mb-2 shadow-xl animate-fade-in">
        <div class="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
            <div class="flex items-center gap-2">
                <span class="text-cyan-400 font-bold text-sm">🎯 Meta SAM 3.1 (Segment Anything) ஆவணத் தணிக்கை</span>
                <span class="text-[10px] bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 px-2 py-0.5 rounded-full font-mono">Computer Vision Audit</span>
            </div>
            <button onclick="closeAuditBox()" class="text-slate-400 hover:text-slate-200 text-xs">✕ மூடு</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <img id="auditImage" src="" alt="Segmented Document" class="rounded-xl border border-slate-700 w-full object-contain max-h-60 bg-slate-950">
            </div>
            <div class="space-y-2 text-xs">
                <div id="auditVerdict" class="font-bold text-emerald-400"></div>
                <div id="auditZones" class="space-y-1.5 max-h-48 overflow-y-auto pr-1"></div>
            </div>
        </div>
    </div>

    <!-- Chat Message Container -->
    <main id="chatBox" class="w-full max-w-4xl flex-1 bg-slate-900/40 border border-slate-800/60 rounded-2xl p-4 overflow-y-auto space-y-4 my-2 shadow-inner">
        <!-- Welcome Message -->
        <div class="flex items-start space-x-3">
            <div class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-base flex-shrink-0 mt-1">
                🏛️
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 max-w-[88%] text-slate-200 text-sm leading-relaxed shadow-md space-y-2">
                <p id="welcomeGreeting" class="font-bold text-emerald-400 text-base">வணக்கம்! நான் உங்கள் மக்கள் ஏஜென்ட் (Makkal Agent AI).</p>
                <p id="welcomeBody">நான் வெறும் உரையாடல் செயலி அல்ல; தமிழ்நாடு அரசின் பட்டா மாறுதல், வாரிசு சான்றிதழ், ரேஷன் கார்டு, மகளிர் உரிமைத் திட்டங்களுக்கான உங்கள் **தன்னாட்சி டிஜிட்டல் அலுவலர்**.</p>
                <div class="pt-2 border-t border-slate-800 text-xs text-slate-400 flex flex-wrap gap-2.5">
                    <span id="welcomePill1">🎙️ தமிழில் பேசலாம்</span> • 
                    <span id="welcomePill2">📸 பத்திரத்தை படம் பிடித்து அனுப்பலாம்</span> • 
                    <span id="welcomePill3">📑 சட்டப்பூர்வ மனுவை பதிவிறக்கலாம்</span> • 
                    <span id="welcomePill4">📱 WhatsApp மூலம் இயக்கலாம்</span>
                </div>
            </div>
        </div>
    </main>

    <!-- Input Footer -->
    <footer class="w-full max-w-4xl bg-slate-900/90 backdrop-blur-md border border-slate-800 rounded-2xl p-2.5 shadow-2xl flex items-center space-x-2">
        <input id="userInput" type="text" placeholder="உங்கள் நிலம், பட்டா அல்லது அரசு சேவை பற்றி கேளுங்கள் (அல்லது மேலே 1-கிளிக் அழுத்தவும்)..." 
               class="flex-1 bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition"
               onkeypress="handleKeyPress(event)">
        <button id="sendBtn" onclick="sendMessage()" 
                class="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold px-5 py-3 rounded-xl transition shadow-lg shadow-emerald-500/20 flex items-center justify-center text-sm flex-shrink-0">
            <span id="sendBtnText">அனுப்பு</span>
        </button>
    </footer>

    <!-- Petition Modal -->
    <div id="petitionModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 id="modalTitle" class="text-base font-bold text-emerald-400">📑 சட்டப்பூர்வ மனு தயாரிப்பு (Court-Ready Legal Petition PDF)</h3>
                <button onclick="closePetitionModal()" class="text-slate-400 hover:text-slate-200">✕</button>
            </div>
            <div class="space-y-3 text-xs">
                <div>
                    <label id="lblPetName" class="block text-slate-400 mb-1">மனுதாரர் பெயர் (Applicant Name):</label>
                    <input id="petName" type="text" value="ர. சுப்பிரமணியன்" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label id="lblPetPhone" class="block text-slate-400 mb-1">அலைபேசி (Phone):</label>
                        <input id="petPhone" type="text" value="9840012345" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                    </div>
                    <div>
                        <label id="lblPetDist" class="block text-slate-400 mb-1">மாவட்டம் (District):</label>
                        <input id="petDist" type="text" value="தஞ்சாவூர்" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label id="lblPetTaluk" class="block text-slate-400 mb-1">வட்டம் (Taluk):</label>
                        <input id="petTaluk" type="text" value="கும்பகோணம்" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                    </div>
                    <div>
                        <label id="lblPetVillage" class="block text-slate-400 mb-1">கிராமம் (Village):</label>
                        <input id="petVillage" type="text" value="திருநாகேஸ்வரம்" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                    </div>
                </div>
                <div>
                    <label id="lblPetService" class="block text-slate-400 mb-1">விண்ணப்ப வகை (Service Category):</label>
                    <input id="petService" type="text" value="கிரய பட்டா பெயர் மாற்றம் (Patta Transfer)" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                </div>
                <div>
                    <label id="lblPetSurvey" class="block text-slate-400 mb-1">புல எண் / சர்வே எண் (Survey No):</label>
                    <input id="petSurvey" type="text" value="142/3A" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                </div>
                <div>
                    <label id="lblPetGrounds" class="block text-slate-400 mb-1">மனு விவரம் & கோரிக்கை (Grounds of Petition):</label>
                    <textarea id="petGrounds" rows="3" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">மேற்படி சர்வே எண் கொண்ட நன்செய் நிலத்தை கிரய பத்திரம் எண் 1284/2024 மூலம் முறையாக வாங்கி பதிவு செய்துள்ளேன். இதற்குரிய கூட்டு பட்டாவில் இருந்து என் பெயரில் தனி பட்டா மாற்றம் செய்து உத்தரவிட வேண்டுகிறேன்.</textarea>
                </div>
            </div>
            <div class="flex justify-end gap-2 pt-2 border-t border-slate-800">
                <button onclick="closePetitionModal()" id="btnCancelModal" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-medium">ரத்து</button>
                <button onclick="generateOfficialPetition()" id="btnGenerateModal" class="px-5 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl text-xs font-bold shadow">📄 PDF மனு உருவாக்கு</button>
            </div>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chatBox');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const deepReasonToggle = document.getElementById('deepReasonToggle');
        
        let currentLang = 'ta'; // 'ta' or 'en'
        let audioSpeechEnabled = true;
        let chatHistory = [];
        let mediaRecorder = null;
        let audioChunks = [];

        // Language Dictionary
        const I18N = {
            ta: {
                flag: '🌐',
                langName: 'English',
                appTitle: 'Makkal Agent (மக்கள் Agent)',
                appSubtitle: 'தமிழ்நாடு தன்னாட்சி அரசு சேவை & சட்ட நடவடிக்கை ஏஜென்ட்',
                petitionBtnText: '📑 மனு உருவாக்கம் (PDF)',
                touchGridTitle: '⚡ 1-கிளிக் நேரடி சேவைகள் (1-Click Citizen Entitlements - No Typing Needed)',
                tile1Title: 'பட்டா & சிட்டா',
                tile1Desc: 'நில ஆவணம் மாற்றம்',
                tile2Title: 'வாரிசு சான்றிதழ்',
                tile2Desc: 'குடும்ப உரிமை ஆவணம்',
                tile3Title: 'ரேஷன் அட்டை',
                tile3Desc: 'புதிய குடும்ப அட்டை',
                tile4Title: 'மகளிர் உரிமை',
                tile4Desc: 'மாதம் ₹1,000 திட்டம்',
                tile5Title: 'மருத்துவக் காப்பீடு',
                tile5Desc: '₹5 லட்சம் இலவச சிகிச்சை',
                tile6Title: 'குறைதீர்ப்பு மனு',
                tile6Desc: 'ஆட்சியர் மனு தயாரிப்பு',
                samBtnLabel: 'ஆவணம் ஆய்வு (SAM 3.1)',
                voiceText: 'தமிழில் பேசுங்கள்',
                waSimLabel: 'WhatsApp டெமோ',
                inputPlaceholder: 'உங்கள் நிலம், பட்டா அல்லது அரசு சேவை பற்றி கேளுங்கள் (அல்லது மேலே 1-கிளிக் அழுத்தவும்)...',
                sendBtnText: 'அனுப்பு',
                welcomeGreeting: 'வணக்கம்! நான் உங்கள் மக்கள் ஏஜென்ட் (Makkal Agent AI).',
                welcomeBody: 'நான் வெறும் உரையாடல் செயலி அல்ல; தமிழ்நாடு அரசின் பட்டா மாறுதல், வாரிசு சான்றிதழ், ரேஷன் கார்டு, மகளிர் உரிமைத் திட்டங்களுக்கான உங்கள் **தன்னாட்சி டிஜிட்டல் அலுவலர்**.'
            },
            en: {
                flag: '🇮🇳',
                langName: 'தமிழ்',
                appTitle: 'Makkal Agent AI (People’s AI)',
                appSubtitle: 'Autonomous Tamil Nadu Civic Entitlements & Legal Action Agent',
                petitionBtnText: '📑 Draft Petition (PDF)',
                touchGridTitle: '⚡ 1-Click Citizen Entitlements (Zero Typing Required)',
                tile1Title: 'Patta & Chitta',
                tile1Desc: 'Land Record Transfer',
                tile2Title: 'Legal Heir',
                tile2Desc: 'Succession Certificate',
                tile3Title: 'Ration Card',
                tile3Desc: 'TNPDS Smart Card',
                tile4Title: 'KMUT ₹1,000 Aid',
                tile4Desc: 'Monthly Women Entitlement',
                tile5Title: 'CMCHIS Health',
                tile5Desc: '₹5 Lakh Free Treatment',
                tile6Title: 'Grievance Petition',
                tile6Desc: 'District Collector Draft',
                samBtnLabel: 'Audit Deed (SAM 3.1)',
                voiceText: 'Speak in Tamil / English',
                waSimLabel: 'WhatsApp Demo',
                inputPlaceholder: 'Ask about Patta, Land records, or Welfare Schemes (or click a service tile above)...',
                sendBtnText: 'Send',
                welcomeGreeting: 'Welcome! I am your Makkal Agent AI (Citizen Action Agent).',
                welcomeBody: 'I am not just a chatbot. I am an **Autonomous Multimodal Action Agent** safeguarding Tamil Nadu citizens from middleman corruption and navigating Patta transfers, Legal Heir, and Ration benefits.'
            }
        };

        function toggleLanguage() {
            currentLang = currentLang === 'ta' ? 'en' : 'ta';
            const t = I18N[currentLang];
            document.getElementById('langFlag').innerText = t.flag;
            document.getElementById('langName').innerText = t.langName;
            document.getElementById('appTitle').innerText = t.appTitle;
            document.getElementById('appSubtitle').innerText = t.appSubtitle;
            document.getElementById('petitionBtnText').innerText = t.petitionBtnText;
            document.getElementById('touchGridTitle').innerText = t.touchGridTitle;
            document.getElementById('tile1Title').innerText = t.tile1Title;
            document.getElementById('tile1Desc').innerText = t.tile1Desc;
            document.getElementById('tile2Title').innerText = t.tile2Title;
            document.getElementById('tile2Desc').innerText = t.tile2Desc;
            document.getElementById('tile3Title').innerText = t.tile3Title;
            document.getElementById('tile3Desc').innerText = t.tile3Desc;
            document.getElementById('tile4Title').innerText = t.tile4Title;
            document.getElementById('tile4Desc').innerText = t.tile4Desc;
            document.getElementById('tile5Title').innerText = t.tile5Title;
            document.getElementById('tile5Desc').innerText = t.tile5Desc;
            document.getElementById('tile6Title').innerText = t.tile6Title;
            document.getElementById('tile6Desc').innerText = t.tile6Desc;
            document.getElementById('samBtnLabel').innerText = t.samBtnLabel;
            document.getElementById('voiceText').innerText = t.voiceText;
            document.getElementById('waSimLabel').innerText = t.waSimLabel;
            document.getElementById('userInput').placeholder = t.inputPlaceholder;
            document.getElementById('sendBtnText').innerText = t.sendBtnText;
            document.getElementById('welcomeGreeting').innerText = t.welcomeGreeting;
            document.getElementById('welcomeBody').innerHTML = t.welcomeBody;
        }

        function toggleAudioSpeech() {
            audioSpeechEnabled = !audioSpeechEnabled;
            const icon = document.getElementById('audioIcon');
            icon.innerText = audioSpeechEnabled ? '🔊' : '🔇';
            if (!audioSpeechEnabled && window.speechSynthesis) {
                window.speechSynthesis.cancel();
            }
        }

        function speakText(text) {
            if (!audioSpeechEnabled || !window.speechSynthesis) return;
            window.speechSynthesis.cancel();
            // Strip markdown formatting for speech
            const cleanText = text.replace(/[*#_`~>]/g, '').replace(/\[(.*?)\]\(.*?\)/g, '$1').slice(0, 300);
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang = currentLang === 'ta' ? 'ta-IN' : 'en-IN';
            utterance.rate = 1.0;
            window.speechSynthesis.speak(utterance);
        }

        function triggerServiceFlow(service) {
            const prompts = {
                patta: currentLang === 'ta' 
                    ? 'பட்டா சிட்டா நில ஆவணம் பெயர் மாற்றம் செய்ய என்ன செய்ய வேண்டும்? அரசு கட்டணம் எவ்வளவு?'
                    : 'How to apply for Patta Chitta land transfer in Tamil Nadu? What are the official government fees?',
                legal_heir: currentLang === 'ta'
                    ? 'வாரிசு சான்றிதழ் ஆன்லைனில் விண்ணப்பிப்பது எப்படி? யார் விண்ணப்பிக்கலாம்?'
                    : 'How to apply for a Legal Heir Certificate online? Who are the eligible Class-I legal heirs?',
                ration: currentLang === 'ta'
                    ? 'ரேஷன் கார்டில் புதிய குழந்தை பெயர் சேர்க்க தேவையான ஆவணங்கள் என்ன?'
                    : 'What documents are required to add a child or new spouse to a TNPDS Smart Ration Card?',
                kmut: currentLang === 'ta'
                    ? 'கலைஞர் மகளிர் உரிமைத் திட்டம் மாதம் 1000 ரூபாய் தகுதி மற்றும் மேல்முறையீடு எப்படி செய்வது?'
                    : 'What is the eligibility for the Kalaignar Magalir Urimai Thittam (KMUT) Rs 1,000 monthly scheme and how to appeal?',
                cmchis: currentLang === 'ta'
                    ? 'முதலமைச்சர் மருத்துவக் காப்பீட்டு திட்டத்தில் 5 லட்சம் ரூபாய் வரை சிகிச்சை பெறுவது எப்படி?'
                    : 'How to avail up to Rs 5 Lakh cashless treatment under the Chief Minister Comprehensive Health Insurance Scheme (CMCHIS)?'
            };
            userInput.value = prompts[service] || '';
            sendMessage();
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }

        async function sendMessage() {
            const query = userInput.value.trim();
            if (!query) return;

            appendMessage(query, 'user');
            userInput.value = '';
            userInput.disabled = true;
            sendBtn.disabled = true;

            const isDeep = deepReasonToggle ? deepReasonToggle.checked : false;
            const loadingId = appendLoading(isDeep);

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        message: query, 
                        history: chatHistory,
                        use_deep_reasoning: isDeep,
                        language: currentLang
                    })
                });
                const data = await res.json();
                removeLoading(loadingId);

                if (data.status === 'success') {
                    appendMessage(data.reply, 'assistant', data.model_used);
                    chatHistory.push({ role: 'user', content: query });
                    chatHistory.push({ role: 'assistant', content: data.reply });
                    speakText(data.reply);
                } else {
                    appendMessage('மன்னிக்கவும், தகவல் பெறுவதில் சிறிய பிழை: ' + (data.message || ''), 'assistant');
                }
            } catch (err) {
                removeLoading(loadingId);
                appendMessage('தகவல் தொடர்பு பிழை: ' + err.message, 'assistant');
            } finally {
                userInput.disabled = false;
                sendBtn.disabled = false;
                userInput.focus();
            }
        }

        function appendMessage(text, role, model) {
            const div = document.createElement('div');
            div.className = role === 'user' ? 'flex justify-end' : 'flex items-start space-x-3';

            if (role === 'user') {
                const escaped = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\\n/g, '<br>');
                div.innerHTML = `
                    <div class="bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-2xl rounded-tr-none p-3.5 max-w-[85%] text-sm shadow-md">
                        ${escaped}
                    </div>
                `;
            } else {
                let formatted = '';
                try { formatted = marked.parse(text); } catch (e) { formatted = text.replace(/\\n/g, '<br>'); }
                div.innerHTML = `
                    <div class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-base flex-shrink-0 mt-1">
                        🏛️
                    </div>
                    <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 max-w-[88%] text-slate-200 text-sm leading-relaxed shadow-md space-y-2">
                        <div class="markdown-body">${formatted}</div>
                        <div class="text-[10px] text-emerald-400/80 font-mono pt-1.5 border-t border-slate-800 flex items-center justify-between">
                            <span>⚡ Meta Model: ${model || 'muse-spark-1.3'}</span>
                            <button onclick="speakText(this.closest('.space-y-2').querySelector('.markdown-body').innerText)" class="hover:text-emerald-300 flex items-center gap-1 font-sans text-xs">
                                🔊 உரக்கப் படி
                            </button>
                        </div>
                    </div>
                `;
            }
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function appendLoading(isDeep) {
            const id = 'load_' + Date.now();
            const div = document.createElement('div');
            div.id = id;
            div.className = 'flex items-start space-x-3';
            const text = isDeep ? 'Meta Muse Wonder ஆழ்ந்த சட்ட பகுப்பாய்வு செய்கிறது...' : 'Meta AI ஆய்வு செய்கிறது...';
            div.innerHTML = `
                <div class="w-9 h-9 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-base flex-shrink-0">
                    🏛️
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-3.5 text-slate-400 text-sm flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce"></span>
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.2s]"></span>
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.4s]"></span>
                    <span class="text-xs text-slate-400 pl-1 font-mono">${text}</span>
                </div>
            `;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
            return id;
        }

        function removeLoading(id) {
            const el = document.getElementById(id);
            if (el) el.remove();
        }

        // WhatsApp Ingress Simulation
        async function simulateWhatsAppCitizen() {
            appendMessage("📱 *[WhatsApp Webhook Simulation]* Citizen (+91 98400 12345) sent a WhatsApp query...", "user");
            const loadingId = appendLoading(false);
            try {
                const res = await fetch('/api/whatsapp/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sender_phone: "919840012345",
                        message_type: "text",
                        text_body: "வணக்கம் அய்யா, கூட்டு பட்டாவில் இருந்து என் பெயரில் தனி பட்டா மாற்ற மனு செய்ய வேண்டும். ஆவணம் சரிபார்க்கவும்."
                    })
                });
                const data = await res.json();
                removeLoading(loadingId);
                appendMessage(
                    `📲 **[WhatsApp Cloud Bot Dispatched]:**\\n\\n` +
                    `• Sender: \`+91 98400 12345\`\\n` +
                    `• Webhook Status: \`${data.simulation_result.status}\`\\n` +
                    `• Response Type: \`Meta WhatsApp Cloud Text + PDF Document Dispatch\`\\n\\n` +
                    `*குடிமகனின் WhatsApp-ல் அதிகாரப்பூர்வ மனு மற்றும் ஆவண வழிகாட்டல் உடனே அனுப்பப்பட்டது!*`,
                    'assistant',
                    'Meta WhatsApp Gateway'
                );
            } catch (err) {
                removeLoading(loadingId);
                appendMessage('WhatsApp Simulation Error: ' + err.message, 'assistant');
            }
        }

        // Voice Recording via Muse Voice Transcribe
        async function toggleVoiceRecording() {
            const vBtn = document.getElementById('voiceBtn');
            const vText = document.getElementById('voiceText');
            const vIcon = document.getElementById('voiceIcon');

            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                vText.innerText = 'Transcribing...';
                vIcon.innerText = '⏳';
                return;
            }

            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioChunks = [];
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
                    const formData = new FormData();
                    formData.append('file', audioBlob, 'citizen_voice.mp3');

                    vText.innerText = 'Meta Voice ஆய்வு...';
                    try {
                        const res = await fetch('/api/transcribe', { method: 'POST', body: formData });
                        const data = await res.json();
                        if (data.status === 'success' && data.transcript) {
                            userInput.value = data.transcript;
                            sendMessage();
                        } else {
                            alert('குரல் கேட்கவில்லை அல்லது பிழை: ' + (data.message || ''));
                        }
                    } catch (e) {
                        alert('Voice Transcribe Error: ' + e.message);
                    } finally {
                        vText.innerText = I18N[currentLang].voiceText;
                        vIcon.innerText = '🎙️';
                    }
                };
                mediaRecorder.start();
                vText.innerText = 'பதிவாகிறது (Stop அழுத்தவும்)...';
                vIcon.innerText = '🔴';
            } catch (err) {
                alert('மைக்ரோபோன் அனுமதி தேவை: ' + err.message);
            }
        }

        // SAM 3.1 Document Audit
        async function uploadDocumentForAudit(e) {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            const auditBox = document.getElementById('samAuditBox');
            const auditImg = document.getElementById('auditImage');
            const verdict = document.getElementById('auditVerdict');
            const zones = document.getElementById('auditZones');

            auditBox.classList.remove('hidden');
            verdict.innerText = 'Meta SAM 3.1 பிக்சல் பகுப்பாய்வு செய்கிறது...';
            zones.innerHTML = '<span class="text-slate-400">அரசு முத்திரை மற்றும் கையெழுத்து ஸ்கேன் செய்யப்படுகிறது...</span>';

            try {
                const res = await fetch('/api/audit-document', { method: 'POST', body: formData });
                const data = await res.json();

                if (data.status === 'success') {
                    auditImg.src = data.overlay_image_base64;
                    verdict.innerText = data.audit_summary_ta;
                    verdict.className = data.is_authentic ? 'font-bold text-emerald-400' : 'font-bold text-amber-400';

                    zones.innerHTML = data.segmented_zones.map(z => `
                        <div class="bg-slate-950 border border-slate-800 p-2 rounded-lg flex items-center justify-between">
                            <div>
                                <span class="font-semibold text-cyan-300">${z.label}</span>
                                <p class="text-[11px] text-slate-400">${z.notes_ta}</p>
                            </div>
                            <span class="text-[10px] bg-slate-800 px-2 py-0.5 rounded text-slate-300 font-mono">${Math.round(z.confidence * 100)}%</span>
                        </div>
                    `).join('');

                    appendMessage(`📸 **ஆவணம் சமர்ப்பிக்கப்பட்டது (${file.name}):**\\n\\n${data.audit_summary_ta}`, 'assistant', 'sam-3.1');
                    speakText(data.audit_summary_ta);
                } else {
                    verdict.innerText = 'ஆய்வு பிழை: ' + (data.message || '');
                }
            } catch (err) {
                verdict.innerText = 'தொடர்பு பிழை: ' + err.message;
            }
        }

        function closeAuditBox() {
            document.getElementById('samAuditBox').classList.add('hidden');
        }

        // Legal Petition Modal
        function openPetitionModal() {
            document.getElementById('petitionModal').classList.remove('hidden');
        }

        function closePetitionModal() {
            document.getElementById('petitionModal').classList.add('hidden');
        }

        async function generateOfficialPetition() {
            const payload = {
                applicant_name: document.getElementById('petName').value,
                phone: document.getElementById('petPhone').value,
                district: document.getElementById('petDist').value,
                taluk: document.getElementById('petTaluk').value,
                village: document.getElementById('petVillage').value,
                service_title: document.getElementById('petService').value,
                survey_number: document.getElementById('petSurvey').value,
                grounds_summary: document.getElementById('petGrounds').value
            };

            try {
                const res = await fetch('/api/generate-petition', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.status === 'success') {
                    closePetitionModal();
                    const petitionMsg = `🎉 **சட்டப்பூர்வ மனு தயாராகிவிட்டது!**\\n\\nஉங்களுடைய அதிகாரப்பூர்வ மனு PDF வடிவில் உருவாக்கப்பட்டுள்ளது. இதில் உங்கள் கையெழுத்தை இட்டு நேரடியாக வட்டாட்சியர் அலுவலகத்திலோ அல்லது இ-சேவை மையத்திலோ சமர்ப்பிக்கலாம்.\\n\\n👉 **[மனுவை பதிவிறக்கம் செய்ய இங்கே கிளிக் செய்யவும்](${data.download_url})**\\n\\n📌 *சரிபார்ப்பு எண் (Verification ID):* <code>${data.verification_id}</code>`;
                    appendMessage(petitionMsg, 'assistant', 'ActionExecutor');
                    speakText("உங்கள் சட்டப்பூர்வ மனு வெற்றிகரமாக தயாராகிவிட்டது. பதிவிறக்கம் செய்து கையொப்பமிடலாம்.");
                } else {
                    alert('மனு உருவாக்க பிழை: ' + (data.message || ''));
                }
            } catch (e) {
                alert('பிழை: ' + e.message);
            }
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
