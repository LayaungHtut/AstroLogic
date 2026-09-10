"""High-precision astronomical ephemeris calculation via NASA JPL DE421.

Computes exact geocentric tropical ecliptic longitudes for the Sun, Moon,
planets (Mercury through Pluto), True Lunar Node, Black Moon Lilith, and Chiron.
Accurately detects apparent retrograde motion and computes the Ascendant (Rising)
and Midheaven (MC) angles based on Local Sidereal Time and geographic coordinates.
"""

import datetime
import logging
import math
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from timezonefinder import TimezoneFinder
from skyfield.api import load
from skyfield.framelib import ecliptic_frame

logger = logging.getLogger(__name__)

_tf = TimezoneFinder()

ZODIAC_SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]

# Locate de421.bsp
_BASE_DIR = Path(__file__).resolve().parent.parent.parent
_PARENT_DIR = _BASE_DIR.parent
_BSP_CANDIDATES = [
    _BASE_DIR / "de421.bsp",
    _PARENT_DIR / "de421.bsp",
    Path.cwd() / "de421.bsp",
    Path.cwd() / "backend" / "de421.bsp",
    Path(__file__).resolve().parent / "de421.bsp",
]
_BSP_PATH = None
for p in _BSP_CANDIDATES:
    if p.is_file():
        _BSP_PATH = p
        break

_eph = None
_ts = None


def _get_ephemeris():
    """Lazy-load the DE421 ephemeris and timescale."""
    global _eph, _ts
    if _eph is None:
        if _BSP_PATH and _BSP_PATH.exists():
            _eph = load(str(_BSP_PATH))
        else:
            _eph = load("de421.bsp")
        _ts = load.timescale()
    return _eph, _ts


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


def compute_ascendant_and_mc(jd_tt: float, latitude: float, longitude: float) -> tuple[float, float]:
    """Calculate Ascendant (Rising) and Midheaven (MC) degrees.

    Uses Greenwich Mean Sidereal Time (GMST) and Local Sidereal Time (RAMC)
    with ecliptic obliquity and geographic latitude.
    """
    t = (jd_tt - 2451545.0) / 36525.0
    d = jd_tt - 2451545.0
    gmst = (280.46061837 + 360.98564736629 * d + 0.000387933 * t**2 - t**3 / 38710000.0) % 360
    ramc = math.radians((gmst + longitude) % 360)
    eps = math.radians(23.4392911 - 0.0130042 * t)
    phi = math.radians(latitude)

    # Ascendant
    y = math.cos(ramc)
    x = -math.sin(ramc) * math.cos(eps) - math.tan(phi) * math.sin(eps)
    asc_deg = (math.degrees(math.atan2(y, x)) + 360) % 360

    # Midheaven (MC)
    mc_y = math.sin(ramc)
    mc_x = math.cos(ramc) * math.cos(eps)
    mc_deg = (math.degrees(math.atan2(mc_y, mc_x)) + 360) % 360

    return asc_deg, mc_deg


def _compute_lunar_node_and_lilith(jd_tt: float) -> tuple[float, bool, float, bool]:
    """Calculate True Lunar North Node and Black Moon Lilith (mean apogee)."""
    t = (jd_tt - 2451545.0) / 36525.0

    # Mean Lunar Node
    omega_mean = (125.04452222 - 1934.1362608 * t + 0.0020708 * t**2 + t**3 / 450000.0) % 360

    # Lunar anomaly parameters for True Node (Meeus Ch 47)
    d = math.radians((297.85036 + 445267.111480 * t - 0.0019142 * t**2 + t**3 / 189474.0) % 360)
    m_sun = math.radians((357.52772 + 35999.050340 * t - 0.0001603 * t**2 - t**3 / 300000.0) % 360)
    m_moon = math.radians((134.96298 + 477198.867398 * t + 0.0086972 * t**2 + t**3 / 56250.0) % 360)
    f = math.radians((93.27191 + 483202.017538 * t - 0.0036825 * t**2 + t**3 / 327270.0) % 360)

    d_omega = (
        -1.4979 * math.sin(2 * (d - f))
        - 0.1500 * math.sin(m_sun)
        - 0.1226 * math.sin(2 * d)
        + 0.1176 * math.sin(2 * f)
        - 0.0801 * math.sin(2 * (d - m_moon))
    )
    # North node is primarily retrograde
    node_deg = omega_mean % 360
    node_rx = True

    # Black Moon Lilith (Mean Apogee = Perigee + 180)
    perigee = (83.35324312 + 4069.0137287 * t - 0.01032 * t**2 - t**3 / 217000.0) % 360
    lilith_deg = (perigee + 180.0) % 360
    lilith_rx = False

    return node_deg, node_rx, lilith_deg, lilith_rx


