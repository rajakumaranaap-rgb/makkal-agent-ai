# -*- coding: utf-8 -*-
"""
==============================================================================
Makkal Agent AI - Hyperlocal Rentals, Agri Machinery & Gig Economy Suite
==============================================================================
Validates:
1. Pincode & Google Maps Geolocation across Tamil Nadu
2. Rapido Bike Taxi, Auto, Cab & Goods Mini-Truck Pricing
3. Custom Hiring Center (e-Vaadagai) Agri Machinery & Drones
4. Daily Wage Laborers & Masons (TN Minimum Wages Act 1948)
5. Dynamic UPI Intent & 1-Click Launchers (GPay, PhonePe, Paytm)
6. 4-Digit Security OTP & WhatsApp < 4096 Character Limits
==============================================================================
"""

import os
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))

from hyperlocal_rental_gig_engine import (
    resolve_location_by_pincode,
    resolve_pincode_by_coordinates,
    calculate_service_quote,
    create_hyperlocal_booking,
    format_whatsapp_hyperlocal_receipt,
    MOBILITY_CATALOG,
    AGRI_MACHINERY_CATALOG,
    LABOR_MARKET_CATALOG
)


def run_tests():
    print("=" * 70)
    print("🛵 RUNNING HYPERLOCAL RENTALS & GIG ECONOMY TEST SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Pincode and GPS Coordinates Resolution
    # -------------------------------------------------------------
    print("\n[TEST 1] Pincode & Location Resolution:")
    loc_chn = resolve_location_by_pincode("600082")
    print(f"  Pincode 600082 -> {loc_chn['district']}: {loc_chn['area_ta']}")
    assert loc_chn["district"] == "Chennai"
    assert "கொளத்தூர்" in loc_chn["area_ta"]

    loc_mdu = resolve_location_by_pincode("625001")
    print(f"  Pincode 625001 -> {loc_mdu['district']}: {loc_mdu['area_ta']}")
    assert loc_mdu["district"] == "Madurai"

    loc_cbe = resolve_location_by_pincode("641001")
    print(f"  Pincode 641001 -> {loc_cbe['district']}: {loc_cbe['area_ta']}")
    assert loc_cbe["district"] == "Coimbatore"

    loc_gps = resolve_pincode_by_coordinates(13.0827, 80.2707)
    print(f"  GPS (13.0827, 80.2707) -> {loc_gps['pincode']} {loc_gps['district']}: {loc_gps['area_en']}")
    assert loc_gps["district"] == "Chennai"
    print("  ✅ Pincode and GPS Geolocation resolved accurately!")

    # -------------------------------------------------------------
    # 2. Mobility Catalog & Pricing (Rapido Bike, Auto, Mini-Truck)
    # -------------------------------------------------------------
    print("\n[TEST 2] Mobility Fleet & Zero-Surge Pricing:")
    quote_bike = calculate_service_quote("bike", pincode="600082", distance_km=6.0)
    print(f"  Bike Taxi (6 km): {quote_bike['total_amount_formatted']} (Base ₹20 + 5km×₹6)")
    assert quote_bike["total_amount"] == 50.0

    quote_auto = calculate_service_quote("auto", pincode="600082", distance_km=5.0)
    print(f"  Namma Auto (5 km): {quote_auto['total_amount_formatted']}")
    assert quote_auto["total_amount"] > 50.0

    quote_truck = calculate_service_quote("goods_mini", pincode="636001", distance_km=8.0)
    print(f"  Goods Mini-Truck (8 km): {quote_truck['total_amount_formatted']}")
    assert quote_truck["total_amount"] == 350.0
    print("  ✅ Mobility pricing formulas verified!")

    # -------------------------------------------------------------
    # 3. Agri Machinery & Tools Custom Hiring (Tractor, Harvester, Drone)
    # -------------------------------------------------------------
    print("\n[TEST 3] Agri Machinery Custom Hiring (e-Vaadagai Rates):")
    quote_harv = calculate_service_quote("paddy_harvester", pincode="613001", duration_units=3.0)
    print(f"  Combined Harvester (3 hrs): {quote_harv['total_amount_formatted']} (3 × ₹2,100)")
    assert quote_harv["total_amount"] == 6300.0

    quote_trac = calculate_service_quote("tractor_rotavator", pincode="625106", duration_units=2.0)
    print(f"  Tractor Rotavator (2 hrs): {quote_trac['total_amount_formatted']} (2 × ₹850)")
    assert quote_trac["total_amount"] == 1700.0

    quote_drone = calculate_service_quote("agri_drone", pincode="610001", duration_units=4.0)
    print(f"  Agri Drone Sprayer (4 acres): {quote_drone['total_amount_formatted']} (4 × ₹400)")
    assert quote_drone["total_amount"] == 1600.0
    print("  ✅ Agri machinery statutory tariffs verified!")

    # -------------------------------------------------------------
    # 4. Daily Wage Laborers & Skilled Artisans
    # -------------------------------------------------------------
    print("\n[TEST 4] Daily Wage Laborers (TN Minimum Wages Act 1948):")
    quote_mason = calculate_service_quote("head_mason", pincode="641001", duration_units=2.0)
    print(f"  Head Mason (2 days): {quote_mason['total_amount_formatted']} (2 × ₹1,000)")
    assert quote_mason["total_amount"] == 2000.0

    quote_labor = calculate_service_quote("farm_labor", pincode="610001", duration_units=5.0)
    print(f"  Farm Labor (5 workers): {quote_labor['total_amount_formatted']} (5 × ₹450)")
    assert quote_labor["total_amount"] == 2250.0

    quote_climber = calculate_service_quote("coconut_climber", pincode="642001", duration_units=20.0)
    print(f"  Coconut Climber (20 trees): {quote_climber['total_amount_formatted']} (20 × ₹50)")
    assert quote_climber["total_amount"] == 1000.0
    print("  ✅ Daily wage labor market calculations verified!")

    # -------------------------------------------------------------
    # 5. End-to-End Booking & Dynamic UPI Deep Links
    # -------------------------------------------------------------
    print("\n[TEST 5] Booking Creation, 4-Digit Security OTP & Dynamic UPI Rail:")
    booking = create_hyperlocal_booking(
        service_id="paddy_harvester",
        customer_phone="9840123456",
        customer_name="செல்வம் (Selvam)",
        pincode="613001",
        duration_units=3.0
    )

    print(f"  Order ID: {booking['order_id']}")
    print(f"  Security OTP: {booking['start_otp']}")
    print(f"  Assigned Provider: {booking['provider']['name']} ({booking['provider']['phone']})")
    print(f"  Total Amount: {booking['total_amount_formatted']}")

    pay = booking["payment"]
    print(f"  UPI Intent: {pay['upi_intent_url'][:60]}...")
    print(f"  Google Pay: {pay['gpay_url'][:60]}...")
    print(f"  PhonePe: {pay['phonepe_url'][:60]}...")
    print(f"  QR Code URL: {pay['qr_code_image_url'][:60]}...")

    assert len(booking["start_otp"]) == 4 and booking["start_otp"].isdigit()
    assert "upi://pay" in pay["upi_intent_url"]
    assert "gpay://" in pay["gpay_url"]
    assert "phonepe://" in pay["phonepe_url"]
    assert pay["amount"] == 6300.0
    print("  ✅ Dynamic UPI payment intent & OTP generated successfully!")

    # -------------------------------------------------------------
    # 6. WhatsApp Message Length Compliance (< 4,096 chars)
    # -------------------------------------------------------------
    print("\n[TEST 6] WhatsApp Cloud API Message Length Audit:")
    receipt = format_whatsapp_hyperlocal_receipt(booking)
    print(f"  Receipt Length: {len(receipt)} characters (Limit: 4096)")
    assert len(receipt) <= 4096, f"Receipt exceeds 4096 chars: {len(receipt)}"
    assert "🔑" in receipt or "OTP" in receipt
    assert "UPI" in receipt
    print("  ✅ WhatsApp receipt strictly complies with Meta Cloud API character limits!")

    print("\n" + "=" * 70)
    print("🎉 ALL HYPERLOCAL RENTALS & GIG ECONOMY TESTS PASSED (6/6)!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
