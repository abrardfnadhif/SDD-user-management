# Backend — User Management API

FastAPI-based backend for secure user management.

## Structure
- `src/models/` — Database models (User, Role, AuditLog, etc.)
- `src/services/` — Business logic (AuthService, MFAService, RBACService, etc.)
- `src/api/` — API routers (auth, profile, admin)
- `tests/contract/` — Contract tests for API endpoints
- `tests/integration/` — Integration tests for user flows
- `tests/unit/` — Unit tests for services and validation
- `tests/perf/` — Performance tests (DB queries, API latency)

## Tech Stack
- Python 3.11
- FastAPI
- PostgreSQL 15 (via psycopg)
- JWT for authentication
- pytest + httpx for testing

## Setup
See root `Makefile` for one-line dev setup.
