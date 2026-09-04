"""Real astronomical position calculation via the Swiss Ephemeris.

Replaces the old day-of-year / birth-hour approximations for Moon and
Rising sign with actual ecliptic longitudes computed from birth date,
time, and location. Uses the Moshier semi-analytic ephemeris built into
pyswisseph (SEFLG_MOSEPH), which needs no external ephemeris data files
and is accurate to a few arcseconds — more than enough for a birth chart.
"""

import datetime
import logging
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import swisseph as swe
from timezonefinder import TimezoneFinder

logger = logging.getLogger(__name__)

_tf = TimezoneFinder()

ZODIAC_SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]

_EPHE_FLAGS = swe.FLG_MOSEPH | swe.FLG_SPEED


def sign_from_degree(degree: float) -> str:
    """Map an ecliptic longitude (0-360) to its zodiac sign (30 degrees each)."""
    index = int(degree % 360 // 30)
    return ZODIAC_SIGNS[index]


def resolve_timezone(latitude: float, longitude: float) -> str | None:
    """Look up the IANA timezone name for a coordinate."""
    try:
        return _tf.timezone_at(lat=latitude, lng=longitude)
    except Exception as e:
        logger.error(f"Timezone lookup failed for ({latitude}, {longitude}): {e}")
        return None


def compute_natal_positions(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    latitude: float,
    longitude: float,
) -> dict | None:
    """Compute real Sun, Moon, and Ascendant (Rising) signs and ecliptic degrees.

    `hour`/`minute` are local birth time; they're converted to UTC using the
    timezone resolved from `latitude`/`longitude` before any ephemeris call.
    Returns None if the timezone can't be resolved or the ephemeris call fails.
    """
    tz_name = resolve_timezone(latitude, longitude)
    if not tz_name:
        return None

    try:
        local_dt = datetime.datetime(
            year, month, day, hour, minute, tzinfo=ZoneInfo(tz_name)
        )
    except (ValueError, ZoneInfoNotFoundError) as e:
        logger.error(f"Invalid birth datetime/timezone: {e}")
        return None

    utc_dt = local_dt.astimezone(datetime.timezone.utc)
    hour_fraction = utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600

    try:
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour_fraction)
        sun_pos, _ = swe.calc_ut(jd, swe.SUN, _EPHE_FLAGS)
        moon_pos, _ = swe.calc_ut(jd, swe.MOON, _EPHE_FLAGS)
        _, ascmc = swe.houses_ex(jd, latitude, longitude, hsys=b"P")
        ascendant_degree = ascmc[0]
    except Exception as e:
        logger.error(f"Swiss Ephemeris calculation failed: {e}")
        return None

    sun_degree = sun_pos[0]
    moon_degree = moon_pos[0]

    return {
        "sun_sign": sign_from_degree(sun_degree),
        "moon_sign": sign_from_degree(moon_degree),
        "rising_sign": sign_from_degree(ascendant_degree),
        "sun_degree": round(sun_degree, 4),
        "moon_degree": round(moon_degree, 4),
        "rising_degree": round(ascendant_degree, 4),
        "timezone": tz_name,
        "utc_datetime": utc_dt.isoformat(),
    }
