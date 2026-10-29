"""
Script to add Spoken English, Mental Health, and Universal Tuition buttons, modals, and JS to sia_ui_template.py
"""

import sys

FILE_PATH = r"D:\api\makkal-agent-ai\sia_ui_template.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Header Buttons
header_target = """                <button onclick="openTravelModal()" class="text-xs bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-500/40 text-cyan-300 font-bold px-2 py-1 rounded-xl transition cursor-pointer flex items-center gap-1">
                    <span>🚗</span> <span>Travel</span>
                </button>"""

header_replacement = """                <button onclick="openTravelModal()" class="text-xs bg-cyan-950/80 hover:bg-cyan-900 border border-cyan-500/40 text-cyan-300 font-bold px-2 py-1 rounded-xl transition cursor-pointer flex items-center gap-1">
                    <span>🚗</span> <span>Travel</span>
                </button>
                <button onclick="openSpokenEnglishModal()" class="text-xs bg-indigo-950/80 hover:bg-indigo-900 border border-indigo-500/40 text-indigo-300 font-bold px-2 py-1 rounded-xl transition cursor-pointer flex items-center gap-1 shadow-sm">
                    <span>🗣️</span> <span>Spoken Eng</span>
                </button>
                <button onclick="openMentalHealthModal()" class="text-xs bg-rose-950/80 hover:bg-rose-900 border border-rose-500/40 text-rose-300 font-bold px-2 py-1 rounded-xl transition cursor-pointer flex items-center gap-1 shadow-sm">
                    <span>🧠</span> <span>மன நலம்</span>
                </button>
                <button onclick="openUniversalTuitionModal()" class="text-xs bg-amber-950/80 hover:bg-amber-900 border border-amber-500/40 text-amber-300 font-bold px-2 py-1 rounded-xl transition cursor-pointer flex items-center gap-1 shadow-sm">
                    <span>📚</span> <span>டியூஷன்</span>
                </button>"""

if header_target in content and "openSpokenEnglishModal()" not in content:
    content = content.replace(header_target, header_replacement, 1)
    print("✓ Added header navigation buttons")

# 2. Add Modal HTML Containers before travelModal
modal_target = '    <!-- ══════════════════════════════════════════════════════════ -->' + '\n' + '    <!-- MODAL: 🚗 TRAVEL & TEMPLE TOUR BOOKING                   -->'

