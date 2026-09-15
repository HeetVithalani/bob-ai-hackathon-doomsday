"""
engine.py — Detection and recommendation logic.

Pure functions: take dicts from data.py, return result dicts.
No I/O, no external dependencies.
"""

from datetime import datetime, timezone

# ── Alternate route lookup ─────────────────────────────────────────────────
# Maps (origin, destination) → alternate route description + reason.
_ALTERNATE_ROUTES = {
    ("Chicago", "Dallas"):           ("via Kansas City, Oklahoma City", "Avoids St. Louis congestion"),
    ("Dallas", "Atlanta"):           ("via Shreveport, Montgomery",     "Bypasses Jackson flood zone"),
    ("Atlanta", "Los Angeles"):      ("via Birmingham, New Orleans",    "Avoids Nashville storm delay"),
    ("Los Angeles", "New York"):     ("via Las Vegas, Salt Lake City",  "Bypasses Rocky Mountain closure"),
    ("New York", "Houston"):         ("via Newark, Richmond, Charlotte", "Avoids I-95 construction"),
    ("Houston", "Phoenix"):          ("via Midland, El Paso",           "Bypasses San Antonio port backup"),
    ("Phoenix", "Denver"):           ("via Flagstaff, Grand Junction",  "Avoids I-25 roadworks"),
    ("Denver", "Seattle"):           ("via Spokane, Yakima",            "Bypasses mountain pass closure"),
    ("Seattle", "Miami"):            ("via Sacramento, Las Vegas",      "Avoids Pacific Coast delays"),
    ("Miami", "Boston"):             ("via Jacksonville, Richmond",     "Bypasses I-95 bridge maintenance"),
    ("Boston", "Detroit"):           ("via Springfield, Buffalo",       "Avoids New England snowstorm"),
    ("Detroit", "Minneapolis"):      ("via Eau Claire, Hudson",         "Bypasses Milwaukee port hold"),
    ("Minneapolis", "Philadelphia"): ("via Madison, Toledo, Cleveland", "Avoids Chicago rail strike"),
    ("Philadelphia", "San Antonio"): ("via Richmond, Knoxville, Nashville", "Bypasses DC traffic incident"),
    ("San Antonio", "Chicago"):      ("via Waco, Kansas City",          "Avoids Dallas hub congestion"),
}

_FALLBACK_ROUTE = ("Coordinate with carrier for alternate routing", "Disruption detected — manual review required")


def detect_disruptions(shipments):
    """Return shipments with status 'delayed' or 'blocked'."""
    return [s for s in shipments if s["status"] in ("delayed", "blocked")]


def recommend_reroutes(disrupted_shipments):
    """
    For each disrupted shipment, add recommended_route and reason fields.
    Returns a new list of dicts (originals are not mutated).
    """
    result = []
    for s in disrupted_shipments:
        key = (s["origin"], s["destination"])
        alt_route, reason = _ALTERNATE_ROUTES.get(key, _FALLBACK_ROUTE)
        result.append({
            **s,
            "recommended_route": alt_route,
            "reroute_reason": reason,
        })
    return result


def detect_idle_fleet(fleet, idle_threshold_hours=4):
    """Return vehicles that are idle for at least idle_threshold_hours."""
    return [v for v in fleet if v["status"] == "idle" and v["idle_hours"] >= idle_threshold_hours]


def detect_cold_chain_alerts(fleet):
    """
    Return reefer vehicles whose temperature is outside [temp_min, temp_max].
    Adds a 'breach_direction' field: 'too_high' or 'too_low'.
    """
    alerts = []
    for v in fleet:
        if v["type"] != "reefer":
            continue
        temp = v["temperature_celsius"]
        if temp is None:
            continue
        if temp > v["temp_max"]:
            alerts.append({**v, "breach_direction": "too_high"})
        elif temp < v["temp_min"]:
            alerts.append({**v, "breach_direction": "too_low"})
    return alerts


def run_all(shipments, fleet):
    """
    Run all detection and recommendation logic.
    Returns a single dict suitable for JSON serialisation.
    """
    disruptions = detect_disruptions(shipments)
    reroutes = recommend_reroutes(disruptions)
    idle_vehicles = detect_idle_fleet(fleet)
    cold_chain_alerts = detect_cold_chain_alerts(fleet)

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": {
            "total_shipments": len(shipments),
            "disruptions": len(disruptions),
            "reroutes": len(reroutes),
            "idle_vehicles": len(idle_vehicles),
            "cold_chain_alerts": len(cold_chain_alerts),
            "total_fleet": len(fleet),
        },
        "shipments": shipments,
        "fleet": fleet,
        "disruptions": disruptions,
        "reroutes": reroutes,
        "idle_vehicles": idle_vehicles,
        "cold_chain_alerts": cold_chain_alerts,
    }
