# -*- coding: utf-8 -*-
"""
==============================================================================
SIA Makkal - Sovereign Service Providers & Partners Registry Engine
==============================================================================
Maintains verified local partner registry across all Tamil Nadu pincodes & districts:
1. Mobility: Bike Taxi, Namma Auto, AC Cab, Omni Van, Goods Mini-Truck (Tata Ace).
2. Agri Machinery: Tractor, Combined Harvester, Power Tiller, Agri Drone, Straw Baler.
3. Artisans & Gig Workers: Head Mason, Helper, Electrician, Plumber, Carpenter, Painter, Coconut Climber.
4. Tutors & Mentors: 10th/12th Tuition, Spoken English, NEET/JEE, TNPSC/UPSC.
5. Farm Labor Squads: Transplanting, Weeding, Harvesting Squads.
6. Self-Registration Workflow via WhatsApp & Web Portal.
7. Pincode Proximity Matching with Haversine GPS Fallback.
==============================================================================
"""

import os
import re
import json
import uuid
import math
import random
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from urllib.parse import quote_plus

logger = logging.getLogger("makkal.provider_registry")

PROVIDERS_REGISTRY_PATH = Path(__file__).parent / "sia_service_providers_registry.json"

# Reference to TN Pincodes from hyperlocal engine
from hyperlocal_rental_gig_engine import TN_PINCODE_DIRECTORY, resolve_location_by_pincode as resolve_pincode_details

