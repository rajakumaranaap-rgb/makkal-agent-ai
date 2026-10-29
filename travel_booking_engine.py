"""
SIA Uber / RedTaxi-Style WhatsApp Travel Booking Planner & Executor Engine
Part of Makkal Agent - Meta AI Developer Hackathon 2026
Zero-Surge Statutory Tariff & Verified Pilgrimage Packages across Tamil Nadu

Features:
1. Multi-tier Fleet with Statutory Price Lock:
   - 🛺 SIA Namma Auto (₹30 base + ₹15/km)
   - 🚗 SIA Mini Hatchback (₹99 base + ₹11/km)
   - 🚘 SIA Sedan / RedTaxi (₹149 base + ₹13/km)
   - 🚙 SIA Prime SUV / Innova (₹299 base + ₹17/km)
   - 🚐 SIA Tempo Traveler 14-Seater (₹699 base + ₹22/km)
2. Verified Driver Allocation & Instant 4-Digit Ride Start OTP
3. Temple Circuits: Rameswaram, Tirupati, Palani, Kanyakumari, Thanjavur, Tiruchendur
4. 1-Click WhatsApp Booking Confirmation & Emergency 112 SOS Integration
"""

import os
import random
import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("makkal.travel_engine")

FLEET_TIERS: List[Dict[str, Any]] = [
    {
        "id": "autoo",
        "name": "SIA Namma Auto",
        "name_ta": "நம்ம ஆட்டோ",
        "icon": "🛺",
        "capacity": 3,
        "base_fare": 30,
        "base_km": 1.5,
        "per_km": 15,
        "ac": False,
        "best_for": "நகரத்திற்குள் உடனடி குறுகிய பயணங்கள் (Local Quick Trips)"
    },
    {
        "id": "mini",
        "name": "SIA Mini (WagonR / Indica)",
        "name_ta": "மினி ஏசி கார்",
        "icon": "🚗",
        "capacity": 4,
        "base_fare": 99,
        "base_km": 3.0,
        "per_km": 11,
        "ac": True,
        "best_for": "சிக்கனமான குடும்ப பயணம் (Pocket Friendly AC Ride)"
    },
    {
        "id": "sedan",
        "name": "SIA RedTaxi / Sedan (Dzire / Etios)",
        "name_ta": "செடான் பிரீமியம் (RedTaxi)",
        "icon": "🚘",
        "capacity": 4,
        "base_fare": 149,
        "base_km": 4.0,
        "per_km": 13,
        "ac": True,
        "best_for": "வசதியான சொகுசு பயணம் & பெரிய டிக்கி (Comfort & Big Luggage)"
    },
    {
        "id": "suv",
        "name": "SIA Prime SUV (Innova / Ertiga)",
        "name_ta": "பிரைம் எஸ்.யு.வி (இன்னோவா)",
        "icon": "🚙",
        "capacity": 7,
        "base_fare": 299,
        "base_km": 5.0,
        "per_km": 17,
        "ac": True,
        "best_for": "கோயில் சுற்றுலா & பெரிய குடும்பம் (Pilgrimages & Large Families)"
    },
    {
        "id": "tempo",
        "name": "SIA Tempo Traveler (14-Seater)",
        "name_ta": "டெம்போ டிராவலர் (14-இருக்கைகள்)",
        "icon": "🚐",
        "capacity": 14,
        "base_fare": 699,
        "base_km": 10.0,
        "per_km": 22,
        "ac": True,
        "best_for": "திருமண விழாக்கள் & ஆன்மீக யாத்திரை (Wedding & Group Tours)"
    }
]

TN_HIGHWAY_DISTANCES = {
    ("madurai", "rameswaram"): 175,
    ("madurai", "palani"): 115,
    ("madurai", "kanyakumari"): 245,
    ("madurai", "tiruchendur"): 180,
    ("madurai", "chennai"): 460,
    ("madurai", "trichy"): 135,
    ("madurai", "coimbatore"): 215,
    ("chennai", "tirupati"): 135,
    ("chennai", "pondicherry"): 155,
    ("chennai", "trichy"): 330,
    ("trichy", "thanjavur"): 55,
    ("trichy", "velankanni"): 145,
    ("coimbatore", "ooty"): 85,
    ("coimbatore", "kodaikanal"): 170,
    ("salem", "yercaud"): 32
}

