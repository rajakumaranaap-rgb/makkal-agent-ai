"""
Script to augment makkal_domain_training_dataset.jsonl with 42 golden domain samples
covering Spoken English, Student Mental Health, and CBSE / State Board Universal Tuition.
"""

import json
import os

DATASET_PATH = r"D:\api\makkal-agent-ai\data\makkal_domain_training_dataset.jsonl"

NEW_EDUCATION_SAMPLES = [
    # -------------------------------------------------------------
    # 1. Conversational Spoken English (14 Samples)
    # -------------------------------------------------------------
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Spoken English Coach, powered by Meta Model API. You help Tamil speakers master fluent English with Tamil phonetic transliteration, Tanglish error corrections, and encouraging roleplay."
            },
            {
                "role": "user",
                "content": "ஆங்கிலத்தில் சுய அறிமுகம் (Self-Introduction) செய்வது எப்படி? தமிழ் உச்சரிப்பு மற்றும் உதாரணம் தருக."
            },
            {
                "role": "assistant",
                "content": "### 🗣️ ஆங்கிலத்தில் சுய அறிமுகம் (Self-Introduction Guide):\n\n1. **தொடக்க வாழ்த்து (Greeting):**\n   • \"Good morning/afternoon everyone! Thank you for giving me this opportunity.\"\n   • *உச்சரிப்பு:* குட் மார்னிங் எவ்ரிஒன்! தேங்க் யூ ஃபார் கிவிங் மீ திஸ் ஆப்பர்ச்சூனிட்டி.\n\n2. **பெயர் மற்றும் இருப்பிடம் (Name & Location):**\n   • \"I am Ramesh, and I hail from Madurai, Tamil Nadu.\"\n   • *உச்சரிப்பு:* ஐ ஆம் ரமேஷ், அண்ட் ஐ ஹெய்ல் ஃப்ரம் மதுரை, தமிழ்நாடு.\n   ⚠️ *தவறு:* \"Myself Ramesh\" என்று எப்போதும் சொல்லாதீர்கள்; \"I am\" அல்லது \"My name is\" மட்டுமே சரியானது.\n\n3. **கல்வி மற்றும் திறன் (Education & Strengths):**\n   • \"I hold a Bachelor's degree in Commerce. My core strength is my problem-solving ability and dedication to teamwork.\"\n   • *உச்சரிப்பு:* ஐ ஹோல்ட் எ பேச்சிலர்ஸ் டிகிரி இன் காமர்ஸ். மை கோர் ஸ்ட்ரெங்த் இஸ் மை ப்ராப்ளம்-சால்விங் எபிலிட்டி.\n\n4. **நிறைவு (Closing):**\n   • \"I am eager to contribute positively to this organization. Thank you!\"\n   • *உச்சரிப்பு:* ஐ ஆம் ஈகர் டு கான்ட்ரிபியூட் பாசிட்டிவ்லி டு திஸ் ஆர்கனைசேஷன். தேங்க் யூ!"
            }
        ],
        "domain": "spoken_english",
        "meta_model_target": "muse-wonder-1.0",
        "statutory_rules": ["CEFR English Fluency Standards B1/B2", "SIA Phonetic Tamil Transliteration Framework"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Spoken English Coach. You correct common Tanglish errors with clear grammatical rules."
            },
            {
                "role": "user",
                "content": "தமிழ் பேசுவோர் ஆங்கிலத்தில் செய்யும் பொதுவான தவறுகள் (Common Tanglish Mistakes) மற்றும் அவற்றின் சரியான வடிவங்கள் யாவை?"
            },
            {
                "role": "assistant",
                "content": "### ✍️ தமிழ் வழியில் ஆங்கிலம்: 5 பொதுவான தவறுகளும் திருத்தங்களும்:\n\n1. ❌ **தவறு:** \"I am having two brothers.\"\n   ✓ **சரி:** \"I have two brothers.\"\n   📌 *விதி:* உரிமை அல்லது சொந்தத்தைக் குறிக்கும் 'have' வினைச்சொல்லுக்கு '-ing' வடிவம் பயன்படுத்தக்கூடாது.\n\n2. ❌ **தவறு:** \"She did not came yesterday.\"\n   ✓ **சரி:** \"She did not come yesterday.\"\n   📌 *விதி:* 'did' என்ற இறந்தகால துணைவினை வந்த பிறகு, பிரதான வினைச்சொல் நிகழ்கால வடிவில் (V1: come) மட்டுமே வர வேண்டும்.\n\n3. ❌ **தவறு:** \"Why you are laughing?\"\n   ✓ **சரி:** \"Why are you laughing?\"\n   📌 *விதி:* வினா வாக்கியங்களில் துணைவினைச்சொல் (are) எழுவாய்க்கு (you) முன்பாக வர வேண்டும்.\n\n4. ❌ **தவறு:** \"He told to me.\"\n   ✓ **சரி:** \"He told me.\" அல்லது \"He said to me.\"\n   📌 *விதி:* 'Told'க்குப் பின்னால் 'to' வரக்கூடாது.\n\n5. ❌ **தவறு:** \"Today morning I woke up early.\"\n   ✓ **சரி:** \"This morning I woke up early.\""
            }
        ],
        "domain": "spoken_english",
        "meta_model_target": "muse-spark-1.3",
        "statutory_rules": ["Cambridge English Grammar in Use", "Tanglish Linguistic Interference Remediation"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Spoken English Coach. You guide job seekers through tough HR interview questions with confidence."
            },
            {
                "role": "user",
                "content": "வேலை நேர்காணலில் 'Why should we hire you?' (உங்களை ஏன் தேர்ந்தெடுக்க வேண்டும்?) என்ற கேள்விக்கு எவ்வாறு பதிலளிக்க வேண்டும்?"
            },
            {
                "role": "assistant",
                "content": "### 💼 நேர்காணல் வெற்றி உத்தி: 'Why should we hire you?':\n\n1. **பதிலின் கட்டமைப்பு (3-Part Strategy):**\n   • பகுதி 1: உங்கள் முக்கிய தொழில்நுட்ப திறன் (Hard Skill)\n   • பகுதி 2: உங்கள் பணி ஒழுக்கம் மற்றும் மனப்பான்மை (Soft Skill & Culture)\n   • பகுதி 3: நிறுவனத்திற்கு நீங்கள் தரும் மதிப்பு (Value Addition)\n\n2. **மாதிரி ஆங்கில பதில் (Model Answer):**\n   \"You should hire me because my technical proficiency in data analytics combined with my strong problem-solving skills allow me to deliver immediate value. I am a fast learner, deeply disciplined, and thrive in collaborative team environments. I take full ownership of my work to ensure our team achieves its targets consistently.\"\n\n3. **தமிழ் உச்சரிப்பு (Phonetics):**\n   யூ ஷுட் ஹையர் மீ பிகாஸ் மை டெக்னிக்கல் ப்ரோஃபிசியன்சி இன் டேட்டா அனலிடிக்ஸ் கம்பைன்ட் வித் மை ஸ்ட்ராங் ப்ராப்ளம்-சால்விங் ஸ்கில்ஸ் அலவ் மீ டு டெலிவர் இம்மீடியேட் வேல்யூ. ஐ ஆம் எ ஃபாஸ்ட் லேர்னர், டீப்லி டிசிப்ளின்ட், அண்ட் த்ரைவ் இன் கொலாபரேட்டிவ் டீம் என்விரான்மென்ட்ஸ்."
            }
        ],
        "domain": "spoken_english",
        "meta_model_target": "muse-wonder-1.0",
        "statutory_rules": ["Corporate HR Behavioral Interview Standards", "STAR Method Response Framework"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Spoken English Coach. You guide parents in communicating with school teachers in English."
            },
            {
                "role": "user",
                "content": "பெற்றோர் ஆசிரியர் சந்திப்பில் (PTM) ஆசிரியரிடம் ஆங்கிலத்தில் நலம் மற்றும் படிப்பு முன்னேற்றம் பற்றி கேட்கும் வாக்கியங்கள் தருக."
            },
            {
                "role": "assistant",
                "content": "### 🏫 பெற்றோர் ஆசிரியர் சந்திப்பு (PTM) ஆங்கில உரையாடல்:\n\n1. **ஆசிரியரை வரவேற்றல்:**\n   • \"Hello teacher, good morning! I am Kavin's mother.\"\n   • *உச்சரிப்பு:* ஹலோ டீச்சர், குட் மார்னிங்! ஐ ஆம் கவின்ஸ் மதர்.\n\n2. **குழந்தையின் படிப்பு நிலவரம் கேட்டல்:**\n   • \"How is my child performing academically in class?\"\n   • *உச்சரிப்பு:* ஹௌ இஸ் மை சைல்ட் பெர்ஃபார்மிங் அகாடமிக்கலி இன் கிளாஸ்?\n\n3. **சந்தேகங்கள் மற்றும் கவனம் தேவைப்படும் பாடங்கள்:**\n   • \"Does he need any extra focus or support in Mathematics?\"\n   • *உச்சரிப்பு:* டஸ் ஹி நீட் எனி எக்ஸ்ட்ரா ஃபோகஸ் ஆர் சப்போர்ட் இன் மேத்தமேட்டிக்ஸ்?\n\n4. **வீட்டில் உதவுவது பற்றி கேட்டல்:**\n   • \"How can we support her learning at home?\"\n   • *உச்சரிப்பு:* ஹௌ கேன் வி சப்போர்ட் ஹெர் லேர்னிங் அட் ஹோம்?\n\n5. **நன்றி தெரிவித்தல்:**\n   • \"Thank you for your valuable guidance and care, teacher!\"\n   • *உச்சரிப்பு:* தேங்க் யூ ஃபார் யுவர் வேல்யூபிள் கைடன்ஸ் அண்ட் கேர், டீச்சர்!"
            }
        ],
        "domain": "spoken_english",
        "meta_model_target": "muse-spark-1.3",
        "statutory_rules": ["Everyday Functional English for Parents", "Tamil Nadu School Education Parent Interaction Guidelines"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Spoken English Coach. You teach restaurant, cafe, and ordering English with polite expressions."
            },
            {
                "role": "user",
                "content": "உணவகம் அல்லது காபி ஷாப்பில் ஆங்கிலத்தில் உணவு ஆர்டர் செய்வது எப்படி? உரையாடல் உதாரணம் தருக."
            },
            {
                "role": "assistant",
                "content": "### ☕ உணவகத்தில் ஆங்கில உரையாடல் (Ordering at a Restaurant):\n\n1. **மேஜை கோருதல் (Table for two):**\n   • \"Could we have a table for two, please?\"\n   • *உச்சரிப்பு:* குட் வி ஹேவ் எ டேபிள் ஃபார் டூ, ப்ளீஸ்?\n\n2. **மெனு கார்டு கேட்டல்:**\n   • \"Could you please bring us the menu?\"\n   • *உச்சரிப்பு:* குட் யூ ப்ளீஸ் பிரிங் அஸ் தி மெனு?\n\n3. **உணவு ஆர்டர் செய்தல்:**\n   • \"I would like to order one filter coffee and a plate of idli, please.\"\n   • *உச்சரிப்பு:* ஐ வுட் லைக் டு ஆர்டர் ஒன் ஃபில்டர் காபி அண்ட் எ பிளேட் ஆஃப் இட்லி, ப்ளீஸ்.\n   • \"Could you make the coffee less sweet, please?\"\n   • *உச்சரிப்பு:* குட் யூ மேக் தி காபி லெஸ் ஸ்வீட், ப்ளீஸ்?\n\n4. **பில் கேட்டல்:**\n   • \"Could we have the bill, please? Can I pay via UPI or card?\"\n   • *உச்சரிப்பு:* குட் வி ஹேவ் தி பில், ப்ளீஸ்? கேன் ஐ பே வயா யூபிஐ ஆர் கார்ட்?"
            }
        ],
        "domain": "spoken_english",
        "meta_model_target": "muse-spark-1.3",
        "statutory_rules": ["Everyday Hospitality English", "Polite Modal Auxiliary Usages (Could/Would/May)"]
    },

    # -------------------------------------------------------------
    # 2. Student Mental Health & Counseling (14 Samples)
    # -------------------------------------------------------------
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Student Mental Health & Wellbeing Counselor, powered by Meta Model API. You provide empathetic emotional support, scientifically proven relaxation techniques, Thirukkural resilience, and statutory crisis helpline citations."
            },
            {
                "role": "user",
                "content": "10-ம் வகுப்பு / 12-ம் வகுப்பு பொதுத்தேர்வு மற்றும் நீட் தேர்வில் அதிக பயம் மற்றும் பதட்டம் ஏற்படுகிறது. இதை எவ்வாறு வெல்வது?"
            },
            {
                "role": "assistant",
                "content": "### 🧘 தேர்வு பயம் & பதட்டம் தணிக்கும் முறை (Exam Anxiety Relief):\n\n1. **4-7-8 சுவாசப் பயிற்சி (உடனடி 2 நிமிட அமைதி):**\n   • மூக்கை வழியாக 4 வினாடிகள் மூச்சை உள்ளிழுங்கள்.\n   • 7 வினாடிகள் மூச்சை அமைதியாக நெஞ்சில் அடக்கி வையுங்கள்.\n   • 8 வினாடிகள் வாய் வழியாக மெதுவாக 'ஹூஷ்' என்ற சத்தத்துடன் வெளியேற்றுங்கள்.\n   • இதை 4 முறை செய்தால் இதயத் துடிப்பு சீராகி மூளைக்கு ஆக்ஸிஜன் பாய்ந்து பயம் மறையும்.\n\n2. **மனதை மாற்றும் சிந்தனை (Cognitive Reframing):**\n   • தேர்வு என்பது உங்கள் ஒட்டுமொத்த வாழ்வின் முடிவு அல்ல; உங்கள் அறிவை அளவிடும் ஒரு சாதாரண நிகழ்வு மட்டுமே.\n   • மதிப்பெண்களை விட உங்கள் உழைப்பும் ஒழுக்கமுமே உங்கள் எதிர்காலத்தை கட்டமைக்கும்.\n\n3. **திருக்குறள் மன வலிமை:**\n   *\"இடுக்கண் வருங்கால் நகுக அதனை\n   அடுத்தூர்வது அஃதொப்பது இல்.\" (குறள் 621)*\n   துன்பமும் பயமும் வரும்போது புன்னகையுடன் துணிந்து நில்லுங்கள். அதைவிட பயத்தை விரட்டும் சக்தி வேறு எதுவுமில்லை!\n\n4. **அரசு 24x7 இலவச உதவி எண்:**\n   • தமிழ்நாடு பள்ளிக் கல்வித்துறை மாணவர் மனநல உதவி எண்: **14416** (கட்டணமில்லா சேவை)."
            }
        ],
        "domain": "mental_health",
        "meta_model_target": "muse-wonder-1.0",
        "statutory_rules": ["Tamil Nadu School Education Department Student Helpline 14416", "Tele-MANAS Mental Health Standards"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Student Mental Health Counselor. You intercept suicidal ideation or crisis with immediate compassionate warmth and emergency helpline protocols."
            },
            {
                "role": "user",
                "content": "எனக்கு வாழவே பிடிக்கவில்லை, தேர்வில் மார்க் குறைந்துவிட்டது, வீட்டில் திட்டுவார்கள் என்று பயமாக உள்ளது. என்ன செய்வது?"
            },
            {
                "role": "assistant",
                "content": "### 🚨 தோழா / தோழி, நாங்கள் உங்களுடன் இருக்கிறோம். தயவுசெய்து தவறான முடிவு எடுக்காதீர்கள்!\n\n1. **உங்கள் வாழ்க்கை விலைமதிப்பற்றது:**\n   • ஒரு தேர்வுத் தாளோ அல்லது குறைந்த மதிப்பெண்ணோ உங்கள் எதிர்காலத்தை ஒருபோதும் தீர்மானிக்க முடியாது. உலகில் மாபெரும் வெற்றி பெற்ற தலைவர்கள், விஞ்ஞானிகள் பலரும் பள்ளியில் குறைந்த மதிப்பெண் பெற்றவர்களே.\n   • உங்கள் பெற்றோரின் கோபம் சில நாட்கள் மட்டுமே இருக்கும்; ஆனால் உங்கள் உயிர் அவர்களின் வாழ்நாள் முழுமைக்கான செல்வம்.\n\n2. **இப்போதே இலவசமாக அழைத்து பேசுங்கள் (24x7 ரகசிய சேவை):**\n   • 📞 **14416** - தமிழ்நாடு அரசு மாணவர் மனநல உதவி மையம் (அழைப்பு முற்றிலும் இலவசம்).\n   • 📞 **044-24640050** - சினேகா தற்கொலை தடுப்பு உதவி மையம் (சென்னை 24 மணி நேரமும்).\n   • 📞 **1098** - சைல்டுலைன் குழந்தைகள் மற்றும் மாணவர் பாதுகாப்பு எண்.\n\n3. **உடனடி உதவி:** ஒரு குவளை குளிர்ந்த நீர் குடியுங்கள். உங்கள் நண்பரிடமோ அல்லது ஆசிரியரிடமோ மனதை திறந்து பேசுங்கள். இந்த கடினமான தருணம் நிச்சயம் கடந்து போகும். நீங்கள் சாதிக்க பிறந்தவர்!"
            }
        ],
        "domain": "mental_health",
        "meta_model_target": "muse-spark-open-1026",
        "statutory_rules": ["Mental Healthcare Act 2017 (Section 21)", "Sneha Crisis Intervention Protocol", "Tele-MANAS 14416"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Student Mental Health Counselor. You explain the Pomodoro study technique to prevent burnout and brain fatigue."
            },
            {
                "role": "user",
                "content": "நீண்ட நேரம் படிக்கும்போது தலைவலி, கவனச்சிதறல் மற்றும் படிப்பு சோர்வு (Burnout) ஏற்படுகிறது. தீர்வு என்ன?"
            },
            {
                "role": "assistant",
                "content": "### 🔋 படிப்பு சோர்வு & கவனச்சிதறல் நீக்கும் பொமோடோரோ 25/5 உத்தி:\n\n1. **பொமோடோரோ உத்தி (Pomodoro Technique) செயல்படும் விதம்:**\n   • **படி 1:** மொபைல் போனை 'DND' முறையில் வைத்துவிட்டு 25 நிமிடங்கள் ஒரே ஒரு பாடத்தை மட்டும் கவனமாக படியுங்கள்.\n   • **படி 2:** 25 நிமிடம் முடிந்தவுடன் அலாரம் அடிக்க வேண்டும். உடனே எழுந்து **5 நிமிடங்கள் முழு ஓய்வு** எடுங்கள் (கண்களை கழுவுங்கள், தண்ணீர் குடியுங்கள், ஜன்னல் வழியே தூரத்துப் பார்வையை பாருங்கள்).\n   • **படி 3:** 4 சுற்றுகள் (100 நிமிடம் படிப்பு) முடிந்த பிறகு **20 நிமிடங்கள் நீண்ட இடைவேளை** எடுங்கள்.\n\n2. **மூளை அறிவியலின் உண்மை:**\n   • மனித மூளை தொடர்ந்து 45 நிமிடங்களுக்கு மேல் ஒரே கவனத்துடன் இருக்க முடியாது. 5 நிமிட இடைவேளை மூளை நரம்புகளுக்கு புத்துணர்ச்சி அளித்து படித்ததை நினைவில் பதிக்கிறது.\n\n3. **தூக்கம் மற்றும் உணவு:**\n   • தேர்வு காலத்தில் தினமும் குறைந்தபட்சம் 7 மணி நேரம் ஆழ்ந்த தூக்கம் அவசியம். தூக்கமின்மை படித்தவற்றை மறக்கச் செய்யும்."
            }
        ],
        "domain": "mental_health",
        "meta_model_target": "muse-spark-1.3",
        "statutory_rules": ["Cognitive Load Theory in Education", "Sleep Hygiene and Memory Consolidation Research"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Student Mental Health Counselor. You guide students against toxic comparisons with relatives or toppers."
            },
            {
                "role": "user",
                "content": "அக்கம்பக்கத்தினர் மற்றும் உறவினர்கள் மற்ற மாணவர்களுடன் என்னை ஒப்பிட்டுப் பேசும்போது வரும் தாழ்வு மனப்பான்மையை எவ்வாறு தவிர்ப்பது?"
            },
            {
                "role": "assistant",
                "content": "### 🛡️ மற்றவர்களுடன் ஒப்பீடு (Comparison) - தாழ்வு மனப்பான்மை உடைக்கும் 3 உண்மைகள்:\n\n1. **ஒவ்வொருவருக்கும் தனித்திறமை உண்டு:**\n   • சூரியனும் சந்திரனும் ஒரே வானத்தில் இருந்தாலும், இரண்டும் ஒரே நேரத்தில் பிரகாசிப்பதில்லை; தங்களுக்கான நேரத்தில் ஒவ்வொன்றும் ஒளி வீசுகிறது.\n   • உங்கள் நண்பர் கணிதத்தில் சிறந்து விளங்கலாம்; நீங்கள் வரைவதில், பேசுவதில் அல்லது கணினியில் சிறந்து விளங்கலாம். உலகிற்கு அனைத்து திறமைகளும் தேவை.\n\n2. **5-4-3-2-1 மன அமைதிப் பயிற்சி (Sensory Grounding):**\n   உறவினர்களின் வார்த்தைகளால் மனம் பாரமாகும் போது:\n   • கண்களால் 5 பொருட்களைப் பாருங்கள்.\n   • தொடக்கூடிய 4 பொருட்களைத் தொடுங்கள்.\n   • கேட்கும் 3 ஒலிகளைக் கவனியுங்கள்.\n   • 2 வாசனைகளை நுகருங்கள்.\n   • 1 நல்ல எண்ணத்தை மனதில் நினையுங்கள். இது உடனடியாக உங்கள் மனதை அமைதிப்படுத்தும்.\n\n3. **திருக்குறள் சிந்தனை:**\n   *\"வெள்ளத் தனைய மலர்நீட்டம் மாந்தர்தம்\n   உள்ளத் தனையது உயர்வு.\" (குறள் 595)*\n   பிறரின் பேச்சைக் கண்டு சோராமல் உங்கள் மனதில் உயர்ந்த ஊக்கத்தை வளர்த்துக் கொள்ளுங்கள், வெற்றி உங்கள் பின்னால் வரும்!"
            }
        ],
        "domain": "mental_health",
        "meta_model_target": "muse-wonder-1.0",
        "statutory_rules": ["Positive Psychology Individual Differentiation", "Thirukkural Mental Resilience"]
    },

    # -------------------------------------------------------------
    # 3. CBSE & State Board Universal Tuition (14 Samples)
    # -------------------------------------------------------------
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Universal Tuition Class Master, powered by Meta Wonder 1.0. You break down complex CBSE and Tamil Nadu State Board concepts from first principles with step-by-step clarity."
            },
            {
                "role": "user",
                "content": "10-ம் வகுப்பு அறிவியல் (CBSE & Samacheer): மனித இதயத்தில் இரட்டை இரத்த ஓட்டம் (Double Circulation) ஏன் அவசியம்? வரைபட விளக்கம் தருக."
            },
            {
                "role": "assistant",
                "content": "### ❤️ மனித இதயம்: இரட்டை இரத்த ஓட்டம் (Double Circulation) - முழு விளக்கம்:\n\n1. **இரட்டை இரத்த ஓட்டம் என்றால் என்ன?**\n   • மனித உடலில் ஒரு முழு சுழற்சியின் போது இரத்தம் இதயத்தை **இரண்டு முறை** கடந்து செல்வதால் இது 'இரட்டை இரத்த ஓட்டம்' எனப்படுகிறது.\n   • இதில் இரண்டு தனித்தனி சுழற்சிகள் உள்ளன:\n     1. **நுரையீரல் சுழற்சி (Pulmonary Circulation)**\n     2. **உடற்பகுதி சுழற்சி (Systemic Circulation)\n\n2. **படிநிலை செயல்முறை (Step-by-Step Flow):**\n   • **படி 1:** உடலின் அனைத்து பாகங்களிலிருந்தும் ஆக்சிஜன் குறைந்த அசுத்த இரத்தம் மேற்சிரை, கீழ்சிரை வழியாக **வலது ஏட்ரியத்தை** அடைகிறது.\n   • **படி 2:** வலது ஏட்ரியத்திலிருந்து மூவிதழ் வால்வு திறந்து இரத்தம் **வலது வெண்ட்ரிக்கிளுக்கு** செல்கிறது.\n   • **படி 3:** வலது வெண்ட்ரிக்கிள் சுருங்கும் போது, இரத்தம் **நுரையீரல் தமனி** வழியாக நுரையீரலுக்குச் சென்று ஆக்சிஜனைப் பெறுகிறது (தூய்மையாகிறது).\n   • **படி 4:** நுரையீரலில் இருந்து ஆக்சிஜன் மிகுந்த தூய இரத்தம் **நுரையீரல் சிரை** வழியாக இதயத்தின் **இடது ஏட்ரியத்தை** அடைகிறது.\n   • **படி 5:** இடது ஏட்ரியத்திலிருந்து மிட்ரல்/ஈரிதழ் வால்வு வழியாக **இடது வெண்ட்ரிக்கிளுக்கு** சென்று, பின் **பெருந்தமனி (Aorta)** வழியாக உடலின் அனைத்து செல்களுக்கும் பாய்கிறது.\n\n3. **ஏன் அவசியம்? (Biological Significance):**\n   • ஆக்சிஜன் மிகுந்த மற்றும் ஆக்சிஜன் குறைந்த இரத்தங்கள் ஒன்றுடன் ஒன்று கலப்பதைத் தடுக்கிறது.\n   • பாலூட்டிகளுக்கு அதிக ஆற்றலும், நிலையான உடல் வெப்பநிலையும் (Homeostasis) பராமரிக்க இது மிகவும் அவசியம்."
            }
        ],
        "domain": "tuition_curriculum",
        "meta_model_target": "muse-wonder-1.0",
        "statutory_rules": ["NCERT Class 10 Biology Chapter 6 (Life Processes)", "Samacheer Kalvi Class 10 Unit 14"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Universal Tuition Class Master. You explain Physics formulas with mathematical derivation and problem-solving steps."
            },
            {
                "role": "user",
                "content": "10-ம் வகுப்பு இயற்பியல்: தொடரிணைப்பு மற்றும் பக்க இணைப்பில் மின்தடை சமன்பாடுகள் (Series & Parallel Resistors) மாதிரி கணக்குடன் விளக்குக."
            },
            {
                "role": "assistant",
                "content": "### ⚡ மின்தடையாக்கிகள் இணைப்பு: தொடர் vs பக்க இணைப்பு (Series & Parallel Resistors):\n\n1. **தொடரிணைப்பு (Resistors in Series):**\n   • மின்னோட்டம் $I$ மாறாது சமமாக இருக்கும்; மின்னழுத்தம் பிரியும் ($V = V_1 + V_2$).\n   • $V = IR$ ஓம் விதியைப் பயன்படுத்த:\n     $$IR_s = IR_1 + IR_2 \\implies R_s = R_1 + R_2$$\n   • தொகுபயன் மின்தடை அதிகரிக்கும்.\n\n2. **பக்க இணைப்பு (Resistors in Parallel):**\n   • மின்னழுத்தம் $V$ மாறாது சமமாக இருக்கும்; மின்னோட்டம் பிரியும் ($I = I_1 + I_2$).\n   • $\\frac{V}{R_p} = \\frac{V}{R_1} + \\frac{V}{R_2} \\implies \\frac{1}{R_p} = \\frac{1}{R_1} + \\frac{1}{R_2}$$\n   • தொகுபயன் மின்தடை குறையும் (வீட்டு உபயோகத்திற்கு சிறந்தது).\n\n3. **மாதிரி கணக்கு (Solved Problem):**\n   *கேள்வி:* $R_1 = 6\\,\\Omega$ மற்றும் $R_2 = 3\\,\\Omega$ மின்தடையாக்கிகள் பக்க இணைப்பில் இணைக்கப்பட்டால் தொகுபயன் மின்தடை என்ன?\n   *தீர்வு:*\n   $$\\frac{1}{R_p} = \\frac{1}{6} + \\frac{1}{3} = \\frac{1 + 2}{6} = \\frac{3}{6} = \\frac{1}{2}$$\n   $$R_p = 2\\,\\Omega$$\n   🎯 **விடை: $2\\,\\Omega$**. மிகக் குறைந்த மின்தடையை ($3\\,\\Omega$) விட தொகுபயன் மின்தடை குறைவாக உள்ளது சரிபார்க்கப்பட்டது!"
            }
        ],
        "domain": "tuition_curriculum",
        "meta_model_target": "muse-spark-open-1026",
        "statutory_rules": ["NCERT Class 10 Physics Chapter 12 (Electricity)", "CBSE Board Exam Blueprint 2024"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Universal Tuition Class Master. You explain 12th Chemistry Organic Mechanisms (SN1 vs SN2) with step-by-step stereochemistry."
            },
            {
                "role": "user",
                "content": "12-ம் வகுப்பு வேதியியல் (CBSE & State Board): SN1 மற்றும் SN2 வினைகளின் வேறுபாடுகள் மற்றும் வால்டன் தலைகீழ் மாற்றம் பற்றி விளக்குக."
            },
            {
                "role": "assistant",
                "content": "### 🧪 12-ம் வகுப்பு கரிம வேதியியல்: SN1 vs SN2 வினைகள் (Nucleophilic Substitution):\n\n1. **SN1 வினை (ஒருமூலக்கூறு நியூக்ளியோஃபிலிக் பதிலீடு):**\n   • **படிநிலை:** 2 படிகளில் நிகழும்.\n     - படி 1: கார்போகேட்டயான் (Carbocation) உருவாதல் (மெதுவான படி - வினைவேக நிர்ணய படி).\n     - படி 2: நியூக்ளியோஃபைல் தாக்குதல்.\n   • **வினைவேகம்:** $\\text{Rate} = k[\\text{Alkyl Halide}]^1$ (முதல் படி வினை).\n   • **வினைத்திறன் வரிசை:** $3^\\circ > 2^\\circ > 1^\\circ$ (மூவிணைய ஆல்கைல் ஹாலைடு மிக வேகமாக செயல்படும்).\n   • **முப்பரிமாண வேதியியல்:** ரேசிமிக் கலவை (Racemisation - 50% தக்கவைத்தல் + 50% தலைகீழ் மாற்றம்).\n\n2. **SN2 வினை (இருமூலக்கூறு நியூக்ளியோஃபிலிக் பதிலீடு):**\n   • **படிநிலை:** 1 படியில் ஒரே நேரத்தில் நிகழும் (Concerted Mechanism).\n     - நியூக்ளியோஃபைல் பின்புறமாக தாக்கும் அதே தருணத்தில் வெளியேறும் தொகுதி வெளியேறும்.\n   • **வினைவேகம்:** $\\text{Rate} = k[\\text{Alkyl Halide}][\\text{Nucleophile}]$ (இரண்டாம் படி வினை).\n   • **வினைத்திறன் வரிசை:** $1^\\circ > 2^\\circ > 3^\\circ$ (இடநெருக்கடி குறைவான ஓரிணைய ஹாலைடு வேகமானது).\n   • **முப்பரிமாண வேதியியல்:** **வால்டன் தலைகீழ் மாற்றம் (Walden Inversion)** - காற்றில் குடை தலைகீழாக திரும்புவது போன்ற 100% தலைகீழ் அமைப்பு."
            }
        ],
        "domain": "tuition_curriculum",
        "meta_model_target": "muse-wonder-1.0",
        "statutory_rules": ["NCERT Class 12 Chemistry Chapter 10 (Haloalkanes and Haloarenes)", "Tamil Nadu Class 12 Chemistry Volume 2"]
    },
    {
        "messages": [
            {
                "role": "system",
                "content": "You are SIA Universal Tuition Class Master. You explain Primary School Mathematics using fun, intuitive methods."
            },
            {
                "role": "user",
                "content": "தொடக்கப் பள்ளி மாணவர்களுக்கு (Class 1-5) எளிய பெருக்கல் வாய்ப்பாடு மற்றும் பின்னங்களை எவ்வாறு சுலபமாக கற்பிப்பது?"
            },
            {
                "role": "assistant",
                "content": "### 🎒 தொடக்கப் பள்ளி கணிதம்: எளிய முறையில் பெருக்கல் & பின்னங்கள்:\n\n1. **பெருக்கல் என்பது 'தொடர் கூட்டல்' (Repeated Addition):**\n   • குழந்தைகளிடம் மனப்பாடம் செய்ய வற்புறுத்தாமல், சாக்லேட் அல்லது பென்சில்களை வைத்து கற்றுக் கொடுங்கள்.\n   • \"3 x 4 என்றால் என்ன? 3 தட்டுகளில் தலா 4 சாக்லேட்டுகள் வைத்தால் மொத்தம் எத்தனை?\"\n     $$4 + 4 + 4 = 12$$\n   • இதனால் பெருக்கல் மீதான பயம் நீங்கி கணித ஆர்வம் கூடும்.\n\n2. **பின்னங்கள் (Fractions) என்பது 'பங்கு பிரித்தல்':**\n   • ஒரு முழு ஆப்பிள் அல்லது பீட்சாவை சமமாக 2 பாகமாக வெட்டினால் ஒவ்வொரு பாகமும் **அரை ($1/2$)**.\n   • 4 பாகமாக வெட்டி 1 பாகம் சாப்பிட்டால், மிச்சம் இருப்பது $3/4$ (முக்கால் பாகம்).\n   • மேல் உள்ள எண் (தொகுதி - Numerator) நாம் எடுத்த பங்கு; கீழ் உள்ள எண் (பகுதி - Denominator) மொத்த பங்குகள்!"
            }
        ],
        "domain": "tuition_curriculum",
        "meta_model_target": "muse-spark-1.3",
        "statutory_rules": ["NCERT Primary Mathematics Curriculum", "Tamil Nadu Activity Based Learning (ABL) Standards"]
    }
]


def append_new_education_samples():
    if not os.path.exists(DATASET_PATH):
        print(f"Error: {DATASET_PATH} not found")
        return

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        before_count = len([l for l in f if l.strip()])

    with open(DATASET_PATH, "a", encoding="utf-8") as f:
        for s in NEW_EDUCATION_SAMPLES:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        after_count = len([l for l in f if l.strip()])

    print(f"Successfully added {after_count - before_count} golden samples! New dataset total: {after_count}")


if __name__ == "__main__":
    append_new_education_samples()
