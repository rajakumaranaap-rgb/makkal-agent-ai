# -*- coding: utf-8 -*-
"""
==============================================================================
SIA Makkal - Hyperlocal Rentals, Agri Machinery & Gig Economy Engine
==============================================================================
Provides end-to-end On-Demand Super-App functionality for Tamil Nadu:
1. Pincode (600xxx-643xxx) and Google Maps Location Resolution (38 Districts).
2. Mobility & Goods Logistics (Rapido Bike Taxi, Auto, Cab, Tata Ace Goods Truck).
3. Agricultural Machinery & Implements Custom Hiring (Tractors, Harvesters, Drones, Pumps).
4. Daily Wage Laborers & Skilled Artisans (Farm Hands, Masons, Electricians, Coconut Climbers).
5. Zero-Surge Statutory Rates & Dynamic UPI Deep Links (GPay, PhonePe, Paytm, BHIM).
6. 4-Digit Security OTP & WhatsApp <-> Web Two-Way Synchronization.
==============================================================================
"""

import os
import re
import math
import uuid
import random
import logging
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import quote_plus
from datetime import datetime

logger = logging.getLogger("makkal.hyperlocal_gig_engine")

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL") or os.getenv("AWS_PUBLIC_URL") or "https://regulatory-stack-counter-lady.trycloudflare.com"

