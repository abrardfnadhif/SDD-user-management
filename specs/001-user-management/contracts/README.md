# API Contracts — User Management

This directory will contain endpoint contracts (OpenAPI fragments or JSON schemas) and associated contract tests.

## Endpoints (from spec FRs)
- POST /api/register — Create user account (requires email verification via 24h magic link)
- POST /api/login — Issue access (≤15m) and refresh (≤7d) tokens in secure cookies
- POST /api/token/refresh — Rotate/refresh access token
- POST /api/2fa/enable — Enroll TOTP; return provisioning data
- POST /api/2fa/verify — Verify TOTP during login or enrollment
- GET /api/profile — Get own user profile
- PUT /api/profile — Update own profile
- GET /api/admin/users/{id} — Admin view user
- PUT /api/admin/users/{id} — Admin update user
- DELETE /api/admin/users/{id} — Admin delete user (respect deletion policy)
- POST /api/admin/users/{id}/role — Admin change role (enforce at least one Admin)

## Contract Tests (to be created in Phase 2 via /tasks)
- One test file per endpoint asserting request/response schemas and status codes.

## Notes
- Do not include secrets/PII in examples
- Enforce security headers on responses where applicable