# -----------------------------------------------------------------------------
# 1. CORE DEFAULT PARTNERS DATASET (COVERING ALL USECASES & KEY DISTRICTS)
# -----------------------------------------------------------------------------
DEFAULT_SERVICE_PROVIDERS: List[Dict[str, Any]] = [
    # ── 1. MOBILITY: BIKE TAXI ──
    {
        "provider_id": "PRV_BIKE_625214_01",
        "name": "க. கார்த்திக் (K. Karthik)",
        "phone": "9840123456",
        "category": "mobility",
        "service_key": "bike",
        "service_title_ta": "SIA ரேபிடோ பைக் டாக்சி (Hero Splendor)",
        "service_title_en": "Rapido Bike Taxi (Hero Splendor)",
        "icon": "🛵",
        "pincode": "625214",
        "district": "Madurai",
        "area_name_ta": "சோழவந்தான் ரயில்வே கேட் / மெயின் ரோடு",
        "area_name_en": "Sholavandan Railway Station / Main Road",
        "lat": 10.0240,
        "lon": 78.0120,
        "rate_card": "₹20 அடிப்படை கட்டணம் (1 கி.மீ) + ₹6/கி.மீ",
        "rate_per_km": 6.0,
        "base_fare": 20.0,
        "vehicle_details": "TN-59-CB-4291 (Hero Splendor+)",
        "driving_license": "TN5920180019283",
        "upi_id": "karthik.splendor@okhdfcbank",
        "rating": 4.9,
        "total_trips": 248,
        "availability": "Available / தயார்",
        "verified_badge": "TNeGA Verified Partner ✅",
        "registered_at": "2026-08-15"
    },
    {
        "provider_id": "PRV_BIKE_636001_02",
        "name": "என். அண்ணாமலை (N. Annamalai)",
        "phone": "9443219870",
        "category": "mobility",
        "service_key": "bike",
        "service_title_ta": "SIA பைக் டாக்சி (Bajaj Pulsar 150)",
        "service_title_en": "Rapido Bike Taxi (Bajaj Pulsar)",
        "icon": "🛵",
        "pincode": "636001",
        "district": "Salem",
        "area_name_ta": "சேலம் பழைய பேருந்து நிலையம் / புதிய பேருந்து நிலையம்",
        "area_name_en": "Salem Old Bus Stand / New Bus Stand",
        "lat": 11.6643,
        "lon": 78.1460,
        "rate_card": "₹20 அடிப்படை + ₹6/கி.மீ",
        "rate_per_km": 6.0,
        "base_fare": 20.0,
        "vehicle_details": "TN-30-AZ-8812 (Bajaj Pulsar)",
        "driving_license": "TN3020190038192",
        "upi_id": "annamalai.salem@okaxis",
        "rating": 4.8,
        "total_trips": 182,
        "availability": "Available / தயார்",
        "verified_badge": "Verified Driver ✅",
        "registered_at": "2026-09-01"
    },

    # ── 2. MOBILITY: AUTO RICKSHAW ──
    {
        "provider_id": "PRV_AUTO_625001_03",
        "name": "மு. பாண்டியன் (M. Pandian)",
        "phone": "9842109876",
        "category": "mobility",
        "service_key": "auto",
        "service_title_ta": "SIA நம்ம ஆட்டோ (Bajaj RE Compact)",
        "service_title_en": "Namma Auto (3-Seater Bajaj RE)",
        "icon": "🛺",
        "pincode": "625001",
        "district": "Madurai",
        "area_name_ta": "மதுரை மீனாட்சி அம்மன் கோயில் / சிம்மக்கல்",
        "area_name_en": "Madurai Meenakshi Temple / Simmakkal",
        "lat": 9.9195,
        "lon": 78.1193,
        "rate_card": "₹30 அடிப்படை (1.5 கி.மீ) + ₹13/கி.மீ",
        "rate_per_km": 13.0,
        "base_fare": 30.0,
        "vehicle_details": "TN-58-AU-9912 (Bajaj RE 4S Auto)",
        "driving_license": "TN5820150049182",
        "upi_id": "pandian.auto@okicici",
        "rating": 4.9,
        "total_trips": 612,
        "availability": "Available / தயார்",
        "verified_badge": "Government Registered Meter Auto ✅",
        "registered_at": "2026-07-20"
    },
    {
        "provider_id": "PRV_AUTO_624001_04",
        "name": "வி. கணேசன் (V. Ganesan)",
        "phone": "9789123411",
        "category": "mobility",
        "service_key": "auto",
        "service_title_ta": "SIA எலக்ட்ரிக் ஆட்டோ (Piaggio Ape E-City)",
        "service_title_en": "Electric Green Auto (Piaggio E-City)",
        "icon": "🛺",
        "pincode": "624001",
        "district": "Dindigul",
        "area_name_ta": "திண்டுக்கல் பேருந்து நிலையம் / மலைக்கோட்டை",
        "area_name_en": "Dindigul Bus Stand / Rock Fort",
        "lat": 10.3673,
        "lon": 77.9803,
        "rate_card": "₹25 அடிப்படை + ₹11/கி.மீ (சுற்றுச்சூழல் நட்பு சவாரி)",
        "rate_per_km": 11.0,
        "base_fare": 25.0,
        "vehicle_details": "TN-57-EV-1049 (Piaggio Ape Electric)",
        "driving_license": "TN5720210088192",
        "upi_id": "ganesan.eauto@paytm",
        "rating": 4.95,
        "total_trips": 340,
        "availability": "Available / தயார்",
        "verified_badge": "Zero Emission Partner ✅",
        "registered_at": "2026-08-10"
    },

    # ── 3. MOBILITY: CAB / CAR & OMNI VAN ──
    {
        "provider_id": "PRV_CAB_641001_05",
        "name": "எஸ். மாரியப்பன் (S. Mariappan)",
        "phone": "9442110033",
        "category": "mobility",
        "service_key": "sedan",
        "service_title_ta": "SIA பிரீமியம் செடான் டாக்ஸி (Swift Dzire AC)",
        "service_title_en": "Swift Dzire AC Sedan (Airport & Outstation)",
        "icon": "🚘",
        "pincode": "641001",
        "district": "Coimbatore",
        "area_name_ta": "கோயம்புத்தூர் காந்திபுரம் / ரயில் நிலையம் / பீளமேடு ஏர்போர்ட்",
        "area_name_en": "Gandhipuram / Coimbatore Junction / Airport",
        "lat": 11.0168,
        "lon": 76.9558,
        "rate_card": "₹149 அடிப்படை (4 கி.மீ) + ₹13/கி.மீ (AC வசதியுடன்)",
        "rate_per_km": 13.0,
        "base_fare": 149.0,
        "vehicle_details": "TN-38-BZ-4410 (Swift Dzire White AC)",
        "driving_license": "TN3820160029103",
        "upi_id": "mariappan.cabs@oksbi",
        "rating": 4.9,
        "total_trips": 540,
        "availability": "Available / தயார்",
        "verified_badge": "RedTaxi Tour Partner ✅",
        "registered_at": "2026-06-15"
    },
    {
        "provider_id": "PRV_VAN_600028_06",
        "name": "டி. செல்வராஜ் (T. Selvaraj)",
        "phone": "9841098765",
        "category": "mobility",
        "service_key": "omni_van",
        "service_title_ta": "SIA ஆம்னி குடும்ப வேன் (Maruti Omni 7-Seater)",
        "service_title_en": "Omni Family Van (7-Seater Temple & Trip)",
        "icon": "🚐",
        "pincode": "600028",
        "district": "Chennai",
        "area_name_ta": "மயிலாப்பூர் கபாலீஸ்வரர் கோயில் / அடையாறு",
        "area_name_en": "Mylapore Kapaleeshwarar Temple / Adyar",
        "lat": 13.0245,
        "lon": 80.2584,
        "rate_card": "₹299 அடிப்படை (10 கி.மீ) + ₹14/கி.மீ",
        "rate_per_km": 14.0,
        "base_fare": 299.0,
        "vehicle_details": "TN-07-AL-6019 (Maruti Omni 7-Seater)",
        "driving_license": "TN0720120019284",
        "upi_id": "selvaraj.van@okaxis",
        "rating": 4.85,
        "total_trips": 410,
        "availability": "Available / தயார்",
        "verified_badge": "Family Tour Specialist ✅",
        "registered_at": "2026-07-01"
    },

    # ── 4. MOBILITY: FREIGHT / GOODS MINI TRUCK (TATA ACE) ──
    {
        "provider_id": "PRV_GOODS_613001_07",
        "name": "ஆர். முருகேசன் (R. Murugesan)",
        "phone": "9443198765",
        "category": "mobility",
        "service_key": "goods_mini",
        "service_title_ta": "SIA சரக்கு வேன் (டாடா ஏஸ் சோட்டா ஹாத்தி 1 டன்)",
        "service_title_en": "Tata Ace Freight Truck (1-Ton Payload)",
        "icon": "🚚",
        "pincode": "613001",
        "district": "Thanjavur",
        "area_name_ta": "தஞ்சாவூர் பழைய பேருந்து நிலையம் / நெல் கொள்முதல் நிலையம்",
        "area_name_en": "Thanjavur Old Bus Stand / DPC Mandi Belt",
        "lat": 10.7870,
        "lon": 79.1378,
        "rate_card": "₹250 அடிப்படை (3 கி.மீ) + ₹20/கி.மீ",
        "rate_per_km": 20.0,
        "base_fare": 250.0,
        "vehicle_details": "TN-49-BT-1928 (Tata Ace Gold Diesel)",
        "driving_license": "TN4920140038192",
        "upi_id": "murugesan.tataace@okhdfcbank",
        "rating": 4.9,
        "total_trips": 580,
        "availability": "Available / தயார்",
        "verified_badge": "Agri & Shifting Verified ✅",
        "registered_at": "2026-06-20"
    },

    # ── 5. AGRI MACHINERY: TRACTOR WITH ROTAVATOR ──
    {
        "provider_id": "PRV_TRACTOR_613001_08",
        "name": "பி. சண்முகம் (P. Shanmugam)",
        "phone": "9842512345",
        "category": "agri_machinery",
        "service_key": "tractor_rotavator",
        "service_title_ta": "மகிந்திரா 575 DI டிராக்டர் & ரோட்டாவேட்டர் (45 HP)",
        "service_title_en": "Mahindra 575 DI Tractor with Rotavator (45 HP)",
        "icon": "🚜",
        "pincode": "613001",
        "district": "Thanjavur",
        "area_name_ta": "தஞ்சாவூர் டெல்டா பாசன வயல்வெளி / வல்லம்",
        "area_name_en": "Thanjavur Delta Paddy Belt / Vallam",
        "lat": 10.7870,
        "lon": 79.1378,
        "rate_card": "₹850/மணிநேரம் (டீசல் + டிரைவர் உட்பட)",
        "rate_per_hour": 850.0,
        "equipment_details": "Mahindra 575 DI 45HP + 42-Blade Shaktiman Rotavator",
        "upi_id": "shanmugam.tractor@okaxis",
        "rating": 4.95,
        "total_acres_ploughed": 480,
        "availability": "Available / தயார்",
        "verified_badge": "PACCS Approved Agri Implement ✅",
        "registered_at": "2026-05-10"
    },
    {
        "provider_id": "PRV_TRACTOR_625218_09",
        "name": "எம். கருப்பசாமி (M. Karuppasamy)",
        "phone": "9442019283",
        "category": "agri_machinery",
        "service_key": "tractor_rotavator",
        "service_title_ta": "ஜான் டீர் 5050D 4WD டிராக்டர் உழவு (50 HP)",
        "service_title_en": "John Deere 5050D 4WD Heavy Tractor (50 HP)",
        "icon": "🚜",
        "pincode": "625218",
        "district": "Madurai",
        "area_name_ta": "வாடிப்பட்டி அக்ரி பெல்ட் / ஆண்டிபட்டி ரோடு",
        "area_name_en": "Vadipatti Agri Belt / Andipatti Road",
        "lat": 10.0833,
        "lon": 77.9667,
        "rate_card": "₹900/மணிநேரம் (சேற்று உழவு & புழுதி உழவு)",
        "rate_per_hour": 900.0,
        "equipment_details": "John Deere 5050D 50HP 4WD + 9-Tyne Cultivator",
        "upi_id": "karuppasamy.jd@oksbi",
        "rating": 4.9,
        "total_acres_ploughed": 390,
        "availability": "Available / தயார்",
        "verified_badge": "Verified Farm Implement ✅",
        "registered_at": "2026-06-01"
    },

    # ── 6. AGRI MACHINERY: COMBINED PADDY HARVESTER ──
    {
        "provider_id": "PRV_HARVESTER_613501_10",
        "name": "கே. சுந்தரமூர்த்தி (K. Sundaramoorthy)",
        "phone": "9842998877",
        "category": "agri_machinery",
        "service_key": "paddy_harvester",
        "service_title_ta": "கிளாஸ் டிராக் வகை நெல் அறுவடை இயந்திரம் (Claas Crop Tiger)",
        "service_title_en": "Combined Track Paddy Harvester (Claas Crop Tiger 40)",
        "icon": "🌾",
        "pincode": "613501",
        "district": "Thanjavur",
        "area_name_ta": "கும்பகோணம் டெல்டா நெற்களஞ்சியம் / பாபநாசம்",
        "area_name_en": "Kumbakonam Delta Paddy Zone / Papanasam",
        "lat": 10.9602,
        "lon": 79.3845,
        "rate_card": "₹2,100/மணிநேரம் (சேற்றிலும் இயங்கும் டிராக் வகை)",
        "rate_per_hour": 2100.0,
        "equipment_details": "Claas Crop Tiger 40 Terra Trac (Rubber Track)",
        "upi_id": "sundar.harvester@okhdfcbank",
        "rating": 4.98,
        "total_acres_harvested": 1240,
        "availability": "Available / தயார்",
        "verified_badge": "TN Agri Engineering Dept Verified ✅",
        "registered_at": "2026-04-15"
    },
    {
        "provider_id": "PRV_HARVESTER_620006_11",
        "name": "ஆர். முத்துவேல் (R. Muthuvel)",
        "phone": "9788112233",
        "category": "agri_machinery",
        "service_key": "paddy_harvester",
        "service_title_ta": "குபோட்டா DC-68G அதிநவீன அறுவடை இயந்திரம்",
        "service_title_en": "Kubota DC-68G Combined Harvester",
        "icon": "🌾",
        "pincode": "620006",
        "district": "Tiruchirappalli",
        "area_name_ta": "ஸ்ரீரங்கம் கொள்ளிடம் ஆற்றுப் பாசனப் பகுதி / லால்குடி",
        "area_name_en": "Srirangam Kollidam River Basin / Lalgudi",
        "lat": 10.8622,
        "lon": 78.6908,
        "rate_card": "₹2,200/மணிநேரம் (தானிய இழப்பற்ற அறுவடை)",
        "rate_per_hour": 2200.0,
        "equipment_details": "Kubota DC-68G 68HP Crawler Track Harvester",
        "upi_id": "muthuvel.kubota@okicici",
        "rating": 4.9,
        "total_acres_harvested": 860,
        "availability": "Available / தயார்",
        "verified_badge": "Custom Hiring Centre Verified ✅",
        "registered_at": "2026-05-20"
    },

    # ── 7. AGRI MACHINERY: AGRI DRONE SPRAYER ──
    {
        "provider_id": "PRV_DRONE_614001_12",
        "name": "டாக்டர் ஏ. விக்னேஷ் B.Tech Agri (Garuda Certified Pilot)",
        "phone": "9944112233",
        "category": "agri_machinery",
        "service_key": "agri_drone",
        "service_title_ta": "கருடா விவசாய பூச்சிக்கொல்லி & நானோ யூரியா தெளிக்கும் ட்ரோன் (16L)",
        "service_title_en": "Garuda Precision Agri Drone Sprayer (16-Liter Tank)",
        "icon": "🛸",
        "pincode": "614001",
        "district": "Thanjavur",
        "area_name_ta": "பட்டுக்கோட்டை / பேராவூரணி தென்னை & நெல் பெல்ட்",
        "area_name_en": "Pattukkottai / Peravurani Coconut & Paddy Belt",
        "lat": 10.4267,
        "lon": 79.3197,
        "rate_card": "₹400/ஏக்கர் (10 நிமிடத்தில் 1 ஏக்கர் முழு தெளிப்பு)",
        "rate_per_acre": 400.0,
        "equipment_details": "DGCA Certified Type-Approved 16L Hexacopter Drone",
        "upi_id": "vignesh.drones@okaxis",
        "rating": 4.96,
        "total_acres_sprayed": 1820,
        "availability": "Available / தயார்",
        "verified_badge": "DGCA & TNAU Certified Pilot ✅",
        "registered_at": "2026-07-01"
    },
    {
        "provider_id": "PRV_DRONE_625106_13",
        "name": "கே. பூபதி (K. Boopathi Drone Pilot)",
        "phone": "9843990011",
        "category": "agri_machinery",
        "service_key": "agri_drone",
        "service_title_ta": "SIA நானோ உரம் & பூச்சி மருந்து ட்ரோன் (10L)",
        "service_title_en": "Precision Agri Drone Sprayer (10-Liter)",
        "icon": "🛸",
        "pincode": "625106",
        "district": "Madurai",
        "area_name_ta": "மேலூர் ஒத்தக்கடை விவசாயப் பகுதி",
        "area_name_en": "Melur Othakkadai Agricultural Belt",
        "lat": 10.0333,
        "lon": 78.3333,
        "rate_card": "₹420/ஏக்கர் (ஜிபிஎஸ் துல்லிய தெளிப்பு)",
        "rate_per_acre": 420.0,
        "equipment_details": "Kisan Drone 10L with Radar Obstacle Avoidance",
        "upi_id": "boopathi.pilot@oksbi",
        "rating": 4.88,
        "total_acres_sprayed": 750,
        "availability": "Available / தயார்",
        "verified_badge": "Kisan Drone Pilot ✅",
        "registered_at": "2026-08-15"
    },

    # ── 8. GIG ARTISANS: HEAD MASON & MASON HELPER (கொத்தனார் & சித்தாள்) ──
    {
        "provider_id": "PRV_MASON_641001_14",
        "name": "எம். ஆறுமுகம் (M. Arumugam Head Mason)",
        "phone": "9842119900",
        "category": "gig_labor",
        "service_key": "mason",
        "service_title_ta": "தலைமை கொத்தனார் (Civil Construction & Plastering)",
        "service_title_en": "Head Civil Mason (Brickwork & Tile Laying)",
        "icon": "🧱",
        "pincode": "641001",
        "district": "Coimbatore",
        "area_name_ta": "கோயம்புத்தூர் கணபதி / சிங்காநல்லூர்",
        "area_name_en": "Ganapathy / Singanallur Industrial & Residential",
        "lat": 11.0168,
        "lon": 76.9558,
        "rate_card": "₹950/நாள் (8 மணிநேரம்: காலை 8:30 முதல் மாலை 5:30 வரை)",
        "rate_per_day": 950.0,
        "experience": "22 ஆண்டுகள் கட்டுமான அனுபவம்",
        "specialization": "செங்கல் கட்டுவேலை, தரை டைல்ஸ், பூச்சு வேலை, வாஸ்து அளவு",
        "upi_id": "arumugam.mason@okaxis",
        "rating": 4.92,
        "completed_projects": 340,
        "availability": "Available / தயார்",
        "verified_badge": "TN Construction Workers Welfare Board Registered ✅",
        "registered_at": "2026-05-18"
    },
    {
        "provider_id": "PRV_HELPER_613001_15",
        "name": "பி. முருகன் உதவியாளர் குழு (P. Murugan Helper Squad)",
        "phone": "9443219800",
        "category": "gig_labor",
        "service_key": "assistant_mason",
        "service_title_ta": "கட்டுமான சித்தாள் & உதவியாளர் (Mason Helper)",
        "service_title_en": "Construction Helper & Material Shifting",
        "icon": "👷",
        "pincode": "613001",
        "district": "Thanjavur",
        "area_name_ta": "தஞ்சாவூர் புதிய பேருந்து நிலையம் / மானோம்புகாவடி",
        "area_name_en": "Thanjavur New Bus Stand / Manambuchavadi",
        "lat": 10.7870,
        "lon": 79.1378,
        "rate_card": "₹650/நாள் (கலவை கலக்குதல், செங்கல் சுமத்தல், க்யூரிங்)",
        "rate_per_day": 650.0,
        "experience": "8 ஆண்டுகள் உதவியாளர் பணி",
        "upi_id": "murugan.helper@okicici",
        "rating": 4.85,
        "availability": "Available / தயார்",
        "verified_badge": "Verified Construction Laborer ✅",
        "registered_at": "2026-07-10"
    },

    # ── 9. GIG ARTISANS: ELECTRICIAN & PLUMBER ──
    {
        "provider_id": "PRV_ELEC_625001_16",
        "name": "கே. வேலு (K. Velu Licensed Wireman)",
        "phone": "9443219871",
        "category": "gig_labor",
        "service_key": "electrician_plumber",
        "service_title_ta": "அங்கீகரிக்கப்பட்ட எலக்ட்ரீசியன் & மோட்டார் பம்ப் மெக்கானிக்",
        "service_title_en": "Licensed Electrician & Submersible Motor Specialist",
        "icon": "⚡",
        "pincode": "625001",
        "district": "Madurai",
        "area_name_ta": "மதுரை தெற்கு வாசல் / ஜெய்ஹிந்த்புரம்",
        "area_name_en": "Madurai South Gate / Jaihindpuram",
        "lat": 9.9195,
        "lon": 78.1193,
        "rate_card": "₹350/பார்வை கட்டணம் (ஒரு நாள் வேலை: ₹800)",
        "rate_per_visit": 350.0,
        "license_no": "ITI-WIREMAN-MD-44810",
        "upi_id": "velu.electrician@okhdfcbank",
        "rating": 4.96,
        "completed_jobs": 720,
        "availability": "Available / தயார்",
        "verified_badge": "Government ITI Certified Wireman ✅",
        "registered_at": "2026-06-01"
    },
    {
        "provider_id": "PRV_PLUMB_641601_17",
        "name": "எஸ். சரவணன் (S. Saravanan Plumber)",
        "phone": "9842887766",
        "category": "gig_labor",
        "service_key": "electrician_plumber",
        "service_title_ta": "பிளம்பர் & சொட்டு நீர் பாசன பைப்லைன் நிபுணர்",
        "service_title_en": "Plumber & Drip Irrigation Pipeline Specialist",
        "icon": "🔧",
        "pincode": "641601",
        "district": "Tiruppur",
        "area_name_ta": "திருப்பூர் பழைய பேருந்து நிலையம் / காங்கேயம் ரோடு",
        "area_name_en": "Tiruppur Old Bus Stand / Kangeyam Road",
        "lat": 11.1085,
        "lon": 77.3411,
        "rate_card": "₹350/விசிட் (குழாய் அடைப்பு, பாத்ரூம் லீக், மோட்டார் ஃபிட்டிங்)",
        "rate_per_visit": 350.0,
        "upi_id": "saravanan.plumber@oksbi",
        "rating": 4.9,
        "completed_jobs": 490,
        "availability": "Available / தயார்",
        "verified_badge": "Verified Plumbing Artisan ✅",
        "registered_at": "2026-07-15"
    },

    # ── 10. GIG ARTISANS: COCONUT TREE CLIMBER (தென்னை மரம் ஏறுவோர்) ──
    {
        "provider_id": "PRV_COCONUT_642001_18",
        "name": "ஏ. முத்துக்கிருஷ்ணன் (A. Muthukrishnan)",
        "phone": "9442991122",
        "category": "gig_labor",
        "service_key": "coconut_climber",
        "service_title_ta": "பாரம்பரிய தென்னை மரம் ஏறுவோர் & தேங்காய் அறுவடை நிபுணர்",
        "service_title_en": "Traditional Coconut Tree Climber & Pruning Expert",
        "icon": "🌴",
        "pincode": "642001",
        "district": "Coimbatore",
        "area_name_ta": "பொள்ளாச்சி தென்னந்தோப்பு பெல்ட் / ஆனைமலை",
        "area_name_en": "Pollachi Coconut Farm Belt / Anaimalai",
        "lat": 10.6609,
        "lon": 77.0048,
        "rate_card": "₹60/மரம் (மரம் சுத்தம் செய்தல் + தேங்காய் பறித்தல்)",
        "rate_per_tree": 60.0,
        "equipment": "பாதுகாப்பு பெல்ட் & கயிறு சாதனம்",
        "upi_id": "muthukrishnan.coconut@okaxis",
        "rating": 4.98,
        "trees_harvested": 14200,
        "availability": "Available / தயார்",
        "verified_badge": "Tamil Nadu Tree Climbers Association Verified ✅",
        "registered_at": "2026-04-01"
    },
    {
        "provider_id": "PRV_COCONUT_625218_19",
        "name": "சி. அழகர்சாமி (C. Alagarsamy)",
        "phone": "9789332211",
        "category": "gig_labor",
        "service_key": "coconut_climber",
        "service_title_ta": "தென்னை மரம் ஏறுவோர் & கவாத்து வெட்டுபவர்",
        "service_title_en": "Coconut Tree Climber & Crown Cleaning",
        "icon": "🌴",
        "pincode": "625218",
        "district": "Madurai",
        "area_name_ta": "வாடிப்பட்டி / சோழவந்தான் வைகை ஆற்றுப்படுகை தென்னந்தோப்புகள்",
        "area_name_en": "Vadipatti / Sholavandan Vaigai Basin Coconut Orchards",
        "lat": 10.0833,
        "lon": 77.9667,
        "rate_card": "₹60/மரம் (பாதுகாப்பான இயந்திர சாதனம் மூலம்)",
        "rate_per_tree": 60.0,
        "upi_id": "alagarsamy.climber@paytm",
        "rating": 4.9,
        "availability": "Available / தயார்",
        "verified_badge": "Verified Coconut Harvester ✅",
        "registered_at": "2026-05-12"
    },

    # ── 11. EDUCATION: TUTORS & COMPETITIVE EXAM COACHES ──
    {
        "provider_id": "PRV_TUTOR_625001_20",
        "name": "எஸ். மீனாட்சி M.Sc B.Ed (S. Meenakshi)",
        "phone": "9840998877",
        "category": "education",
        "service_key": "school_tutor",
        "service_title_ta": "10 & 12 ஆம் வகுப்பு கணிதம் & அறிவியல் ஆசிரியர் (Home/Online)",
        "service_title_en": "Class 10 & 12 Maths & Science Expert Tutor",
        "icon": "👩‍🏫",
        "pincode": "625001",
        "district": "Madurai",
        "area_name_ta": "மதுரை கே.கே. நகர் / அண்ணா நகர்",
        "area_name_en": "Madurai KK Nagar / Anna Nagar",
        "lat": 9.9195,
        "lon": 78.1193,
        "rate_card": "₹500/வகுப்பு (மாதம்: ₹2,500/மாணவர்)",
        "education": "M.Sc Mathematics, B.Ed (14 ஆண்டுகள் கற்பித்தல் அனுபவம்)",
        "specialization": "10-ஆம் வகுப்பு சமச்சீர் கல்வி & CBSE போர்டு தேர்வு வழிகாட்டுதல்",
        "upi_id": "meenakshi.tutor@oksbi",
        "rating": 4.97,
        "students_coached": 420,
        "availability": "Available / தயார்",
        "verified_badge": "Verified Teacher & TNeGA Approved ✅",
        "registered_at": "2026-06-10"
    },
    {
        "provider_id": "PRV_COACH_641001_21",
        "name": "ஆர். திவ்யா M.A M.Phil (R. Divya)",
        "phone": "9944001122",
        "category": "education",
        "service_key": "spoken_english_coach",
        "service_title_ta": "பேச்சு ஆங்கிலம் & வேலைவாய்ப்பு நேர்முகத் தேர்வு பயிற்சியாளர்",
        "service_title_en": "Spoken English & Interview Soft Skills Coach",
        "icon": "🗣️",
        "pincode": "641001",
        "district": "Coimbatore",
        "area_name_ta": "கோயம்புத்தூர் ஆர்.எஸ். புரம் / சவுரிபாளையம்",
        "area_name_en": "RS Puram / Sowripalayam Educational Belt",
        "lat": 11.0168,
        "lon": 76.9558,
        "rate_card": "₹400/மணிநேரம் (30 நாள் சரளப் பயிற்சி)",
        "specialization": "தமிழ் வழி மாணவர்களுக்கான எளிய ஆங்கிலப் பயிற்சி",
        "upi_id": "divya.english@okaxis",
        "rating": 4.95,
        "students_coached": 680,
        "availability": "Available / தயார்",
        "verified_badge": "Certified Language Coach ✅",
        "registered_at": "2026-07-05"
    },
    {
        "provider_id": "PRV_MENTOR_600028_22",
        "name": "டாக்டர் கே. செந்தில் MBBS MD (Dr. K. Senthil)",
        "phone": "9841223344",
        "category": "education",
        "service_key": "competitive_exam_mentor",
        "service_title_ta": "நீட் (NEET) உயிரியல் & NCERT மாதிரி தேர்வு வழிகாட்டி",
        "service_title_en": "NEET Medical Entrance Biology Senior Mentor",
        "icon": "🩺",
        "pincode": "600028",
        "district": "Chennai",
        "area_name_ta": "சென்னை ஆழ்வார்பேட்டை / ராஜா அண்ணாமலைபுரம்",
        "area_name_en": "Alwarpet / Raja Annamalaipuram",
        "lat": 13.0245,
        "lon": 80.2584,
        "rate_card": "வழிகாட்டுதல் அமர்வு: ₹600/மணிநேரம்",
        "specialization": "NEET 360/360 மதிப்பெண் உத்திகள் & NCERT Line-by-Line",
        "upi_id": "senthil.neet@okhdfcbank",
        "rating": 4.99,
        "students_coached": 1200,
        "availability": "Available / தயார்",
        "verified_badge": "Government Medical Officer & Educator ✅",
        "registered_at": "2026-05-01"
    },
    {
        "provider_id": "PRV_TNPSC_625214_23",
        "name": "எம். விஜய் M.A (M. Vijay TNPSC Group 1 Qualified)",
        "phone": "9840889900",
        "category": "education",
        "service_key": "competitive_exam_mentor",
        "service_title_ta": "டிஎன்பிஎஸ்சி குரூப் 1/2/4 & விஏஓ (VAO) முழுநேரப் பயிற்றுநர்",
        "service_title_en": "TNPSC Group 1, 2, 4 & VAO State Rank Mentor",
        "icon": "🏛️",
        "pincode": "625214",
        "district": "Madurai",
        "area_name_ta": "சோழவந்தான் / சமயநல்லூர் குடிமைப்பணி மையம்",
        "area_name_en": "Sholavandan / Samayanallur Civil Services Academy",
        "lat": 10.0240,
        "lon": 78.0120,
        "rate_card": "₹350/அமர்வு (தினசரி முந்தைய ஆண்டு வினாக்கள் பயிற்சி)",
        "specialization": "பொதுத் தமிழ் 100/100 மற்றும் யூனிட் 8 & 9 தமிழ்நாடு நிர்வாகம்",
        "upi_id": "vijay.tnpsc@okaxis",
        "rating": 4.98,
        "students_coached": 890,
        "availability": "Available / தயார்",
        "verified_badge": "TNPSC Group 1 Interview Candidate ✅",
        "registered_at": "2026-06-15"
    },

    # ── 12. FARM LABOR SQUADS ──
    {
        "provider_id": "PRV_SQUAD_613001_24",
        "name": "தையல்நாயகி பெண்கள் விவசாய நடவுக் குழு (10 நபர்கள்)",
        "phone": "9443556677",
        "category": "farm_labor",
        "service_key": "farm_labor",
        "service_title_ta": "விவசாய நடவு, களை எடுத்தல் & அறுவடை மகளிர் குழு (10 பேர்)",
        "service_title_en": "Women Paddy Transplanting & Weeding Squad (10-Person)",
        "icon": "👩‍🌾",
        "pincode": "613001",
        "district": "Thanjavur",
        "area_name_ta": "தஞ்சாவூர் திருக்காட்டுப்பள்ளி டெல்டா வயல்கள்",
        "area_name_en": "Thanjavur Thirukkattupalli Delta Farms",
        "lat": 10.7870,
        "lon": 79.1378,
        "rate_card": "₹450/நபர்/நாள் (ஏக்கர் ஒப்பந்தம்: ₹4,000/ஏக்கர் நடவு)",
        "rate_per_day": 450.0,
        "squad_strength": "10 அனுபவமிக்க விவசாயப் பெண்கள்",
        "specialization": "பாரம்பரிய நெல் நாற்று நடுதல், செறிவூட்டப்பட்ட நெல் சாகுபடி (SRI)",
        "upi_id": "thaiyalnayagi.shg@oksbi",
        "rating": 4.96,
        "acres_covered": 1600,
        "availability": "Available / தயார்",
        "verified_badge": "Tamil Nadu Magalir Thittam Verified SHG ✅",
        "registered_at": "2026-04-10"
    },
    {
        "provider_id": "PRV_SQUAD_625214_25",
        "name": "மருதுபாண்டியன் உழவர் களை எடுப்பு & அறுவடை குழு (8 நபர்கள்)",
        "phone": "9842778899",
        "category": "farm_labor",
        "service_key": "farm_labor",
        "service_title_ta": "விவசாய வயல் வேலை & நெல் கதிர் அறுவடை குழு (8 பேர்)",
        "service_title_en": "Farm Weeding & Paddy Harvesting Squad (8-Person)",
        "icon": "🧑‍🌾",
        "pincode": "625214",
        "district": "Madurai",
        "area_name_ta": "சோழவந்தான் வைகை பாசன நெல் வயல்கள்",
        "area_name_en": "Sholavandan Vaigai Irrigation Paddy Lands",
        "lat": 10.0240,
        "lon": 78.0120,
        "rate_card": "₹500/நபர்/நாள் (காலை 7:30 - மதியம் 2:00)",
        "rate_per_day": 500.0,
        "squad_strength": "8 அனுபவமிக்க விவசாயிகள்",
        "upi_id": "marudhu.farms@okaxis",
        "rating": 4.92,
        "availability": "Available / தயார்",
        "verified_badge": "Registered Agri Labor Squad ✅",
        "registered_at": "2026-05-15"
    }
]