# -----------------------------------------------------------------------------
# 1. TAMIL NADU PINCODE & GEOLOCATION DIRECTORY (ALL 38 DISTRICTS)
# -----------------------------------------------------------------------------
TN_PINCODE_DIRECTORY: Dict[str, Dict[str, Any]] = {
    # Chennai District
    "600001": {"district": "Chennai", "area_en": "George Town / Parrys", "area_ta": "பாரிமுனை / ஜார்ஜ் டவுன்", "lat": 13.0900, "lon": 80.2880},
    "600003": {"district": "Chennai", "area_en": "Chennai Central / Park Town", "area_ta": "சென்னை சென்ட்ரல் / பூங்கா நகர்", "lat": 13.0827, "lon": 80.2707},
    "600004": {"district": "Chennai", "area_en": "Mylapore", "area_ta": "மயிலாப்பூர்", "lat": 13.0368, "lon": 80.2676},
    "600028": {"district": "Chennai", "area_en": "Raja Annamalaipuram", "area_ta": "ராஜா அண்ணாமலைபுரம்", "lat": 13.0245, "lon": 80.2584},
    "600082": {"district": "Chennai", "area_en": "Kolathur", "area_ta": "கொளத்தூர்", "lat": 13.1235, "lon": 80.2093},
    "600096": {"district": "Chennai", "area_en": "Perungudi / OMR", "area_ta": "பெருங்குடி / ஓ.எம்.ஆர்", "lat": 12.9654, "lon": 80.2461},

    # Tiruvallur District
    "601201": {"district": "Tiruvallur", "area_en": "Gummidipoondi", "area_ta": "கும்மிடிப்பூண்டி", "lat": 13.4072, "lon": 80.1278},
    "602001": {"district": "Tiruvallur", "area_en": "Tiruvallur Town", "area_ta": "திருவள்ளூர் நகரம்", "lat": 13.1432, "lon": 79.9083},
    "631209": {"district": "Tiruvallur", "area_en": "Tiruttani", "area_ta": "திருத்தணி", "lat": 13.1812, "lon": 79.6267},

    # Kanchipuram & Chengalpattu
    "631501": {"district": "Kanchipuram", "area_en": "Kanchipuram Central", "area_ta": "காஞ்சிபுரம் மத்தி", "lat": 12.8342, "lon": 79.7036},
    "603001": {"district": "Chengalpattu", "area_en": "Chengalpattu Town", "area_ta": "செங்கல்பட்டு நகரம்", "lat": 12.6841, "lon": 79.9836},
    "603103": {"district": "Chengalpattu", "area_en": "Kelambakkam / OMR", "area_ta": "கேளம்பாக்கம் / பழைய மகாபலிபுரம் சாலை", "lat": 12.7842, "lon": 80.2215},

    # Vellore, Ranipet & Tirupathur
    "632001": {"district": "Vellore", "area_en": "Vellore Fort / Town", "area_ta": "வேலூர் கோட்டை / நகரம்", "lat": 12.9165, "lon": 79.1325},
    "632401": {"district": "Ranipet", "area_en": "Ranipet SIPCOT", "area_ta": "ராணிப்பேட்டை சிப்காட்", "lat": 12.9274, "lon": 79.3330},
    "635601": {"district": "Tirupathur", "area_en": "Tirupathur Town", "area_ta": "திருப்பத்தூர் நகரம்", "lat": 12.4958, "lon": 78.5678},

    # Krishnagiri & Dharmapuri
    "635001": {"district": "Krishnagiri", "area_en": "Krishnagiri Town", "area_ta": "கிருஷ்ணகிரி நகரம்", "lat": 12.5266, "lon": 78.2146},
    "635109": {"district": "Krishnagiri", "area_en": "Hosur Industrial Hub", "area_ta": "ஓசூர் தொழிற்பேட்டை", "lat": 12.7409, "lon": 77.8253},
    "636701": {"district": "Dharmapuri", "area_en": "Dharmapuri Town", "area_ta": "தருமபுரி நகரம்", "lat": 12.1211, "lon": 78.1582},

    # Tiruvannamalai, Viluppuram & Kallakurichi
    "606601": {"district": "Tiruvannamalai", "area_en": "Tiruvannamalai Temple", "area_ta": "திருவண்ணாமலை கோயில் நகரம்", "lat": 12.2253, "lon": 79.0747},
    "605602": {"district": "Viluppuram", "area_en": "Viluppuram Junction", "area_ta": "விழுப்புரம் சந்திப்பு", "lat": 11.9401, "lon": 79.4861},
    "606202": {"district": "Kallakurichi", "area_en": "Kallakurichi Town", "area_ta": "கள்ளக்குறிச்சி நகரம்", "lat": 11.7375, "lon": 78.9632},

    # Salem & Namakkal
    "636001": {"district": "Salem", "area_en": "Salem Old Bus Stand", "area_ta": "சேலம் பழைய பேருந்து நிலையம்", "lat": 11.6643, "lon": 78.1460},
    "637101": {"district": "Salem", "area_en": "Edappadi Town", "area_ta": "எடப்பாடி நகரம்", "lat": 11.5833, "lon": 77.8500},
    "637001": {"district": "Namakkal", "area_en": "Namakkal Fort", "area_ta": "நாமக்கல் கோட்டை", "lat": 11.2189, "lon": 78.1674},
    "637211": {"district": "Namakkal", "area_en": "Tiruchengode", "area_ta": "திருச்செங்கோடு", "lat": 11.3808, "lon": 77.8942},

    # Erode, Tiruppur & Coimbatore
    "638001": {"district": "Erode", "area_en": "Erode Junction / Market", "area_ta": "ஈரோடு சந்திப்பு / ஜவுளி சந்தை", "lat": 11.3410, "lon": 77.7172},
    "641601": {"district": "Tiruppur", "area_en": "Tiruppur Cotton Hub", "area_ta": "திருப்பூர் பின்னலாடை நகரம்", "lat": 11.1085, "lon": 77.3411},
    "641001": {"district": "Coimbatore", "area_en": "Coimbatore Gandhipuram", "area_ta": "கோயம்புத்தூர் காந்திபுரம்", "lat": 11.0168, "lon": 76.9558},
    "642001": {"district": "Coimbatore", "area_en": "Pollachi Town", "area_ta": "பொள்ளாச்சி நகரம்", "lat": 10.6609, "lon": 77.0048},

    # Nilgiris
    "643001": {"district": "Nilgiris", "area_en": "Udhagamandalam (Ooty)", "area_ta": "உதகமண்டலம் (ஊட்டி)", "lat": 11.4102, "lon": 76.6950},
    "643101": {"district": "Nilgiris", "area_en": "Coonoor", "area_ta": "குன்னூர்", "lat": 11.3530, "lon": 76.7959},

    # Dindigul & Theni
    "624001": {"district": "Dindigul", "area_en": "Dindigul Rock Fort", "area_ta": "திண்டுக்கல் மலைக்கோட்டை", "lat": 10.3673, "lon": 77.9803},
    "624601": {"district": "Dindigul", "area_en": "Palani Murugan Temple", "area_ta": "பழனி தண்டாயுதபாணி கோயில்", "lat": 10.4500, "lon": 77.5167},
    "625531": {"district": "Theni", "area_en": "Theni Allinagaram", "area_ta": "தேனி அல்லிநகரம்", "lat": 10.0104, "lon": 77.4768},

    # Madurai & Virudhunagar
    "625001": {"district": "Madurai", "area_en": "Madurai Meenakshi Temple", "area_ta": "மதுரை மீனாட்சி அம்மன் கோயில்", "lat": 9.9195, "lon": 78.1193},
    "625106": {"district": "Madurai", "area_en": "Melur Agri Belt", "area_ta": "மேலூர் விவசாயப் பகுதி", "lat": 10.0333, "lon": 78.3333},
    "625214": {"district": "Madurai", "area_en": "Sholavandan Agri Belt", "area_ta": "சோழவந்தான் விவசாயப் பகுதி", "lat": 10.0240, "lon": 78.0120},
    "626001": {"district": "Virudhunagar", "area_en": "Virudhunagar Town", "area_ta": "விருதுநகர் நகரம்", "lat": 9.5680, "lon": 77.9624},
    "626123": {"district": "Virudhunagar", "area_en": "Sivakasi Fireworks Hub", "area_ta": "சிவகாசி", "lat": 9.4533, "lon": 77.7947},

    # Karur, Tiruchirappalli, Perambalur & Ariyalur
    "639001": {"district": "Karur", "area_en": "Karur Textile City", "area_ta": "கரூர் ஜவுளி நகரம்", "lat": 10.9601, "lon": 78.0766},
    "620001": {"district": "Tiruchirappalli", "area_en": "Tiruchirappalli Central", "area_ta": "திருச்சிராப்பள்ளி மத்தி / சத்திரம்", "lat": 10.7905, "lon": 78.7047},
    "620006": {"district": "Tiruchirappalli", "area_en": "Srirangam Ranganathaswamy", "area_ta": "ஸ்ரீரங்கம் திருத்தலம்", "lat": 10.8622, "lon": 78.6908},
    "621212": {"district": "Perambalur", "area_en": "Perambalur Town", "area_ta": "பெரம்பலூர் நகரம்", "lat": 11.2333, "lon": 78.8833},
    "621704": {"district": "Ariyalur", "area_en": "Ariyalur Cement Hub", "area_ta": "அரியலூர் நகரம்", "lat": 11.1401, "lon": 79.0786},

    # Cuddalore, Mayiladuthurai, Nagapattinam & Tiruvarur
    "607001": {"district": "Cuddalore", "area_en": "Cuddalore Port / Town", "area_ta": "கடலூர் துறைமுகம் / நகரம்", "lat": 11.7480, "lon": 79.7714},
    "608001": {"district": "Cuddalore", "area_en": "Chidambaram Natarajar Temple", "area_ta": "சிதம்பரம் நடராஜர் கோயில்", "lat": 11.3992, "lon": 79.6936},
    "609001": {"district": "Mayiladuthurai", "area_en": "Mayiladuthurai Junction", "area_ta": "மயிலாடுதுறை சந்திப்பு", "lat": 11.1018, "lon": 79.6522},
    "611001": {"district": "Nagapattinam", "area_en": "Nagapattinam Port", "area_ta": "நாகப்பட்டினம் துறைமுகம்", "lat": 10.7672, "lon": 79.8449},
    "610001": {"district": "Tiruvarur", "area_en": "Tiruvarur Thyagaraja Temple", "area_ta": "திருவாரூர் தியாகராஜர் கோயில்", "lat": 10.7725, "lon": 79.6365},

    # Thanjavur & Pudukkottai
    "613001": {"district": "Thanjavur", "area_en": "Thanjavur Brihadisvara Temple", "area_ta": "தஞ்சாவூர் பெரிய கோயில்", "lat": 10.7870, "lon": 79.1378},
    "612001": {"district": "Thanjavur", "area_en": "Kumbakonam Mahamaham", "area_ta": "கும்பகோணம் மகாமகம் நகரம்", "lat": 10.9602, "lon": 79.3845},
    "622001": {"district": "Pudukkottai", "area_en": "Pudukkottai Palace", "area_ta": "புதுக்கோட்டை அரண்மனை", "lat": 10.3797, "lon": 78.8208},

    # Sivaganga & Ramanathapuram
    "630001": {"district": "Sivaganga", "area_en": "Karaikudi Chettinad", "area_ta": "காரைக்குடி செட்டிநாடு", "lat": 10.0735, "lon": 78.7732},
    "623501": {"district": "Ramanathapuram", "area_en": "Ramanathapuram Town", "area_ta": "ராமநாதபுரம் நகரம்", "lat": 9.3639, "lon": 78.8395},
    "623526": {"district": "Ramanathapuram", "area_en": "Rameswaram Temple Island", "area_ta": "ராமேஸ்வரம் தீவு", "lat": 9.2876, "lon": 79.3129},

    # Thoothukudi, Tirunelveli, Tenkasi & Kanniyakumari
    "628001": {"district": "Thoothukudi", "area_en": "Thoothukudi Pearl City", "area_ta": "தூத்துக்குடி முத்துநகர் துறைமுகம்", "lat": 8.7642, "lon": 78.1348},
    "627001": {"district": "Tirunelveli", "area_en": "Tirunelveli Junction", "area_ta": "திருநெல்வேலி சந்திப்பு", "lat": 8.7139, "lon": 77.7567},
    "627811": {"district": "Tenkasi", "area_en": "Tenkasi Courtallam Falls", "area_ta": "தென்காசி குற்றாலம்", "lat": 8.9594, "lon": 77.3149},
    "629001": {"district": "Kanniyakumari", "area_en": "Nagercoil Central", "area_ta": "நாகர்கோவில் மத்தி", "lat": 8.1833, "lon": 77.4119},
    "629702": {"district": "Kanniyakumari", "area_en": "Kanniyakumari Sunset Point", "area_ta": "கன்னியாகுமரி முக்கடல் சங்கமம்", "lat": 8.0883, "lon": 77.5385}
}