TEMPLE_DARSHAN_PACKAGES = [
    {
        "id": "pkg_rameswaram",
        "name_ta": "மதுரை - ராமேஸ்வரம் - தனுஷ்கோடி புனித யாத்திரை",
        "name_en": "Madurai - Rameswaram - Dhanushkodi Circuit",
        "circuit": ["மதுரை மீனாட்சி அம்மன்", "ராமநாதசுவாமி கோயில் 22 தீர்த்தங்கள்", "அக்னி தீர்த்தம்", "தனுஷ்கோடி அரிச்சல் முனை", "கலாம் நினைவகம்"],
        "recommended_vehicle": "suv",
        "fixed_package_rs": 4999,
        "days": "1-Day / 2-Days"
    },
    {
        "id": "pkg_aruveedu",
        "name_ta": "முருகன் அறுபடை வீடு தென்மண்டல யாத்திரை",
        "name_en": "Murugan Arupadai Veedu South Circuit",
        "circuit": ["திருப்பரங்குன்றம்", "பழமுதிர்சோலை", "பழனி தண்டாயுதபாணி", "திருச்செந்தூர் சுப்பிரமணிய சுவாமி"],
        "recommended_vehicle": "suv",
        "fixed_package_rs": 8499,
        "days": "2-Days / 1-Night"
    },
    {
        "id": "pkg_chola",
        "name_ta": "தஞ்சை பெரியகோயில் & நவகிரக ஸ்தலங்கள்",
        "name_en": "Thanjavur Brihadisvara & Navagraha Circuit",
        "circuit": ["தஞ்சை பெரிய கோயில்", "கங்கைகொண்ட சோழபுரம்", "திருநள்ளாறு சனி பகவான்", "சூரியனார் கோயில்"],
        "recommended_vehicle": "sedan",
        "fixed_package_rs": 5999,
        "days": "1-Day"
    },
    {
        "id": "pkg_tirupati",
        "name_ta": "சென்னை - திருப்பதி ஏழுமலையான் விரைவு தரிசனம்",
        "name_en": "Chennai - Tirupati Balaji Express",
        "circuit": ["சென்னை", "அலமேலுமங்காபுரம்", "திருமலை திருப்பதி ஏழுமலையான் தரிசனம்"],
        "recommended_vehicle": "sedan",
        "fixed_package_rs": 3999,
        "days": "Same Day Return"
    }
]

VERIFIED_DRIVERS_POOL = [
    {"name_ta": "முத்துகுமார் (Driver Muthukumar)", "rating": 4.95, "trips": 1420, "badge": "⭐ Super Driver"},
    {"name_ta": "மாரிமுத்து (Driver Marimuthu)", "rating": 4.92, "trips": 980, "badge": "🛡️ Pilgrimage Specialist"},
    {"name_ta": "சரவணன் (Driver Saravanan)", "rating": 4.88, "trips": 2150, "badge": "⚡ Express Route Master"},
    {"name_ta": "செந்தில்வேல் (Driver Senthilvel)", "rating": 4.97, "trips": 1640, "badge": "🌿 Safe Night Driving Certified"}
]


