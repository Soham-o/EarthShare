"""Tests that all endpoints emit the required security headers."""


class TestSecurityHeaders:
    def test_health_returns_csp_header(self, client):
        resp = client.get("/health")
        assert "content-security-policy" in resp.headers
        assert "frame-ancestors" in resp.headers["content-security-policy"]

    def test_health_returns_x_content_type_options(self, client):
        resp = client.get("/health")
        assert resp.headers.get("x-content-type-options") == "nosniff"

    def test_health_returns_x_frame_options(self, client):
        resp = client.get("/health")
        assert resp.headers.get("x-frame-options") == "DENY"

    def test_health_returns_referrer_policy(self, client):
        resp = client.get("/health")
        assert resp.headers.get("referrer-policy") == "strict-origin-when-cross-origin"

    def test_auth_endpoint_has_csp(self, client):
        resp = client.post("/api/v1/auth/login", json={"email": "x@x.com", "password": "wrong"})
        assert "content-security-policy" in resp.headers

    def test_no_hsts_in_non_production(self, client):
        """HSTS must not be sent in dev/test to avoid locking out http:// dev URLs."""
        resp = client.get("/health")
        assert "strict-transport-security" not in resp.headers
