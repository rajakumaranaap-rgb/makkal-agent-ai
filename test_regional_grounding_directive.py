"""
==============================================================================
Test Suite: Tamil Nadu Civic & Regional Grounding Directive
Part of Makkal Agent AI - Meta AI Developer Hackathon 2026
==============================================================================
Tests all 4 Pillars:
1. Agri Advisory (TNAU & GRAINS): Turmeric, Paddy, Banana, Pulses, Pendimethalin, Nano DAP, Bio-inputs.
2. Civic & E-Governance (TNeGA & Llama 3.2 Vision): Patta, EC, Ration Card, Scholarships, Fee Locking.
3. Samacheer Kalvi (Standards 1 to 12): Curriculum Mappings, Homework Explainer, 5-Question Quiz.
4. Bilingual Code-Switching & SeamlessM4T v2: Spoken Tamil, Tanglish, Regional Intonations (Madurai, Kongu).
==============================================================================
"""

import sys
import os
import unittest
from pathlib import Path

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_DIR = Path("D:/api/makkal-agent-ai")
sys.path.insert(0, str(PROJECT_DIR))

import agriculture_engine
import tnega_civic_engine
import llama_vision_auditor
import family_education_engine
import seamless_speech_engine


class TestTamilNaduRegionalGrounding(unittest.TestCase):

    # =========================================================================
    # PILLAR 1: AGRI ADVISORY (TNAU & GRAINS)
    # =========================================================================
    def test_01_tnau_turmeric_advisory(self):
        """Verifies Turmeric TNAU guidelines: Pendimethalin, Nano DAP, Pseudomonas, and GRAINS subsidy."""
        adv = agriculture_engine.get_tnau_agronomy_advisory("turmeric")
        self.assertNotIn("error", adv, "Turmeric should exist in TNAU agronomy registry")
        
        # Weed control check
        weed = adv["weed_control"]
        self.assertIn("Pendimethalin 30% EC", weed["chemical_ta"])
        self.assertIn("3.3", weed["dosage_metric"], "Pendimethalin dosage metric must mention 3.3 L/ha")
        
        # Foliar nutrition check
        foliar = adv["foliar_nutrition"]
        self.assertIn("Nano DAP", foliar["product_ta"])
        self.assertIn("4 மிலி", foliar["spray_ratio"], "Nano DAP ratio must specify 4 ml/L")
        
        # Bio-fertilizer check
        bio = adv["bio_fertilizers"]
        self.assertIn("Pseudomonas fluorescens", bio["agents_ta"])
        self.assertIn("Trichoderma viride", bio["agents_ta"])
        
        # GRAINS subsidy check
        subsidy = adv["grains_subsidy"]
        self.assertIn("GRAINS", subsidy["scheme_name_ta"])
        self.assertIn("Uzhavan App", subsidy["portal_url"])

    def test_02_tnau_pulses_advisory(self):
        """Verifies Pulses (Blackgram/Greengram) TNAU guidelines: Pendimethalin, Pulse Wonder/Nano DAP."""
        adv = agriculture_engine.get_tnau_agronomy_advisory("pulses")
        self.assertNotIn("error", adv)
        
        weed = adv["weed_control"]
        self.assertIn("Pendimethalin 30% EC", weed["chemical_ta"])
        self.assertIn("Pre-emergence", weed["timing_ta"])
        
        foliar = adv["foliar_nutrition"]
        self.assertTrue(
            "TNAU Pulse Wonder" in foliar["product_ta"] or "Nano DAP" in foliar["product_ta"]
        )
        self.assertIn("2-4 மிலி", foliar["spray_ratio"])

        bio = adv["bio_fertilizers"]
        self.assertIn("Rhizobium", bio["agents_ta"])
        self.assertIn("Trichoderma viride", bio["agents_ta"])

    def test_03_tnau_paddy_and_banana_advisory(self):
        """Verifies Paddy and Banana TNAU guidelines & bio-control alternatives."""
        paddy_adv = agriculture_engine.get_tnau_agronomy_advisory("paddy")
        self.assertIn("Pendimethalin", paddy_adv["weed_control"]["chemical_ta"])
        self.assertIn("3-5", paddy_adv["weed_control"]["timing_ta"])
        self.assertIn("Pseudomonas", paddy_adv["bio_fertilizers"]["agents_ta"])

        banana_adv = agriculture_engine.get_tnau_agronomy_advisory("banana")
        self.assertIn("Nano DAP", banana_adv["foliar_nutrition"]["product_ta"])
        self.assertIn("Pseudomonas", banana_adv["bio_fertilizers"]["agents_ta"])
        self.assertIn("Trichoderma", banana_adv["bio_fertilizers"]["agents_ta"])

    # =========================================================================
    # PILLAR 2: CIVIC & E-GOVERNANCE (TNeGA & LLAMA 3.2 VISION)
    # =========================================================================
    def test_04_tnega_services_and_fee_locks(self):
        """Verifies all 4 required TNeGA services exist with official fee locks blocking middlemen."""
        services = tnega_civic_engine.get_all_tnega_services()
        s_ids = [s["service_id"] for s in services]
        self.assertIn("patta_chitta", s_ids)
        self.assertIn("encumbrance_certificate", s_ids)
        self.assertIn("smart_ration_card", s_ids)
        self.assertIn("higher_education_scholarships", s_ids)

        # Check Patta/Chitta statutory fee lock
        patta_info = tnega_civic_engine.get_tnega_service_checklist("patta_chitta")
        self.assertIn("₹60", patta_info["statutory_fee_lock"])
        self.assertIn("₹3,500", patta_info["middleman_extortion_blocked"])

        # Check Smart Ration Card free lock
        ration_info = tnega_civic_engine.get_tnega_service_checklist("smart_ration_card")
        self.assertIn("இலவசம்", ration_info["statutory_fee_lock"])

    def test_05_tnega_document_bundle_validation(self):
        """Verifies cross-checking uploaded documents against mandatory TNeGA checklist."""
        # Test full bundle (ready)
        ready_bundle = ["sale_deed", "previous_patta", "encumbrance_certificate", "aadhaar_card"]
        res_ready = tnega_civic_engine.validate_citizen_document_bundle("patta_chitta", ready_bundle)
        self.assertTrue(res_ready["is_ready_for_esevai"])
        self.assertEqual(res_ready["readiness_percentage"], 100)
        self.assertIn("வாழ்த்துகள்", res_ready["advice_ta"])

        # Test partial bundle (missing documents)
        partial_bundle = ["aadhaar_card"]
        res_partial = tnega_civic_engine.validate_citizen_document_bundle("patta_chitta", partial_bundle)
        self.assertFalse(res_partial["is_ready_for_esevai"])
        self.assertLess(res_partial["readiness_percentage"], 100)
        self.assertGreater(len(res_partial["missing_mandatory_documents"]), 0)

    def test_06_llama_vision_document_audit(self):
        """Verifies local Llama 3.2 Vision entity extraction, seal check, and TNeGA cross-checking."""
        # Generate dummy 100x100 white image bytes for testing
        from PIL import Image
        import io
        img = Image.new("RGB", (600, 800), color=(240, 245, 250))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        test_bytes = buf.getvalue()

        audit = llama_vision_auditor.scan_document_with_llama_vision(
            image_bytes=test_bytes,
            service_target="patta_chitta",
            filename="test_sale_deed.jpg"
        )
        self.assertEqual(audit["status"], "success")
        self.assertIn("extracted_entities", audit)
        entities = audit["extracted_entities"]
        self.assertTrue(entities["has_official_seal"])
        self.assertTrue(entities["has_signature"])
        self.assertIn("tnega_service_compliance", audit)
        self.assertIn("bilingual_advice", audit)
        self.assertIn("spoken_tamil", audit["bilingual_advice"])
        self.assertIn("colloquial_tanglish", audit["bilingual_advice"])

    # =========================================================================
    # PILLAR 3: LOCAL CURRICULUM (SAMACHEER KALVI STANDARDS 1 TO 12)
    # =========================================================================
    def test_07_samacheer_kalvi_curriculum_mappings(self):
        """Verifies TNSB Samacheer Kalvi syllabus covers Standards 1 to 12."""
        curriculum = family_education_engine.SAMACHEER_KALVI_CURRICULUM_DB
        self.assertIn("standards_1_to_5", curriculum)
        self.assertIn("standards_6_to_8", curriculum)
        self.assertIn("standards_9_to_10", curriculum)
        self.assertIn("standards_11_to_12", curriculum)

    def test_08_samacheer_kalvi_homework_solver(self):
        """Verifies homework assistance maps to Samacheer Kalvi textbook chapters and exam tips."""
        hw = family_education_engine.solve_samacheer_homework(
            question="நியூட்டனின் இரண்டாம் இயக்க விதி என்றால் என்ன?",
            standard=10,
            subject="science"
        )
        self.assertEqual(hw["status"], "success")
        self.assertIn("இயக்க விதிகள்", hw["textbook_unit"])
        self.assertIn("F = m × a", hw["step_by_step_explanation_ta"])
        self.assertIn("board_exam_tip_ta", hw)

    def test_09_samacheer_kalvi_quiz_generator(self):
        """Verifies adaptive 5-question quiz generation with Tamil/English options and explanations."""
        quiz = family_education_engine.generate_samacheer_quiz(standard=10, subject="science")
        self.assertEqual(quiz["status"], "success")
        self.assertEqual(quiz["total_questions"], 5)
        for q in quiz["questions"]:
            self.assertIn("question_ta", q)
            self.assertIn("question_en", q)
            self.assertEqual(len(q["options"]), 4)
            self.assertIn("correct_index", q)
            self.assertIn("explanation_ta", q)

    # =========================================================================
    # PILLAR 4: BILINGUAL CODE-SWITCHING & SEAMLESSM4T V2 SPEECH
    # =========================================================================
    def test_10_bilingual_code_switching_and_speech(self):
        """Verifies natural spoken Tamil, colloquial Tanglish, and regional intonations (Madurai & Kongu)."""
        input_text = "பட்டா மாறுதல் செய்ய என்ன ஆவணங்கள் தேவை?"
        
        # Madurai dialect
        res_madurai = seamless_speech_engine.generate_regional_bilingual_voice(input_text, region="madurai")
        self.assertIn("வணக்கம் அண்ணே!", res_madurai["spoken_tamil"])
        self.assertIn("Vanakkam anne!", res_madurai["colloquial_tanglish"])
        self.assertIn("Patta", res_madurai["colloquial_tanglish"])
        self.assertEqual(res_madurai["audio_synthesis"]["status"], "success")

        # Kongu dialect
        res_kongu = seamless_speech_engine.generate_regional_bilingual_voice(input_text, region="kongu")
        self.assertIn("வணக்கமுங்க! சொல்லுங்க கண்ணு", res_kongu["spoken_tamil"])
        self.assertIn("Vanakkamunga! Sollunga kannu", res_kongu["colloquial_tanglish"])
        self.assertEqual(res_kongu["audio_synthesis"]["status"], "success")


if __name__ == "__main__":
    unittest.main(verbosity=2)
