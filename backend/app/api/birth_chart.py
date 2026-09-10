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

    has_year = year is not None

    if has_year:
        try:
            year = int(year)
            lat = float(latitude) if latitude is not None and str(latitude).strip() != "" else None
            lon = float(longitude) if longitude is not None and str(longitude).strip() != "" else None
        except (ValueError, TypeError):
            return {"error": "year, latitude, and longitude must be numbers"}

        if lat is not None and not (-90 <= lat <= 90):
            return {"error": "latitude must be between -90 and 90"}
        if lon is not None and not (-180 <= lon <= 180):
            return {"error": "longitude must be between -180 and 180"}

        # compute_natal_positions runs NASA JPL DE421 ephemeris calculations off
        # the event loop to ensure high concurrency.
        positions = await asyncio.to_thread(
            compute_natal_positions, year, month, day, hour, minute, lat, lon
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
                chart["mc_degree"] = positions.get("mc_degree")
                chart["mc_sign"] = positions.get("mc_sign")
                chart["timezone"] = positions["timezone"]
                chart["precise"] = True
                chart["has_exact_location"] = lat is not None and lon is not None

                other_planets = positions.get("planets", {})
                standard_planets = {"mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"}
                planet_signs = {name: info["sign"] for name, info in other_planets.items() if name in standard_planets}
                planets_profile = await asyncio.to_thread(
                    PrologService.get_planet_positions_profile, planet_signs
                )
                existing_names = {p["name"] for p in planets_profile}

                # Helper to get element and modality for any sign
                SIGN_PROPERTIES = {
                    "aries": ("fire", "cardinal"), "taurus": ("earth", "fixed"), "gemini": ("air", "mutable"),
                    "cancer": ("water", "cardinal"), "leo": ("fire", "fixed"), "virgo": ("earth", "mutable"),
                    "libra": ("air", "cardinal"), "scorpio": ("water", "fixed"), "sagittarius": ("fire", "mutable"),
                    "capricorn": ("earth", "cardinal"), "aquarius": ("air", "fixed"), "pisces": ("water", "mutable"),
                }

                extra_bodies = {
                    "node": {"symbol": "☊", "influence": "Destiny & Spiritual Evolutionary Path"},
                    "lilith": {"symbol": "⚸", "influence": "Unconscious Desires & Raw Primal Nature"},
                    "chiron": {"symbol": "⚷", "influence": "The Wounded Healer & Deep Soul Wisdom"},
                }
                for name, meta in extra_bodies.items():
                    if name in other_planets and name not in existing_names:
                        info = other_planets[name]
                        elem, mod = SIGN_PROPERTIES.get(info["sign"], ("", ""))
                        planets_profile.append({
                            "name": name,
                            "sign": info["sign"],
                            "symbol": meta["symbol"],
                            "element": elem,
                            "modality": mod,
                            "influence": meta["influence"],
                            "degree": info.get("degree"),
                            "retrograde": info.get("retrograde", False),
                        })

                # Merge in the degree/retrograde data ephemeris computed but
                # Prolog doesn't carry (it only reasons over the sign).
                for p in planets_profile:
                    info = other_planets.get(p["name"], {})
                    if "degree" not in p or p["degree"] is None:
                        p["degree"] = info.get("degree")
                    if "retrograde" not in p:
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
        # Fall through to approximate calculation if ephemeris somehow failed

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


@router.post("/explain")
async def explain_birth_chart(data: dict):
    """Generate in-depth bilingual psychological and astrological explanation.

    Accepts the calculated chart object and optional requested locale ('en' | 'my').
    Returns deep breakdown of the Big Three, planetary archetypes, major aspects,
    and elemental constitution.
    """
    chart = data.get("chart")
    if not chart:
        return {"error": "chart data is required"}
    locale = data.get("locale", "en")
    if locale not in ("en", "my"):
        locale = "en"

    from app.services.birth_chart_explanation_service import generate_birth_chart_explanation
    explanation = await asyncio.to_thread(generate_birth_chart_explanation, chart, locale)
    return {"explanation": explanation}