def resolve_location_by_pincode(pincode: str) -> Dict[str, Any]:
    """Finds exact or nearest district match for a given 6-digit Indian postal pincode."""
    clean_pin = re.sub(r"[^0-9]", "", str(pincode).strip())
    if len(clean_pin) != 6:
        # Fallback to default Chennai Central
        return {
            "matched": False,
            "pincode": "600003",
            "district": "Chennai",
            "area_en": "Chennai Central / Park Town",
            "area_ta": "சென்னை சென்ட்ரல் / பூங்கா நகர்",
            "lat": 13.0827,
            "lon": 80.2707,
            "maps_url": "https://www.google.com/maps/search/?api=1&query=13.0827,80.2707"
        }

    if clean_pin in TN_PINCODE_DIRECTORY:
        info = TN_PINCODE_DIRECTORY[clean_pin]
        return {
            "matched": True,
            "pincode": clean_pin,
            "district": info["district"],
            "area_en": info["area_en"],
            "area_ta": info["area_ta"],
            "lat": info["lat"],
            "lon": info["lon"],
            "maps_url": f"https://www.google.com/maps/search/?api=1&query={info['lat']},{info['lon']}"
        }

    # Match by 3-digit prefix
    prefix = clean_pin[:3]
    for pin, data in TN_PINCODE_DIRECTORY.items():
        if pin.startswith(prefix):
            return {
                "matched": True,
                "pincode": clean_pin,
                "district": data["district"],
                "area_en": f"{data['district']} Region (Near {data['area_en']})",
                "area_ta": f"{data['district']} மண்டலம் ({data['area_ta']})",
                "lat": data["lat"],
                "lon": data["lon"],
                "maps_url": f"https://www.google.com/maps/search/?api=1&query={data['lat']},{data['lon']}"
            }

    # Default to Madurai Agri Heart of TN
    return {
        "matched": False,
        "pincode": clean_pin,
        "district": "Madurai",
        "area_en": "Madurai District Belt",
        "area_ta": "மதுரை மாவட்ட மண்டலம்",
        "lat": 9.9195,
        "lon": 78.1193,
        "maps_url": "https://www.google.com/maps/search/?api=1&query=9.9195,78.1193"
    }


