"""
Update get_domain_grounding_prompt in domain_training_engine.py
"""

import sys

FILE_PATH = r"D:\api\makkal-agent-ai\domain_training_engine.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''        for sample in self._samples:
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

        for _, sample in scored_samples[:6]:
            asst_msg = next((m["content"] for m in sample.get("messages", []) if m["role"] == "assistant"), "")
            for line in asst_msg.split("\\n"):
                if any(marker in line for marker in ["₹", "இலவசம்", "கட்டணம்", "SLA", "பிரிவு", "சட்டம்", "TNAU", "TNSB", "விதி", "OTP", "கி.மீ"]):
                    clean_l = line.strip().lstrip("•-* ")
                    if clean_l and len(clean_l) > 5 and clean_l not in matched_rules:
                        matched_rules.append("• " + clean_l)
            for st in sample.get("statutory_rules", []):
                if st not in matched_statutes:
                    matched_statutes.append(st)'''

new_block = '''        for sample in self._samples:
            user_msg = next((m["content"] for m in sample.get("messages", []) if m["role"] == "user"), "")
            u_clean = user_msg.lower()
            score = 0

            # Match target domain
            if target_domain:
                if any(k in u_clean for k in domain_keywords[target_domain]):
                    score += 10

            # Specific phrase boosts
            if "உட்பிரிவு உள்ள" in clean_q and "உட்பிரிவு உள்ள" in u_clean:
                score += 30
            elif "உட்பிரிவு இல்லாத" in clean_q and "உட்பிரிவு இல்லாத" in u_clean:
                score += 30

            # Token overlap
            query_words = set(clean_q.split())
            sample_words = set(u_clean.split())
            overlap = len(query_words & sample_words)
            score += overlap * 2

            if score > 0:
                scored_samples.append((score, sample))

        scored_samples.sort(key=lambda x: x[0], reverse=True)

        fee_rules: List[str] = []
        general_rules: List[str] = []
        matched_statutes: List[str] = []

        for _, sample in scored_samples[:5]:
            asst_msg = next((m["content"] for m in sample.get("messages", []) if m["role"] == "assistant"), "")
            for line in asst_msg.split("\\n"):
                clean_l = line.strip().lstrip("•-* ")
                if not clean_l or clean_l.startswith("#") or clean_l.endswith(":") or len(clean_l) < 8:
                    continue
                if any(marker in clean_l for marker in ["₹", "இலவசம்", "கட்டணம்", "SLA", "பிரிவு", "சட்டம்", "TNAU", "TNSB", "விதி", "OTP", "கி.மீ", "ரூ."]):
                    rule_entry = "• " + clean_l
                    if any(c in clean_l for c in ["₹", "இலவசம்", "ரூ."]):
                        if rule_entry not in fee_rules:
                            fee_rules.append(rule_entry)
                    elif rule_entry not in general_rules:
                        general_rules.append(rule_entry)
            for st in sample.get("statutory_rules", []):
                if st not in matched_statutes:
                    matched_statutes.append(st)

        matched_rules = fee_rules + general_rules'''

if old_block in content:
    content = content.replace(old_block, new_block, 1)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Successfully updated domain_training_engine.py with fee prioritization and phrase boosting!")
else:
    print("Old block not found. Checking normalized...")
    # normalized replace
    import re
    # write via lines
    print("Writing directly...")