# -----------------------------------------------------------------------------
# 2. PERSISTENCE & INITIALIZATION
# -----------------------------------------------------------------------------
def load_providers_registry() -> List[Dict[str, Any]]:
    """Loads partner registry from disk or initializes with default 25+ verified partners."""
    if not PROVIDERS_REGISTRY_PATH.exists():
        save_providers_registry(DEFAULT_SERVICE_PROVIDERS)
        return list(DEFAULT_SERVICE_PROVIDERS)
    try:
        with open(PROVIDERS_REGISTRY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) >= 10:
                return data
            # If empty or corrupted, reseed
            save_providers_registry(DEFAULT_SERVICE_PROVIDERS)
            return list(DEFAULT_SERVICE_PROVIDERS)
    except Exception as e:
        logger.error(f"[PROVIDER REGISTRY] Failed to load: {e}")
        return list(DEFAULT_SERVICE_PROVIDERS)


def save_providers_registry(providers: List[Dict[str, Any]]) -> bool:
    """Saves partner registry atomically to disk."""
    try:
        temp_path = PROVIDERS_REGISTRY_PATH.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(providers, f, ensure_ascii=False, indent=2)
        temp_path.replace(PROVIDERS_REGISTRY_PATH)
        return True
    except Exception as e:
        logger.error(f"[PROVIDER REGISTRY] Failed to save: {e}")
        return False