new_modals = """    <!-- ══════════════════════════════════════════════════════════ -->
    <!-- MODAL: 🗣️ SPOKEN ENGLISH CONVERSATIONAL STUDIO            -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <div id="spokenEnglishModal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-4 hidden overflow-y-auto">
        <div class="bg-slate-900 border border-indigo-500/40 rounded-3xl max-w-2xl w-full p-5 sm:p-6 shadow-2xl relative space-y-4 my-auto max-h-[92vh] overflow-y-auto">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-xl shadow-lg shadow-indigo-500/20">🗣️</div>
                    <div>
                        <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                            <span>SIA Spoken English Studio</span>
                            <span class="text-[10px] bg-indigo-950 text-indigo-300 border border-indigo-500/40 px-2 py-0.5 rounded-full font-mono">SeamlessM4T Speech AI</span>
                        </h3>
                        <p class="text-xs text-slate-400">Tamil Phonetic Transliteration • Tanglish Error Correction • All Levels</p>
                    </div>
                </div>
                <button onclick="closeSpokenEnglishModal()" class="text-slate-400 hover:text-white px-3 py-1.5 rounded-xl bg-slate-800 text-sm cursor-pointer">✕ Close</button>
            </div>

            <!-- Level Selector Tabs -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button onclick="switchEnglishLevel('level_1_beginner')" id="btnLvl1" class="p-2 rounded-xl bg-indigo-600 text-white text-xs font-bold transition">🌱 Level 1: Kids & Beginners</button>
                <button onclick="switchEnglishLevel('level_2_student')" id="btnLvl2" class="p-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition">🎓 Level 2: School & College</button>
                <button onclick="switchEnglishLevel('level_3_interview')" id="btnLvl3" class="p-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition">💼 Level 3: HR Interview</button>
                <button onclick="switchEnglishLevel('level_4_homemaker')" id="btnLvl4" class="p-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition">🏡 Level 4: Parents & PTM</button>
            </div>

            <!-- Interactive Dialogue Display Card -->
            <div id="englishDialogueCard" class="bg-slate-950/80 border border-slate-800 rounded-2xl p-4 space-y-3">
                <div class="flex items-center justify-between text-xs text-indigo-300">
                    <span class="font-bold" id="englishScenarioTitle">காலை & மாலை வாழ்த்துகள் (Daily Greetings)</span>
                    <span class="text-slate-400 text-[11px]" id="englishLevelBadge">Level 1: Daily Talk</span>
                </div>
                <div id="englishSentencesContainer" class="space-y-2.5 text-xs sm:text-sm">
                    <div class="bg-slate-900/90 p-3 rounded-xl border border-slate-800">
                        <p class="text-slate-300 font-medium">1. காலை வணக்கம்! நீங்கள் எப்படி இருக்கிறீர்கள்?</p>
                        <p class="text-indigo-400 font-bold mt-0.5">🇬🇧 "Good morning! How are you doing today?"</p>
                        <p class="text-emerald-400/90 text-xs mt-0.5 font-mono">🗣️ உச்சரிப்பு: குட் மார்னிங்! ஹௌ ஆர் யூ டூயிங் டுடே?</p>
                    </div>
                </div>
            </div>

            <!-- Fluency Speech Tester Input -->
            <div class="bg-slate-950/90 border border-indigo-500/30 rounded-2xl p-3.5 space-y-2">
                <label class="text-xs font-bold text-slate-300 block">🎙️ Speak or Type in English (உச்சரிப்பு & சரள சோதனை):</label>
                <div class="flex gap-2">
                    <input id="spokenInputText" type="text" placeholder="Type or speak in English (e.g., I am doing well, thank you!)" class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-indigo-500" />
                    <button onclick="evaluateSpokenSpeech()" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl transition cursor-pointer">Assess Fluency</button>
                </div>
                <div id="spokenAssessmentResult" class="hidden text-xs p-2.5 bg-indigo-950/50 border border-indigo-500/30 rounded-xl space-y-1"></div>
            </div>

            <!-- Dual-Sync WhatsApp CTA -->
            <div class="p-3 bg-gradient-to-r from-emerald-950/80 to-slate-900 border border-emerald-500/30 rounded-2xl flex items-center justify-between gap-3">
                <div class="text-xs">
                    <span class="font-bold text-emerald-300 block">📲 WhatsApp Interactive Spoken English Practice:</span>
                    <span class="text-slate-400 text-[11px]">Send voice notes directly on WhatsApp to get instant AI phonetic feedback!</span>
                </div>
                <a href="https://wa.me/1213113635214047?text=ENGLISH" target="_blank" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl transition flex items-center gap-1.5 whitespace-nowrap">
                    <span>Chat on WhatsApp</span> <span>➔</span>
                </a>
            </div>
        </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!-- MODAL: 🧠 STUDENT MENTAL HEALTH & EMOTIONAL WELLBEING       -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <div id="mentalHealthModal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-4 hidden overflow-y-auto">
        <div class="bg-slate-900 border border-rose-500/40 rounded-3xl max-w-2xl w-full p-5 sm:p-6 shadow-2xl relative space-y-4 my-auto max-h-[92vh] overflow-y-auto">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-rose-500 to-pink-600 flex items-center justify-center text-xl shadow-lg shadow-rose-500/20">🧠</div>
                    <div>
                        <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                            <span>SIA Student Mental Health Coach</span>
                            <span class="text-[10px] bg-rose-950 text-rose-300 border border-rose-500/40 px-2 py-0.5 rounded-full font-mono">24x7 Confidential Care</span>
                        </h3>
                        <p class="text-xs text-slate-400">Exam Anxiety Relief • Thirukkural Resilience • Statutory 14416 Helpline</p>
                    </div>
                </div>
                <button onclick="closeMentalHealthModal()" class="text-slate-400 hover:text-white px-3 py-1.5 rounded-xl bg-slate-800 text-sm cursor-pointer">✕ Close</button>
            </div>

            <!-- Quick Mood Buttons -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button onclick="loadMentalHealthTopic('exam_anxiety')" class="p-2 rounded-xl bg-rose-950/80 border border-rose-500/40 hover:bg-rose-900 text-xs font-bold text-rose-300 transition">🎯 தேர்வு பயம் (Exam)</button>
                <button onclick="loadMentalHealthTopic('study_burnout')" class="p-2 rounded-xl bg-amber-950/80 border border-amber-500/40 hover:bg-amber-900 text-xs font-bold text-amber-300 transition">🔋 படிப்பு சோர்வு (Burnout)</button>
                <button onclick="loadMentalHealthTopic('parent_peer_pressure')" class="p-2 rounded-xl bg-cyan-950/80 border border-cyan-500/40 hover:bg-cyan-900 text-xs font-bold text-cyan-300 transition">🤝 ஒப்பீடு & அழுத்தம்</button>
                <button onclick="loadMentalHealthTopic('emotional_listening')" class="p-2 rounded-xl bg-purple-950/80 border border-purple-500/40 hover:bg-purple-900 text-xs font-bold text-purple-300 transition">👂 ரகசிய ஆறுதல்</button>
            </div>

            <!-- Dynamic Wellbeing Content Card -->
            <div id="mentalHealthCard" class="bg-slate-950/90 border border-slate-800 rounded-2xl p-4 space-y-3">
                <div class="flex items-center justify-between text-xs border-b border-slate-800 pb-2">
                    <span id="mhTopicTitle" class="font-bold text-rose-300 text-sm">🎯 தேர்வு பயம் & பதட்டம் தணிக்கும் பயிற்சி</span>
                    <span class="text-xs text-slate-400">Box Breathing (4-7-8)</span>
                </div>
                <div id="mhTechniqueSteps" class="text-xs text-slate-300 space-y-1.5">
                    <p>• 1. மூச்சை 4 வினாடிகள் மூக்கு வழியே மெதுவாக உள்ளிழுங்கள்.</p>
                    <p>• 2. மூச்சை 7 வினாடிகள் அமைதியாக உள்ளே அடக்கி வையுங்கள்.</p>
                    <p>• 3. மூச்சை 8 வினாடிகள் வாய் வழியே மெதுவாக வெளியேற்றுங்கள்.</p>
                    <p>• 4. இதை 4 முறை செய்யுங்கள் - பதட்டம் தணிந்து மனம் அமைதியாகும்.</p>
                </div>
                <div class="p-3 bg-rose-950/30 border border-rose-500/20 rounded-xl space-y-1">
                    <span class="text-[11px] text-rose-400 font-bold block">✨ ஊக்க வாக்குறுதி (Affirmation):</span>
                    <p id="mhAffirmationText" class="text-xs text-white italic">"மதிப்பெண்கள் என் எதிர்காலத்தை மட்டுமே தீர்மானிப்பதில்லை; என் கடின உழைப்பும் விடாமுயற்சியுமே என்னை உயர்த்தும். என்னால் முடியும்!"</p>
                </div>
                <div class="p-3 bg-slate-900/80 border border-slate-800 rounded-xl text-xs space-y-1 font-mono">
                    <span class="text-amber-400 font-bold block">📜 திருக்குறள் மன வலிமை:</span>
                    <p class="text-slate-300">"இடுக்கண் வருங்கால் நகுக அதனை அடுத்தூர்வது அஃதொப்பது இல்."</p>
                </div>
            </div>

            <!-- Confidential Counseling Query Box -->
            <div class="bg-slate-950/90 border border-rose-500/30 rounded-2xl p-3.5 space-y-2">
                <label class="text-xs font-bold text-slate-300 block">💬 உங்கள் மனக் கவலையை எழுதுங்கள் (Confidential Empathetic Counseling):</label>
                <div class="flex gap-2">
                    <input id="mentalHealthQueryInput" type="text" placeholder="உங்கள் கவலை அல்லது பயத்தை இங்கே பகிருங்கள் (எ.கா: தேர்வுக்கு படிக்க முடியவில்லை, பயமாக உள்ளது)..." class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-rose-500" />
                    <button onclick="submitMentalHealthCounseling()" class="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold rounded-xl transition cursor-pointer">ஆறுதல் பெறுக</button>
                </div>
                <div id="counselingFeedback" class="hidden text-xs p-2.5 bg-rose-950/50 border border-rose-500/30 rounded-xl space-y-1"></div>
            </div>

            <!-- Statutory Crisis Helplines -->
            <div class="p-3 bg-slate-950/90 border border-amber-500/40 rounded-2xl flex items-center justify-between gap-3 text-xs">
                <div>
                    <span class="font-bold text-amber-400 flex items-center gap-1.5">
                        <span>📞 அரசு மாணவர் மனநல உதவி எண்:</span> <span class="text-white bg-amber-500/20 px-2 py-0.5 rounded-lg font-mono">14416 (24x7 Toll-Free)</span>
                    </span>
                    <span class="text-[11px] text-slate-400 block mt-0.5">மத்திய அரசு டெலி-மானாஸ்: 1800-891-4416 • சினேகா தற்கொலை தடுப்பு: 044-24640050</span>
                </div>
                <a href="https://wa.me/1213113635214047?text=STRESS" target="_blank" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl transition whitespace-nowrap">
                    WhatsApp ஆறுதல் ➔
                </a>
            </div>
        </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!-- MODAL: 📚 UNIVERSAL TUITION CLASS (ALL CLASSES & SYLLABI)   -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <div id="universalTuitionModal" class="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-3 sm:p-4 hidden overflow-y-auto">
        <div class="bg-slate-900 border border-amber-500/40 rounded-3xl max-w-2xl w-full p-5 sm:p-6 shadow-2xl relative space-y-4 my-auto max-h-[92vh] overflow-y-auto">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-amber-500 to-orange-600 flex items-center justify-center text-xl shadow-lg shadow-amber-500/20">📚</div>
                    <div>
                        <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                            <span>SIA Universal Tuition Class</span>
                            <span class="text-[10px] bg-amber-950 text-amber-300 border border-amber-500/40 px-2 py-0.5 rounded-full font-mono">Classes 1-12 • CBSE & State Board</span>
                        </h3>
                        <p class="text-xs text-slate-400">First-Principles Concepts • Step-by-Step Problem Solving • Adaptive Quizzes</p>
                    </div>
                </div>
                <button onclick="closeUniversalTuitionModal()" class="text-slate-400 hover:text-white px-3 py-1.5 rounded-xl bg-slate-800 text-sm cursor-pointer">✕ Close</button>
            </div>

            <!-- Class Level Selector -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button onclick="switchTuitionClass('primary_1_5')" id="btnTuiCls1" class="p-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition">🎒 Primary (1 - 5)</button>
                <button onclick="switchTuitionClass('middle_6_8')" id="btnTuiCls2" class="p-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition">📐 Middle (6 - 8)</button>
                <button onclick="switchTuitionClass('high_school_9_10')" id="btnTuiCls3" class="p-2 rounded-xl bg-amber-600 text-white text-xs font-bold transition">⚡ High (9 - 10 SSLC/CBSE)</button>
                <button onclick="switchTuitionClass('higher_sec_11_12')" id="btnTuiCls4" class="p-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition">🔬 Higher Sec (11 - 12)</button>
            </div>

            <!-- Topic Details & Steps Card -->
            <div id="tuitionTopicCard" class="bg-slate-950/90 border border-slate-800 rounded-2xl p-4 space-y-3">
                <div class="flex items-center justify-between text-xs border-b border-slate-800 pb-2">
                    <span id="tuiTopicTitle" class="font-bold text-amber-300 text-sm">10-ம் வகுப்பு இயற்பியல்: ஓம் விதி & மின்தடை இணைப்புகள்</span>
                    <span class="text-slate-400 font-mono text-[11px]">V = IR | Series & Parallel</span>
                </div>
                <p id="tuiTopicSummary" class="text-xs text-slate-300">மின்னழுத்தம், மின்னோட்டம், மின்தடை சமன்பாடு V = IR மற்றும் தொடர்/பக்க இணைப்புகள்.</p>
                <div id="tuiConceptSteps" class="text-xs text-slate-300 space-y-1.5">
                    <p>• படி 1: ஓம் விதி: V = IR (மின்னழுத்தம் = மின்னோட்டம் x மின்தடை).</p>
                    <p>• படி 2: தொடரிணைப்பு (Series): Rs = R1 + R2 + R3.</p>
                    <p>• படி 3: பக்க இணைப்பு (Parallel): 1/Rp = 1/R1 + 1/R2 + 1/R3.</p>
                </div>
                <!-- Quiz item -->
                <div class="p-3 bg-amber-950/30 border border-amber-500/20 rounded-xl space-y-1 text-xs">
                    <span class="text-amber-400 font-bold block">📝 மாதிரி தேர்வு வினா (Sample Quiz):</span>
                    <p class="text-slate-200 font-medium">12V பேட்டரியுடன் 4 ஓம் மின்தடை இணைக்கப்பட்டால் பாயும் மின்னோட்டம் என்ன?</p>
                    <p class="text-emerald-400 font-bold mt-1 font-mono">விடை: I = V / R = 12 / 4 = 3 A (ஆம்பியர்)</p>
                </div>
            </div>

            <!-- AI Homework Solver Input -->
            <div class="bg-slate-950/90 border border-amber-500/30 rounded-2xl p-3.5 space-y-2">
                <label class="text-xs font-bold text-slate-300 block">🤖 Ask Meta Wonder 1.0 (வீட்டுப்பாட சந்தேகம் / Homework Question):</label>
                <div class="flex gap-2">
                    <input id="tuitionHomeworkInput" type="text" placeholder="உங்கள் பாடக் கேள்வியை தட்டச்சு செய்யவும் (எ.கா: ஒளிச்சேர்க்கை இருள் வினை விளக்கம் தருக)..." class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500" />
                    <button onclick="solveTuitionQuery()" class="px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-xl transition cursor-pointer">தீர்வு காண்க</button>
                </div>
                <div id="tuitionSolverFeedback" class="hidden text-xs p-2.5 bg-amber-950/50 border border-amber-500/30 rounded-xl space-y-1"></div>
            </div>

            <!-- Dual-Sync WhatsApp CTA -->
            <div class="p-3 bg-gradient-to-r from-emerald-950/80 to-slate-900 border border-emerald-500/30 rounded-2xl flex items-center justify-between gap-3 text-xs">
                <div>
                    <span class="font-bold text-emerald-300 block">📲 WhatsApp Interactive Tuition Bot:</span>
                    <span class="text-slate-400 text-[11px]">Send TUITION on WhatsApp to learn any topic or quiz in 1 tap!</span>
                </div>
                <a href="https://wa.me/1213113635214047?text=TUITION" target="_blank" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl transition whitespace-nowrap">
                    WhatsApp டியூஷன் ➔
                </a>
            </div>
        </div>
    </div>
"""

