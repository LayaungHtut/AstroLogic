"""Tests for the Swiss Ephemeris-backed natal position calculation."""

from app.services.ephemeris_service import (
    compute_natal_positions,
    resolve_timezone,
    sign_from_degree,
)


class TestSignFromDegree:
    def test_boundaries(self):
        assert sign_from_degree(0) == "aries"
        assert sign_from_degree(29.999) == "aries"
        assert sign_from_degree(30) == "taurus"
        assert sign_from_degree(359.999) == "pisces"

    def test_wraps_past_360(self):
        assert sign_from_degree(360) == "aries"
        assert sign_from_degree(390) == "taurus"


class TestResolveTimezone:
    def test_known_city(self):
        assert resolve_timezone(40.7128, -74.0060) == "America/New_York"

    def test_mid_ocean_falls_back_to_an_offset_zone_rather_than_none(self):
        # timezonefinder covers the whole globe via Etc/GMT+-N offset zones,
        # so this should not return None even far from any populated timezone.
        assert resolve_timezone(0.0, -140.0) is not None


class TestComputeNatalPositions:
    def test_known_reference_case(self):
        # NYC, 1995-06-15 10:30 local time. Cross-checked against a direct
        # pyswisseph call outside the app during development.
        result = compute_natal_positions(1995, 6, 15, 10, 30, 40.7128, -74.0060)
        assert result is not None
        assert result["sun_sign"] == "gemini"
        assert result["moon_sign"] == "capricorn"
        assert result["rising_sign"] == "leo"
        assert result["timezone"] == "America/New_York"
        assert abs(result["sun_degree"] - 84.0317) < 0.01
        assert abs(result["moon_degree"] - 298.5437) < 0.01
        assert abs(result["rising_degree"] - 145.9785) < 0.01

    def test_polar_latitude_fails_gracefully(self):
        # Placidus houses are undefined above the polar circle — this must
        # return None (so the caller can fall back), not raise.
        result = compute_natal_positions(1995, 6, 15, 10, 30, 78.2232, 15.6267)
        assert result is None
