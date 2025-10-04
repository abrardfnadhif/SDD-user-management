"""
Rate limiting middleware for failed login attempts
Constitution V: 5 failed logins per 15m/IP
"""
from datetime import datetime, timedelta
from typing import Dict, List
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter
    
    For production, consider using Redis for distributed rate limiting
    """

    def __init__(self):
        # Store: {ip: [(timestamp, endpoint), ...]}
        self.attempts: Dict[str, List[tuple[datetime, str]]] = {}
        self.max_attempts = 5
        self.window_minutes = 15

    def _clean_old_attempts(self, ip: str) -> None:
        """Remove attempts older than window"""
        if ip not in self.attempts:
            return

        cutoff = datetime.utcnow() - timedelta(minutes=self.window_minutes)
        self.attempts[ip] = [
            (ts, endpoint)
            for ts, endpoint in self.attempts[ip]
            if ts > cutoff
        ]

    def check_rate_limit(self, ip: str, endpoint: str) -> bool:
        """
        Check if IP has exceeded rate limit for endpoint
        
        Returns:
            True if rate limit exceeded
        """
        self._clean_old_attempts(ip)

        if ip not in self.attempts:
            return False

        # Count attempts for this endpoint
        count = sum(1 for _, ep in self.attempts[ip] if ep == endpoint)
        return count >= self.max_attempts

    def record_attempt(self, ip: str, endpoint: str) -> None:
        """Record a failed attempt"""
        if ip not in self.attempts:
            self.attempts[ip] = []

        self.attempts[ip].append((datetime.utcnow(), endpoint))
        self._clean_old_attempts(ip)

    def reset(self, ip: str, endpoint: str) -> None:
        """Reset attempts for IP and endpoint (on successful login)"""
        if ip not in self.attempts:
            return

        self.attempts[ip] = [
            (ts, ep) for ts, ep in self.attempts[ip] if ep != endpoint
        ]


# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce rate limiting on sensitive endpoints
    
    Currently applies to:
    - /api/login
    - /api/2fa/verify
    """

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Check if this is a rate-limited endpoint
        path = request.url.path
        rate_limited_endpoints = ["/api/login", "/api/2fa/verify"]

        if path in rate_limited_endpoints:
            # Check rate limit before processing
            if rate_limiter.check_rate_limit(client_ip, path):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many failed attempts. Please try again later.",
                )

        # Process request
        response = await call_next(request)

        # Record failed attempts (4xx status codes)
        if path in rate_limited_endpoints and 400 <= response.status_code < 500:
            rate_limiter.record_attempt(client_ip, path)

        # Reset on successful login (2xx status codes)
        if path in rate_limited_endpoints and 200 <= response.status_code < 300:
            rate_limiter.reset(client_ip, path)

        return response


def get_rate_limiter() -> InMemoryRateLimiter:
    """Get the global rate limiter instance"""
    return rate_limiter