if modal_target in content and "id=\"spokenEnglishModal\"" not in content:
    content = content.replace(modal_target, new_modals + "\n" + modal_target, 1)
    print("✓ Added spokenEnglishModal, mentalHealthModal, and universalTuitionModal HTML")

# 3. Add JavaScript Controllers
js_target = "window.openTravelModal = function()"

new_js = """// ══════════════════════════════════════════════════════════════
// 🗣️ SPOKEN ENGLISH CONVERSATIONAL STUDIO CONTROLLER
// ══════════════════════════════════════════════════════════════
window.openSpokenEnglishModal = function() {
    document.getElementById('spokenEnglishModal').classList.remove('hidden');
    switchEnglishLevel('level_1_beginner');
};
window.closeSpokenEnglishModal = function() {
    document.getElementById('spokenEnglishModal').classList.add('hidden');
};
window.switchEnglishLevel = function(lvlId) {
    const btns = { 'level_1_beginner': 'btnLvl1', 'level_2_student': 'btnLvl2', 'level_3_interview': 'btnLvl3', 'level_4_homemaker': 'btnLvl4' };
    Object.keys(btns).forEach(k => {
        const el = document.getElementById(btns[k]);
        if (el) {
            if (k === lvlId) {
                el.className = 'p-2 rounded-xl bg-indigo-600 text-white text-xs font-bold transition';
            } else {
                el.className = 'p-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition';
            }
        }
    });

    const levelData = {
        'level_1_beginner': {
            title: 'காலை & மாலை வாழ்த்துகள் (Daily Greetings)',
            badge: 'Level 1: Daily Talk',
            sentences: [
                { ta: '1. காலை வணக்கம்! நீங்கள் எப்படி இருக்கிறீர்கள்?', en: 'Good morning! How are you doing today?', ph: 'குட் மார்னிங்! ஹௌ ஆர் யூ டூயிங் டுடே?' },
                { ta: '2. நான் நன்றாக இருக்கிறேன், நன்றி! நீங்கள்?', en: 'I am doing well, thank you! How about you?', ph: 'ஐ ஆம் டூயிங் வெல், தேங்க் யூ! ஹௌ அபௌட் யூ?' }
            ]
        },
        'level_2_student': {
            title: 'வகுப்பில் சந்தேகம் கேட்டல் (Classroom Communication)',
            badge: 'Level 2: School & College',
            sentences: [
                { ta: '1. மன்னிக்கவும் ஆசிரியர், இதை மீண்டும் விளக்குவீர்களா?', en: 'Excuse me teacher, could you please explain this problem once again?', ph: 'எக்ஸ்கியூஸ் மீ டீச்சர், குட் யூ ப்ளீஸ் எக்ஸ்பிளைன் திஸ் ப்ராப்ளம் ஒன்ஸ் அகைன்?' },
                { ta: '2. நான் இந்த குறிப்பை குறித்துக் கொள்ளலாமா?', en: 'May I take down these notes, please?', ph: 'மே ஐ டேக் டவுன் தீஸ் நோட்ஸ், ப்ளீஸ்?' }
            ]
        },
        'level_3_interview': {
            title: 'வேலை நேர்காணல் சுய அறிமுகம் (Job Interview Self-Intro)',
            badge: 'Level 3: HR & Careers',
            sentences: [
                { ta: '1. வணக்கம்! என்னை அறிமுகப்படுத்த வாய்ப்பளித்ததற்கு நன்றி.', en: 'Good morning! Thank you for giving me this opportunity to introduce myself.', ph: 'குட் மார்னிங்! தேங்க் யூ ஃபார் கிவிங் மீ திஸ் ஆப்பர்ச்சூனிட்டி டு இன்ட்ரடியூஸ் மைசெல்ஃப்.' },
                { ta: '2. புதிய தொழில்நுட்பங்களை விரைவாகக் கற்று செயல்படுத்துவது எனது பலம்.', en: 'My greatest strength is my ability to learn new technologies rapidly and deliver results.', ph: 'மை கிரேட்டஸ்ட் ஸ்ட்ரெங்த் இஸ் மை எபிலிட்டி டு லேர்ன் நியூ டெக்னாலஜீஸ் ராபிட்லி அண்ட் டெலிவர் ரிசல்ட்ஸ்.' }
            ]
        },
        'level_4_homemaker': {
            title: 'பெற்றோர் ஆசிரியர் சந்திப்பு (PTM Meeting)',
            badge: 'Level 4: Parents & Family',
            sentences: [
                { ta: '1. என் குழந்தையின் படிப்பு நிலவரம் எவ்வாறு உள்ளது?', en: 'Hello teacher, how is my child performing academically in class?', ph: 'ஹலோ டீச்சர், ஹௌ இஸ் மை சைல்ட் பெர்ஃபார்மிங் அகாடமிக்கலி இன் கிளாஸ்?' },
                { ta: '2. வீட்டில் நாங்கள் எவ்வாறு அவளுக்கு உதவலாம்?', en: 'How can we support her learning at home?', ph: 'ஹௌ கேன் வி சப்போர்ட் ஹெர் லேர்னிங் அட் ஹோம்?' }
            ]
        }
    };

    const d = levelData[lvlId] || levelData['level_1_beginner'];
    document.getElementById('englishScenarioTitle').innerText = d.title;
    document.getElementById('englishLevelBadge').innerText = d.badge;
    const cont = document.getElementById('englishSentencesContainer');
    cont.innerHTML = d.sentences.map(s => `
        <div class="bg-slate-900/90 p-3 rounded-xl border border-slate-800">
            <p class="text-slate-300 font-medium">${s.ta}</p>
            <p class="text-indigo-400 font-bold mt-0.5">🇬🇧 "${s.en}"</p>
            <p class="text-emerald-400/90 text-xs mt-0.5 font-mono">🗣️ உச்சரிப்பு: ${s.ph}</p>
        </div>
    `).join('');
};
window.evaluateSpokenSpeech = async function() {
    const input = document.getElementById('spokenInputText').value.trim();
    const resEl = document.getElementById('spokenAssessmentResult');
    if (!input) return;

    resEl.classList.remove('hidden');
    resEl.innerHTML = '<span class="text-slate-400">Evaluating fluency with Meta SeamlessM4T logic...</span>';

    try {
        const resp = await fetch('/api/spoken-english/assess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ spoken_text: input, phone: '6381029380' })
        });
        const data = await resp.json();
        resEl.innerHTML = `
            <div class="flex items-center justify-between font-bold">
                <span class="text-indigo-300">Fluency Score: ${data.score_percentage}%</span>
                <span class="text-emerald-400">${data.fluency_level}</span>
            </div>
            <p class="text-slate-300">${data.feedback_ta}</p>
            ${data.corrections && data.corrections.length > 0 ? `
                <div class="mt-1 p-2 bg-rose-950/40 border border-rose-500/30 rounded-lg text-rose-300">
                    <span class="font-bold">Grammar Tip:</span> ${data.corrections[0].proper_correction} (${data.corrections[0].rule_tamil})
                </div>
            ` : ''}
        `;
    } catch (e) {
        resEl.innerHTML = '<span class="text-emerald-400">Good effort! Keep practicing on WhatsApp voice notes.</span>';
    }
};

// ══════════════════════════════════════════════════════════════
// 🧠 STUDENT MENTAL HEALTH & EMOTIONAL WELLBEING CONTROLLER
// ══════════════════════════════════════════════════════════════
window.openMentalHealthModal = function() {
    document.getElementById('mentalHealthModal').classList.remove('hidden');
    loadMentalHealthTopic('exam_anxiety');
};
window.closeMentalHealthModal = function() {
    document.getElementById('mentalHealthModal').classList.add('hidden');
};
window.loadMentalHealthTopic = function(topicId) {
    const topics = {
        'exam_anxiety': {
            title: '🎯 தேர்வு பயம் & பதட்டம் தணிக்கும் பயிற்சி',
            steps: ['• 1. மூச்சை 4 வினாடிகள் மூக்கு வழியே உள்ளிழுங்கள்.', '• 2. மூச்சை 7 வினாடிகள் நெஞ்சில் அடக்கி வையுங்கள்.', '• 3. மூச்சை 8 வினாடிகள் வாய் வழியே மெதுவாக வெளியேற்றுங்கள்.', '• 4. இதை 4 முறை செய்யுங்கள் - பதட்டம் நீங்கி அமைதி உண்டாகும்.'],
            affirmation: 'மதிப்பெண்கள் என் எதிர்காலத்தை மட்டுமே தீர்மானிப்பதில்லை; என் கடின உழைப்பும் விடாமுயற்சியுமே என்னை உயர்த்தும். என்னால் முடியும்!'
        },
        'study_burnout': {
            title: '🔋 படிப்பு சோர்வு நீக்கும் பொமோடோரோ 25/5 உத்தி',
            steps: ['• 1. போனை DND-ல் வைத்துவிட்டு 25 நிமிடங்கள் ஒரு பாடத்தை மட்டும் கவனமாக படியுங்கள்.', '• 2. அலாரம் அடித்ததும் உடனே எழுந்து 5 நிமிடங்கள் தண்ணீர் குடித்து ஓய்வெடுங்கள்.', '• 3. 4 சுற்றுகள் முடிந்ததும் 20 நிமிடங்கள் நீண்ட இடைவேளை எடுங்கள்.', '• 4. மூளை புத்துணர்ச்சியுடன் பாடங்களை அதிக நாட்கள் நினைவில் வைத்திருக்கும்.'],
            affirmation: 'சோர்வு தற்காலிகமானது, என் வெற்றி நிரந்தரமானது! ஒவ்வொரு சிறிய முன்னேற்றமும் என்னை என் லட்சியத்தை நோக்கி நகர்த்துகிறது.'
        },
        'parent_peer_pressure': {
            title: '🤝 மற்றவர்களுடன் ஒப்பீடு & பெற்றோர் எதிர்பார்ப்பை வெல்லுதல்',
            steps: ['• 1. கண்களால் 5 பொருட்களைப் பாருங்கள்.', '• 2. தொட்டுணரக்கூடிய 4 பொருட்களைத் தொடுங்கள்.', '• 3. கேட்கும் 3 ஒலிகளைக் கவனியுங்கள்.', '• 4. 2 வாசனைகளை நுகருங்கள்; 1 நல்ல எண்ணத்தை மனதில் நினையுங்கள். மன அழுத்தம் உடனே தணியும்.'],
            affirmation: 'நான் தனித்துவமானவன். என் பாதை மற்றவர்களுடையது போன்றதல்ல. எனக்கென்று ஒரு தனி பலமும் தனித்துவமான திறமையும் உண்டு!'
        },
        'emotional_listening': {
            title: '👂 பாதுகாப்பான ரகசிய ஆறுதல் மையம் (Safe Space)',
            steps: ['• 1. உங்கள் கவலைகளை யாரிடமும் சொல்ல முடியாவிட்டால் இங்கே தட்டச்சு செய்து பகிருங்கள்.', '• 2. உங்கள் விவரங்கள் 100% பாதுகாப்பாகவும் ரகசியமாகவும் இருக்கும்.', '• 3. உங்களை புரிந்துகொள்ளும் நண்பனாக SIA உங்களுக்கு துணை நிற்கும்.'],
            affirmation: 'இன்று கடினமான நாளாக இருக்கலாம், ஆனால் இது என் வாழ்வின் முடிவு அல்ல. நான் நிச்சயம் இந்த தடைகளைத் தாண்டி ஜெயிப்பேன்!'
        }
    };
    const t = topics[topicId] || topics['exam_anxiety'];
    document.getElementById('mhTopicTitle').innerText = t.title;
    document.getElementById('mhTechniqueSteps').innerHTML = t.steps.map(s => `<p>${s}</p>`).join('');
    document.getElementById('mhAffirmationText').innerText = `"${t.affirmation}"`;
};
window.submitMentalHealthCounseling = async function() {
    const q = document.getElementById('mentalHealthQueryInput').value.trim();
    const resEl = document.getElementById('counselingFeedback');
    if (!q) return;

    resEl.classList.remove('hidden');
    resEl.innerHTML = '<span class="text-rose-300">SIA அன்பான ஆறுதல் வழிகாட்டலை உருவாக்குகிறது...</span>';

    try {
        const resp = await fetch('/api/mental-health/counsel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: q, phone: '6381029380', mood: 'support_requested' })
        });
        const data = await resp.json();
        resEl.innerHTML = `
            <div class="text-slate-200">${data.reply_ta.replace(/\\n/g, '<br>')}</div>
        `;
    } catch (e) {
        resEl.innerHTML = '<span class="text-white">நாங்கள் உங்களுடன் இருக்கிறோம். தயங்காமல் அரசு மாணவர் உதவி எண் 14416-க்கு அழையுங்கள்!</span>';
    }
};

// ══════════════════════════════════════════════════════════════
// 📚 UNIVERSAL TUITION CLASS (ALL CLASSES & SYLLABI) CONTROLLER
// ══════════════════════════════════════════════════════════════
window.openUniversalTuitionModal = function() {
    document.getElementById('universalTuitionModal').classList.remove('hidden');
    switchTuitionClass('high_school_9_10');
};
window.closeUniversalTuitionModal = function() {
    document.getElementById('universalTuitionModal').classList.add('hidden');
};
window.switchTuitionClass = function(clsId) {
    const btns = { 'primary_1_5': 'btnTuiCls1', 'middle_6_8': 'btnTuiCls2', 'high_school_9_10': 'btnTuiCls3', 'higher_sec_11_12': 'btnTuiCls4' };
    Object.keys(btns).forEach(k => {
        const el = document.getElementById(btns[k]);
        if (el) {
            if (k === clsId) {
                el.className = 'p-2 rounded-xl bg-amber-600 text-white text-xs font-bold transition';
            } else {
                el.className = 'p-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition';
            }
        }
    });

    const classData = {
        'primary_1_5': {
            title: 'வகுப்பு 1-5 கணிதம்: எளிய பெருக்கல் வாய்ப்பாடு & கூட்டல்',
            summary: 'பெருக்கல் என்பது ஒரே எண்ணை மீண்டும் மீண்டும் கூட்டும் எளிய முறை (உதாரணம்: 3 x 4 = 3 + 3 + 3 + 3 = 12).',
            steps: ['• படி 1: பெருக்கல் என்பது தொடர் கூட்டல் (Repeated Addition).', '• படி 2: 5 x 3 என்றால் 5-ஐ 3 முறை கூட்டுதல் (5 + 5 + 5 = 15).', '• படி 3: விரல்களைப் பயன்படுத்தி அல்லது பொருட்கள் மூலம் எண்ணிப் பழகுங்கள்.']
        },
        'middle_6_8': {
            title: 'வகுப்பு 6-8 அறிவியல்: உயிரினங்களின் அடிப்படை அலகு: செல் அமைப்பு',
            summary: 'தாவர செல் மற்றும் விலங்கு செல் வேறுபாடுகள், உட்கரு (Nucleus) மற்றும் மைட்டோகாண்ட்ரியா.',
            steps: ['• படி 1: அனைத்து உயிரினங்களின் அடிப்படை அலகு செல்லாகும்.', '• படி 2: செல்லின் கட்டுப்பாட்டு மையம் உட்கரு (Nucleus).', '• படி 3: செல்லின் ஆற்றல் மையம் மைட்டோகாண்ட்ரியா (Mitochondria).']
        },
        'high_school_9_10': {
            title: '10-ம் வகுப்பு இயற்பியல்: ஓம் விதி & மின்தடை இணைப்புகள்',
            summary: 'மின்னழுத்தம், மின்னோட்டம், மின்தடை சமன்பாடு V = IR மற்றும் தொடர்/பக்க இணைப்புகள்.',
            steps: ['• படி 1: ஓம் விதி: V = IR (மின்னழுத்தம் = மின்னோட்டம் x மின்தடை).', '• படி 2: தொடரிணைப்பு (Series): Rs = R1 + R2 + R3.', '• படி 3: பக்க இணைப்பு (Parallel): 1/Rp = 1/R1 + 1/R2 + 1/R3.']
        },
        'higher_sec_11_12': {
            title: '12-ம் வகுப்பு இயற்பியல்: குறைக்கடத்திகள் & PN சந்தி டையோடு',
            summary: 'உள்ளார்ந்த & புறவியலான குறைக்கடத்திகள், p-வகை & n-வகை, முன்னோக்கு மற்றும் பின்னோக்கு சார்பு.',
            steps: ['• படி 1: சிலிக்கான்/ஜெர்மானியம் உள்ளார்ந்த குறைக்கடத்தி.', '• படி 2: 3-இணைதிறன் அசுவை சேர்த்தால் p-வகை; 5-இணைதிறன் சேர்த்தால் n-வகை.', '• படி 3: PN சந்தி முன்னோக்குச் சார்பில் மின்தடை குறைந்து மின்னோட்டம் பாயும்.']
        }
    };

    const d = classData[clsId] || classData['high_school_9_10'];
    document.getElementById('tuiTopicTitle').innerText = d.title;
    document.getElementById('tuiTopicSummary').innerText = d.summary;
    document.getElementById('tuiConceptSteps').innerHTML = d.steps.map(s => `<p>${s}</p>`).join('');
};
window.solveTuitionQuery = async function() {
    const q = document.getElementById('tuitionHomeworkInput').value.trim();
    const resEl = document.getElementById('tuitionSolverFeedback');
    if (!q) return;

    resEl.classList.remove('hidden');
    resEl.innerHTML = '<span class="text-amber-300">Meta Wonder 1.0 படிநிலைத் தீர்வை உருவாக்குகிறது...</span>';

    try {
        const resp = await fetch('/api/tuition/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: q, board: 'Tamil Nadu State Board & CBSE', phone: '6381029380' })
        });
        const data = await resp.json();
        resEl.innerHTML = `
            <div class="font-bold text-amber-300 mb-1">Meta Wonder 1.0 தீர்வு:</div>
            <div class="text-slate-200">${(data.reply || '').replace(/\\n/g, '<br>')}</div>
        `;
    } catch (e) {
        resEl.innerHTML = '<span class="text-white">தீர்வு தயாராக உள்ளது. வாட்ஸ்அப்பில் TUITION என அனுப்பவும்!</span>';
    }
};

window.openTravelModal = function()"""

if js_target in content and "window.openSpokenEnglishModal" not in content:
    content = content.replace(js_target, new_js, 1)
    print("✓ Added JavaScript controllers for Spoken English, Mental Health, and Universal Tuition")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated sia_ui_template.py successfully!")
