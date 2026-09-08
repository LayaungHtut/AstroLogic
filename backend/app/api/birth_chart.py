import asyncio

from fastapi import APIRouter
from app.services.prolog_service import PrologService
from app.services.ephemeris_service import compute_natal_positions

router = APIRouter(prefix="/api/birth-chart", tags=["birth-chart"])


@router.post("/calculate")
async def calculate_birth_chart(data: dict):
    """Calculate birth chart from birth date, time, and (optionally) location.

    When `year`, `latitude`, and `longitude` are all supplied, Sun/Moon/Rising
    signs are computed from real ecliptic positions via the Swiss Ephemeris
    (see app.services.ephemeris_service). Without them, falls back to the
    older date/hour-based approximation.
    """
    month = data.get("month")
    day = data.get("day")
    hour = data.get("hour", 12)
    minute = data.get("minute", 0)
    year = data.get("year")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not month or not day:
        return {"error": "month and day are required"}

    try:
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
    except (ValueError, TypeError):
        return {"error": "month, day, hour, and minute must be integers"}

    if month < 1 or month > 12:
        return {"error": "month must be between 1 and 12"}
    if day < 1 or day > 31:
        return {"error": "day must be between 1 and 31"}
    if not (0 <= hour <= 23):
        return {"error": "hour must be between 0 and 23"}
    if not (0 <= minute <= 59):
        return {"error": "minute must be between 0 and 59"}

    has_precise_inputs = year is not None and latitude is not None and longitude is not None

    if has_precise_inputs:
        try:
            year = int(year)
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            return {"error": "year, latitude, and longitude must be numbers"}

        if not (-90 <= latitude <= 90):
            return {"error": "latitude must be between -90 and 90"}
        if not (-180 <= longitude <= 180):
            return {"error": "longitude must be between -180 and 180"}

        # compute_natal_positions and every PrologService call are synchronous,
        # blocking calls (pyswisseph, timezonefinder, pyswip) — run each off
        # the event loop so one slow request doesn't stall every other one.
        positions = await asyncio.to_thread(
            compute_natal_positions, year, month, day, hour, minute, latitude, longitude
        )
        if positions:
            chart = await asyncio.to_thread(
                PrologService.get_full_birth_chart_precise,
                positions["sun_sign"], positions["moon_sign"], positions["rising_sign"],
            )
            if chart:
                chart["sun_degree"] = positions["sun_degree"]
                chart["moon_degree"] = positions["moon_degree"]
                chart["rising_degree"] = positions["rising_degree"]
                chart["timezone"] = positions["timezone"]
                chart["precise"] = True

                other_planets = positions.get("planets", {})
                planet_signs = {name: info["sign"] for name, info in other_planets.items()}
                planets_profile = await asyncio.to_thread(
                    PrologService.get_planet_positions_profile, planet_signs
                )
                # Merge in the degree/retrograde data ephemeris computed but
                # Prolog doesn't carry (it only reasons over the sign).
                for p in planets_profile:
                    info = other_planets.get(p["name"], {})
                    p["degree"] = info.get("degree")
                    p["retrograde"] = info.get("retrograde", False)
                chart["planets"] = planets_profile

                reasoning = await asyncio.to_thread(
                    PrologService.get_birth_chart_reasoning_precise,
                    positions["sun_sign"],
                    positions["moon_sign"],
                    positions["rising_sign"],
                    positions["sun_degree"],
                    positions["moon_degree"],
                    positions["rising_degree"],
                )
                return {"chart": chart, "reasoning": reasoning}
        # Ephemeris/timezone lookup failed (e.g. unresolvable coordinates) —
        # fall through to the approximate calculation below.

    chart = await asyncio.to_thread(PrologService.get_full_birth_chart, month, day, hour)
    if not chart:
        return {"error": "Could not calculate birth chart"}
    chart["precise"] = False

    reasoning = await asyncio.to_thread(
        PrologService.get_birth_chart_reasoning, month, day, hour
    )

    return {
        "chart": chart,
        "reasoning": reasoning,
    }
