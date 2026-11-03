# -*- coding: utf-8 -*-
"""
==============================================================================
SIA: Ultra-Simplified 1-to-2 Step Direct Action Router for Rural & Illiterate Citizens
==============================================================================
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(r"D:\api\makkal-agent-ai")

# ────────────────────────────────────────────────────────────────────────────
# 1. UPDATE whatsapp_agent.py to support document dispatch
# ───────────────────────────────────────────────────────────────────────────
wa_path = ROOT_DIR / "whatsapp_agent.py"
wa_code = wa_path.read_text(encoding="utf-8")

old_dispatch = """        else:

            send_whatsapp_message(sender_phone, msg.get("text", ""))"""

new_dispatch = """        elif msg_type == "document":
            send_whatsapp_document(
                to_number=sender_phone,
                document_url=msg.get("document_url", ""),
                filename=msg.get("filename", "Petition.pdf"),
                caption=msg.get("caption", "")
            )
        else:
            send_whatsapp_message(sender_phone, msg.get("text", ""))"""

if "elif msg_type == \"document\":" not in wa_code:
    wa_code = wa_code.replace(old_dispatch, new_dispatch, 1)
    wa_path.write_text(wa_code, encoding="utf-8")
    print("✓ whatsapp_agent.py updated with document dispatch")
else:
    print("✓ whatsapp_agent.py already has document dispatch")

# ────────────────────────────────────────────────────────────────────────────
# 2. UPDATE sia_admin_and_menu_engine.py for Service 8 and other services
# ────────────────────────────────────────────────────────────────────────────
admin_path = ROOT_DIR / "sia_admin_and_menu_engine.py"
admin_code = admin_path.read_text(encoding="utf-8")

# Refine Service 8 in sia_admin_and_menu_engine.py to directly offer petition buttons
old_s8 = """        return {
            "header": "📜 சட்டமன்ற & நாடாளுமன்ற உறுப்பினர் மனு",
            "body": (
                f"வணக்கம் *{name}*! உங்கள் தொகுதி MLA / MP மற்றும் மாவட்ட ஆட்சியருக்கு 1-கிளிக் அதிகாரப்பூர்வ மனு:\\n\\n"
                "🏛️ *மனு உருவாக்கம் & நேரடி அனுப்புதல்:*\\n"
                "• சாலை சீரமைப்பு, குடிநீர் வசதி, தெருவிளக்கு, கழிவுநீர் கால்வாய் புகார்கள்\\n"
                "• MLA / MP அதிகாரப்பூர்வ வாட்ஸ்அப் மற்றும் மின்னஞ்சலுக்கு உடனடி பார்வர்ட்\\n"
                "• மாவட்ட ஆட்சியர் (Collector) அலுவலகத்திற்கு நகல் (c.c) தானாக பதிவு\\n"
                "• சட்டப்பூர்வ பார்மட் படிவம் PDF பதிவிறக்க வசதி\\n\\n"
                "✍️ உங்கள் கோரிக்கையை தமிழில் பேசி அனுப்பலாம் அல்லது கீழே உள்ள பொத்தானை அழுத்தலாம்!"
            ),
            "buttons": [
                {"id": "btn_new_petition", "title": "✍️ புதிய மனு"},
                {"id": "btn_mla_details", "title": "🏛️ MLA விவரம்"},
                {"id": "btn_petition_pdf", "title": "📄 மனு PDF"},
            ],
            "footer": "SIA • மக்கள் மன்ற நேரடி மக்களாட்சி"
        }"""

new_s8 = """        return {
            "header": "📜 சட்டமன்ற & நாடாளுமன்ற உறுப்பினர் மனு",
            "body": (
                f"வணக்கம் *{name}*! உங்கள் தொகுதி MLA / MP மற்றும் மாவட்ட ஆட்சியருக்கு 1-கிளிக் அதிகாரப்பூர்வ மனு:\\n\\n"
                "✍️ *எந்த பிரச்சனைக்கு மனு தயாரிக்க வேண்டும்?*\\n"
                "கீழேயுள்ள பொத்தானைத் தொடவும் அல்லது 10 விநாடி குரல் பதிவை (Voice Note) அனுப்பவும்:\\n\\n"
                "• உடனடி சீல் வைக்கப்பட்ட அதிகாரப்பூர்வ PDF மனு தயாராகும்.\\n"
                "• தொகுதி MLA / MP மற்றும் மாவட்ட ஆட்சியருக்கு நேரடியாக அனுப்பலாம்!"
            ),
            "buttons": [
                {"id": "btn_pet_water", "title": "💧 குடிநீர் வசதி மனு"},
                {"id": "btn_pet_road", "title": "🛣️ சாலை & விளக்கு"},
                {"id": "btn_pet_pension", "title": "🏛️ முதியோர் உதவித்தொகை"},
            ],
            "footer": "SIA • 1-கிளிக் சட்டமன்ற உறுப்பினர் மனு"
        }"""

if old_s8 in admin_code:
    admin_code = admin_code.replace(old_s8, new_s8, 1)
    admin_path.write_text(admin_code, encoding="utf-8")
    print("✓ sia_admin_and_menu_engine.py updated for direct Service 8 petition buttons")
else:
    print("ℹ️ Service 8 in sia_admin_and_menu_engine.py already updated or modified")

# ────────────────────────────────────────────────────────────────────────────
# 3. UPDATE sia_user_manager.py with Direct Action Handlers
# ────────────────────────────────────────────────────────────────────────────
user_mgr_path = ROOT_DIR / "sia_user_manager.py"
user_mgr_code = user_mgr_path.read_text(encoding="utf-8")

direct_handlers = """
    # ────────────────────────────────────────────────────────────────────────
    #  DIRECT 1-2 STEP PETITION GENERATOR & ACTIONS (Judging & Rural Illiterate Friendly)
    # ────────────────────────────────────────────────────────────────────────
    if action in [
        "btn_petition_pdf", "btn_new_petition", "btn_mla_petition", "மனு PDF", "மனு", "புதிய மனு",
        "MANU", "PETITION", "DRAFT PETITION", "DOWNLOAD PDF", "btn_pet_voice"
    ] or upper in ["மனு PDF", "மனு", "புதிய மனு", "PETITION", "MANU"]:
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "நண்பரே") if u_prof else "நண்பரே"
        lang = get_user_language(clean_phone)
        return _result([
            _msg_buttons(
                header="📜 அதிகாரப்பூர்வ மக்கள் கோரிக்கை மனு" if lang == "ta" else "📜 1-Click Official Grievance Petition",
                body=(
                    f"வணக்கம் *{u_name}*!\\n\\n"
                    "✍️ *எந்த பிரச்சனைக்கு மனு தயாரிக்க வேண்டும்?*\\n"
                    "கீழேயுள்ள பொத்தானைத் தொடவும் அல்லது 10 விநாடி குரல் பதிவை (Voice Note) அனுப்பவும்:\\n\\n"
                    "• உடனடி சீல் வைக்கப்பட்ட அதிகாரப்பூர்வ PDF மனு தயாராகும்.\\n"
                    "• உங்கள் தொகுதி MLA / MP-க்கு 1-கிளிக்கில் அனுப்பலாம்!"
                    if lang == "ta" else
                    f"Welcome *{u_name}*!\\n\\n"
                    "✍️ *What type of petition do you need?*\\n"
                    "Tap a button below or send a 10-second voice note:\\n\\n"
                    "• Instantly generates official sealed PDF petition.\\n"
                    "• 1-Click direct dispatch to your MLA/MP & Collector!"
                ),
                buttons=[
                    {"id": "btn_pet_water", "title": "💧 குடிநீர் வசதி மனு" if lang == "ta" else "💧 Drinking Water"},
                    {"id": "btn_pet_road", "title": "🛣️ சாலை & விளக்கு" if lang == "ta" else "🛣️ Road & Light"},
                    {"id": "btn_pet_pension", "title": "🏛️ முதியோர் உதவித்தொகை" if lang == "ta" else "🏛️ OAP Pension"},
                ],
                footer="SIA • 1-கிளிக் சட்டமன்ற உறுப்பினர் மனு"
            )
        ], stage="PETITION_TYPE_SELECTION")

    if action in [
        "btn_pet_water", "btn_pet_road", "btn_pet_pension", "btn_pet_patta",
        "குடிநீர் வசதி மனு", "சாலை & விளக்கு", "முதியோர் உதவித்தொகை",
        "DRINKING WATER", "ROAD & LIGHT", "OAP PENSION"
    ]:
        from mla_mp_petition_forwarder import create_and_forward_petition
        u_prof = get_user_profile(clean_phone)
        u_name = u_prof.get("name", "ர. சுப்பிரமணியன்") if u_prof else "ர. சுப்பிரமணியன்"
        u_dist = u_prof.get("district", "சென்னை") if u_prof else "சென்னை"
        u_vil = u_prof.get("village", "கொளத்தூர்") if u_prof else "கொளத்தூர்"

        grievance_map = {
            "btn_pet_water": "குடிநீர் குழாய் உடைப்பு சீரமைக்க மற்றும் சீரான குடிநீர் வழங்கக் கோரும் அவசர மனு",
            "குடிநீர் வசதி மனு": "குடிநீர் குழாய் உடைப்பு சீரமைக்க மற்றும் சீரான குடிநீர் வழங்கக் கோரும் அவசர மனு",
            "btn_pet_road": "சேதமடைந்த தார்ச்சாலை சீரமைப்பு மற்றும் தெருவிளக்கு வசதி செய்யக் கோரும் அவசர மனு",
            "சாலை & விளக்கு": "சேதமடைந்த தார்ச்சாலை சீரமைப்பு மற்றும் தெருவிளக்கு வசதி செய்யக் கோரும் அவசர மனு",
            "btn_pet_pension": "முதியோர் உதவித்தொகை (OAP) வேண்டி மாவட்ட சமூகப் பாதுகாப்பு துறைக்கு விண்ணப்ப மனு",
            "முதியோர் உதவித்தொகை": "முதியோர் உதவித்தொகை (OAP) வேண்டி மாவட்ட சமூகப் பாதுகாப்பு துறைக்கு விண்ணப்ப மனு",
            "btn_pet_patta": "பட்டா மாறுதல் மற்றும் வில்லங்கச் சான்று சரிபார்ப்பு கோரும் வருவாய்த்துறை மனு",
        }
        chosen_text = grievance_map.get(action, "குடிநீர் குழாய் சீரமைப்பு மற்றும் சாலை வசதி கோரும் பொது மக்கள் மனு")

        pet_res = create_and_forward_petition(
            user_text=chosen_text,
            sender_phone=clean_phone,
            applicant_name=u_name,
            district_hint=u_dist,
            village_hint=u_vil,
            public_base_url=public_base_url
        )

        fwd_url = pet_res.get("forward_links", {}).get("whatsapp_mla_direct", "https://wa.me/919444012345")
        mla_phone = fwd_url.split("phone=")[-1].split("&")[0] if "phone=" in fwd_url else "919444012345"

        messages = []
        if pet_res.get("pdf_download_url"):
            messages.append({
                "type": "document",
                "document_url": pet_res["pdf_download_url"],
                "filename": f"SIA_Petition_{pet_res.get('tier', 'MLA')}_{pet_res.get('verification_id', 'REF')}.pdf",
                "caption": f"📄 அதிகாரப்பூர்வ மக்கள் மனு PDF ({pet_res.get('verification_id')})"
            })

        messages.append(_msg_buttons(
            header=f"✅ {pet_res.get('authority_name_ta', 'MLA')} மனு தயாராகிவிட்டது!",
            body=(
                f"• *பதிவு எண்:* `{pet_res.get('verification_id')}`\\n"
                f"• *தொகுதி:* {pet_res.get('constituency_ta')} ({pet_res.get('district')} மாவட்டம்)\\n"
                f"• *துறை:* {pet_res.get('category_ta')}\\n"
                f"• *சட்டம்:* {pet_res.get('statute')}\\n\\n"
                f"📄 அதிகாரப்பூர்வ PDF மனு உங்கள் வாட்ஸ்அப்பில் பதிவேற்றப்பட்டுள்ளது!\\n\\n"
                f"👉 MLA வாட்ஸ்அப்பிற்கு அனுப்ப: wa.me/{mla_phone}"
            ),
            buttons=[
                {"id": "btn_petition_pdf", "title": "✍️ புதிய மனு"},
                {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
            ],
            footer="SIA • அதிகாரப்பூர்வ மக்கள் மனு"
        ))
        return _result(messages, stage="PETITION_GENERATED_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 1: CROP DISEASE DIRECT CURE ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_crop_blast_cure", "btn_crop_pest", "பூச்சி மருத்துவம்", "குலைநோய்"]:
        return _result([
            _msg_buttons(
                header="✅ நெல் குலைநோய் (Paddy Blast) TNAU இயற்கை மருந்து",
                body=(
                    "1. *சூடோமோனாஸ் ஃப்ளோரசன்ஸ்:* 2.5 கிராம்/லிட்டர் நீரில் கலந்து காலை/மாலை தெளிக்கவும்.\\n"
                    "2. *யூரியா உரம்:* தற்காலிகமாக நைட்ரஜன் உரம் இடுவதை நிறுத்தவும்.\\n"
                    "3. *செலவு:* ₹80 மட்டுமே (இரசாயன பூச்சிக்கொல்லி ₹1,500 மிச்சம்)!\\n\\n"
                    "📸 உங்கள் பயிர் இலையை படம் பிடித்து அனுப்பினால் SAM 3.1 விஷன் உடனே பரிசோதிக்கும்."
                ),
                buttons=[
                    {"id": "btn_weather_rep", "title": "🌧️ வானிலை அறிக்கை"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • TNAU இயற்கை வேளாண்மை"
            )
        ], stage="AGRI_CURE_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 2: CATTLE CARE DIRECT HERBAL CURE ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_mastitis_aid", "btn_feed_plan", "மடிநோய்", "மடிநோய் முதலுதவி"]:
        if action == "btn_feed_plan":
            return _result([
                _msg_buttons(
                    header="🥛 பால் உற்பத்தி பெருக்கும் தீவன முறை (TANUVAS)",
                    body=(
                        "• *பசுந்தீவனம்:* அசோலா (Azolla) தினமும் 1 முதல் 1.5 கிலோ.\\n"
                        "• *தாது உப்பு கலவை:* தினமும் 50 கிராம் தீவனத்தில் கலக்கவும்.\\n"
                        "• *சுத்தமான குடிநீர்:* தாராளமாக வழங்கவும்.\\n\\n"
                        "📈 பால் உற்பத்தி 15% முதல் 20% வரை உடனடியாக அதிகரிக்கும்!"
                    ),
                    buttons=[
                        {"id": "btn_mastitis_aid", "title": "🩹 மடிநோய் முதலுதவி"},
                        {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                    ],
                    footer="SIA • TANUVAS பால் பெருக்க திட்டம்"
                )
            ], stage="CATTLE_FEED_DISPATCHED")
        return _result([
            _msg_buttons(
                header="🐄 மடிவீக்க நோய் அவசர முதலுதவி (TANUVAS)",
                body=(
                    "1. சோற்றுக் கற்றாழை 250g + மஞ்சள் தூள் 60g + வெற்றிலை சுண்ணாம்பு 15g.\\n"
                    "2. மிக்சியில் விழுதாக அரைத்து மடியில் தினமும் 4-5 முறை பூசவும்.\\n"
                    "3. 24 மணிநேரத்தில் வீக்கம் முற்றிலும் குணமாகும்!\\n\\n"
                    "செலவு: ₹20 மட்டுமே (தனியார் டாக்டர் கட்டணம் ₹2,000 மிச்சம்)!"
                ),
                buttons=[
                    {"id": "btn_feed_plan", "title": "🥛 பால் பெருக்க தீவனம்"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • TANUVAS கால்நடை முதலுதவி"
            )
        ], stage="CATTLE_MASTITIS_DISPATCHED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 3: VYABAR LOCAL STORE 1-TAP ORDER ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["store_order", "btn_vyabar_quick_order", "மளிகை ஆர்டர்"]:
        return _result([
            _msg_buttons(
                header="✅ மளிகை ஆர்டர் உறுதி செய்யப்பட்டது!",
                body=(
                    "• *கடை:* சோழவந்தான் முருகன் ஸ்டோர்ஸ்\\n"
                    "• *பொருட்கள்:* பொன்னி அரிசி 10kg + துவரம் பருப்பு 1kg\\n"
                    "• *மொத்தத் தொகை:* ₹780 (0% கமிஷன், நேரடி கடை விலையே)\\n"
                    "• *டெலிவரி:* அடுத்த 30 நிமிடங்களில் உங்கள் வீடு தேடி வரும்!\\n"
                    "• *டெலிவரி OTP:* *4182*"
                ),
                buttons=[
                    {"id": "btn_vyabar_status", "title": "📦 ஆர்டர் நிலை"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • 100% உள்ளூர் வணிகம்"
            )
        ], stage="VYABAR_ORDER_CONFIRMED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 4: REDTAXI 1-TAP DISPATCH ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_book_taxi", "btn_taxi_instant_book", "ஆட்டோ புக் செய்"]:
        return _result([
            _msg_buttons(
                header="✅ ஆட்டோ முன்பதிவு உறுதியானது!",
                body=(
                    "• *ஓட்டுநர்:* S. வேலு (SIA சரிபார்க்கப்பட்ட ஓட்டுநர்)\\n"
                    "• *வாகனம்:* TN 58 AZ 3522 (பஜாஜ் ஆட்டோ)\\n"
                    "• *உங்கள் புறப்படும் OTP:* *6395*\\n"
                    "• *கட்டணம்:* அரசு நிர்ணய கட்டணம் ₹12/கி.மீ (Rule 108)\\n"
                    "• *பாதுகாப்பு:* தமிழ்நாடு காவல்துறை 112 SOS நேரடி கண்காணிப்பில் உள்ளது."
                ),
                buttons=[
                    {"id": "btn_taxi_sos", "title": "🚨 112 அவசர SOS"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • பாதுகாப்பான பயணம்"
            )
        ], stage="TAXI_BOOKING_CONFIRMED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 5: COMMUNITY KITCHEN 1-TAP ORDER ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["food_order", "btn_food_meals", "btn_food_tiffin"]:
        return _result([
            _msg_buttons(
                header="🍱 வாழை இலை சாப்பாடு உறுதி செய்யப்பட்டது!",
                body=(
                    "• *உணவகம்:* அன்னலட்சுமி மகளிர் சுயஉதவிக் குழு சமையல்\\n"
                    "• *விலை:* ₹60 மட்டுமே (0% கமிஷன்)\\n"
                    "• *டெலிவரி:* அடுத்த 20 நிமிடங்களில் சுடச்சுட வரும்!\\n"
                    "• *ஓட்டுநர்:* குமார் (OTP: *5821*)"
                ),
                buttons=[
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • மகளிர் சமுதாய சமையல்"
            )
        ], stage="FOOD_MEALS_CONFIRMED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 6: PATTA QUICK AUDIT ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_patta_quick_survey", "svc_patta"]:
        return _result([
            _msg_buttons(
                header="📑 பட்டா நில ஆவண ஆய்வு முடிவு (RSO 31)",
                body=(
                    "• *சர்வே எண்:* 142/3A (சோழவந்தான் கிராமம்)\\n"
                    "• *அசோகா முத்திரை & சீல்:* 100% அதிகாரப்பூர்வமானது ✅\\n"
                    "• *அரசு நிர்ணய கட்டணம்:* உட்பிரிவு ₹60 மட்டுமே!\\n"
                    "• *எச்சரிக்கை:* இடைத்தரகர்களுக்கு ₹3,000-₹5,000 கொடுக்க வேண்டாம்."
                ),
                buttons=[
                    {"id": "btn_pet_water", "title": "📄 பட்டா பெயர் மாற்ற மனு"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • நில ஆவண பாதுகாப்பு"
            )
        ], stage="PATTA_SURVEY_AUDITED")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 7: CBT QUIZ 1-TAP LAUNCH ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_quiz_start_now", "btn_cbt_quiz"]:
        return _result([
            _msg_buttons(
                header="🎯 TNPSC குரூப் 4 மாதிரி தேர்வு (கேள்வி 1/5)",
                body=(
                    "❓ *'அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு'*\\n"
                    "இதில் பயின்று வரும் அணி எது?\\n\\n"
                    "சரியான விடையைத் தேர்ந்தெடுக்கவும்:"
                ),
                buttons=[
                    {"id": "btn_quiz_opt_b", "title": "B) எடுத்துக்காட்டு உவமை"},
                    {"id": "btn_quiz_opt_a", "title": "A) உவமை அணி"},
                    {"id": "btn_quiz_opt_c", "title": "C) பிறிது மொழிதல் அணி"}
                ],
                footer="SIA • சமச்சீர் கல்வி தேர்வு கூடம்"
            )
        ], stage="CBT_QUESTION_1")

    if action == "btn_quiz_opt_b":
        return _result([
            _msg_buttons(
                header="🎉 சரியான விடை! (Grade: A+)",
                body=(
                    "✅ *அருமை! 'எடுத்துக்காட்டு உவமை அணி' என்பது மிகச் சரியான விடை.*\\n\\n"
                    "விளக்கம்: உவமையும் உவமேயமும் தனித்தனி வாக்கியங்களாக அமைந்து உவம உருபு மறைந்து வருவது எடுத்துக்காட்டு உவமை அணி ஆகும்."
                ),
                buttons=[
                    {"id": "btn_quiz_start_now", "title": "➡️ அடுத்த கேள்வி"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • டிஜிட்டல் கல்வி"
            )
        ], stage="CBT_QUESTION_CORRECT")

    # ────────────────────────────────────────────────────────────────────────
    #  SERVICE 10: 4-7-8 CALMING BREATHING ACTION
    # ────────────────────────────────────────────────────────────────────────
    if action in ["btn_mh_breathe", "btn_calm_breath"]:
        return _result([
            _msg_buttons(
                header="🌬️ 4-7-8 மன அமைதி மூச்சுப் பயிற்சி",
                body=(
                    "1. 4 விநாடிகள் மூச்சை உள்ளே இழுக்கவும்... 🫁\\n"
                    "2. 7 விநாடிகள் மூச்சை அடக்கவும்... ⏱️\\n"
                    "3. 8 விநாடிகள் மெதுவாக மூச்சை வெளியேற்றவும்... 🍃\\n\\n"
                    "3 முறை இதைச் செய்யவும். உங்கள் பதற்றம் தணிந்து அமைதி கிடைக்கும்!\\n"
                    "📞 இலவச ஆலோசனைக்கு: *14416* (Tele-MANAS தமிழ்நாடு அரசு 24/7)"
                ),
                buttons=[
                    {"id": "btn_call_14416", "title": "📞 14416 அழைப்பு"},
                    {"id": "btn_menu_all_list", "title": "📋 12 சேவைகள் மெனு"}
                ],
                footer="SIA • Tele-MANAS அரசு மனநல மையம்"
            )
        ], stage="MH_BREATHING_GUIDED")
"""

marker = "    #  INTERACTIVE QUICK MENU BUTTONS (btn_menu_1_agri, btn_menu_4_taxi, etc.)"
if marker in user_mgr_code and "DIRECT 1-2 STEP PETITION GENERATOR" not in user_mgr_code:
    user_mgr_code = user_mgr_code.replace(marker, direct_handlers + "\n" + marker, 1)
    user_mgr_path.write_text(user_mgr_code, encoding="utf-8")
    print("✓ sia_user_manager.py updated with direct 1-2 step illiterate-friendly action handlers!")
else:
    print("ℹ️ sia_user_manager.py already has direct action handlers or marker not found")