def resolve_pincode_by_coordinates(lat: float, lon: float) -> Dict[str, Any]:
    """Finds nearest Tamil Nadu district, pincode, and area using Haversine distance."""
    closest_pin = "600003"
    min_dist = float("inf")

    for pin, data in TN_PINCODE_DIRECTORY.items():
        # Simple Haversine approx
        d_lat = math.radians(data["lat"] - lat)
        d_lon = math.radians(data["lon"] - lon)
        a = (math.sin(d_lat / 2) ** 2 +
             math.cos(math.radians(lat)) * math.cos(math.radians(data["lat"])) *
             math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist_km = 6371 * c

        if dist_km < min_dist:
            min_dist = dist_km
            closest_pin = pin

    info = TN_PINCODE_DIRECTORY[closest_pin]
    return {
        "pincode": closest_pin,
        "district": info["district"],
        "area_en": info["area_en"],
        "area_ta": info["area_ta"],
        "lat": lat,
        "lon": lon,
        "distance_to_centre_km": round(min_dist, 1),
        "maps_url": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    }


# -----------------------------------------------------------------------------
# 2. MOBILITY & GOODS LOGISTICS (RAPIDO / AUTO / CAB / CHOTA HATHI)
# -----------------------------------------------------------------------------
MOBILITY_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "bike",
        "name_ta": "SIA ரேபிடோ பைக் டாக்சி",
        "name_en": "SIA Rapido Bike Taxi",
        "icon": "🛵",
        "category": "mobility",
        "capacity": "1 பயணி (Single Rider)",
        "base_fare": 20,
        "base_km": 1.0,
        "per_km": 6,
        "estimated_arrival_mins": 4,
        "desc_ta": "போக்குவரத்து நெரிசலில் அதிவிரைவாக செல்ல சிக்கனமான பைக் பயணம். ஹெல்மெட் கட்டாயம்.",
        "desc_en": "Fastest single-rider commute through town traffic. Sanitized helmet provided."
    },
    {
        "id": "auto",
        "name_ta": "SIA நம்ம ஆட்டோ",
        "name_en": "SIA Namma Auto",
        "icon": "🛺",
        "category": "mobility",
        "capacity": "3 பயணிகள் (3 Passengers)",
        "base_fare": 30,
        "base_km": 1.5,
        "per_km": 13,
        "estimated_arrival_mins": 6,
        "desc_ta": "அரசு மீட்டருக்கு நிகரான வெளிப்படையான கட்டணத்தில் பாதுகாப்பான ஆட்டோ சவாரி.",
        "desc_en": "Safe, fixed meter rate auto ride across city and rural hubs."
    },
    {
        "id": "mini",
        "name_ta": "SIA மினி கார் (WagonR / Indica)",
        "name_en": "SIA Mini AC Cab",
        "icon": "🚗",
        "category": "mobility",
        "capacity": "4 பயணிகள் (AC 4 Seats)",
        "base_fare": 99,
        "base_km": 3.0,
        "per_km": 11,
        "estimated_arrival_mins": 8,
        "desc_ta": "குடும்பத்துடன் ஏசி வசதியுடன் மிதமான கட்டணத்தில் பயணம் செய்ய.",
        "desc_en": "Affordable AC cab for daily family visits, railway stations, and hospitals."
    },
    {
        "id": "sedan",
        "name_ta": "SIA பிரீமியம் செடான் (RedTaxi)",
        "name_en": "SIA RedTaxi / Sedan",
        "icon": "🚘",
        "category": "mobility",
        "capacity": "4 பயணிகள் (AC Boot Space)",
        "base_fare": 149,
        "base_km": 4.0,
        "per_km": 13,
        "estimated_arrival_mins": 9,
        "desc_ta": "சொகுசான நீண்ட தூர மற்றும் விமான நிலைய பயணங்களுக்கான செடான் கார்.",
        "desc_en": "Comfortable Dzire/Etios for business and outstation pilgrimage tours."
    },
    {
        "id": "goods_mini",
        "name_ta": "SIA சரக்கு வேன் (டாடா ஏஸ் / தோஸ்த்)",
        "name_en": "SIA Goods Mini-Truck (Tata Ace / Dost)",
        "icon": "🚚",
        "category": "mobility",
        "capacity": "1 டன் சரக்கு (1 Ton Payload)",
        "base_fare": 250,
        "base_km": 3.0,
        "per_km": 20,
        "estimated_arrival_mins": 12,
        "desc_ta": "விவசாய விளைபொருட்கள், உரம், கட்டுமானப் பொருட்கள், வீடு மாற்ற சரக்கு போக்குவரத்து.",
        "desc_en": "Reliable freight mini-truck for agri produce, market transport, and shifting."
    }
]


