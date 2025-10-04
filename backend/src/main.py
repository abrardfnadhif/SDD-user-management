"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="User Management API",
    description="Secure user management with authentication, RBAC, and 2FA",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy", "message": "User Management API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "not_connected",  # Will be updated when DB is connected
        "version": "0.1.0",
    }
