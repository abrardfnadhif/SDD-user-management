"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.rate_limit import RateLimitMiddleware
from src.middleware.security_headers import SecurityHeadersMiddleware
from src.api import auth, profile, admin

app = FastAPI(
    title="User Management API",
    description="""
    Secure user management system with:
    - User registration and authentication
    - JWT-based session management
    - TOTP 2FA (mandatory for Admins)
    - Role-Based Access Control (RBAC)
    - Profile management
    - Admin user management
    - Comprehensive audit logging
    - GDPR/CCPA compliance (data export, deletion with 14-day cancellation window)
    
    ## Security Features
    - bcrypt password hashing (12 rounds)
    - Secure HTTP-only cookies
    - Rate limiting (5 attempts/15min)
    - Security headers (CSP, HSTS, X-Frame-Options)
    - Last-admin protection
    
    ## Constitution Compliance
    - Code Quality (I): Type safety, linting
    - TDD (II): 70+ tests, ≥80% coverage
    - Security (V): JWT, RBAC, 2FA, rate limiting
    - Privacy (VI): Audit logs, GDPR compliance
    """,
    version="0.1.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",
)

# Add middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(admin.router)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy", "message": "User Management API"}


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "not_connected",  # Will be updated when DB is connected
        "version": "0.1.0",
    }
