"""
Makkal Agent (மக்கள் Agent) - FastAPI Server & Multimodal Citizen Portal
Meta AI Developer Hackathon 2026 (Indie Developer Track)

Powered by:
- Meta Muse Spark (muse-spark-1.3)
- Meta Muse Wonder (muse-wonder-1.0)
- Meta SAM 3.1 (sam-3.1)
- Meta Muse Voice Transcribe (muse-voice-transcribe-1.0)
- Baseten Open-Weight Bridge (meta-models/muse-spark-open-1026)
"""

import os
import json
import uuid
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from meta_client import meta_client, DEFAULT_CHAT_MODEL, REASONING_MODEL, SEGMENT_MODEL, BASETEN_MODEL_ID
from sam_document_auditor import sam_auditor
from action_executor import action_executor
from knowledge_base import SERVICES_CATALOG, search_knowledge_base

app = FastAPI(
    title="Makkal Agent (மக்கள் Agent)",
    description="Autonomous Multimodal Citizen Action Agent for Tamil Nadu powered by Meta Model API & SAM 3.1",
    version="2.0.0"
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
1. Tone: Respectful, patient, colloquial Tamil (மரியாதையான எளிய தமிழ்). If spoken to in English, provide bilingual responses.
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


class PetitionRequest(BaseModel):
    applicant_name: str
    phone: str
    district: str
    taluk: str
    village: str
    service_title: str
    survey_number: str
    grounds_summary: str


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

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT + f"\n\n[OFFICIAL TAMIL NADU STATUTORY CONTEXT]:\n{kb_context}"}
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


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Interactive Multimodal Action Portal for Makkal Agent."""
    html_content = """