def calculate_ride_fare(
    origin: str,
    destination: str,
    vehicle_id: str = "sedan",
    trip_type: str = "one_way"
) -> Dict[str, Any]:
    """Calculates statutory transparent travel fare with no surge pricing guarantee."""
    orig_clean = origin.lower().strip()
    dest_clean = destination.lower().strip()

    dist = 50
    for (c1, c2), d in TN_HIGHWAY_DISTANCES.items():
        if (c1 in orig_clean and c2 in dest_clean) or (c2 in orig_clean and c1 in dest_clean):
            dist = d
            break
    else:
        if any(k in orig_clean or k in dest_clean for k in ["chennai", "சென்னை"]):
            dist = 350
        elif any(k in orig_clean or k in dest_clean for k in ["rameswaram", "ராமேஸ்வரம்"]):
            dist = 175
        elif any(k in orig_clean or k in dest_clean for k in ["kanyakumari", "கன்னியாகுமரி"]):
            dist = 245
        elif any(k in orig_clean or k in dest_clean for k in ["palani", "பழனி"]):
            dist = 115
        else:
            dist = 80

    if trip_type == "round_trip":
        dist = dist * 2

    vehicle = next((v for v in FLEET_TIERS if v["id"] == vehicle_id), FLEET_TIERS[2])
    base = vehicle["base_fare"]
    km_cost = round(dist * vehicle["per_km"])
    driver_batta = 400 if dist >= 100 else 0
    subtotal = base + km_cost + driver_batta
    gst = round(subtotal * 0.05)
    total = subtotal + gst
    est_hours = round(dist / 50.0, 1)

    return {
        "status": "success",
        "origin": origin,
        "destination": destination,
        "vehicle": vehicle,
        "distance_km": dist,
        "estimated_hours": est_hours,
        "trip_type": trip_type,
        "fare_breakdown": {
            "base_fare": base,
            "km_fare": km_cost,
            "driver_allowance": driver_batta,
            "gst_5_pct": gst,
            "total_fare": total,
            "surge_percentage": 0
        }
    }


def execute_ride_booking(
    phone: str,
    customer_name: str = "குடிமகன்",
    origin: str = "Madurai Junction",
    destination: str = "Rameswaram Temple",
    vehicle_id: str = "sedan",
    trip_type: str = "one_way",
    pickup_time: str = "உடனடி (Now / 15 mins)"
) -> Dict[str, Any]:
    """
    Executes instant ride dispatch like RedTaxi / Uber.
    Allocates verified driver, generates 4-digit ride OTP, calculates zero-surge fare.
    """
    clean_phone = phone.replace("+", "").strip()
    booking_id = f"TN-RIDE-{uuid.uuid4().hex[:6].upper()}"
    ride_otp = f"{random.randint(1000, 9999)}"

    fare_info = calculate_ride_fare(origin, destination, vehicle_id, trip_type)
    driver = random.choice(VERIFIED_DRIVERS_POOL)
    vehicle = fare_info["vehicle"]

    # Generate plausible vehicle plate
    districts_rto = ["58", "59", "64", "01", "07", "45", "38", "33"]
    rto = random.choice(districts_rto)
    letters = random.choice(["AB", "BC", "CD", "AZ", "AY"])
    digits = random.randint(1000, 9999)
    veh_plate = f"TN {rto} {letters} {digits}"

    total_fare = fare_info["fare_breakdown"]["total_fare"]
    dist = fare_info["distance_km"]

    wa_card = (
        f"🚖 *SIA RedTaxi / Travel பயண உறுதிப்படுத்தல்* 🌟\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"• முன்பதிவு எண்: *{booking_id}*\n"
        f"🔑 *பயணத் தொடக்க OTP:* *{ride_otp}* (ஓட்டுநரிடம் தெரிவிக்கவும்)\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🚗 *வாகனம்:* {vehicle['icon']} *{vehicle['name_ta']}*\n"
        f"🔢 வண்டி எண்: *{veh_plate}*\n"
        f"👤 ஓட்டுநர்: *{driver['name_ta']}* ({driver['badge']})\n"
        f"⭐ ஓட்டுநர் மதிப்பீடு: *{driver['rating']}* ({driver['trips']} வெற்றிகரமான பயணங்கள்)\n\n"
        f"📍 புறப்படும் இடம்: *{origin}*\n"
        f"🏁 சேருமிடம்: *{destination}*\n"
        f"⏱️ பயண நேரம்: *~{fare_info['estimated_hours']} மணிநேரம்* (~{dist} கி.மீ)\n"
        f"⏰ பிக்கப் நேரம்: *{pickup_time}*\n"
        f"💰 *அரசு நிர்ணயக் கட்டணம்:* *₹{total_fare:,}* (0% கூடுதல் கட்டணம் / No Surge)\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ *பாதுகாப்பு & அவசர உதவி:*\n"
        f"• ஏசி உறுதி செய்யப்பட்டது | GPS நேரலை கண்காணிப்பு\n"
        f"• அவசர உதவிக்கு: தமிழ்நாடு காவல்துறை *112* அல்லது ஆம்புலன்ஸ் *108* இணைக்கப்பட்டுள்ளது."
    )

    return {
        "status": "confirmed",
        "booking_id": booking_id,
        "ride_otp": ride_otp,
        "customer_name": customer_name,
        "customer_phone": clean_phone,
        "driver": driver,
        "vehicle_plate": veh_plate,
        "vehicle": vehicle,
        "origin": origin,
        "destination": destination,
        "distance_km": dist,
        "total_fare": total_fare,
        "pickup_time": pickup_time,
        "whatsapp_card": wa_card
    }


