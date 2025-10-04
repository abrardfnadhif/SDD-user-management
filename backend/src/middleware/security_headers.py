"""
Security headers middleware
Constitution V: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses
    
    Headers added:
    - Content-Security-Policy (CSP)
    - Strict-Transport-Security (HSTS)
    - X-Frame-Options
    - X-Content-Type-Options
    - Referrer-Policy
    - X-XSS-Protection (legacy, but still useful)
    - Permissions-Policy
    """

    def __init__(self, app, csp_policy: str = None, hsts_max_age: int = 31536000):
        super().__init__(app)
        # Relaxed CSP for API docs (Swagger UI and ReDoc)
        self.csp_policy = csp_policy or (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://fastapi.tiangolo.com"
        )
        self.hsts_max_age = hsts_max_age

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Content Security Policy
        # Prevents XSS and data injection attacks
        # Relaxed for /docs and /redoc endpoints
        response.headers["Content-Security-Policy"] = self.csp_policy

        # HTTP Strict Transport Security
        # Forces HTTPS connections
        response.headers["Strict-Transport-Security"] = (
            f"max-age={self.hsts_max_age}; includeSubDomains"
        )

        # X-Frame-Options
        # Prevents clickjacking attacks
        response.headers["X-Frame-Options"] = "DENY"

        # X-Content-Type-Options
        # Prevents MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Referrer-Policy
        # Controls referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # X-XSS-Protection (legacy, but still useful for older browsers)
        # Enables XSS filtering
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Permissions-Policy (formerly Feature-Policy)
        # Controls browser features
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        return response


def create_security_headers_middleware(
    csp_policy: str = None, hsts_max_age: int = 31536000
):
    """
    Factory function to create security headers middleware with custom config
    
    Args:
        csp_policy: Content Security Policy string
        hsts_max_age: HSTS max-age in seconds (default 1 year)
    """

    def middleware_factory(app):
        return SecurityHeadersMiddleware(app, csp_policy, hsts_max_age)

    return middleware_factory
