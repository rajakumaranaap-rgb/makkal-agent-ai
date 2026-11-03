# -*- coding: utf-8 -*-
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sia_admin_and_menu_engine import (
    get_simplified_pictorial_menu,
    get_menu_guide_response,
    get_inactivity_nudge
)

menu_ta = get_simplified_pictorial_menu("சுந்தர்", lang="ta")
print("Menu TA Header:", menu_ta["header"])
print("Menu TA Button Count:", len(menu_ta["buttons"]))
assert "வணக்கம்!" in menu_ta["header"]
assert len(menu_ta["buttons"]) == 3

# Test each service from 1 to 12
for i in range(1, 13):
    resp = get_menu_guide_response(str(i), citizen_name="சுந்தர்", lang="ta")
    assert resp is not None, f"Failed for service {i}"
    print(f"Service {i} OK: {resp['header']}")

# Test inactivity nudge
nudge = get_inactivity_nudge("சுந்தர்", lang="ta")
assert nudge is not None
print("Inactivity Nudge OK:", nudge["header"], len(nudge["buttons"]))
print("ALL TESTS PASSED IN MENU ENGINE!")