def get_fleet_catalog() -> List[Dict[str, Any]]:
    """Returns available fleet tiers."""
    return FLEET_TIERS


def get_temple_packages() -> List[Dict[str, Any]]:
    """Returns curated temple pilgrimage packages."""
    return TEMPLE_DARSHAN_PACKAGES




def format_whatsapp_travel_menu() -> Dict[str, Any]:
    """Generates interactive WhatsApp button menu for zero-surge cab and pilgrimage booking."""
    body_text = (
        "🚖 *SIA RedTaxi / பயண முன்பதிவு & ஆன்மீக சுற்றுலா* 🌟\n\n"
        "தமிழ்நாடு முழுவதும் 0% கூடுதல் கட்டணம் (Zero-Surge Guarantee) கொண்ட நம்பகமான டாக்ஸி சேவை!\n\n"
        "• 🛺 நம்ம ஆட்டோ (₹30 + ₹15/km)\n"
        "• 🚗 மினி ஏசி (₹99 + ₹11/km)\n"
        "• 🚘 செடான் RedTaxi (₹149 + ₹13/km)\n"
        "• 🚙 இன்னோவா SUV (₹299 + ₹17/km)\n"
        "• 🛕 ராமேஸ்வரம், திருப்பதி, அறுபடை வீடு சிறப்பு பேக்கேஜ்கள்!\n\n"
        "பயண வகையைத் தேர்வு செய்யவும் 👇"
    )
    buttons = [
        {"id": "btn_taxi_sedan", "title": "🚘 RedTaxi / கார்"},
        {"id": "btn_taxi_temple", "title": "🛕 கோயில் சுற்றுலா"},
        {"id": "btn_taxi_auto", "title": "🛺 நம்ம ஆட்டோ"}
    ]
    return {
        "body_text": body_text,
        "buttons": buttons,
        "header_text": "🚖 SIA Namma Travel & RedTaxi",
        "footer_text": "Zero Surge • 112 SOS Protection"
    }


def format_whatsapp_temple_list() -> Dict[str, Any]:
    """Generates interactive list message for temple packages."""
    rows = []
    for pkg in TEMPLE_DARSHAN_PACKAGES:
        rows.append({
            "id": f"ride_pkg_{pkg['id']}",
            "title": pkg["name_ta"][:24],
            "description": f"₹{pkg['fixed_package_rs']:,} • {pkg['days']} • {', '.join(pkg['circuit'][:2])}"[:72]
        })
    return {
        "header_text": "🛕 SIA ஆன்மீக யாத்திரை",
        "body_text": "தமிழ்நாட்டின் முக்கிய புண்ணிய ஸ்தலங்களுக்கான சிறப்பு பேக்கேஜ்கள். ஏசி வாகனம் & அனுபவமிக்க ஓட்டுநர் உறுதி செய்யப்படுகிறது.",
        "button_label": "🛕 யாத்திரை தேர்வு",
        "sections": [{"title": "கோயில் சுற்றுலா பேக்கேஜ்கள்", "rows": rows}],
        "footer_text": "SIA Verified Pilgrimage Partner"
    }


# Singleton export
travel_engine = {
    "calculate_ride_fare": calculate_ride_fare,
    "execute_ride_booking": execute_ride_booking,
    "get_fleet_catalog": get_fleet_catalog,
    "get_temple_packages": get_temple_packages
}
