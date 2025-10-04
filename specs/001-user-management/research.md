# Research (Phase 0) — User Management

## Unknowns and Decisions

- **Email Verification Service**
  - Decision: Use transactional email provider with verified sender domain.
  - SLA: Magic link expiry 24h; resend limit 3/hour, 10/day.
  - Open item: Choose provider (Postmark/SES/SendGrid) based on cost/compliance.

- **Security Headers Enforcement**
  - Decision: Enforce CSP/HSTS via reverse proxy (preferred) or ASGI middleware fallback.
  - CSP policy: strict default-src 'self'; allowlists documented per asset.

- **Rate Limiting Implementation**
  - Decision: 5 failed logins per 15m/IP using in-memory + persistent store (redis preferred when available). Fallback to in-process for dev.

- **Data Residency**
  - Decision: No explicit residency requirement; store in primary region. Document process if constraints change.

- **Legal Hold Handling**
  - Decision: While on legal hold, deletion is blocked; account can be deactivated. Resumes after hold lifted.

- **Session Revocation Strategy**
  - Decision: Revoke all sessions on password change or email change.

## Rationale
- Aligns with Constitution v1.1.0 Principles V (Security) and VI (Privacy): clear policies for verification, headers, rate limits, and deletion.

## Actions
- Evaluate and select email provider (security, deliverability, logs).
- Define CSP allowlist process; document exception workflow.
- Decide on proxy vs app middleware based on deployment environment.
- Prepare redis option for rate limiting in staging/prod.

## Output
This document validates assumptions made in the spec; no unresolved blockers for Phase 1.
