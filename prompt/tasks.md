Generate a complete, actionable tasks list for the User Management feature using `.specify/templates/tasks-template.md`, aligned with the Constitution and the design artifacts in `specs/001-user-management/`.

## Inputs
- Feature Plan: `specs/001-user-management/plan.md` (required)
- Design Docs: `specs/001-user-management/research.md`, `specs/001-user-management/data-model.md`, `specs/001-user-management/quickstart.md`, `specs/001-user-management/contracts/`
- Constitution: `.specify/memory/constitution.md`
- Template: `.specify/templates/tasks-template.md`

## Output
- Write tasks to: `specs/001-user-management/tasks.md`
- Follow the template’s Execution Flow, Format, and Validation Checklist. No placeholders left.

## Format
- Use template format: `[ID] [P?] Description`
- Include exact file paths in every task
- Tag the owning area in parentheses at end: `(frontend|backend|db|devops|qa|docs)`
- Mark `[P]` only when tasks touch different files and have no dependencies

## Constraints (Constitution-aligned)
- Stack: Next.js (TypeScript), FastAPI (Python 3.11), PostgreSQL (Dockerized)
- Code Quality: SOLID, Five Lines of Code where reasonable, DRY, function length ≤50 lines
- TDD: tests first; coverage ≥80% overall, 100% on auth/RBAC/validation paths
- Security: JWT secure cookies (HttpOnly, Secure, SameSite=Strict), access ≤15m, refresh ≤7d, rate limit 5/15m/IP, bcrypt ≥12, CSRF/XSS protections, CSP/HSTS, 2FA, RBAC
- Privacy: GDPR/CCPA, data export, deletion with 14-day cancellation, backups purge ≤90 days, audit logs (no PII in logs)
- Performance: API p50<100ms reads, p95<200ms reads, p95<500ms writes; Lighthouse ≥90; initial JS bundle <200KB gz; no N+1; indexed queries
## Milestones (map tasks accordingly)
1. Project setup & environment
2. Authentication & registration
3. Profile management
4. Role-based access control
5. Two-factor authentication
6. Audit logging system
7. Testing & security hardening
8. Deployment & CI/CD pipeline

## Generation Rules (apply in addition to template)
- Derive contract test tasks from each endpoint listed in `contracts/README.md`.
- Derive model tasks from each entity in `data-model.md`.
- Derive integration/E2E tasks from `quickstart.md` scenarios.
- Always schedule tests before implementation for the same concern.
- For parallelization, group tasks by file path; same-file tasks must be sequential.
- Use project structure from plan:
  - Backend code at `backend/src/...`, tests at `backend/tests/...`
  - Frontend code at `frontend/src/...`, tests at `frontend/tests/...`

## Mandatory Coverage (must appear in tasks)
- Setup: repo structure, lint/format, pre-commit, env files, docker-compose, Makefile scripts (dev one-liner)
- Backend contracts/tests: register, login, refresh, 2FA enable/verify, profile get/update, admin user CRUD, role change
- Backend implementation: services, routers, validation, rate limiting, security headers, audit logging
- Frontend: pages and forms for register/login/profile/admin users; error/loading states; accessibility
- RBAC: server-side guards, admin UI; prevent orphaned admin
- 2FA: enrollment, verification, backup codes, recovery
- Account deletion: schedule, cancellation window, backup purge policy
- Logging/Monitoring: auth success/failure, authorization failures, admin actions, sensitive data access (no PII)
- Performance checks: DB indexes, no N+1, bundle budget enforcement
- CI: lint/tests coverage gates; security scans (SAST/DAST placeholder), dependency scanning
- Docs: API docs, quickstart updates, operations readme

## Validation Checklist (augment template)
- All endpoints have contract tests and implementation tasks
- All entities have model tasks
- Tests precede implementation for each concern
- [P] tasks touch different files with no dependencies
- Each task includes exact file path and owner area
- Security and privacy tasks present (headers, rate limits, deletion, export)
- Performance targets addressed (indexes, budgets)

## Notes
- Use absolute paths rooted at repository root in descriptions when helpful.
- Keep tasks small, clear, and developer-ready.