# -----------------------------------------------------------------------------
# 3. AGRI MACHINERY & IMPLEMENTS (CUSTOM HIRING CENTRE / E-VAADAGAI)
# -----------------------------------------------------------------------------
AGRI_MACHINERY_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "tractor_rotavator",
        "name_ta": "டிராக்டர் உழவு & ரோட்டாவேட்டர் (45-55 HP)",
        "name_en": "Tractor with Rotavator / Plough (45-55 HP)",
        "icon": "🚜",
        "category": "agri_machinery",
        "unit": "hour",
        "rate_per_unit": 850,
        "includes": "டீசல் + அனுபவமிக்க டிரைவர்",
        "desc_ta": "வயல் உழவு, வரப்பு வெட்டுதல், புழுதி உழவு மற்றும் தட்டை வெட்ட உகந்தது.",
        "desc_en": "Dry & wet land ploughing with heavy-duty rotavator. Diesel & driver included."
    },
    {
        "id": "paddy_harvester",
        "name_ta": "நெல் அறுவடை இயந்திரம் (Combined Harvester)",
        "name_en": "Combined Paddy Harvester (Wheel/Track)",
        "icon": "🌾",
        "category": "agri_machinery",
        "unit": "hour",
        "rate_per_unit": 2100,
        "includes": "அறுவடை + கதிரடித்தல் + தூய்மை செய்தல்",
        "desc_ta": "ஈரநில சேற்றிலும் இயங்கும் டிராக் வகை அறுவடை இயந்திரம். 1 மணி நேரத்தில் 1 ஏக்கர் வரை அறுவடை.",
        "desc_en": "All-in-one paddy harvesting, threshing and grain separation. 1 acre/hour."
    },
    {
        "id": "power_tiller",
        "name_ta": "பவர் டில்லர் (12-15 HP)",
        "name_en": "Power Tiller (12-15 HP)",
        "icon": "🚜",
        "category": "agri_machinery",
        "unit": "hour",
        "rate_per_unit": 500,
        "includes": "ஆபரேட்டர் + ரோட்டரி பிளேடுகள்",
        "desc_ta": "சிறிய நிலங்கள், நஞ்சை வயல்கள் மற்றும் தென்னந்தோப்பு உழவுக்கு உகந்தது.",
        "desc_en": "Compact tiller for small farms, wet paddy fields, and coconut orchards."
    },
    {
        "id": "agri_drone",
        "name_ta": "விவசாய பூச்சிக்கொல்லி & உரம் தெளிக்கும் ட்ரோன்",
        "name_en": "Agricultural Drone Sprayer (10L/16L)",
        "icon": "🛸",
        "category": "agri_machinery",
        "unit": "acre",
        "rate_per_unit": 400,
        "includes": "ட்ரோன் பைலட் + 10 நிமிடத்தில் 1 ஏக்கர்",
        "desc_ta": "மருந்து வீணாகாமல் துல்லியமாக பூச்சிக்கொல்லி, நானோ யூரியா தெளிக்க ட்ரோன் சேவை.",
        "desc_en": "Precision GPS aerial spraying of pesticides and nano urea in 10 minutes/acre."
    },
    {
        "id": "diesel_pump",
        "name_ta": "டீசல் பாசன பம்ப் செட் (5 HP Portable)",
        "name_en": "Portable Diesel / Solar Irrigation Pump (5 HP)",
        "icon": "💧",
        "category": "agri_machinery",
        "unit": "day",
        "rate_per_unit": 800,
        "includes": "பம்ப் செட் + 50 அடி டெலிவரி குழாய்",
        "desc_ta": "மின்சாரம் இல்லாத அவசர நேரங்களில் ஏரி, குளம், கிணறுகளில் இருந்து தண்ணீர் பாய்ச்ச.",
        "desc_en": "Emergency irrigation water pumping from wells and ponds. 50ft hose included."
    },
    {
        "id": "straw_baler",
        "name_ta": "வைக்கோல் உருண்டை கட்டும் இயந்திரம் (Straw Baler)",
        "name_en": "Paddy Straw Baler Machine",
        "icon": "📦",
        "category": "agri_machinery",
        "unit": "hour",
        "rate_per_unit": 750,
        "includes": "கட்டும் கயிறு + டிராக்டர் இயக்கம்",
        "desc_ta": "அறுவடைக்கு பின் வைக்கோலை சுத்தமாக உருண்டையாக கட்டி கால்நடை தீவனத்திற்கு பாதுகாக்க.",
        "desc_en": "Automated straw gathering and round/square baling for cattle feed storage."
    }
]