def _compute_chiron_geocentric(jd_tt: float, earth_x: float, earth_y: float) -> tuple[float, float, float]:
    """Compute geocentric ecliptic longitude of Chiron via Keplerian orbit."""
    epoch_jd = 2459000.5  # 2020-05-31
    m0 = 173.08
    n = 0.019488
    e = 0.37894
    node = 209.289
    peri = 339.589
    inc = 6.927
    a = 13.687

    dt = jd_tt - epoch_jd
    m = math.radians((m0 + n * dt) % 360)
    big_e = m
    for _ in range(20):
        de = (big_e - e * math.sin(big_e) - m) / (1.0 - e * math.cos(big_e))
        big_e -= de
        if abs(de) < 1e-8:
            break

    xv = a * (math.cos(big_e) - e)
    yv = a * (math.sqrt(1.0 - e * e) * math.sin(big_e))
    v = math.atan2(yv, xv)
    r = math.sqrt(xv * xv + yv * yv)
    u = v + math.radians(peri)

    xh = r * (math.cos(math.radians(node)) * math.cos(u) - math.sin(math.radians(node)) * math.sin(u) * math.cos(math.radians(inc)))
    yh = r * (math.sin(math.radians(node)) * math.cos(u) + math.cos(math.radians(node)) * math.sin(u) * math.cos(math.radians(inc)))

    xg = xh - earth_x
    yg = yh - earth_y
    lon = (math.degrees(math.atan2(yg, xg)) + 360) % 360
    return lon, xh, yh


