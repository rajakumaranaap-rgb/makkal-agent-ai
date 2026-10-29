"""
Script to add Spoken English, Mental Health, and Universal Tuition endpoints to app.py
"""

import sys

FILE_PATH = r"D:\api\makkal-agent-ai\app.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

target = '@app.get("/", response_class=HTMLResponse)'

new_endpoints = """# ==============================================================================
# 🗣️ 4. CONVERSATIONAL SPOKEN ENGLISH COACH ENDPOINTS
# ==============================================================================

@app.get("/api/spoken-english/levels")
async def get_spoken_english_levels_endpoint():
    \"\"\"Returns level-wise conversational spoken English modules (Levels 1 to 4).\"\"\"
    from spoken_english_coach import get_all_english_levels
    return {"status": "success", "levels": get_all_english_levels()}


@app.get("/api/spoken-english/scenario/{scenario_id}")
async def get_spoken_english_scenario_endpoint(scenario_id: str):
    \"\"\"Retrieves specific scenario dialogue pairs with phonetic Tamil transliteration.\"\"\"
    from spoken_english_coach import get_scenario_details
    res = get_scenario_details(scenario_id)
    if not res:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "success", "scenario": res}


@app.post("/api/spoken-english/assess")
async def assess_spoken_english_endpoint(req: Request):
    \"\"\"Evaluates citizen/student spoken English fluency and provides phonetic tips.\"\"\"
    from spoken_english_coach import evaluate_spoken_sentence
    from student_learning_vault import record_spoken_english_practice
    body = await req.json()
    spoken = body.get("spoken_text", "")
    target = body.get("target_sentence")
    phone = body.get("phone", "6381029380")
    scenario_id = body.get("scenario_id", "daily_greetings")
    res = evaluate_spoken_sentence(spoken_text=spoken, target_sentence=target)
    record_spoken_english_practice(phone, scenario_id, score=res.get("score_percentage", 80), channel="Web")
    return JSONResponse(content=res)


# ==============================================================================
# 🧠 5. STUDENT MENTAL HEALTH & EMOTIONAL WELLBEING COACH ENDPOINTS
# ==============================================================================

@app.get("/api/mental-health/modules")
async def get_mental_health_modules_endpoint():
    \"\"\"Returns all mental health support modules (Exam Anxiety, Burnout, Peer Pressure).\"\"\"
    from student_mental_health_coach import get_all_wellbeing_modules
    return {"status": "success", "modules": get_all_wellbeing_modules()}


@app.get("/api/mental-health/helplines")
async def get_mental_health_helplines_endpoint():
    \"\"\"Returns statutory 24x7 crisis helplines (14416, Tele-MANAS, Sneha).\"\"\"
    from student_mental_health_coach import get_statutory_helplines
    return {"status": "success", "helplines": get_statutory_helplines()}


@app.post("/api/mental-health/counsel")
async def mental_health_counsel_endpoint(req: Request):
    \"\"\"Provides compassionate emotional support, breathing exercises, and Thirukkural resilience.\"\"\"
    from student_mental_health_coach import handle_empathetic_counseling_query
    from student_learning_vault import record_mental_health_checkin
    body = await req.json()
    query = body.get("query", "")
    phone = body.get("phone", "6381029380")
    mood = body.get("mood", "calm")
    res = handle_empathetic_counseling_query(user_query=query)
    record_mental_health_checkin(phone, mood=mood, channel="Web")
    return JSONResponse(content=res)


# ==============================================================================
# 📚 6. UNIVERSAL TUITION CLASS (ALL CLASSES & CBSE / STATE BOARD) ENDPOINTS
# ==============================================================================

@app.get("/api/tuition/classes")
async def get_tuition_classes_endpoint():
    \"\"\"Returns universal tuition classes across State Board and CBSE (Classes 1-12).\"\"\"
    from universal_tuition_engine import get_all_tuition_classes
    return {"status": "success", "classes": get_all_tuition_classes()}


@app.get("/api/tuition/topic/{topic_id}")
async def get_tuition_topic_endpoint(topic_id: str):
    \"\"\"Retrieves full step-by-step tuition lesson and self-assessment quiz.\"\"\"
    from universal_tuition_engine import get_tuition_topic_by_id
    res = get_tuition_topic_by_id(topic_id)
    if not res:
        raise HTTPException(status_code=404, detail="Tuition topic not found")
    return {"status": "success", "topic": res}


@app.post("/api/tuition/solve")
async def solve_tuition_query_endpoint(req: Request):
    \"\"\"Solves any CBSE / State Board problem with first-principles reasoning via Meta Wonder 1.0.\"\"\"
    from meta_client import meta_client
    from student_learning_vault import record_tuition_quiz_attempt
    body = await req.json()
    query = body.get("query", "")
    board = body.get("board", "Tamil Nadu State Board & CBSE")
    phone = body.get("phone", "6381029380")
    topic_id = body.get("topic_id", "general_tuition")
    
    orch_res = meta_client.orchestrate_meta_models(
        query=f"[{board} Tuition Homework Query]: {query}",
        preferred_model="muse-wonder-1.0"
    )
    record_tuition_quiz_attempt(phone, topic_id=topic_id, is_correct=True, score_pct=100.0, channel="Web")
    return JSONResponse(content=orch_res)


# ==============================================================================
# 🔄 7. STUDENT LEARNING & WELLBEING STATE VAULT (DUAL SYNC)
# ==============================================================================

@app.get("/api/student-vault/profile")
async def get_student_vault_profile_endpoint(phone: str = Query("6381029380")):
    \"\"\"Retrieves live unified learning streak, mental health mood, and tuition progress.\"\"\"
    from student_learning_vault import get_student_profile
    return {"status": "success", "profile": get_student_profile(phone)}


@app.get("/", response_class=HTMLResponse)"""

if target in content and "/api/spoken-english/levels" not in content:
    content = content.replace(target, new_endpoints, 1)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Added Spoken English, Mental Health, and Universal Tuition endpoints to app.py")
else:
    print("Endpoints already present in app.py or target not found.")