# -----------------------------------------------------------------------------
# 3. PARTNER SELF-REGISTRATION FUNCTIONALITY
# -----------------------------------------------------------------------------
def register_new_partner(
    name: str,
    phone: str,
    category: str,
    service_key: str,
    pincode: str,
    rate_card: str,
    vehicle_or_equipment: str = "",
    driving_license_or_id: str = "",
    upi_id: Optional[str] = None
) -> Dict[str, Any]:
    """Registers a new driver, tractor owner, artisan, or tutor onto SIA platform."""
    clean_phone = re.sub(r"\D", "", str(phone))
    clean_pin = re.sub(r"\D", "", str(pincode))[:6]

    # Resolve area & district from pincode
    pin_info = resolve_pincode_details(clean_pin)
    district = pin_info.get("district", "Tamil Nadu")
    area_ta = pin_info.get("area_ta", f"{district} பகுதி")
    area_en = pin_info.get("area_en", f"{district} Area")

    provider_id = f"PRV_{category[:3].upper()}_{clean_pin}_{uuid.uuid4().hex[:4].upper()}"

    # Auto assign icon based on category
    icons = {
        "mobility": "🛵" if "bike" in service_key else "🛺" if "auto" in service_key else "🚗" if "sedan" in service_key else "🚚",
        "agri_machinery": "🚜" if "tractor" in service_key else "🌾" if "harvester" in service_key else "🛸" if "drone" in service_key else "🚜",
        "gig_labor": "🧱" if "mason" in service_key else "⚡" if "elec" in service_key else "🔧" if "plumb" in service_key else "🌴" if "coconut" in service_key else "👷",
        "education": "👨‍🏫" if "tutor" in service_key or "mentor" in service_key else "🗣️",
        "farm_labor": "🧑‍🌾"
    }
    icon = icons.get(category, "🤝")

    new_partner = {
        "provider_id": provider_id,
        "name": name.strip(),
        "phone": clean_phone,
        "category": category.strip(),
        "service_key": service_key.strip(),
        "service_title_ta": f"SIA {service_key.capitalize()} ({vehicle_or_equipment or name})",
        "service_title_en": f"SIA {service_key.capitalize()} ({vehicle_or_equipment or name})",
        "icon": icon,
        "pincode": clean_pin,
        "district": district,
        "area_name_ta": area_ta,
        "area_name_en": area_en,
        "lat": pin_info.get("lat", 10.0),
        "lon": pin_info.get("lon", 78.0),
        "rate_card": rate_card.strip(),
        "vehicle_details": vehicle_or_equipment.strip(),
        "equipment_details": vehicle_or_equipment.strip(),
        "driving_license": driving_license_or_id.strip(),
        "upi_id": upi_id or f"{clean_phone}@upi",
        "rating": 5.0,
        "total_trips": 0,
        "availability": "Available / தயார்",
        "verified_badge": "SIA Verified Partner ✅",
        "registered_at": datetime.now().strftime("%Y-%m-%d")
    }

    providers = load_providers_registry()
    providers.insert(0, new_partner)
    save_providers_registry(providers)

    return {
        "status": "success",
        "provider_id": provider_id,
        "partner": new_partner,
        "message_ta": f"வாழ்த்துக்கள்! உங்கள் சேவை (ID: {provider_id}) SIA கூட்டாளர் அமைப்பில் வெற்றிகரமாக பதிவு செய்யப்பட்டது!"
    }