# -----------------------------------------------------------------------------
# 4. DAILY WAGE LABORERS & SKILLED ARTISANS (தினக்கூலி & கைவினைஞர் சந்தை)
# -----------------------------------------------------------------------------
LABOR_MARKET_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "farm_labor",
        "name_ta": "விவசாய தினக்கூலி தொழிலாளர் (நடவு / களை / அறுவடை)",
        "name_en": "Agricultural Farm Laborer (Transplanting/Weeding)",
        "icon": "🧑‍🌾",
        "category": "labor",
        "unit": "day (8 hours)",
        "rate_per_unit": 450,
        "govt_act": "தமிழ்நாடு விவசாய தொழிலாளர்கள் குறைந்தபட்ச கூலிச் சட்டம் 1948",
        "desc_ta": "நெல் நடவு, வாழை பராமரிப்பு, களை எடுத்தல், காய்கறி பறிப்பு மற்றும் பண்ணை வேலைகள்.",
        "desc_en": "Experienced farm hand for transplanting, weeding, crop care, and plucking."
    },
    {
        "id": "coconut_climber",
        "name_ta": "தென்னை மரம் ஏறுபவர் & தேங்காய் பறிப்பாளர்",
        "name_en": "Coconut Tree Climber & Harvester",
        "icon": "🌴",
        "category": "labor",
        "unit": "tree (or day: ₹800)",
        "rate_per_unit": 50,
        "govt_act": "பாதுகாப்பு உபகரணங்களுடன் கூடிய கிராமிய தொழில் திட்டம்",
        "desc_ta": "பாதுகாப்பு பெல்ட் மூலம் மரம் ஏறி தேங்காய் பறித்தல், மட்டை கவாத்து மற்றும் பூச்சி சுத்தம்.",
        "desc_en": "Skilled climber with safety harness for coconut harvesting and crown cleaning."
    },
    {
        "id": "head_mason",
        "name_ta": "தலைமை கொத்தனார் (Master Mason)",
        "name_en": "Head Mason / Building Construction Specialist",
        "icon": "🧱",
        "category": "labor",
        "unit": "day (8:30 AM - 5:30 PM)",
        "rate_per_unit": 1000,
        "govt_act": "தமிழ்நாடு கட்டுமானத் தொழிலாளர் நல வாரிய வழிகாட்டுதல்",
        "desc_ta": "அடித்தளம், செங்கல் கட்டுமானம், பூச்சு வேலை, டைல்ஸ் ஒட்டுதல் மற்றும் தளம் அமைத்தல்.",
        "desc_en": "Brick masonry, foundation alignment, plastering, flooring, and tiling expert."
    },
    {
        "id": "assistant_mason",
        "name_ta": "சித்தாள் / உதவியாளர் (Mason Helper)",
        "name_en": "Mason Assistant / Labor Helper",
        "icon": "👷",
        "category": "labor",
        "unit": "day (8:30 AM - 5:30 PM)",
        "rate_per_unit": 650,
        "govt_act": "தமிழ்நாடு கட்டுமானத் தொழிலாளர் நல வாரியம்",
        "desc_ta": "கலவை கலக்குதல், செங்கல் சுமத்தல், க்யூரிங் தண்ணீர் ஊற்றுதல் மற்றும் தூய்மை பணி.",
        "desc_en": "Mortar mixing, material shifting, brick soaking, and curing assistance."
    },
    {
        "id": "bar_bender",
        "name_ta": "கம்பி கட்டுபவர் & சென்ட்ரிங் தச்சர்",
        "name_en": "Steel Bar Bender & Centering Shuttering Worker",
        "icon": "🏗️",
        "category": "labor",
        "unit": "day (8 hours)",
        "rate_per_unit": 850,
        "govt_act": "தமிழ்நாடு கட்டுமானத் தொழிலாளர் நல வாரியம்",
        "desc_ta": "கான்கிரீட் கூரை கம்பி கட்டுதல், பில்லர் கம்பி அமைத்தல் மற்றும் பலகை சென்ட்ரிங் வேலை.",
        "desc_en": "TMT steel reinforcement bar bending, beam binding, and slab shuttering."
    },
    {
        "id": "electrician_plumber",
        "name_ta": "எலக்ட்ரீசியன் & பிளம்பர் (மின் & குழாய் பழுது)",
        "name_en": "Electrician & Plumber (Wiring / Pipes)",
        "icon": "⚡",
        "category": "labor",
        "unit": "visit (Day work: ₹800)",
        "rate_per_unit": 350,
        "govt_act": "அங்கீகரிக்கப்பட்ட ITI தொழில் வழிகாட்டல்",
        "desc_ta": "வீட்டு மின் வயரிங், மோட்டார் பழுது, குடிநீர் குழாய் அடைப்பு, பாத்ரூம் ஃபிட்டிங் சீரமைப்பு.",
        "desc_en": "Household electrical wiring, pump motor fixing, tap leaks, and PVC piping."
    },
    {
        "id": "painter",
        "name_ta": "வீட்டு பெயிண்டர் (House Painter)",
        "name_en": "House & Commercial Painter",
        "icon": "🎨",
        "category": "labor",
        "unit": "day (8 hours)",
        "rate_per_unit": 800,
        "govt_act": "தமிழ்நாடு முறைசாரா தொழிலாளர் நல வாரியம்",
        "desc_ta": "சுவர் பிரைமர், புட்டி போடுதல், எமல்ஷன் வர்ணம் பூசுதல் மற்றும் மர பாலிஷ் வேலை.",
        "desc_en": "Wall putty, primer coat, acrylic emulsion painting, and wood varnish coating."
    },
    {
        "id": "carpenter",
        "name_ta": "ஆசாரி / தச்சர் (Wood Artisan & Carpenter)",
        "name_en": "Wood Artisan & Furniture Carpenter",
        "icon": "🪚",
        "category": "labor",
        "unit": "day (8 hours)",
        "rate_per_unit": 950,
        "govt_act": "தமிழ்நாடு பாரம்பரிய கைவினைஞர் வழிகாட்டல்",
        "desc_ta": "மரக் கதவு, ஜன்னல் பொருத்துதல், அலமாரி, கட்டில் செய்தல் மற்றும் பூட்டு சீரமைப்பு.",
        "desc_en": "Teak/country wood door fitting, wardrobe woodwork, and lock maintenance."
    }
]


