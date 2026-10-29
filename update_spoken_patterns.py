"""
Script to refine COMMON_ERRORS_TAMIL_USERS in spoken_english_coach.py
"""

import sys

FILE_PATH = r"D:\api\makkal-agent-ai\spoken_english_coach.py"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''COMMON_ERRORS_TAMIL_USERS = [
    {"mistake": "I am having two brothers.", "correction": "I have two brothers.", "rule_ta": "'Have' என்பது உடைமையைக் குறிக்கும் போது '-ing' வராது."},
    {"mistake": "She did not came yesterday.", "correction": "She did not come yesterday.", "rule_ta": "'Did' வந்த பிறகு பிரதான வினைச்சொல் நிகழ்கால வடிவில் (V1: come) மட்டுமே வர வேண்டும்."},
    {"mistake": "Myself Suresh.", "correction": "I am Suresh. / My name is Suresh.", "rule_ta": "அறிமுகத்தில் 'Myself' எழுவாயாக (Subject) வரக்கூடாது."},
    {"mistake": "Why you are late?", "correction": "Why are you late?", "rule_ta": "கேள்வி வாக்கியங்களில் துணை வினைச்சொல் (are) எழுவாய்க்கு (you) முன் வர வேண்டும்."},
    {"mistake": "I told to him.", "correction": "I told him. / I said to him.", "rule_ta": "'Told' பின்னால் 'to' வரக்கூடாது."}
]'''

new_block = '''COMMON_ERRORS_TAMIL_USERS = [
    {"pattern": "am having", "correction": "have (e.g. I have a brother)", "rule_ta": "'Have' என்பது உடைமையைக் குறிக்கும் போது '-ing' வராது."},
    {"pattern": "did not came", "correction": "did not come", "rule_ta": "'Did' வந்த பிறகு பிரதான வினைச்சொல் நிகழ்கால வடிவில் (come) மட்டுமே வர வேண்டும்."},
    {"pattern": "did not went", "correction": "did not go", "rule_ta": "'Did' வந்த பிறகு go மட்டுமே வர வேண்டும்."},
    {"pattern": "myself ", "correction": "I am / My name is", "rule_ta": "அறிமுகத்தில் 'Myself' பயன்பாடு தவறானது, 'I am' அல்லது 'My name is' மட்டுமே பயன்படுத்தவும்."},
    {"pattern": "why you are", "correction": "why are you", "rule_ta": "கேள்வி வாக்கியங்களில் 'Why are you' என துணைவினைச்சொல் முன்னே வர வேண்டும்."},
    {"pattern": "told to", "correction": "told / said to", "rule_ta": "'Told' பின்னால் 'to' வரக்கூடாது."}
]'''

eval_old = '''    spoken_lower = clean_spoken.lower()
    for err in COMMON_ERRORS_TAMIL_USERS:
        if err["mistake"].lower() in spoken_lower:
            corrections.append({
                "found_error": err["mistake"],
                "proper_correction": err["correction"],
                "rule_tamil": err["rule_ta"]
            })
            score = max(50, score - 20)'''

eval_new = '''    spoken_lower = clean_spoken.lower()
    for err in COMMON_ERRORS_TAMIL_USERS:
        if err["pattern"] in spoken_lower:
            corrections.append({
                "found_error": err["pattern"],
                "proper_correction": err["correction"],
                "rule_tamil": err["rule_ta"]
            })
            score = max(50, score - 20)'''

if old_block in content:
    content = content.replace(old_block, new_block, 1)
if eval_old in content:
    content = content.replace(eval_old, eval_new, 1)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated spoken_english_coach.py with flexible pattern matching!")
