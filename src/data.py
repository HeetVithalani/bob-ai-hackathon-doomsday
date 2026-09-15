"""
data.py — Synthetic supply-chain data generator.

All data is deterministic (fixed random seed). Returns plain JSON-serialisable dicts.
No external dependencies — Python stdlib only.
"""

import random

_RNG = random.Random(42)

# ── Static reference tables ────────────────────────────────────────────────

CITIES = [
    "Chicago", "Dallas", "Atlanta", "Los Angeles", "New York",
    "Houston", "Phoenix", "Philadelphia", "San Antonio", "Denver",
    "Seattle", "Miami", "Boston", "Detroit", "Minneapolis",
]

CARRIERS = ["FastFreight Co.", "BlueLine Logistics", "PeakHaul Inc.", "SwiftMove Ltd.", "IronRoute Express"]

ROUTES = {
    ("Chicago", "Dallas"):       ["via St. Louis", "via Memphis"],
    ("Dallas", "Atlanta"):       ["via Jackson", "via Birmingham"],
    ("Atlanta", "Los Angeles"):  ["via Dallas", "via Nashville, Memphis"],
    ("Los Angeles", "New York"): ["via Denver, Chicago", "via Phoenix, Dallas"],
    ("New York", "Houston"):     ["via Philadelphia, Atlanta", "via Baltimore, Charlotte"],
    ("Houston", "Phoenix"):      ["via San Antonio, El Paso", "via Austin, Tucson"],
    ("Phoenix", "Denver"):       ["via Flagstaff", "via Albuquerque"],
    ("Denver", "Seattle"):       ["via Salt Lake City", "via Boise"],
    ("Seattle", "Miami"):        ["via Los Angeles, Houston", "via Portland, San Francisco"],
    ("Miami", "Boston"):         ["via Atlanta, Washington DC", "via Charlotte, Philadelphia"],
    ("Boston", "Detroit"):       ["via Hartford, Albany", "via Providence, New Haven"],
    ("Detroit", "Minneapolis"):  ["via Milwaukee", "via Green Bay"],
    ("Minneapolis", "Philadelphia"): ["via Chicago, Cleveland", "via Madison, Toledo"],
    ("Philadelphia", "San Antonio"): ["via Washington DC, Atlanta", "via Baltimore, Charlotte"],
    ("San Antonio", "Chicago"):  ["via Dallas, St. Louis", "via Houston, Memphis"],
}

_ROUTE_KEYS = list(ROUTES.keys())

STATUSES = ["on_time", "on_time", "on_time", "delayed", "delayed", "blocked"]

VEHICLE_TYPES = ["truck", "truck", "van", "reefer", "reefer"]

VEHICLE_STATUSES = ["active", "active", "active", "idle", "maintenance"]

# Normal operating range for reefer units (°C)
REEFER_TEMP_MIN = 2.0
REEFER_TEMP_MAX = 8.0


# ── Generators ────────────────────────────────────────────────────────────

def generate_shipments():
    """Return a deterministic list of 15 shipment dicts."""
    rng = random.Random(42)
    shipments = []
    for i in range(1, 16):
        route_key = _ROUTE_KEYS[rng.randint(0, len(_ROUTE_KEYS) - 1)]
        origin, destination = route_key
        status = rng.choice(STATUSES)
        eta_base = rng.randint(6, 72)
        delay = rng.randint(4, 24) if status in ("delayed", "blocked") else 0
        current_idx = rng.randint(0, len(CITIES) - 1)
        shipments.append({
            "id": f"SHP-{1000 + i}",
            "origin": origin,
            "destination": destination,
            "carrier": rng.choice(CARRIERS),
            "status": status,
            "eta_hours": eta_base + delay,
            "delay_hours": delay,
            "current_location": CITIES[current_idx],
            "route": ROUTES[route_key][0],
        })
    return shipments


def generate_fleet():
    """Return a deterministic list of 12 fleet vehicle dicts."""
    rng = random.Random(99)
    fleet = []
    for i in range(1, 13):
        vtype = rng.choice(VEHICLE_TYPES)
        vstatus = rng.choice(VEHICLE_STATUSES)
        idle_hours = rng.randint(5, 20) if vstatus == "idle" else 0
        location = rng.choice(CITIES)

        if vtype == "reefer":
            # Occasionally breach the temperature band
            breach = rng.random() < 0.4
            if breach:
                direction = rng.choice(["high", "low"])
                if direction == "high":
                    temp = round(rng.uniform(9.0, 15.0), 1)
                else:
                    temp = round(rng.uniform(-3.0, 1.5), 1)
            else:
                temp = round(rng.uniform(REEFER_TEMP_MIN, REEFER_TEMP_MAX), 1)
            temp_min = REEFER_TEMP_MIN
            temp_max = REEFER_TEMP_MAX
        else:
            temp = None
            temp_min = None
            temp_max = None

        fleet.append({
            "id": f"VEH-{200 + i}",
            "type": vtype,
            "status": vstatus,
            "idle_hours": idle_hours,
            "last_location": location,
            "temperature_celsius": temp,
            "temp_min": temp_min,
            "temp_max": temp_max,
        })
    return fleet