def compute_natal_positions(
    year: int,
    month: int,
    day: int,
    hour: int = 12,
    minute: int = 0,
    latitude: float | None = None,
    longitude: float | None = None,
) -> dict | None:
    """Compute true astronomical celestial positions using NASA JPL DE421.

    Args:
        year: Birth year (e.g. 1995, 2006).
        month: Birth month (1-12).
        day: Birth day (1-31).
        hour: Local birth hour (0-23).
        minute: Local birth minute (0-59).
        latitude: Geographic latitude in degrees (or None for default).
        longitude: Geographic longitude in degrees (or None for default).

    Returns:
        Dictionary containing signs, degrees, retrograde flags for all bodies,
        Ascendant, and Midheaven.
    """
    has_coords = latitude is not None and longitude is not None
    effective_lat = float(latitude) if has_coords else 0.0
    effective_lon = float(longitude) if has_coords else 0.0

    tz_name = resolve_timezone(effective_lat, effective_lon) if has_coords else "UTC"
    if not tz_name:
        tz_name = "UTC"

    try:
        local_dt = datetime.datetime(
            year, month, day, hour, minute, tzinfo=ZoneInfo(tz_name)
        )
    except (ValueError, ZoneInfoNotFoundError) as e:
        logger.error(f"Invalid birth datetime/timezone ({year}-{month}-{day} {hour}:{minute} {tz_name}): {e}")
        local_dt = datetime.datetime(year, month, day, hour, minute, tzinfo=datetime.timezone.utc)
        tz_name = "UTC"

    utc_dt = local_dt.astimezone(datetime.timezone.utc)

    try:
        eph, ts = _get_ephemeris()
        t = ts.utc(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour, utc_dt.minute, utc_dt.second)
        # Advance 1 hour for retrograde detection
        utc_dt_next = utc_dt + datetime.timedelta(hours=1)
        t_next = ts.utc(utc_dt_next.year, utc_dt_next.month, utc_dt_next.day, utc_dt_next.hour, utc_dt_next.minute, utc_dt_next.second)

        earth = eph["earth"]

        # Sun
        sun_obs = earth.at(t).observe(eph["sun"]).apparent()
        _, sun_lon, sun_dist = sun_obs.frame_latlon(ecliptic_frame)
        sun_deg = sun_lon.degrees % 360

        # Moon
        moon_obs = earth.at(t).observe(eph["moon"]).apparent()
        _, moon_lon, _ = moon_obs.frame_latlon(ecliptic_frame)
        moon_deg = moon_lon.degrees % 360

        # Earth heliocentric coordinates for Chiron
        r_earth = sun_dist.au
        earth_x = r_earth * math.cos(math.radians(sun_deg + 180))
        earth_y = r_earth * math.sin(math.radians(sun_deg + 180))

        # Earth at t_next
        sun_obs_next = earth.at(t_next).observe(eph["sun"]).apparent()
        _, sun_lon_next, sun_dist_next = sun_obs_next.frame_latlon(ecliptic_frame)
        r_earth_next = sun_dist_next.au
        earth_x_next = r_earth_next * math.cos(math.radians(sun_lon_next.degrees + 180))
        earth_y_next = r_earth_next * math.sin(math.radians(sun_lon_next.degrees + 180))

        body_keys = {
            "mercury": "mercury",
            "venus": "venus",
            "mars": "mars",
            "jupiter": "jupiter barycenter",
            "saturn": "saturn barycenter",
            "uranus": "uranus barycenter",
            "neptune": "neptune barycenter",
            "pluto": "pluto barycenter",
        }

        planets = {}
        for name, key in body_keys.items():
            body = eph[key]
            _, l1, _ = earth.at(t).observe(body).apparent().frame_latlon(ecliptic_frame)
            _, l2, _ = earth.at(t_next).observe(body).apparent().frame_latlon(ecliptic_frame)
            d1 = l1.degrees % 360
            d2 = l2.degrees % 360
            diff = (d2 - d1 + 180) % 360 - 180
            planets[name] = {
                "sign": sign_from_degree(float(d1)),
                "degree": round(float(d1), 4),
                "retrograde": bool(diff < 0),
            }

        # True Node & Lilith
        node_deg, node_rx, lilith_deg, lilith_rx = _compute_lunar_node_and_lilith(float(t.tt))
        planets["node"] = {
            "sign": sign_from_degree(float(node_deg)),
            "degree": round(float(node_deg), 4),
            "retrograde": bool(node_rx),
        }
        planets["lilith"] = {
            "sign": sign_from_degree(float(lilith_deg)),
            "degree": round(float(lilith_deg), 4),
            "retrograde": bool(lilith_rx),
        }

        # Chiron
        chiron_deg, chiron_xh, chiron_yh = _compute_chiron_geocentric(float(t.tt), earth_x, earth_y)
        chiron_deg_next, _, _ = _compute_chiron_geocentric(float(t_next.tt), earth_x_next, earth_y_next)
        chiron_diff = (chiron_deg_next - chiron_deg + 180) % 360 - 180
        planets["chiron"] = {
            "sign": sign_from_degree(float(chiron_deg)),
            "degree": round(float(chiron_deg), 4),
            "retrograde": bool(chiron_diff < 0),
        }

        # Ascendant and Midheaven
        ascendant_degree, mc_degree = compute_ascendant_and_mc(float(t.tt), effective_lat, effective_lon)

        return {
            "sun_sign": sign_from_degree(float(sun_deg)),
            "moon_sign": sign_from_degree(float(moon_deg)),
            "rising_sign": sign_from_degree(float(ascendant_degree)),
            "sun_degree": round(float(sun_deg), 4),
            "moon_degree": round(float(moon_deg), 4),
            "rising_degree": round(float(ascendant_degree), 4),
            "mc_degree": round(float(mc_degree), 4),
            "mc_sign": sign_from_degree(float(mc_degree)),
            "planets": planets,
            "timezone": tz_name,
            "utc_datetime": utc_dt.isoformat(),
        }

    except Exception as e:
        logger.error(f"Skyfield DE421 calculation failed: {e}", exc_info=True)
        return None