<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Makkal Agent (மக்கள் Agent) - Meta AI Hackathon 2026</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Mukta+Malar:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
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
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col items-center justify-between p-2 sm:p-4">

    <!-- Header -->
    <header class="w-full max-w-3xl bg-slate-900/90 backdrop-blur-md border border-slate-800 rounded-2xl p-4 mb-3 shadow-2xl flex items-center justify-between">
        <div class="flex items-center space-x-3.5">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-emerald-500 via-teal-500 to-cyan-500 flex items-center justify-center text-2xl shadow-lg shadow-emerald-500/20">
                🏛️
            </div>
            <div>
                <div class="flex items-center gap-2">
                    <h1 class="text-xl font-bold bg-gradient-to-r from-emerald-400 via-teal-200 to-cyan-300 bg-clip-text text-transparent">Makkal Agent (மக்கள் Agent)</h1>
                    <span class="text-[10px] bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-mono font-medium">Meta AI Hackathon 2026</span>
                </div>
                <p class="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    Autonomous Multimodal Action Agent (Muse Spark • Muse Wonder • SAM 3.1 • Muse Voice)
                </p>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <button onclick="openPetitionModal()" class="text-xs bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold px-3 py-1.5 rounded-xl shadow transition flex items-center gap-1">
                📑 மனு உருவாக்கம் (PDF)
            </button>
        </div>
    </header>

    <!-- Multimodal Action Bar (Voice & SAM 3.1 Vision) -->
    <div class="w-full max-w-3xl bg-slate-900/60 border border-slate-800/80 rounded-2xl p-3 mb-2 flex items-center justify-between gap-2 text-xs">
        <div class="flex items-center gap-2">
            <!-- SAM 3.1 Camera Upload -->
            <label class="cursor-pointer bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-xl text-slate-300 flex items-center gap-1.5 transition">
                <span>📸 ஆவணம் ஆய்வு (SAM 3.1)</span>
                <input type="file" id="docUpload" accept="image/*" class="hidden" onchange="uploadDocumentForAudit(event)">
            </label>
            <!-- Voice Input Button -->
            <button id="voiceBtn" onclick="toggleVoiceRecording()" class="bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-xl text-slate-300 flex items-center gap-1.5 transition">
                <span id="voiceIcon">🎙️</span> <span id="voiceText">தமிழில் பேசுங்கள்</span>
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
    <div id="samAuditBox" class="hidden w-full max-w-3xl bg-slate-900/90 border border-cyan-500/40 rounded-2xl p-4 mb-2 shadow-xl animate-fade-in">
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

    <!-- Quick Action Badges -->
    <div class="w-full max-w-3xl flex gap-2 overflow-x-auto pb-2 scrollbar-none text-xs">
        <button onclick="sendQuickPrompt('பட்டா சிட்டா நில ஆவணம் பெயர் மாற்றம் செய்ய என்ன செய்ய வேண்டும்?')" class="whitespace-nowrap bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 px-3 py-1.5 rounded-full transition shadow-sm">📜 பட்டா / சிட்டா பெயர் மாற்றம்</button>
        <button onclick="sendQuickPrompt('வாரிசு சான்றிதழ் ஆன்லைனில் விண்ணப்பிப்பது எப்படி? யார் விண்ணப்பிக்கலாம்?')" class="whitespace-nowrap bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 px-3 py-1.5 rounded-full transition shadow-sm">🏷️ வாரிசு சான்றிதழ்</button>
        <button onclick="sendQuickPrompt('ரேஷன் கார்டில் புதிய குழந்தை பெயர் சேர்க்க தேவையான ஆவணங்கள் என்ன?')" class="whitespace-nowrap bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 px-3 py-1.5 rounded-full transition shadow-sm">👶 ரேஷன் பெயர் சேர்க்க</button>
        <button onclick="sendQuickPrompt('கலைஞர் மகளிர் உரிமைத் திட்டம் 1000 ரூபாய் தகுதி மற்றும் மேல்முறையீடு எப்படி செய்வது?')" class="whitespace-nowrap bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 px-3 py-1.5 rounded-full transition shadow-sm">💰 மகளிர் உரிமை ₹1,000</button>
    </div>

    <!-- Chat Message Container -->
    <main id="chatBox" class="w-full max-w-3xl flex-1 bg-slate-900/40 border border-slate-800/60 rounded-2xl p-4 overflow-y-auto space-y-4 my-2 shadow-inner">
        <!-- Welcome Message -->
        <div class="flex items-start space-x-3">
            <div class="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-sm flex-shrink-0 mt-1">
                🏛️
            </div>
            <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 max-w-[85%] text-slate-200 text-sm leading-relaxed shadow-md">
                <p class="font-bold text-emerald-400 mb-1">வணக்கம்! நான் உங்கள் மக்கள் ஏஜென்ட் (Makkal Agent).</p>
                <p>நான் வெறும் உரையாடல் செயலி அல்ல; தமிழ்நாடு அரசின் பட்டா, வாரிசு சான்றிதழ், ரேஷன் கார்டு, மகளிர் உரிமைத் திட்டங்களுக்கான உங்கள் **டிஜிட்டல் அலுவலர்**.</p>
                <div class="mt-2.5 pt-2 border-t border-slate-800 text-xs text-slate-400 flex flex-wrap gap-2">
                    <span>🎙️ தமிழில் பேசலாம்</span> • <span>📸 பத்திரத்தை படம் பிடித்து அனுப்பலாம்</span> • <span>📑 சட்டப்பூர்வ மனுவை பதிவிறக்கலாம்</span>
                </div>
            </div>
        </div>
    </main>

    <!-- Input Footer -->
    <footer class="w-full max-w-3xl bg-slate-900/90 backdrop-blur-md border border-slate-800 rounded-2xl p-2.5 shadow-2xl flex items-center space-x-2">
        <input id="userInput" type="text" placeholder="உங்கள் நிலம், பட்டா அல்லது அரசு சேவை பற்றி கேளுங்கள்..." 
               class="flex-1 bg-slate-950 border border-slate-800 text-slate-100 placeholder-slate-500 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition"
               onkeypress="handleKeyPress(event)">
        <button id="sendBtn" onclick="sendMessage()" 
                class="bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold px-5 py-3 rounded-xl transition shadow-lg shadow-emerald-500/20 flex items-center justify-center text-sm flex-shrink-0">
            அனுப்பு
        </button>
    </footer>

    <!-- Petition Modal -->
    <div id="petitionModal" class="hidden fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full shadow-2xl space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <h3 class="text-base font-bold text-emerald-400">📑 சட்டப்பூர்வ மனு தயாரிப்பு (Legal Petition PDF)</h3>
                <button onclick="closePetitionModal()" class="text-slate-400 hover:text-slate-200">✕</button>
            </div>
            <div class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-400 mb-1">மனுதாரர் பெயர் (Applicant Name):</label>
                    <input id="petName" type="text" value="ர. சுப்பிரமணியன்" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label class="block text-slate-400 mb-1">அலைபேசி (Phone):</label>
                        <input id="petPhone" type="text" value="9840012345" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1">மாவட்டம் (District):</label>
                        <input id="petDist" type="text" value="தஞ்சாவூர்" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label class="block text-slate-400 mb-1">வட்டம் (Taluk):</label>
                        <input id="petTaluk" type="text" value="கும்பகோணம்" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                    </div>
                    <div>
                        <label class="block text-slate-400 mb-1">கிராமம் (Village):</label>
                        <input id="petVillage" type="text" value="திருநாகேஸ்வரம்" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                    </div>
                </div>
                <div>
                    <label class="block text-slate-400 mb-1">விண்ணப்ப வகை (Service):</label>
                    <input id="petService" type="text" value="கிரய பட்டா பெயர் மாற்றம் (Patta Transfer)" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                </div>
                <div>
                    <label class="block text-slate-400 mb-1">புல எண் / சர்வே எண் (Survey No):</label>
                    <input id="petSurvey" type="text" value="142/3A" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">
                </div>
                <div>
                    <label class="block text-slate-400 mb-1">மனு விவரம் & கோரிக்கை (Grounds):</label>
                    <textarea id="petGrounds" rows="3" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-slate-200">மேற்படி சர்வே எண் கொண்ட நன்செய் நிலத்தை கிரய பத்திரம் எண் 1284/2024 மூலம் முறையாக வாங்கி பதிவு செய்துள்ளேன். இதற்குரிய கூட்டு பட்டாவில் இருந்து என் பெயரில் தனி பட்டா மாற்றம் செய்து உத்தரவிட வேண்டுகிறேன்.</textarea>
                </div>
            </div>
            <div class="flex justify-end gap-2 pt-2 border-t border-slate-800">
                <button onclick="closePetitionModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-medium">ரத்து</button>
                <button onclick="generateOfficialPetition()" class="px-5 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white rounded-xl text-xs font-bold shadow">📄 PDF மனு உருவாக்கு</button>
            </div>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chatBox');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const deepReasonToggle = document.getElementById('deepReasonToggle');
        let chatHistory = [];
        let mediaRecorder = null;
        let audioChunks = [];

        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }

        function sendQuickPrompt(text) {
            userInput.value = text;
            sendMessage();
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
                        use_deep_reasoning: isDeep
                    })
                });
                const data = await res.json();
                removeLoading(loadingId);

                if (data.status === 'success') {
                    appendMessage(data.reply, 'assistant', data.model_used);
                    chatHistory.push({ role: 'user', content: query });
                    chatHistory.push({ role: 'assistant', content: data.reply });
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
                    <div class="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-sm flex-shrink-0 mt-1">
                        🏛️
                    </div>
                    <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-4 max-w-[85%] text-slate-200 text-sm leading-relaxed shadow-md space-y-2">
                        <div class="markdown-body">${formatted}</div>
                        ${model ? `<div class="text-[10px] text-emerald-400/80 font-mono pt-1.5 border-t border-slate-800 flex items-center justify-between"><span>⚡ Meta Model: ${model}</span><span class="text-slate-500">Makkal Agent Action Loop</span></div>` : ''}
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
            const text = isDeep ? 'Meta muse-wonder ஆழ்ந்த சட்ட ஆய்வு செய்கிறது...' : 'Meta AI ஆய்வு செய்கிறது...';
            div.innerHTML = `
                <div class="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-sm flex-shrink-0">
                    🏛️
                </div>
                <div class="bg-slate-900 border border-slate-800 rounded-2xl rounded-tl-none p-3.5 text-slate-400 text-sm flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce"></span>
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.2s]"></span>
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.4s]"></span>
                    <span class="text-xs text-slate-400 pl-1">${text}</span>
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
                        vText.innerText = 'தமிழில் பேசுங்கள்';
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

                    appendMessage(`📸 **ஆவணம் சமர்ப்பிக்கப்பட்டது (${file.name}):**\n\n${data.audit_summary_ta}`, 'assistant', 'sam-3.1');
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
                    appendMessage(`🎉 **சட்டப்பூர்வ மனு தயாராகிவிட்டது!**\\n\\nஉங்களுடைய அதிகாரப்பூர்வ மனு PDF வடிவில் உருவாக்கப்பட்டுள்ளது. இதில் உங்கள் கையெழுத்தை இட்டு நேரடியாக வட்டாட்சியர் அலுவலகத்திலோ அல்லது இ-சேவை மையத்திலோ சமர்ப்பிக்கலாம்.\\n\\n👉 **[மனுவை பதிவிறக்கம் செய்ய இங்கே கிளிக் செய்யவும்](${data.download_url})**\\n\\n📌 *சரிபார்ப்பு எண் (Verification ID):* <code>${data.verification_id}</code>`, 'assistant', 'ActionExecutor');
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
    uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True)