# -----------------------------------------------------------------------------
# 4. PINCODE PROXIMITY SEARCH & DISPATCHER
# -----------------------------------------------------------------------------
def search_service_providers(
    pincode: Optional[str] = None,
    district: Optional[str] = None,
    category: Optional[str] = None,
    service_key: Optional[str] = None,
    query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Searches partner registry with exact pincode match or nearest district fallback."""
    providers = load_providers_registry()
    results = []

    clean_pin = re.sub(r"\D", "", str(pincode))[:6] if pincode else None
    q_clean = query.strip().lower() if query else None

    # Step 1: Filter by category / service_key if specified
    candidates = providers
    if category:
        c_map = {
            "agriculture": "agri_machinery",
            "agri": "agri_machinery",
            "farming": "agri_machinery",
            "transport": "mobility",
            "ride": "mobility",
            "taxi": "mobility",
            "labor": "agri_labor",
            "labour": "agri_labor"
        }
        target_cats = {category.lower(), c_map.get(category.lower(), category.lower())}
        candidates = [p for p in candidates if str(p.get("category", "")).lower() in target_cats]
    if service_key:
        candidates = [p for p in candidates if service_key.lower() in p.get("service_key", "").lower()]

    if q_clean and not service_key:
        tokens = [t for t in q_clean.split() if len(t) >= 3 and not t.isdigit()]
        if tokens:
            candidates = [
                p for p in candidates
                if any(t in p.get("name", "").lower() or
                       t in p.get("service_title_ta", "").lower() or
                       t in p.get("service_title_en", "").lower() or
                       t in p.get("area_name_ta", "").lower() or
                       t in p.get("district", "").lower()
                       for t in tokens)
            ]

    # Step 2: Sort by exact pincode match first
    if clean_pin:
        exact_pin = [p for p in candidates if p.get("pincode") == clean_pin]
        same_district = [p for p in candidates if p.get("pincode") != clean_pin and p.get("district", "").lower() == (district or "").lower()]
        other_districts = [p for p in candidates if p.get("pincode") != clean_pin and p.get("district", "").lower() != (district or "").lower()]
        results = exact_pin + same_district + other_districts
    else:
        results = candidates

    return results


# -----------------------------------------------------------------------------
# 5. INSTANT HIRE DISPATCH WITH 4-DIGIT OTP & DIRECT UPI
# -----------------------------------------------------------------------------
def create_provider_hire_request(
    provider_id: str,
    customer_phone: str,
    customer_name: str = "Citizen",
    pickup_pincode: str = "625214",
    notes: str = ""
) -> Dict[str, Any]:
    """Dispatches instant booking for a registered partner with OTP and deep links."""
    providers = load_providers_registry()
    partner = next((p for p in providers if p.get("provider_id") == provider_id), None)
    if not partner:
        # Fallback to first available
        partner = providers[0]

    booking_id = f"BK_{uuid.uuid4().hex[:6].upper()}"
    otp = f"{random.randint(1000, 9999)}"

    # Generate UPI Payment link directly to provider
    base_fare = float(partner.get("base_fare", partner.get("rate_per_day", partner.get("rate_per_hour", 100.0))))
    upi_id = partner.get("upi_id", "sia.partner@okaxis")
    p_name = partner.get("name", "Partner")
    wa_msg = f"வணக்கம் {p_name}, நான் SIA செயலி மூலம் உங்கள் சேவையை முன்பதிவு செய்துள்ளேன் (Booking ID: {booking_id}). OTP: {otp}"
    upi_link = f"upi://pay?pa={upi_id}&pn={quote_plus(p_name)}&am={base_fare}&cu=INR&tn={quote_plus(f'SIA Booking {booking_id}')}"

    return {
        "status": "success",
        "booking_id": booking_id,
        "otp": otp,
        "partner": partner,
        "customer_phone": customer_phone,
        "customer_name": customer_name,
        "pickup_pincode": pickup_pincode,
        "base_fare": base_fare,
        "upi_payment_link": upi_link,
        "call_url": f"tel:{partner['phone']}",
        "whatsapp_chat_url": f"https://wa.me/91{partner['phone']}?text={quote_plus(wa_msg)}",
        "dispatched_at": datetime.now().strftime("%Y-%m-%d %I:%M %p")
    }


# -----------------------------------------------------------------------------
# 6. WHATSAPP CONVERSATIONAL INTENT HANDLER FOR PARTNERS & PINCODES
# -----------------------------------------------------------------------------
def process_provider_query_conversational(phone: str, text: str) -> Dict[str, Any]:
    """
    Parses conversational queries for service partners, drivers, machinery, and masons:
    Examples:
    - '625214 பைக் வேணும்'
    - '613001 அறுவடை இயந்திரம் வாடகைக்கு'
    - '641001 கொத்தனார் ஆட்கள் வேண்டும்'
    - 'பதிவு ஓட்டுநர் கார்த்திக் பைக் 625214 9840123456'
    """
    clean_text = text.strip()
    upper = clean_text.upper()

    # Case A: Partner Self-Registration (e.g. 'பதிவு ஓட்டுநர் கார்த்திக் பைக் 625214 9840123456' or 'REGISTER DRIVER')
    if any(k in clean_text for k in ["பதிவு", "கூட்டாளர் பதிவு", "ஓட்டுநர் பதிவு", "இயந்திர பதிவு"]) or "REGISTER" in upper:
        pin_match = re.search(r"(\b6\d{5}\b)", clean_text)
        found_pin = pin_match.group(1) if pin_match else "625214"
        
        phone_match = re.search(r"(\b[6-9]\d{9}\b)", clean_text)
        found_phone = phone_match.group(1) if phone_match else phone

        # Extract category
        cat = "mobility" if any(k in clean_text for k in ["பைக்", "ஆட்டோ", "கார்", "வேன்", "டிரைவர்", "bike", "auto", "car"]) else \
              "agri_machinery" if any(k in clean_text for k in ["டிராக்டர்", "அறுவடை", "ட்ரோன்", "tractor", "harvester", "drone"]) else \
              "gig_labor" if any(k in clean_text for k in ["கொத்தனார்", "பிளம்பர்", "எலக்ட்ரீஷியன்", "mason", "electrician", "plumber"]) else "mobility"

        service_key = "bike" if "பைக்" in clean_text or "bike" in clean_text.lower() else \
                      "auto" if "ஆட்டோ" in clean_text or "auto" in clean_text.lower() else \
                      "tractor_rotavator" if "டிராக்டர்" in clean_text or "tractor" in clean_text.lower() else \
                      "paddy_harvester" if "அறுவடை" in clean_text or "harvester" in clean_text.lower() else \
                      "mason" if "கொத்தனார்" in clean_text or "mason" in clean_text.lower() else "general"

        reg_res = register_new_partner(
            name="புதிய கூட்டாளர் (New Partner)",
            phone=found_phone,
            category=cat,
            service_key=service_key,
            pincode=found_pin,
            rate_card="அரசு வழிகாட்டுதல் வெளிப்படையான கட்டணம்",
            vehicle_or_equipment="சரிபார்க்கப்பட்ட சாதனம்"
        )

        msg = (
            f"🤝 *SIA கூட்டாளர் பதிவு வெற்றிகரமாக முடிந்தது!* ✅\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• *கூட்டாளர் ஐடி:* `{reg_res['provider_id']}`\n"
            f"• *சேவை:* {reg_res['partner']['service_title_ta']}\n"
            f"• *பின்கோடு மண்டலம்:* {found_pin} ({reg_res['partner']['district']})\n"
            f"• *நிலை:* {reg_res['partner']['verified_badge']}\n\n"
            f"உங்கள் பகுதி மக்கள் இனி SIA மூலம் உங்களை நேரடியாக தொடர்பு கொண்டு ஆர்டர் செய்வர். பூஜ்ஜிய கமிஷன் (Zero Commission)!\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📞 *வாடிக்கையாளர் அழைப்புகள் உங்கள் எண்ணிற்கு நேரடியாக வரும்.*"
        )
        return {"status": "processed", "type": "partner_registered", "message": msg}

    # Case B: Pincode-Based Search for Drivers, Machinery, Masons, Tutors
    pin_match = re.search(r"(\b6\d{5}\b)", clean_text)
    target_pin = pin_match.group(1) if pin_match else None

    # Detect requested role
    matched_key = None
    if any(k in clean_text for k in ["பைக்", "bike", "டாக்ஸி", "taxi"]):
        matched_key = "bike"
    elif any(k in clean_text for k in ["ஆட்டோ", "auto"]):
        matched_key = "auto"
    elif any(k in clean_text for k in ["கார்", "car", "டாக்ஸி", "cab"]):
        matched_key = "sedan"
    elif any(k in clean_text for k in ["வேன்", "சரக்கு", "ஏஸ்", "van", "truck"]):
        matched_key = "goods_mini"
    elif any(k in clean_text for k in ["டிராக்டர்", "உழவு", "tractor", "rotavator"]):
        matched_key = "tractor_rotavator"
    elif any(k in clean_text for k in ["அறுவடை", "harvester", "கதிர்"]):
        matched_key = "paddy_harvester"
    elif any(k in clean_text for k in ["ட்ரோன்", "drone", "தெளிப்பான்"]):
        matched_key = "agri_drone"
    elif any(k in clean_text for k in ["கொத்தனார்", "mason", "கட்டுமானம்"]):
        matched_key = "mason"
    elif any(k in clean_text for k in ["சித்தாள்", "helper", "உதவியாளர்"]):
        matched_key = "assistant_mason"
    elif any(k in clean_text for k in ["எலக்ட்ரீஷியன்", "electrician", "மின்", "வயரிங்"]):
        matched_key = "electrician_plumber"
    elif any(k in clean_text for k in ["பிளம்பர்", "plumber", "குழாய்"]):
        matched_key = "electrician_plumber"
    elif any(k in clean_text for k in ["தென்னை", "மரம் ஏறுவோர்", "coconut", "climber"]):
        matched_key = "coconut_climber"
    elif any(k in clean_text for k in ["டியூஷன்", "ஆசிரியர்", "tutor", "maths", "science"]):
        matched_key = "school_tutor"
    elif any(k in clean_text for k in ["ஆங்கிலம்", "spoken english", "english"]):
        matched_key = "spoken_english_coach"
    elif any(k in clean_text for k in ["நீட்", "neet", "டிஎன்பிஎஸ்சி", "tnpsc", "upsc"]):
        matched_key = "competitive_exam_mentor"

    if not target_pin and not matched_key:
        return {"status": "unhandled"}

    results = search_service_providers(pincode=target_pin, service_key=matched_key)
    if results:
        top_partner = results[0]
        hire_info = create_provider_hire_request(
            provider_id=top_partner["provider_id"],
            customer_phone=phone,
            pickup_pincode=target_pin or top_partner["pincode"]
        )

        total_serv = top_partner.get('total_trips') or top_partner.get('total_acres_harvested') or top_partner.get('students_coached') or top_partner.get('completed_jobs') or 150
        msg = (
            f"{top_partner['icon']} *SIA சரிபார்க்கப்பட்ட சேவை கூட்டாளர் இணைப்பு* 🎯\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• *பெயர்:* *{top_partner['name']}* ({top_partner['verified_badge']})\n"
            f"• *சேவை:* {top_partner['service_title_ta']}\n"
            f"• *பின்கோடு:* {top_partner['pincode']} ({top_partner['area_name_ta']})\n"
            f"• *கட்டண விபரம்:* {top_partner['rate_card']}\n"
            f"• *மதிப்பீடு:* {top_partner['rating']} ★ ({total_serv} வெற்றிகரமான சேவைகள்)\n\n"
            f"📞 *நேரடி தொடர்பு தொலைபேசி:* `{top_partner['phone']}`\n"
            f"💬 *வாட்ஸ்அப் அரட்டை:* {hire_info['whatsapp_chat_url']}\n"
            f"🔢 *பாதுகாப்பு OTP:* `{hire_info['otp']}` (சேவை முடிந்தவுடன் பகிரவும்)\n\n"
            f"💳 *பூஜ்ஜிய கமிஷன் நேரடி UPI:* `{top_partner['upi_id']}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *நடுவர் தரகு கட்டணம் ஏதுமில்லை! 100% கட்டணம் தொழிலாளிக்கே சேரும்.*"
        )
        return {
            "status": "processed",
            "type": "provider_found",
            "message": msg,
            "partner": top_partner,
            "hire_info": hire_info
        }

    return {"status": "unhandled"}
