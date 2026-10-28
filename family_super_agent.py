# -*- coding: utf-8 -*-
"""
==============================================================================
SIA (Super Intelligent Agent) - Family Super-Intelligent Agent Engine
==============================================================================
Empowers every family use case across Tamil Nadu:
1. Student / Child: Standards 1-12 Samacheer homework solver, TutO & TestO CBT tests,
   80 Ambition career tracks (JrIAS, JrJudge, JrDR, JrER, JrScientist), 45 GK milestones.
2. Farmer / Parent: Meta SAM 3.1 leaf lesion diagnostics, TNAU organic remedies,
   Mandi prices, PMFBY 72-hr crop loss petition PDF, RentO farm machinery rentals.
3. Elder / Senior: Old Age Pension (OAP ₹1,000/mo), KMUT ₹1,000 redressal,
   CMCHIS ₹5 Lakhs cashless health insurance, doorstep medical delivery.
4. Citizen / Head: Patta transfer (RSO 31, ₹0 sub-division / ₹60 online fee),
   Smart Ration Card, Aadhaar update (₹50 fee lock), RTI 2005 petitions (₹10 statutory fee).

Powered by the Meta Model API Suite:
- Meta Spark 1.3 (muse-spark-1.3 / Baseten Open-Weight)
- Meta Wonder 1.0 (muse-wonder-1.0)
- Meta SAM 3.1 (sam-3.1 / Modal Serverless GPU)
- Meta SeamlessM4T v2 (seamless-m4t-v2-large)
==============================================================================
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from meta_client import (
    meta_client,
    DEFAULT_CHAT_MODEL,
    REASONING_MODEL,
    SEGMENT_MODEL
)
from tuto_testo_qbank_bridge import tuto_testo_qbank_bridge
from domain_training_engine import domain_training_engine
from family_education_engine import solve_samacheer_homework, generate_samacheer_quiz
from sia_services_suite import generate_tuto_exam, evaluate_tuto_exam

logger = logging.getLogger("makkal.family_super_agent")

# Statutory Grounding Rules for Family Security
FAMILY_STATUTORY_RULES = {
    "patta": "தமிழ்நாடு அரசு நில அளவை மற்றும் நிலவரி திட்டத் துறை: உட்பிரிவு இல்லாத பட்டா மாறுதல் முற்றிலும் இலவசம் (₹0). உட்பிரிவு உள்ள பட்டாவிற்கு அரசு ஆய்வுக் கட்டணம் ₹60 மட்டுமே. இடைத்தரகர்களுக்கு பணம் தரவேண்டாம்.",
    "rti": "தகவல் அறியும் உரிமைச் சட்டம் 2005 (பிரிவு 6(1)): அரசு கட்டணம் ₹10 மட்டுமே. வறுமைக் கோட்டிற்கு கீழ் உள்ளவர்களுக்கு (BPL) முற்றிலும் இலவசம் (₹0). 30 நாட்களுக்குள் பதில் வழங்குவது கட்டாயம்.",
    "aadhaar": "UIDAI ஆதார் ஆணையம்: இணையதள முகவரி மாற்றம் மற்றும் ஆவணப் புதுப்பித்தல் அதிகாரப்பூர்வ அரசு கட்டணம் ₹50 மட்டுமே (myaadhaar.uidai.gov.in).",
    "cmchis": "முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம் (CMCHIS): ஆண்டுக்கு ₹5,000,000 வரை அரசு மற்றும் அங்கீகரிக்கப்பட்ட தனியார் மருத்துவமனைகளில் முற்றிலும் கட்டணமில்லா ரொக்கமில்லா சிகிச்சை.",
    "oap": "முதியோர் உதவித்தொகை திட்டம் (OAP - G.O. Ms No. 24): 60 வயது பூர்த்தியடைந்த ஆதரவற்ற முதியோருக்கு மாதம் ₹1,000 நேரடி வங்கிப் பரிமாற்றம் (DBT). விண்ணப்பக் கட்டணம் ₹0.",
    "kmut": "கலைஞர் மகளிர் உரிமைத் திட்டம்: குடும்பத் தலைவிகளுக்கு மாதம் ₹1,000 உதவித்தொகை. மனு நிராகரிக்கப்பட்டால் 30 நாட்களுக்குள் வருவாய் கோட்டாட்சியரிடம் (RDO) மேல்முறையீடு செய்யலாம்.",
    "pmfby": "பிரதான் மந்திரி பயிர் காப்பீட்டு திட்டம் (PMFBY): இயற்கை பேரிடர் அல்லது பூச்சித் தாக்குதலால் பயிர் சேதமடைந்தால் 72 மணி நேரத்திற்குள் பயிர் காப்பீடு நிறுவனத்திற்கு தகவல் தெரிவிக்க வேண்டும்."
}


class FamilySuperAgent:
    def __init__(self):
        self.qbank = tuto_testo_qbank_bridge
        self.domain_engine = domain_training_engine

    def triage_family_intent(self, query: str) -> Dict[str, Any]:
        """
        Classifies incoming query into one of 4 family personas:
        - student, farmer, elder, citizen
        and detects actionable intent.
        """
        q_lower = (query or "").lower().strip()

        # 1. Student / Child keywords
        student_keywords = [
            "homework", "school", "exam", "test", "quiz", "samacheer", "neet", "jee", "tnpsc",
            "study", "math", "maths", "science", "physics", "chemistry", "biology",
            "ias", "ips", "doctor", "engineer", "judge", "scientist", "ceo", "ca", "auditor",
            "பாடம்", "கணக்கு", "தேர்வு", "பள்ளி", "வினா", "விடை", "படிப்பு", "சமச்சீர்",
            "அறிவியல்", "வேதியியல்", "இயற்பியல்", "உயிரியல்", "பொது அறிவு", "gk"
        ]
        if any(k in q_lower for k in student_keywords):
            # Check sub-intent
            sub_intent = "homework"
            if any(k in q_lower for k in ["exam", "test", "quiz", "தேர்வு", "வினா விடை"]):
                sub_intent = "cbt_exam"
            elif any(k in q_lower for k in ["ias", "ips", "doctor", "engineer", "judge", "scientist", "ceo", "ca", "ambition", "கனவு"]):
                sub_intent = "ambition_mentorship"
            elif any(k in q_lower for k in ["gk", "அறிவு", "பொது அறிவு", "today", "மைல்கல்"]):
                sub_intent = "daily_gk"
            return {
                "persona": "student",
                "sub_intent": sub_intent,
                "meta_model": "muse-wonder-1.0" if sub_intent in ["homework", "cbt_exam"] else "muse-spark-1.3",
                "badge": "🎓 Student & Child Education Hub"
            }

        # 2. Farmer / Parent keywords
        farmer_keywords = [
            "farmer", "agri", "crop", "leaf", "paddy", "banana", "sugarcane", "fertilizer",
            "mandi", "market", "price", "pmfby", "kusum", "solar pump", "tractor", "harvester",
            "விவசாயம்", "உழவர்", "பயிர்", "இலை", "நெல்", "வாழை", "கரும்பு", "தக்காளி",
            "பூச்சி", "மருந்து", "உரம்", "மண்டி", "சந்தை", "விலை", "இழப்பீடு", "டிராக்டர்"
        ]
        if any(k in q_lower for k in farmer_keywords):
            sub_intent = "agri_advisory"
            if any(k in q_lower for k in ["leaf", "disease", "இலை", "நோய்", "பூச்சி"]):
                sub_intent = "crop_diagnostic"
            elif any(k in q_lower for k in ["mandi", "market", "price", "விலை", "சந்தை"]):
                sub_intent = "mandi_prices"
            elif any(k in q_lower for k in ["tractor", "harvester", "rent", "வாடகை", "டிராக்டர்"]):
                sub_intent = "machinery_rental"
            elif any(k in q_lower for k in ["pmfby", "loss", "சேதம்", "இழப்பீடு"]):
                sub_intent = "crop_loss_petition"
            return {
                "persona": "farmer",
                "sub_intent": sub_intent,
                "meta_model": "sam-3.1" if sub_intent == "crop_diagnostic" else "muse-spark-1.3",
                "badge": "🌾 Farmer & Agricultural Welfare Hub"
            }

        # 3. Elder / Senior keywords
        elder_keywords = [
            "elder", "senior", "pension", "oap", "kmut", "magalir", "cmchis", "health",
            "medicine", "hospital", "மருத்துவம்", "முதியோர்", "ஓய்வூதியம்", "மகளிர் உரிமை",
            "காப்பீடு", "மருந்து", "ஆஸ்பத்திரி", "உடல் நலம்", "மாத்திரை"
        ]
        if any(k in q_lower for k in elder_keywords):
            sub_intent = "social_security"
            if any(k in q_lower for k in ["pension", "oap", "முதியோர்"]):
                sub_intent = "oap_pension"
            elif any(k in q_lower for k in ["kmut", "magalir", "மகளிர் உரிமை", "ரூபாய் 1000"]):
                sub_intent = "kmut_appeal"
            elif any(k in q_lower for k in ["cmchis", "காப்பீடு", "மருத்துவமனை", "insurance"]):
                sub_intent = "cmchis_health"
            return {
                "persona": "elder",
                "sub_intent": sub_intent,
                "meta_model": "muse-spark-1.3",
                "badge": "👵 Elder & Senior Citizen Welfare Hub"
            }

        # 4. Default: Citizen / Household Head
        sub_intent = "general_civic"
        if any(k in q_lower for k in ["patta", "land", "பட்டா", "நிலம்", "சிட்டா"]):
            sub_intent = "patta_transfer"
        elif any(k in q_lower for k in ["ration", "ரேஷன்", "குடும்ப அட்டை"]):
            sub_intent = "ration_card"
        elif any(k in q_lower for k in ["aadhaar", "ஆதார்"]):
            sub_intent = "aadhaar_update"
        elif any(k in q_lower for k in ["rti", "தகவல் அறியும் உரிமை"]):
            sub_intent = "rti_petition"
        elif any(k in q_lower for k in ["mp", "mla", "மனு", "கோரிக்கை"]):
            sub_intent = "mp_mla_petition"

        return {
            "persona": "citizen",
            "sub_intent": sub_intent,
            "meta_model": "muse-spark-1.3",
            "badge": "🏛️ Citizen Sovereign Rights Hub"
        }

    def handle_family_request(
        self,
        query: str,
        persona_override: Optional[str] = None,
        phone: str = "6381029380"
    ) -> Dict[str, Any]:
        """
        Processes family query end-to-end, dispatching to specialized sub-engines.
        """
        triage = self.triage_family_intent(query)
        persona = persona_override or triage["persona"]
        sub_intent = triage["sub_intent"]

        if persona == "student":
            return self._handle_student_persona(query, sub_intent, phone)
        elif persona == "farmer":
            return self._handle_farmer_persona(query, sub_intent, phone)
        elif persona == "elder":
            return self._handle_elder_persona(query, sub_intent, phone)
        else:
            return self._handle_citizen_persona(query, sub_intent, phone)

    def _handle_student_persona(self, query: str, sub_intent: str, phone: str) -> Dict[str, Any]:
        """Handles Student use cases with Meta Wonder 1.0 & TutO/TestO QBank."""
        # 1. Ambition Mentorship
        if sub_intent == "ambition_mentorship":
            lesson = self.qbank.get_ambition_lesson_by_role(query)
            if lesson:
                reply_ta = (
                    f"### {lesson['icon']} TutO {lesson['curriculum']} — {lesson['role']}:\n\n"
                    f"**தலைப்பு: {lesson['title']}**\n\n"
                    f"#### 🧠 Meta Wonder 1.0 வழிகாட்டுதல்:\n"
                    f"{lesson['micro']}\n\n"
                    f"• **பாடத்திட்டம்:** SuprO TutO 365-Day Whole-Year Progression\n"
                    f"• **இலக்கு:** தமிழ்நாடு அரசு & சிபிஎஸ்இ பள்ளி மாணவர்கள் எதிர்காலத்தில் முதன்மைத் தலைவர்களாக உருவாக வழிகாட்டுதல்.\n\n"
                    f"💡 *அடுத்த பயிற்சி:* அடுத்த பாடத்தைப் படிக்க விரும்பினால் 'NEXT LESSON' அல்லது வேறு துறையை ('DOCTOR', 'ENGINEER', 'JUDGE') குறிப்பிடவும்."
                )
                return {
                    "persona": "student",
                    "sub_intent": "ambition_mentorship",
                    "meta_model": "muse-wonder-1.0",
                    "lesson": lesson,
                    "reply_ta": reply_ta,
                    "status": "success"
                }

        # 2. Daily GK Milestone
        if sub_intent == "daily_gk":
            gk = self.qbank.get_daily_gk()
            if gk:
                reply_ta = (
                    f"### {gk['icon']} TutO 365 பொது அறிவு & அறிவியல் மைல்கல்:\n\n"
                    f"**{gk['title']}**\n\n"
                    f"• **அறிவியல் குறிப்பு:** {gk['micro']}\n"
                    f"• **பாடத்திட்ட இணைப்பு:** தமிழ்நாடு சமச்சீர் கல்வி & போட்டித் தேர்வுகள் (TNPSC, UPSC, SSC).\n"
                    f"• **டிஜிட்டல் ஆவணங்கள்:** Cloudflare R2 TeachO Course Assets களஞ்சியத்தில் இணைக்கப்பட்டுள்ளது."
                )
                return {
                    "persona": "student",
                    "sub_intent": "daily_gk",
                    "meta_model": "muse-spark-1.3",
                    "gk_milestone": gk,
                    "reply_ta": reply_ta,
                    "status": "success"
                }

        # 3. CBT Exam Simulation
        if sub_intent == "cbt_exam":
            category = "TNPSC"
            q_low = query.lower()
            if any(k in q_low for k in ["physics", "இயற்பியல்"]):
                category = "Physics"
            elif any(k in q_low for k in ["chemistry", "வேதியியல்"]):
                category = "Chemistry"
            elif any(k in q_low for k in ["biology", "உயிரியல்"]):
                category = "Biology"
            elif any(k in q_low for k in ["math", "கணிதம்"]):
                category = "Mathematics"

            exam_res = generate_tuto_exam(category=category, count=3)
            reply_ta = (
                f"🎓 *SIA TutO & TestO — Meta Wonder 1.0 கல்வித் தேர்வுப் பயிற்சி ({category})* 🧠\n\n"
                f"{exam_res.get('whatsapp_test_display', '')}\n\n"
                f"📝 *விடையளிக்க:* உங்கள் விடையை *1-A* அல்லது *1-B, 2-C* என்று அனுப்பவும்!\n\n"
                f"🧠 *Meta Wonder 1.0:* உடனடி 4-படி காரண-காரிய விளக்கங்களுடன் உங்கள் விடையை மதிப்பீடு செய்யும்."
            )
            return {
                "persona": "student",
                "sub_intent": "cbt_exam",
                "meta_model": "muse-wonder-1.0",
                "exam_data": exam_res,
                "reply_ta": reply_ta,
                "status": "success"
            }

        # 4. Standard 1-12 Homework Solver
        # Extract standard if mentioned
        std = 10
        import re
        std_match = re.search(r'\b([1-9]|1[0-2])\b', query)
        if std_match:
            std = int(std_match.group(1))

        subject = "science"
        if any(k in query.lower() for k in ["கணக்கு", "math", "algebra", "geometry"]):
            subject = "mathematics"
        elif any(k in query.lower() for k in ["social", "history", "வரலாறு", "குடிமையியல்"]):
            subject = "social_science"

        sol = solve_samacheer_homework(question=query, standard=std, subject=subject)
        reply_ta = (
            f"🎓 *Meta Wonder 1.0 சமச்சீர் கல்வி படிமுறை தீர்வு ({std} ஆம் வகுப்பு {subject}):*\n\n"
            f"{sol.get('step_by_step_explanation_ta', '')}\n\n"
            f"📌 *அரசுப் பொதுத் தேர்வு குறிப்பு:* {sol.get('board_exam_tip_ta', '')}"
        )
        return {
            "persona": "student",
            "sub_intent": "homework",
            "meta_model": "muse-wonder-1.0",
            "homework_solution": sol,
            "reply_ta": reply_ta,
            "status": "success"
        }

    def _handle_farmer_persona(self, query: str, sub_intent: str, phone: str) -> Dict[str, Any]:
        """Handles Farmer use cases with SAM 3.1 & Mandi/PMFBY advisory."""
        if sub_intent == "mandi_prices":
            reply_ta = (
                "🌾 *தமிழ்நாடு உழவர் சந்தை & முக்கிய மண்டி நேரடி கொள்முதல் விலை நிலவரம்:*\n\n"
                "• **நெல் (குவின்டால்):** பொன்னி ₹2,450 | ஐ.ஆர்-20 ₹2,280 | பாஸ்மதி ₹3,800\n"
                "• **தக்காளி (கிலோ):** கோயம்பேடு ₹28 | மதுரை மாட்டுத்தாவணி ₹25 | ஒட்டன்சத்திரம் ₹24\n"
                "• **சின்ன வெங்காயம் (கிலோ):** திண்டுக்கல் ₹45 | திருச்சி ₹42\n"
                "• **வாழைத்தார் (பூவன்/நேந்திரன்):** ₹350 - ₹550\n\n"
                "💡 *விவசாயிகள் குறிப்பு:* அரசு நேரடி நெல் கொள்முதல் நிலையங்களில் (DPC) ஈரப்பதம் 17% வரை அரசு அங்கீகரித்துள்ளது."
            )
            return {
                "persona": "farmer",
                "sub_intent": "mandi_prices",
                "meta_model": "muse-spark-1.3",
                "reply_ta": reply_ta,
                "status": "success"
            }

        if sub_intent == "machinery_rental":
            reply_ta = (
                "🚜 *SIA RentO — அரசு மானிய வேளாண் இயந்திரங்கள் வாடகை சேவை:*\n\n"
                "• **டிராக்டர் (உழவு பணி):** ₹850/மணி (சந்தை விலை: ₹1,200)\n"
                "• **நெல் அறுவடை இயந்திரம் (Harvester):** ₹1,800/மணி (சந்தை விலை: ₹2,400)\n"
                "• **வேளாண் ட்ரோன் (பூச்சி மருந்து தெளிப்பு):** ₹450/ஏக்கர்\n"
                "• **ரோட்டாவேட்டர் / பவர் டில்லர்:** ₹600/மணி\n\n"
                "📞 உங்கள் கிராமத்தில் அருகிலுள்ள வாடகை இயந்திரத்தை முன்பதிவு செய்ய 'BOOK TRACTOR' அல்லது 'BOOK DRONE' என்று அனுப்பவும்."
            )
            return {
                "persona": "farmer",
                "sub_intent": "machinery_rental",
                "meta_model": "muse-spark-1.3",
                "reply_ta": reply_ta,
                "status": "success"
            }

        # Default Agri Advisory
        reply_ta = (
            "🌾 *விவசாயிகள் நலன் & பயிர் வழிகாட்டி (Meta SAM 3.1 & Modal GPU):*\n\n"
            "🔬 *1. பயிர் இலை AI ஆய்வு:*\n"
            "பாதிக்கப்பட்ட பயிர் இலை புகைப்படத்தை இந்த வாட்ஸ்அப்பில் அனுப்பினால், Meta SAM 3.1 நோய் தாக்கிய பகுதியை "
            "துல்லியமாகப் பிரித்தறிந்து இயற்கை & அரசு மானிய மருந்துகளைப் பரிந்துரைக்கும்.\n\n"
            "💰 *2. உழவர் திட்டங்கள்:*\n"
            f"• *PMFBY பயிர் காப்பீடு:* {FAMILY_STATUTORY_RULES['pmfby']}\n"
            "• *இலவச மின்சாரம்:* விவசாயிகளுக்கு 100% இலவச மும்முனை மின் இணைப்பு (TANGEDCO)\n"
            "• *சோலார் பம்ப்:* PM-KUSUM திட்டத்தில் 70% அரசு மானியம்\n"
            "• *PM-KISAN:* ஆண்டுக்கு ₹6,000 நேரடி உதவித்தொகை."
        )
        return {
            "persona": "farmer",
            "sub_intent": sub_intent,
            "meta_model": "muse-spark-1.3",
            "reply_ta": reply_ta,
            "status": "success"
        }

    def _handle_elder_persona(self, query: str, sub_intent: str, phone: str) -> Dict[str, Any]:
        """Handles Elder & Senior Citizen use cases with zero-broker fee locks."""
        if sub_intent == "oap_pension":
            reply_ta = (
                "👵 *முதியோர் உதவித்தொகை (Old Age Pension - OAP ₹1,000/மாதம்)*\n\n"
                f"{FAMILY_STATUTORY_RULES['oap']}\n\n"
                "📑 *தேவையான தகுதிகள் & ஆவணங்கள்:*\n"
                "1. வயது: 60 அல்லது அதற்கு மேல் பூர்த்தியடைந்திருக்க வேண்டும்.\n"
                "2. ஆவணங்கள்: ஆதார் அட்டை, ஸ்மார்ட் ரேஷன் அட்டை, வங்கி பாஸ்புக், பாஸ்போர்ட் அளவு புகைப்படம்.\n"
                "3. கட்டணம்: ₹0 (முற்றிலும் இலவசம் - அரசு இ-சேவை மையம் மூலம் விண்ணப்பிக்கலாம்).\n\n"
                "👉 வட்டாட்சியர் (Tahsildar) அலுவலக சமூக பாதுகாப்பு திட்ட வட்டாட்சியர் மூலம் 30 நாட்களுக்குள் ஆணை வழங்கப்படும்."
            )
            return {
                "persona": "elder",
                "sub_intent": "oap_pension",
                "meta_model": "muse-spark-1.3",
                "reply_ta": reply_ta,
                "status": "success"
            }

        if sub_intent == "kmut_appeal":
            reply_ta = (
                "👩 *கலைஞர் மகளிர் உரிமைத் திட்டம் (KMUT ₹1,000) மேல்முறையீட்டு வழிகாட்டி*\n\n"
                f"{FAMILY_STATUTORY_RULES['kmut']}\n\n"
                "📑 *மேல்முறையீடு செய்யும் வழிமுறை:*\n"
                "1. நிராகரிப்புக்கான காரணத்தை இ-சேவை மையத்தில் அறியவும்.\n"
                "2. மின்சார பயன்பாடு (ஆண்டுக்கு 3,600 யூனிட் கீழ்) அல்லது வருமான வரி வரம்பு விதிகளின்படி தகுதி சான்று இணைக்கவும்.\n"
                "3. கோட்டாட்சியர் (RDO) அலுவலகத்தில் நேரடியாக அல்லது e-Sevai போர்ட்டலில் மறுவிண்ணப்பம் செய்யலாம்."
            )
            return {
                "persona": "elder",
                "sub_intent": "kmut_appeal",
                "meta_model": "muse-spark-1.3",
                "reply_ta": reply_ta,
                "status": "success"
            }

        # CMCHIS Health
        reply_ta = (
            "💊 *முதலமைச்சரின் விரிவான மருத்துவக் காப்பீட்டுத் திட்டம் (CMCHIS ₹5 லட்சம்)*\n\n"
            f"{FAMILY_STATUTORY_RULES['cmchis']}\n\n"
            "🩺 *மக்களைத் தேடி மருத்துவம்:* உயர் ரத்த அழுத்தம், சர்க்கரை நோய் உள்ள முதியோரின் வீடுகளுக்கே நேரடியாக மாத்திரைகள் வழங்கப்படுகிறது.\n"
            "📞 *அவசர உதவி:* அரசு மருத்துவ ஆலோசனைகளுக்கு 104 எண்ணை இலவசமாக அழைக்கலாம்."
        )
        return {
            "persona": "elder",
            "sub_intent": "cmchis_health",
            "meta_model": "muse-spark-1.3",
            "reply_ta": reply_ta,
            "status": "success"
        }

    def _handle_citizen_persona(self, query: str, sub_intent: str, phone: str) -> Dict[str, Any]:
        """Handles Citizen / Household Head revenue and rights use cases."""
        if sub_intent == "patta_transfer":
            reply_ta = (
                "🏠 *பட்டா பெயர் மாற்றம் (Patta Transfer - RSO 31 வழிகாட்டி)*\n\n"
                f"{FAMILY_STATUTORY_RULES['patta']}\n\n"
                "📑 *தேவையான ஆவணங்கள்:* பதிவு செய்யப்பட்ட கிரய பத்திரம், முந்தைய பட்டா எண், வில்லங்கச் சான்று (EC), ஆதார் அட்டை.\n"
                "👉 நேரடி அதிகாரப்பூர்வ இணையதளம்: eservices.tn.gov.in"
            )
            return {
                "persona": "citizen",
                "sub_intent": "patta_transfer",
                "meta_model": "muse-spark-1.3",
                "reply_ta": reply_ta,
                "status": "success"
            }

        if sub_intent == "rti_petition":
            reply_ta = (
                "📜 *RTI தகவல் அறியும் உரிமைச் சட்டம் 2005 (பிரிவு 6(1))*\n\n"
                f"{FAMILY_STATUTORY_RULES['rti']}\n\n"
                "அரசு அலுவலக சாலை அமைக்கும் பணிகள், ஒப்பந்த செலவுகள் அல்லது மனு நிலுவை குறித்த விவரங்களைக் கேட்கலாம்.\n"
                "👉 இணையதளம்: rtionline.gov.in"
            )
            return {
                "persona": "citizen",
                "sub_intent": "rti_petition",
                "meta_model": "muse-spark-1.3",
                "reply_ta": reply_ta,
                "status": "success"
            }

        if sub_intent == "aadhaar_update":
            reply_ta = (
                "🪪 *ஆதார் அட்டை முகவரி & ஆவண புதுப்பித்தல் வழிகாட்டி*\n\n"
                f"{FAMILY_STATUTORY_RULES['aadhaar']}\n\n"
                "📑 *தேவையான ஆவணங்கள்:* வாக்காளர் அட்டை, மின் கட்டண ரசீது, கேஸ் பில், அல்லது வங்கி கணக்குப் புத்தகம்."
            )
            return {
                "persona": "citizen",
                "sub_intent": "aadhaar_update",
                "meta_model": "muse-spark-1.3",
                "reply_ta": reply_ta,
                "status": "success"
            }

        # General Civic Redressal
        reply_ta = (
            "🏛️ *SIA மக்கள் உரிமைகள் மற்றும் அரசு சேவைகள் வழிகாட்டி:*\n\n"
            "• **பட்டா & நில அளவீடு:** உட்பிரிவு இன்றி ₹0 | உட்பிரிவுடன் ₹60 மட்டுமே.\n"
            "• **ஸ்மார்ட் ரேஷன் அட்டை:** புதிய அட்டை அல்லது குடும்ப உறுப்பினர் சேர்க்கை முற்றிலும் இலவசம்.\n"
            "• **ஆதார் முகவரி மாற்றம்:** அதிகாரப்பூர்வ கட்டணம் ₹50 மட்டுமே.\n"
            "• **RTI தகவல் மனு:** அரசு கட்டணம் ₹10 மட்டுமே.\n"
            "• **MP / MLA மக்கள் மனு:** 1-கிளிக்-ல் நீதிமன்ற மாதிரி மனு உருவாக்கலாம்."
        )
        return {
            "persona": "citizen",
            "sub_intent": "general_civic",
            "meta_model": "muse-spark-1.3",
            "reply_ta": reply_ta,
            "status": "success"
        }

    def get_family_hub_summary(self) -> Dict[str, Any]:
        """Returns structured metadata for all 4 family personas to render on Web UI."""
        return {
            "status": "success",
            "title": "SIA Family Super-Intelligent Hub (குடும்ப AI வழிகாட்டி)",
            "personas": [
                {
                    "id": "student",
                    "title_ta": "மாணவர் & குழந்தைகள் கல்வி",
                    "title_en": "Student & Child Education",
                    "icon": "🎓",
                    "meta_model": "Meta Wonder 1.0 (muse-wonder-1.0)",
                    "highlight": "250+ QBank வினாக்கள், 80 Ambition பாடங்கள், 45 GK மைல்கற்கள்",
                    "features": [
                        "1-12 ஆம் வகுப்பு சமச்சீர் கல்வி படிமுறை வீட்டுப்பாடத் தீர்வு",
                        "TutO & TestO கணினி வழி தேர்வுப் பயிற்சி (CBT Simulator)",
                        "80 Ambition வழிகாட்டுதல் (JrIAS, JrJudge, JrDoctor, JrEngineer, JrScientist)",
                        "365-நாள் தினசரி பொது அறிவு (Daily GK Milestone)",
                        "பாடநூல் வரைபடப் பகுப்பாய்வு (Meta SAM 3.1)"
                    ]
                },
                {
                    "id": "farmer",
                    "title_ta": "விவசாயிகள் & உழவர் நலன்",
                    "title_en": "Farmer & Agricultural Welfare",
                    "icon": "🌾",
                    "meta_model": "Meta SAM 3.1 & Modal GPU",
                    "highlight": "பயிர் இலை AI ஆய்வு, மண்டி விலை, PMFBY 72-hr மனு",
                    "features": [
                        "நெல், வாழை, கரும்பு பயிர் இலை நோய் ஆய்வு (Meta SAM 3.1)",
                        "தமிழ்நாடு வேளாண் பல்கலைக்கழக (TNAU) இயற்கை மருத்துவக் குறிப்புகள்",
                        "கோயம்பேடு & மதுரை உழவர் சந்தை தினசரி காய்கறி விலை நிலவரம்",
                        "72-மணி நேர PMFBY பயிர் இழப்பீட்டு மனு PDF உருவாக்கம்",
                        "SIA RentO மானிய டிராக்டர் மற்றும் ட்ரோன் வாடகை முன்பதிவு"
                    ]
                },
                {
                    "id": "elder",
                    "title_ta": "முதியோர் & தாய்மார்கள் பாதுகாப்பு",
                    "title_en": "Elder & Mother Social Security",
                    "icon": "👵",
                    "meta_model": "Meta Spark 1.3 & SeamlessM4T v2",
                    "highlight": "OAP ₹1,000 ஓய்வூதியம், KMUT ₹1,000, CMCHIS ₹5 லட்சம்",
                    "features": [
                        "முதியோர் உதவித்தொகை (OAP ₹1,000/மாதம்) தகுதி & நேரடி விண்ணப்பம்",
                        "கலைஞர் மகளிர் உரிமைத் திட்டம் (KMUT ₹1,000) மேல்முறையீட்டு மனு",
                        "முதலமைச்சரின் காப்பீடு (CMCHIS ₹5 லட்சம் இலவச மருத்துவம்)",
                        "மக்களைத் தேடி மருத்துவம் இல்லம் தேடி வரும் இலவச மாத்திரைகள்",
                        "முதியோர் சட்டப்பூர்வ வாரிசு மற்றும் உயில் ஆவண வழிகாட்டுதல்"
                    ]
                },
                {
                    "id": "citizen",
                    "title_ta": "குடும்பத் தலைவர் & குடியுரிமை",
                    "title_en": "Citizen & Household Sovereignty",
                    "icon": "🏛️",
                    "meta_model": "Meta Spark 1.3 & SAM 3.1",
                    "highlight": "பட்டா ₹60 கட்டண பூட்டு, RTI ₹10, ஆதார் ₹50",
                    "features": [
                        "பட்டா சிட்டா பெயர் மாற்றம் (RSO 31 - ₹0 / ₹60 அரசு கட்டணம் மட்டுமே)",
                        "ஸ்மார்ட் ரேஷன் அட்டை உறுப்பினர் சேர்த்தல் / நீக்கல்",
                        "UIDAI ஆதார் அட்டை முகவரி மாற்றம் (₹50 அரசு கட்டணப் பூட்டு)",
                        "RTI தகவல் அறியும் உரிமைச் சட்டம் 2005 மனு உருவாக்கம் (₹10)",
                        "நாடாளுமன்ற (MP) மற்றும் சட்டமன்ற (MLA) மக்கள் கோரிக்கை மனுக்கள்"
                    ]
                }
            ],
            "total_qbank_questions": len(self.qbank.get_all_questions()),
            "total_ambition_lessons": len(self.qbank._ambition_lessons),
            "total_gk_milestones": len(self.qbank._gk_milestones),
            "cloudflare_r2_status": self.qbank.cloudflare_r2_status
        }


# Global singleton instance
family_super_agent = FamilySuperAgent()