# -----------------------------------------------------------------------------
# 5. UNIFIED UPI DEEP LINK & QR CODE GENERATOR
# -----------------------------------------------------------------------------
def generate_upi_payment_bundle(
    amount: float,
    service_id: str,
    order_id: str,
    customer_name: str,
    payee_upi: str = "makkal.sia@oksbi",
    payee_name: str = "SIA Makkal Services"
) -> Dict[str, Any]:
    """
    Generates standard and app-specific UPI intent deep-links, dynamic QR code payload,
    and instructions for instant mobile checkout.
    """
    clean_amt = f"{amount:.2f}"
    txn_note = f"SIA-{service_id.upper()[:6]}-{order_id[:8]}"

    # Standard NPCI UPI Intent URL
    upi_intent_url = (
        f"upi://pay?pa={payee_upi}"
        f"&pn={quote_plus(payee_name)}"
        f"&am={clean_amt}"
        f"&cu=INR"
        f"&tn={quote_plus(txn_note)}"
        f"&tr={order_id}"
    )

    # 1-Click Launchers for Popular UPI Apps
    gpay_url = (
        f"gpay://upi/pay?pa={payee_upi}"
        f"&pn={quote_plus(payee_name)}"
        f"&am={clean_amt}"
        f"&cu=INR"
        f"&tn={quote_plus(txn_note)}"
    )

    phonepe_url = (
        f"phonepe://pay?pa={payee_upi}"
        f"&pn={quote_plus(payee_name)}"
        f"&am={clean_amt}"
        f"&cu=INR"
        f"&tn={quote_plus(txn_note)}"
    )

    paytm_url = (
        f"paytmmp://pay?pa={payee_upi}"
        f"&pn={quote_plus(payee_name)}"
        f"&am={clean_amt}"
        f"&cu=INR"
        f"&tn={quote_plus(txn_note)}"
    )

    # Public QR Code generator endpoint via public API (works without third-party key)
    qr_code_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=260x260&data={quote_plus(upi_intent_url)}"

    return {
        "payee_upi": payee_upi,
        "payee_name": payee_name,
        "amount": amount,
        "amount_formatted": f"₹{amount:,.2f}",
        "txn_note": txn_note,
        "order_id": order_id,
        "upi_intent_url": upi_intent_url,
        "gpay_url": gpay_url,
        "phonepe_url": phonepe_url,
        "paytm_url": paytm_url,
        "qr_code_image_url": qr_code_image_url
    }


# -----------------------------------------------------------------------------
# 6. ON-DEMAND BOOKING & ESTIMATE ENGINE
# -----------------------------------------------------------------------------
def get_service_catalog_item(service_id: str) -> Optional[Dict[str, Any]]:
    """Looks up item across mobility, agri machinery, and labor catalogs."""
    all_items = MOBILITY_CATALOG + AGRI_MACHINERY_CATALOG + LABOR_MARKET_CATALOG
    for item in all_items:
        if item["id"].lower() == service_id.lower():
            return item
    return None


def calculate_service_quote(
    service_id: str,
    pincode: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    duration_units: float = 1.0,
    distance_km: float = 5.0
) -> Dict[str, Any]:
    """Calculates full quotation, base fare, GST (nil on farm labor), and ETA."""
    item = get_service_catalog_item(service_id)
    if not item:
        # Default to Rapido Bike Taxi
        item = MOBILITY_CATALOG[0]

    # Resolve location
    if lat is not None and lon is not None:
        loc_info = resolve_pincode_by_coordinates(lat, lon)
    elif pincode:
        loc_info = resolve_location_by_pincode(pincode)
    else:
        loc_info = resolve_location_by_pincode("600003")

    category = item.get("category", "mobility")
    breakdown = {}
    total_amount = 0.0

    if category == "mobility":
        base = item["base_fare"]
        base_km = item["base_km"]
        extra_km = max(0.0, distance_km - base_km)
        distance_charge = extra_km * item["per_km"]
        total_amount = base + distance_charge
        breakdown = {
            "type": "mobility",
            "base_fare": base,
            "base_included_km": base_km,
            "extra_km": round(extra_km, 1),
            "rate_per_km": item["per_km"],
            "distance_km": round(distance_km, 1),
            "estimated_mins": int(distance_km * 2.8) + item.get("estimated_arrival_mins", 5)
        }
    elif category == "agri_machinery":
        rate = item["rate_per_unit"]
        total_amount = rate * max(1.0, duration_units)
        breakdown = {
            "type": "agri_machinery",
            "unit": item["unit"],
            "rate_per_unit": rate,
            "quantity": duration_units,
            "includes": item.get("includes", "இயந்திரம் + ஆபரேட்டர்")
        }
    elif category == "labor":
        rate = item["rate_per_unit"]
        total_amount = rate * max(1.0, duration_units)
        breakdown = {
            "type": "labor",
            "unit": item["unit"],
            "rate_per_unit": rate,
            "workers_or_units": duration_units,
            "statutory_act": item.get("govt_act", "குறைந்தபட்ச கூலிச் சட்டம் 1948")
        }

    total_amount = round(total_amount, 2)

    return {
        "service": item,
        "location": loc_info,
        "breakdown": breakdown,
        "total_amount": total_amount,
        "total_amount_formatted": f"₹{total_amount:,.2f}"
    }


