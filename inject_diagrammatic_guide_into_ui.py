# -*- coding: utf-8 -*-
"""
Injects the Universal Diagrammatic Visual Roadmap & Government Portal Guide
into sia_ui_template.py.
"""
import sys

def main():
    path = "D:/api/makkal-agent-ai/sia_ui_template.py"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    pod_html = '''
                <!-- 🗺️ UNIVERSAL DIAGRAMMATIC ROADMAP & GOVERNMENT PORTAL GUIDE POD -->
                <div class="bg-gradient-to-b from-slate-950 via-slate-900/95 to-indigo-950/25 border-2 border-indigo-500/50 rounded-3xl p-3.5 shadow-[0_15px_40px_-10px_rgba(0,0,0,0.85),0_0_30px_rgba(99,102,241,0.2)] relative overflow-hidden">
                    <div class="flex items-center justify-between border-b border-indigo-500/30 pb-2.5 mb-3">
                        <div class="flex items-center gap-2.5">
                            <span class="text-2xl p-1.5 bg-indigo-500/15 border border-indigo-500/30 rounded-2xl">🗺️</span>
                            <div>
                                <div class="text-xs sm:text-sm font-black text-white font-orbitron uppercase tracking-wider flex items-center gap-2">
                                    <span>Diagrammatic Knowledge & Exam Guide</span>
                                    <span class="text-[9px] font-mono bg-indigo-950 border border-indigo-500/60 text-indigo-300 px-2 py-0.2 rounded-full font-bold">ALL-INDIA & TN</span>
                                </div>
                                <div class="text-[10px] text-indigo-300">Grounding across tn.gov.in, TNeGA, TNPDS, TNPSC, NTA NEET, UPSC, IGNOU, TNOU & India.gov.in</div>
                            </div>
                        </div>
                        <span class="text-[9px] font-mono bg-emerald-950 border border-emerald-500/40 text-emerald-300 px-2 py-0.5 rounded-full font-bold">100% STATUTORY</span>
                    </div>

                    <!-- Voice & Text Query Input Bar -->
                    <div class="flex items-center gap-2 bg-[#0f172a] border border-indigo-500/40 rounded-2xl p-1.5 shadow-inner">
                        <button onclick="toggleDiagrammaticVoiceInput()" id="diagramVoiceBtn" title="Speak in Tamil" class="p-2 bg-slate-800 hover:bg-indigo-900 text-indigo-300 rounded-xl text-sm transition cursor-pointer flex items-center justify-center">
                            🎙️
                        </button>
                        <input id="diagrammaticQueryInput" type="text" placeholder="கேள்வி அல்லது திட்டத்தை தட்டச்சு செய்க... (எ.கா: TNPSC குரூப் 4, NEET 7.5%, வாரிசு சான்றிதழ், ரேஷன் கார்டு)" 
                               class="flex-1 bg-transparent border-none text-slate-100 placeholder-slate-500 text-xs sm:text-sm px-2 focus:outline-none"
                               onkeydown="if(event.key === 'Enter') executeDiagrammaticSolve()">
                        <button onclick="executeDiagrammaticSolve()" class="py-2 px-3.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-black text-xs rounded-xl transition cursor-pointer flex items-center gap-1.5 shadow">
                            <span>🔍 வழிகாட்டு</span>
                        </button>
                    </div>

                    <!-- 1-Click Topic Chips -->
                    <div class="mt-2.5 flex items-center gap-1.5 overflow-x-auto pb-1 custom-scroll">
                        <button onclick="executeDiagrammaticSolve('TNPSC குரூப் 4 மற்றும் VAO தேர்வு பாடத்திட்டம் தகுதி என்ன?')" class="whitespace-nowrap px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-indigo-500/30 text-indigo-200 rounded-lg text-[11px] font-bold cursor-pointer">🏛️ TNPSC குரூப் 4</button>
                        <button onclick="executeDiagrammaticSolve('NEET 7.5% அரசு பள்ளி இடஒதுக்கீடு விதிகள் என்ன?')" class="whitespace-nowrap px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-emerald-500/30 text-emerald-200 rounded-lg text-[11px] font-bold cursor-pointer">🩺 NEET 7.5% அரசு பள்ளி</button>
                        <button onclick="executeDiagrammaticSolve('UPSC சிவில் சர்வீசஸ் IAS IPS தேர்வு முறை')" class="whitespace-nowrap px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-cyan-500/30 text-cyan-200 rounded-lg text-[11px] font-bold cursor-pointer">🇮🇳 UPSC IAS / IPS</button>
                        <button onclick="executeDiagrammaticSolve('வாரிசுச் சான்றிதழ் Legal Heir பெற கட்டணம் ஆவணங்கள்')" class="whitespace-nowrap px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-amber-500/30 text-amber-200 rounded-lg text-[11px] font-bold cursor-pointer">📜 TNeGA வாரிசு சான்றிதழ்</button>
                        <button onclick="executeDiagrammaticSolve('ரேஷன் கார்டில் பிறந்த குழந்தை பெயர் சேர்க்கும் முறை')" class="whitespace-nowrap px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-teal-500/30 text-teal-200 rounded-lg text-[11px] font-bold cursor-pointer">🍚 TNPDS குழந்தை சேர்க்க</button>
                        <button onclick="executeDiagrammaticSolve('IGNOU தொலைதூர படிப்பு சேர்க்கை அசைன்மென்ட்')" class="whitespace-nowrap px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-purple-500/30 text-purple-200 rounded-lg text-[11px] font-bold cursor-pointer">🎓 IGNOU தொலைதூர கல்வி</button>
                        <button onclick="executeDiagrammaticSolve('PM கிசான் ₹6000 e-KYC உதவித்தொகை')" class="whitespace-nowrap px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-yellow-500/30 text-yellow-200 rounded-lg text-[11px] font-bold cursor-pointer">🌾 PM-KISAN & விஸ்வகர்மா</button>
                        <button onclick="executeDiagrammaticSolve('செல்வமகள் சேமிப்புத் திட்டம் Sukanya 8.2% வட்டி')" class="whitespace-nowrap px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-pink-500/30 text-pink-200 rounded-lg text-[11px] font-bold cursor-pointer">👧 செல்வமகள் சேமிப்பு</button>
                    </div>

                    <!-- Dynamic Diagrammatic Result Container -->
                    <div id="diagrammaticResultContainer" class="mt-3 bg-[#020617] border border-slate-800 rounded-2xl p-3 shadow-inner">
                        <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-2">
                            <div>
                                <h4 id="diagramTitleTa" class="text-xs sm:text-sm font-black text-emerald-300">🏛️ TNPSC குரூப் 4 & VAO தேர்வு முழுமையான வரைபட வழிகாட்டி</h4>
                                <p id="diagramTitleEn" class="text-[10px] text-slate-400 font-mono">TNPSC Group 4 & VAO Interactive Roadmap Guide</p>
                            </div>
                            <a id="diagramPortalLink" href="https://www.tnpsc.gov.in" target="_blank" class="px-2.5 py-1 bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-400 text-indigo-200 rounded-xl text-[10px] font-bold transition flex items-center gap-1 cursor-pointer">
                                <span>🌐 tnpsc.gov.in</span> <span>↗</span>
                            </a>
                        </div>

                        <!-- Statutory Fee Alert -->
                        <div id="diagramFeeBox" class="bg-emerald-950/40 border border-emerald-500/40 rounded-xl p-2 mb-3 text-[11px] text-emerald-200 flex items-center justify-between">
                            <span id="diagramFeeText">💰 விண்ணப்பக் கட்டணம்: ₹100 மட்டுமே | OTR பதிவு: ₹150 (5 ஆண்டுகள் செல்லுபடியாகும்)</span>
                            <span id="diagramExemptionText" class="text-[9px] bg-emerald-900/60 px-1.5 py-0.5 rounded text-emerald-300 font-bold">SC/ST/விதவை ₹0 இலவசம்</span>
                        </div>

                        <!-- 🗺️ Interactive Step-by-Step Visual Flowchart -->
                        <div class="mb-3">
                            <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">🗺️ அதிகாரப்பூர்வ வரைபட நடைமுறை (Step-by-Step Visual Flow):</div>
                            <div id="diagramStepsFlow" class="grid grid-cols-1 sm:grid-cols-5 gap-2">
                                <div class="bg-slate-900 border border-indigo-500/40 rounded-xl p-2 relative shadow">
                                    <div class="flex items-center justify-between mb-1">
                                        <span class="text-[10px] font-black text-indigo-300">1. கல்வித் தகுதி</span>
                                        <span class="text-[8px] bg-indigo-950 border border-indigo-500/40 text-indigo-300 px-1 rounded">கட்டாயம்</span>
                                    </div>
                                    <p class="text-[10px] text-slate-300 leading-tight">10-ம் வகுப்பு தேர்ச்சி (SSLC Pass) குறைந்தபட்சம் போதுமானது.</p>
                                </div>
                                <div class="bg-slate-900 border border-indigo-500/40 rounded-xl p-2 relative shadow">
                                    <div class="flex items-center justify-between mb-1">
                                        <span class="text-[10px] font-black text-indigo-300">2. OTR பதிவு</span>
                                        <span class="text-[8px] bg-indigo-950 border border-indigo-500/40 text-indigo-300 px-1 rounded">5 ஆண்டுகள்</span>
                                    </div>
                                    <p class="text-[10px] text-slate-300 leading-tight">tnpscexams.in தளத்தில் ஆதார், 10-ம் வகுப்பு சான்றிதழுடன் பதிவு.</p>
                                </div>
                                <div class="bg-slate-900 border border-indigo-500/40 rounded-xl p-2 relative shadow">
                                    <div class="flex items-center justify-between mb-1">
                                        <span class="text-[10px] font-black text-emerald-300">3. பகுதி-A தமிழ்</span>
                                        <span class="text-[8px] bg-emerald-950 border border-emerald-500/40 text-emerald-300 px-1 rounded">40% Cut-off</span>
                                    </div>
                                    <p class="text-[10px] text-slate-300 leading-tight">100 வினாக்கள் (150 மதிப்பெண்கள்). 40% கட்டாயம் தேர்ச்சி பெற வேண்டும்.</p>
                                </div>
                                <div class="bg-slate-900 border border-indigo-500/40 rounded-xl p-2 relative shadow">
                                    <div class="flex items-center justify-between mb-1">
                                        <span class="text-[10px] font-black text-indigo-300">4. பகுதி-B GS & Apt</span>
                                        <span class="text-[8px] bg-indigo-950 border border-indigo-500/40 text-indigo-300 px-1 rounded">3 மணி நேரம்</span>
                                    </div>
                                    <p class="text-[10px] text-slate-300 leading-tight">பொது அறிவு 75 வினாக்கள் + ஆப்டிடியூட் 25 வினாக்கள் (150 மதிப்பெண்கள்).</p>
                                </div>
                                <div class="bg-slate-900 border border-indigo-500/40 rounded-xl p-2 relative shadow">
                                    <div class="flex items-center justify-between mb-1">
                                        <span class="text-[10px] font-black text-cyan-300">5. நேரடி நியமனம்</span>
                                        <span class="text-[8px] bg-cyan-950 border border-cyan-500/40 text-cyan-300 px-1 rounded">நேர்காணல் இல்லை</span>
                                    </div>
                                    <p class="text-[10px] text-slate-300 leading-tight">மதிப்பெண் அடிப்படையில் சான்றிதழ் சரிபார்ப்பு மூலம் பணி ஆணை.</p>
                                </div>
                            </div>
                        </div>

                        <!-- Documents & Action Footer -->
                        <div class="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800">
                            <div class="flex items-center gap-1.5">
                                <button onclick="speakCurrentDiagramGuide()" class="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-indigo-300 border border-indigo-500/30 rounded-xl text-xs font-bold transition flex items-center gap-1 cursor-pointer">
                                    <span>🔊 தமிழில் கேட்க</span>
                                </button>
                                <button onclick="pushCurrentDiagramGuideToWhatsApp()" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-black transition flex items-center gap-1 cursor-pointer shadow">
                                    <span>📱 வாட்ஸ்அப்பிற்கு அனுப்புக</span>
                                </button>
                            </div>
                            <span class="text-[9px] font-mono text-slate-400">Meta AI Multi-Model Grounded • Zero Hallucination</span>
                        </div>
                    </div>
                </div>
'''

    hook_right_wing = '<!-- 🎯 4 Core Citizen Access Points (Holographic Glass Cards) -->'
    if "<!-- 🗺️ UNIVERSAL DIAGRAMMATIC ROADMAP & GOVERNMENT PORTAL GUIDE POD -->" not in html:
        html = html.replace(hook_right_wing, pod_html + "\n\n                " + hook_right_wing, 1)
        print("Injected Universal Diagrammatic Roadmap Guide Pod into Right Wing")

    # JavaScript Controller for Diagrammatic Guide
    js_code = '''
        // =====================================================================
        // 🗺️ DIAGRAMMATIC ROADMAP & GOVERNMENT PORTAL GUIDE CONTROLLER
        // =====================================================================
        let currentDiagramData = null;

        async function executeDiagrammaticSolve(presetQuery) {
            const inp = document.getElementById('diagrammaticQueryInput');
            const query = presetQuery || (inp ? inp.value.trim() : '');
            if (!query) return;

            if (inp && presetQuery) inp.value = presetQuery;
            showAuthBanner(`🔍 Meta AI ஆய்வு செய்கிறது: ${query.slice(0, 35)}...`);

            try {
                const res = await fetch('/api/guide/diagrammatic-solve', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        query: query,
                        phone: (currentUser && currentUser.phone) ? currentUser.phone : '6381029380'
                    })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    currentDiagramData = data;
                    renderDiagrammaticResult(data);
                    showAuthBanner(`✅ வரைபட வழிகாட்டல் தயாரானது!`);
                }
            } catch(e) {
                console.error('Failed to solve diagrammatic guide:', e);
            }
        }

        function renderDiagrammaticResult(data) {
            const titleTa = document.getElementById('diagramTitleTa');
            const titleEn = document.getElementById('diagramTitleEn');
            const portalLink = document.getElementById('diagramPortalLink');
            const feeText = document.getElementById('diagramFeeText');
            const exempText = document.getElementById('diagramExemptionText');
            const stepsFlow = document.getElementById('diagramStepsFlow');

            if (titleTa) titleTa.innerText = data.title_ta || 'வழிகாட்டி';
            if (titleEn) titleEn.innerText = data.title_en || '';
            if (portalLink && data.portal_url) {
                portalLink.href = data.portal_url;
                portalLink.innerHTML = `<span>🌐 ${escapeHtml(data.portal_name || 'Portal')}</span> <span>↗</span>`;
            }
            if (feeText) feeText.innerText = data.statutory_fee_text || 'சட்டப்பூர்வ கட்டணம் சரிபார்க்கப்பட்டது.';
            if (exempText) exempText.innerText = data.exemption_note || 'அரசு விதிமுறைகள்';

            if (stepsFlow && data.roadmap_steps) {
                stepsFlow.innerHTML = '';
                const colsClass = (data.roadmap_steps.length >= 5) ? 'sm:grid-cols-5' : `sm:grid-cols-${data.roadmap_steps.length}`;
                stepsFlow.className = `grid grid-cols-1 ${colsClass} gap-2`;

                data.roadmap_steps.forEach((st, idx) => {
                    const stepDiv = document.createElement('div');
                    stepDiv.className = 'bg-slate-900 border border-indigo-500/40 rounded-xl p-2 relative shadow animate-fade-in';
                    stepDiv.innerHTML = `
                        <div class="flex items-center justify-between mb-1">
                            <span class="text-[10px] font-black text-indigo-300">${st.step}. ${escapeHtml(st.title || '')}</span>
                            <span class="text-[8px] bg-indigo-950 border border-indigo-500/40 text-indigo-300 px-1 rounded">${escapeHtml(st.badge || '')}</span>
                        </div>
                        <p class="text-[10px] text-slate-300 leading-tight">${escapeHtml(st.detail || '')}</p>
                    `;
                    stepsFlow.appendChild(stepDiv);
                });
            }
        }

        async function pushCurrentDiagramGuideToWhatsApp() {
            if (!currentDiagramData || !currentDiagramData.whatsapp_push_text) {
                alert('முதலில் ஒரு வழிகாட்டியைத் தேர்ந்தெடுக்கவும்.');
                return;
            }
            const phone = (currentUser && currentUser.phone) ? currentUser.phone : '6381029380';
            showAuthBanner(`📱 வாட்ஸ்அப்பிற்கு வழிகாட்டல் அனுப்பப்படுகிறது (+${phone})...`);

            try {
                const res = await fetch('/api/guide/push-to-whatsapp', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        phone: phone,
                        whatsapp_text: currentDiagramData.whatsapp_push_text
                    })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    showAuthBanner('✅ வாட்ஸ்அப் அரட்டைக்கு வழிகாட்டல் அனுப்பப்பட்டுவிட்டது!');
                }
            } catch(e) {
                console.error('Failed to push to WhatsApp:', e);
            }
        }

        function speakCurrentDiagramGuide() {
            if (!currentDiagramData || !currentDiagramData.audio_tts_text) return;
            if (!('speechSynthesis' in window)) {
                alert('உங்கள் உலாவியில் பேச்சு வசதி ஆதரிக்கப்படவில்லை.');
                return;
            }
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(currentDiagramData.audio_tts_text);
            utterance.lang = 'ta-IN';
            utterance.rate = 0.95;
            window.speechSynthesis.speak(utterance);
            showAuthBanner('🔊 தமிழில் வாசிக்கப்படுகிறது...');
        }

        function toggleDiagrammaticVoiceInput() {
            if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
                alert('தயவுசெய்து Chrome உலாவியைப் பயன்படுத்தவும் (Voice Input)');
                return;
            }
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognizer = new SpeechRec();
            recognizer.lang = 'ta-IN';
            recognizer.interimResults = false;

            const btn = document.getElementById('diagramVoiceBtn');
            if (btn) btn.classList.add('animate-pulse', 'bg-rose-600', 'text-white');
            showAuthBanner('🎙️ பேசவும்... (தமிழ் பேச்சு உள்ளீடு)');

            recognizer.onresult = function(e) {
                if (btn) btn.classList.remove('animate-pulse', 'bg-rose-600', 'text-white');
                const spoken = e.results[0][0].transcript;
                const inp = document.getElementById('diagrammaticQueryInput');
                if (inp) inp.value = spoken;
                executeDiagrammaticSolve(spoken);
            };

            recognizer.onerror = function() {
                if (btn) btn.classList.remove('animate-pulse', 'bg-rose-600', 'text-white');
            };

            recognizer.start();
        }
'''

    if "// 🗺️ DIAGRAMMATIC ROADMAP & GOVERNMENT PORTAL GUIDE CONTROLLER" not in html:
        hook_script = "</script>\n</body>"
        html = html.replace(hook_script, js_code + "\n\n    " + hook_script, 1)
        print("Injected Diagrammatic Guide JavaScript Controller")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("SUCCESS: sia_ui_template.py upgraded with Diagrammatic Guide!")

if __name__ == "__main__":
    main()
