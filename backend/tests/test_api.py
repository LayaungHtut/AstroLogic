"""End-to-end HTTP tests for endpoints that don't call the OpenRouter LLM
(so these run offline, free, and deterministically). LLM-backed endpoints
(/api/reading/analyze, /api/horoscope/generate's AI path, chat) are covered
indirectly via the PrologService/ephemeris unit tests instead.
"""


class TestZodiacEndpoint:
    def test_get_known_sign(self, client):
        resp = client.get("/api/zodiac/aries")
        assert resp.status_code == 200
        data = resp.json()
        assert data["sign"] == "aries"
        assert data["element"] == "fire"

    def test_get_all_signs(self, client):
        resp = client.get("/api/zodiac")
        assert resp.status_code == 200
        assert len(resp.json()) == 12

    def test_injection_attempt_in_path_param_is_handled_safely(self, client):
        resp = client.get("/api/zodiac/aries), true, X = 1, zodiac_info(taurus")
        assert resp.status_code == 200
        assert resp.json() == {"error": "Sign not found"}


class TestTopicsEndpoint:
    def test_get_all_topics(self, client):
        resp = client.get("/api/topics")
        assert resp.status_code == 200
        assert len(resp.json()) > 0

    def test_classify(self, client):
        resp = client.post("/api/topics/classify", json={"question": "Will I find love?"})
        assert resp.status_code == 200
        assert resp.json()["topic"]


class TestCompatibilityEndpoint:
    def test_analyze_known_signs(self, client):
        resp = client.post(
            "/api/compatibility/analyze", json={"sign1": "aries", "sign2": "leo"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["sign1"] == "aries"
        assert data["sign2"] == "leo"
        assert data["level"] in {"low", "moderate", "high", "excellent"}

    def test_injection_attempt_fails_safely_not_with_a_500(self, client):
        resp = client.post(
            "/api/compatibility/analyze",
            json={"sign1": "aries\\'), true, evil('X", "sign2": "leo"},
        )
        assert resp.status_code == 200
        assert resp.json() == {"error": "Could not analyze compatibility"}


class TestBirthChartEndpoint:
    def test_precise_mode_with_known_reference_case(self, client):
        resp = client.post(
            "/api/birth-chart/calculate",
            json={
                "month": 6, "day": 15, "year": 1995, "hour": 10, "minute": 30,
                "latitude": 40.7128, "longitude": -74.0060,
            },
        )
        assert resp.status_code == 200
        chart = resp.json()["chart"]
        assert chart["precise"] is True
        assert chart["sun_sign"] == "gemini"
        assert chart["moon_sign"] == "capricorn"
        assert chart["rising_sign"] == "leo"

    def test_falls_back_without_location(self, client):
        resp = client.post(
            "/api/birth-chart/calculate", json={"month": 6, "day": 15, "hour": 10}
        )
        assert resp.status_code == 200
        chart = resp.json()["chart"]
        assert chart["precise"] is False
        assert chart["sun_sign"] == "gemini"

    def test_rejects_out_of_range_latitude(self, client):
        resp = client.post(
            "/api/birth-chart/calculate",
            json={
                "month": 6, "day": 15, "year": 1995, "hour": 10,
                "latitude": 140, "longitude": -74,
            },
        )
        assert resp.status_code == 200
        assert "error" in resp.json()


class TestSynastryDeepDiveEndpoint:
    def test_returns_full_breakdown(self, client):
        resp = client.post(
            "/api/compatibility/synastry", json={"sign1": "aries", "sign2": "cancer"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["sign1"] == "aries"
        assert set(data["score_breakdown"].keys()) == {
            "element", "modality", "traits", "planetary", "overall"
        }
        assert isinstance(data["complementary_traits"], list)
        assert isinstance(data["strengths"], list)


class TestZodiacProfileEndpoint:
    def test_returns_profile_and_reasoning(self, client):
        resp = client.get("/api/zodiac/leo/profile")
        assert resp.status_code == 200
        data = resp.json()
        assert data["profile"]["sign"] == "leo"
        assert data["profile"]["personality_style"]
        assert len(data["reasoning"]) > 0

    def test_unknown_sign_returns_error(self, client):
        resp = client.get("/api/zodiac/not_a_real_sign/profile")
        assert resp.status_code == 200
        assert "error" in resp.json()