def create_hyperlocal_booking(
    service_id: str,
    customer_phone: str = "9840123456",
    customer_name: Optional[str] = None,
    pincode: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    pickup_address: Optional[str] = None,
    destination_address: Optional[str] = None,
    duration_units: float = 1.0,
    distance_km: float = 5.0,
    custom_upi_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Creates an end-to-end booking:
    1. Computes statutory rates and ETA.
    2. Assigns simulated verified nearby provider & 4-digit start OTP.
    3. Generates Dynamic UPI Intent & QR Code.
    4. Formats WhatsApp and Web response payloads.
    """
    quote = calculate_service_quote(
        service_id=service_id,
        pincode=pincode,
        lat=lat,
        lon=lon,
        duration_units=duration_units,
        distance_km=distance_km
    )

    clean_phone = re.sub(r"[^0-9]", "", str(customer_phone))
    c_name = customer_name or f"வாடிக்கையாளர் ({clean_phone[-4:] if len(clean_phone) >= 4 else 'தோழர்'})"
    order_id = f"SIA-{uuid.uuid4().hex[:8].upper()}"
    start_otp = f"{random.randint(1000, 9999)}"

    # Generate UPI Payment Bundle
    upi_id = custom_upi_id or "makkal.sia@oksbi"
    upi_bundle = generate_upi_payment_bundle(
        amount=quote["total_amount"],
        service_id=service_id,
        order_id=order_id,
        customer_name=c_name,
        payee_upi=upi_id
    )

    # Simulated Verified Nearby Provider
    provider_names = [
        ("மாரிமுத்து (Marimuthu)", "+919443156781", "4.9 ★ (1,240 சவாரிகள்)"),
        ("முருகேசன் (Murugesan)", "+919443278912", "4.8 ★ (980 சவாரிகள்)"),
        ("செல்வராஜ் (Selvaraj)", "+919443312345", "5.0 ★ (450 சவாரிகள்)"),
        ("கார்த்திக் (Karthik)", "+919443498765", "4.8 ★ (620 சவாரிகள்)"),
        ("ஆறுமுகம் (Arumugam)", "+919443587654", "4.9 ★ (1,890 சவாரிகள்)")
    ]
    p_name, p_phone, p_rating = random.choice(provider_names)

    booking_record = {
        "status": "confirmed",
        "order_id": order_id,
        "start_otp": start_otp,
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
        "customer_phone": clean_phone,
        "customer_name": c_name,
        "service": quote["service"],
        "location": quote["location"],
        "pickup_address": pickup_address or quote["location"]["area_ta"],
        "destination_address": destination_address,
        "breakdown": quote["breakdown"],
        "total_amount": quote["total_amount"],
        "total_amount_formatted": quote["total_amount_formatted"],
        "provider": {
            "name": p_name,
            "phone": p_phone,
            "rating": p_rating,
            "arrival_time_mins": quote["service"].get("estimated_arrival_mins", 5)
        },
        "payment": upi_bundle
    }

    return booking_record


def format_whatsapp_hyperlocal_receipt(booking: Dict[str, Any]) -> str:
    """Formats rich, elegant WhatsApp message for the booked ride/service."""
    svc = booking["service"]
    loc = booking["location"]
    pay = booking["payment"]
    prov = booking["provider"]

    msg = (
        f"{svc['icon']} *SIA மக்கள் சேவை முன்பதிவு உறுதி செய்யப்பட்டது!* ✅\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• *சேவை:* {svc['name_ta']} ({svc['name_en']})\n"
        f"• *முன்பதிவு எண்:* `{booking['order_id']}`\n"
        f"• *துவக்க OTP:* 🔑 *`{booking['start_otp']}`* (சேவை துவங்கும் போது கூறவும்)\n\n"
        f"📍 *இடம் & பின்கோடு:* {loc['area_ta']} (பின்கோடு: `{loc['pincode']}`)\n"
        f"🗺️ *Google Maps:* {loc['maps_url']}\n\n"
        f"👤 *ஒதுக்கப்பட்ட ஓட்டுநர் / பணியாளர்:*\n"
        f"• பெயர்: {prov['name']}\n"
        f"• தொலைபேசி: {prov['phone']}\n"
        f"• மதிப்பீடு: {prov['rating']}\n"
        f"• வருகை நேரம்: ~{prov['arrival_time_mins']} நிமிடங்கள்\n\n"
        f"💰 *மொத்தக் கட்டணம்:* *{booking['total_amount_formatted']}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 *1-கிளிக் UPI மூலம் பணம் செலுத்த:*\n"
        f"1. 🟢 *Google Pay (GPay):*\n{pay['gpay_url']}\n\n"
        f"2. 🟣 *PhonePe:*\n{pay['phonepe_url']}\n\n"
        f"3. 🔵 *Paytm / BHIM / Other UPI:*\n{pay['upi_intent_url']}\n\n"
        f"📱 *நேரடி UPI ID:* `{pay['payee_upi']}`\n"
        f"_(தொகையை நேரடியாக செலுத்த UPI செயலியில் மேற்கண்ட ID-ஐ நகலெடுக்கலாம்)_\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ *அவசர உதவிக்கு:* 112 SOS | 100 காவல் | SIA உதவி மையம்"
    )

    return msg[:4090]
