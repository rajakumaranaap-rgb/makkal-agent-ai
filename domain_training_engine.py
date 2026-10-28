"""
==============================================================================
Makkal Agent AI - Domain Training & Dataset Management Engine
==============================================================================
Platform: SIA (Super Intelligent Agent)
Target: Meta AI Developer Hackathon 2026 ($150,000 Track)
Role:
1. Manages curated domain Q&A datasets (Civic, Agronomy, Education, WhatsApp).
2. Generates exportable Baseten LoRA/SFT training files (meta-models/muse-spark-open-1026).
3. Injects in-context domain grounding into Meta Spark 1.3 & Meta Wonder 1.0.
4. Computes automated statutory accuracy, pedagogical completeness & anti-corruption scores.
==============================================================================
"""

import os
import sys
import json
import logging
import random
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("makkal.domain_training_engine")

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "makkal_domain_training_dataset.jsonl")
BASETEN_TRAIN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "baseten_train.jsonl")
BASETEN_EVAL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "baseten_eval.jsonl")


class DomainTrainingEngine:
    def __init__(self, dataset_path: str = DATASET_PATH):
        self.dataset_path = dataset_path
        self._samples: List[Dict[str, Any]] = []
        self._load_dataset()

    def _load_dataset(self) -> None:
        """Loads all domain training samples from JSONL."""
        self._samples = []
        if not os.path.exists(self.dataset_path):
            logger.warning(f"Dataset path {self.dataset_path} does not exist.")
            return

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    record = json.loads(clean_line)
                    self._samples.append(record)
                except Exception as e:
                    logger.error(f"Error parsing line {line_no} in {self.dataset_path}: {e}")

        logger.info(f"Loaded {len(self._samples)} domain training samples.")

    @property
    def total_samples(self) -> int:
        return len(self._samples)

    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Returns deep statistics and governance metrics of the training dataset."""
        domain_counts: Dict[str, int] = {}
        model_counts: Dict[str, int] = {}
        traces_count = 0
        distractors_count = 0
        statutory_rules_count = 0
        total_chars = 0

        for s in self._samples:
            d = s.get("domain", "general")
            domain_counts[d] = domain_counts.get(d, 0) + 1

            m = s.get("meta_model_target", "muse-spark-1.3")
            model_counts[m] = model_counts.get(m, 0) + 1

            if s.get("reasoning_traces"):
                traces_count += 1
            if s.get("distractors"):
                distractors_count += 1
            if s.get("statutory_rules"):
                statutory_rules_count += len(s["statutory_rules"])

            for msg in s.get("messages", []):
                total_chars += len(msg.get("content", ""))

        avg_chars_per_sample = round(total_chars / max(1, len(self._samples)), 1)
        est_tokens = int(total_chars / 4)

        return {
            "status": "ready",
            "total_samples": len(self._samples),
            "estimated_tokens": est_tokens,
            "avg_chars_per_sample": avg_chars_per_sample,
            "domains": domain_counts,
            "meta_model_distribution": model_counts,
            "pedagogical_traces_samples": traces_count,
            "cbt_distractor_samples": distractors_count,
            "statutory_rules_grounded": statutory_rules_count,
            "supported_models": [
                "muse-spark-1.3 (Conversational Triage)",
                "muse-wonder-1.0 (Deep Pedagogical Deliberation)",
                "sam-3.1 (Spatial Visual Segmentation)",
                "meta-models/muse-spark-open-1026 (Baseten Sovereign Edge)"
            ]
        }

    def export_baseten_fine_tuning_dataset(
        self,
        train_path: str = BASETEN_TRAIN_PATH,
        eval_path: str = BASETEN_EVAL_PATH,
        train_ratio: float = 0.8
    ) -> Dict[str, Any]:
        """
        Exports dataset into Baseten LoRA / SFT training format.
        Compatible with Meta Open Weight Models (Llama-3.3-70B-Instruct / muse-spark-open-1026).
        """
        if not self._samples:
            self._load_dataset()

        # Deterministic shuffle for reproducible splits
        shuffled = list(self._samples)
        random.seed(2026)
        random.shuffle(shuffled)

        split_idx = int(len(shuffled) * train_ratio)
        train_records = shuffled[:split_idx]
        eval_records = shuffled[split_idx:]

        os.makedirs(os.path.dirname(train_path), exist_ok=True)

        with open(train_path, "w", encoding="utf-8") as f:
            for r in train_records:
                # Format standard chat completion object
                baseten_format = {"messages": r.get("messages", [])}
                f.write(json.dumps(baseten_format, ensure_ascii=False) + "\n")

        with open(eval_path, "w", encoding="utf-8") as f:
            for r in eval_records:
                baseten_format = {"messages": r.get("messages", [])}
                f.write(json.dumps(baseten_format, ensure_ascii=False) + "\n")

        return {
            "status": "success",
            "train_samples": len(train_records),
            "eval_samples": len(eval_records),
            "train_file": train_path,
            "eval_file": eval_path,
            "target_open_weight_model": "meta-models/muse-spark-open-1026",
            "format": "OpenAI / Baseten Multi-Turn Chat JSONL"
        }

    def get_domain_grounding_prompt(self, user_query: str) -> str:
        """
        Retrieves matching statutory rules, fee locks, and curriculum contexts from the golden dataset.
        Uses relevance scoring to match domain specifics (Patta, RTI, Aadhaar, Crop, Exam).
        """
        clean_q = user_query.lower().strip()
        scored_samples = []

        # Domain priority keywords
        domain_keywords = {
            "rti": ["rti", "தகவல் அறியும்", "பிரிவு 6", "pio", "information officer"],
            "patta": ["பட்டா", "சிட்டா", "fmb", "உட்பிரிவு", "patta", "subdivision", "survey"],
            "aadhaar": ["ஆதார்", "aadhaar", "uidai", "முகவரி மாற்றம்"],
            "agri": ["பயிர்", "நெல்", "மஞ்சள்", "வாழை", "இலை", "நோய்", "crop", "leaf", "blast", "pmfby"],
            "education": ["நியூட்டன்", "ஒளியியல்", "physics", "maths", "science", "tnpsc", "சமச்சீர்", "தேர்வு"]
        }

        # Determine target domain intent
        target_domain = None
        for d, kws in domain_keywords.items():
            if any(k in clean_q for k in kws):
                target_domain = d
                break

        for sample in self._samples:
            user_msg = next((m["content"] for m in sample.get("messages", []) if m["role"] == "user"), "")
            u_clean = user_msg.lower()
            score = 0

            # Match target domain
            if target_domain:
                if any(k in u_clean for k in domain_keywords[target_domain]):
                    score += 10

            # Token overlap
            query_words = set(clean_q.split())
            sample_words = set(u_clean.split())
            overlap = len(query_words & sample_words)
            score += overlap * 2

            if score > 0:
                scored_samples.append((score, sample))

        scored_samples.sort(key=lambda x: x[0], reverse=True)

        matched_rules: List[str] = []
        matched_statutes: List[str] = []

        for _, sample in scored_samples[:5]:
            asst_msg = next((m["content"] for m in sample.get("messages", []) if m["role"] == "assistant"), "")
            for line in asst_msg.split("\n"):
                if any(marker in line for marker in ["₹", "இலவசம்", "கட்டணம்", "SLA", "பிரிவு", "சட்டம்", "TNAU", "TNSB", "விதி"]):
                    clean_l = line.strip().lstrip("•-* ")
                    if clean_l and len(clean_l) > 5 and clean_l not in matched_rules:
                        matched_rules.append("• " + clean_l)
            for st in sample.get("statutory_rules", []):
                if st not in matched_statutes:
                    matched_statutes.append(st)

        if not matched_rules:
            matched_rules = [
                "• உட்பிரிவு இல்லாத பட்டா மாறுதல்: ₹0 (முற்றிலும் இலவசம்)",
                "• உட்பிரிவு உள்ள பட்டா மாறுதல்: ₹60 மட்டுமே",
                "• RTI விண்ணப்ப கட்டணம்: ₹10 (BPL அட்டைதாரர்களுக்கு ₹0)",
                "• TNeGA வருவாய்த்துறை சான்றிதழ்கள் கட்டணம்: ₹60 மட்டுமே",
                "• ஆதார் முகவரி மாற்றம்: ₹50 மட்டுமே"
            ]
            matched_statutes = ["Tamil Nadu Government Services Charter 2024"]

        grounding_block = (
            "### 🔒 STATUTORY REGIONAL GROUNDING DIRECTIVE (MANDATORY ZERO-HALLUCINATION RULES):\n"
            + "\n".join(matched_rules[:6]) + "\n"
            + "• Applicable Statutes: " + ", ".join(matched_statutes[:4]) + "\n"
            + "• Anti-Middleman Mandate: Proactively alert citizens against unofficial broker/middleman fees.\n"
        )
        return grounding_block

    def evaluate_response(
        self,
        generated_reply: str,
        query: str,
        expected_domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates a model output against statutory fee locks, anti-hallucination guardrails,
        and pedagogical reasoning completeness.
        """
        gen_lower = generated_reply.lower()
        score_breakdown = {
            "statutory_fee_accuracy": 100,
            "anti_middleman_warning": 100,
            "pedagogical_clarity": 100,
            "tamil_fluency": 100
        }
        flags: List[str] = []

        # 1. Statutory Fee Lock Verification
        if "பட்டா" in query and "உட்பிரிவு" in query:
            if "இல்லாத" in query or "without" in query.lower():
                if "₹0" not in generated_reply and "இலவசம்" not in generated_reply and "free" not in gen_lower:
                    score_breakdown["statutory_fee_accuracy"] = 0
                    flags.append("Failed zero-fee lock for subdivision-less patta")
            elif "உள்ள" in query or "with" in query.lower():
                if "₹60" not in generated_reply and "60" not in generated_reply:
                    score_breakdown["statutory_fee_accuracy"] = 0
                    flags.append("Failed ₹60 fee lock for patta with subdivision")

        if "rti" in query.lower() or "தகவல் அறியும்" in query:
            if "₹10" not in generated_reply and "10" not in generated_reply:
                score_breakdown["statutory_fee_accuracy"] = 50
                flags.append("Missing standard RTI ₹10 court-fee citation")

        if "ஆதார்" in query or "aadhaar" in query.lower():
            if "₹50" not in generated_reply and "50" not in generated_reply:
                score_breakdown["statutory_fee_accuracy"] = 50
                flags.append("Missing UIDAI official ₹50 tariff citation")

        # 2. Anti-Middleman Verification
        if any(w in query for w in ["பட்டா", "சான்றிதழ்", "இ-சேவை", "ரேஷன்"]):
            if any(w in gen_lower for w in ["இடைத்தரகர்", "புரோக்கர்", "லஞ்சம்", "broker", "middleman", "கூடுதல் கட்டணம்"]):
                score_breakdown["anti_middleman_warning"] = 100
            else:
                score_breakdown["anti_middleman_warning"] = 80

        # 3. Pedagogical Deliberation Verification (Meta Wonder 1.0)
        if any(w in query.lower() for w in ["விதி", "law", "optics", "myopia", "maths", "science", "tnpsc"]):
            if any(w in gen_lower for w in ["படிமுறை", "step", "சூத்திரம்", "formula", "குறிப்பு", "tip"]):
                score_breakdown["pedagogical_clarity"] = 100
            else:
                score_breakdown["pedagogical_clarity"] = 70

        total_score = round(sum(score_breakdown.values()) / len(score_breakdown), 1)

        return {
            "query": query,
            "overall_score": total_score,
            "metrics": score_breakdown,
            "passed": total_score >= 85,
            "flags": flags
        }


# Singleton Instance
domain_training_engine = DomainTrainingEngine()

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    stats = domain_training_engine.get_dataset_statistics()
    print("=" * 60)
    print("MAKKAL AGENT AI - DOMAIN TRAINING ENGINE STATS")
    print("=" * 60)
    print(f"Total Samples: {stats['total_samples']}")
    print(f"Estimated Tokens: {stats['estimated_tokens']}")
    print(f"Domains Covered: {len(stats['domains'])}")
    for d, c in stats['domains'].items():
        print(f"  • {d}: {c} samples")
    print(f"Model Targets:")
    for m, c in stats['meta_model_distribution'].items():
        print(f"  • {m}: {c} samples")

    print("\nTesting Baseten fine-tuning export...")
    exp = domain_training_engine.export_baseten_fine_tuning_dataset()
    print(f"  ✓ Exported Train Set: {exp['train_samples']} samples ({exp['train_file']})")
    print(f"  ✓ Exported Eval Set:  {exp['eval_samples']} samples ({exp['eval_file']})")
    print("=" * 60)
