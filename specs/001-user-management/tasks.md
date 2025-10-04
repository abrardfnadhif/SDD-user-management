# Tasks: User Management

**Input**: Design documents from `/Users/abrar.d.f.nadhif/project/SDD-FS/specs/001-user-management/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Format: `[ID] [P?] Description`
- Include exact file paths in descriptions
- Tag owner at end: `(frontend|backend|db|devops|qa|docs)`
- Mark `[P]` only for different files with no dependencies

## Phase 3.1: Setup (Project setup & environment)
- [x] T001 Create project structure per plan (backend/, frontend/, specs/) at `/Users/abrar.d.f.nadhif/project/SDD-FS/` (devops)
- [x] T002 Initialize backend Python project; add FastAPI, pydantic, JWT, psycopg, test deps in `backend/` (devops)
- [x] T003 Initialize frontend Next.js TypeScript app; add Tailwind, shadcn/ui in `frontend/` (devops)
- [x] T004 [P] Configure ESLint/Prettier and zero-error policy for frontend in `frontend/.eslintrc` and `frontend/package.json` (devops)
- [x] T005 [P] Configure ruff/flake8 or linters for backend in `backend/pyproject.toml` with function length guidance (devops)
- [x] T006 Create `.env.sample` for backend and frontend; document secrets in `README.md` (devops)
- [x] T007 Create `docker-compose.yml` for postgres, backend, (optional) reverse proxy at repo root (devops)
- [x] T008 Add Makefile scripts: `make dev` one-liner to start services and seed roles at `/Users/abrar.d.f.nadhif/project/SDD-FS/Makefile` (devops)
- [x] T009 Add base pages and routes: `/login`, `/register`, `/profile`, `/admin/users` in `frontend/src/pages/*.tsx` (frontend)
- [x] T010 Add API client with centralized error handling at `frontend/src/services/apiClient.ts` (frontend)

## Phase 3.2: Tests First (TDD) — Contract & Integration Tests
- [x] T011 [P] Contract test POST /api/register in `backend/tests/contract/test_register_post.py` (qa)
- [x] T012 [P] Contract test POST /api/login in `backend/tests/contract/test_login_post.py` (qa)
- [x] T013 [P] Contract test POST /api/token/refresh in `backend/tests/contract/test_refresh_post.py` (qa)
- [x] T014 [P] Contract test POST /api/2fa/enable in `backend/tests/contract/test_2fa_enable_post.py` (qa)
- [x] T015 [P] Contract test POST /api/2fa/verify in `backend/tests/contract/test_2fa_verify_post.py` (qa)
- [x] T016 [P] Contract test GET /api/profile in `backend/tests/contract/test_profile_get.py` (qa)
- [x] T017 [P] Contract test PUT /api/profile in `backend/tests/contract/test_profile_put.py` (qa)
- [x] T018 [P] Contract test GET /api/admin/users/{id} in `backend/tests/contract/test_admin_users_get.py` (qa)
- [x] T019 [P] Contract test PUT /api/admin/users/{id} in `backend/tests/contract/test_admin_users_put.py` (qa)
- [x] T020 [P] Contract test DELETE /api/admin/users/{id} in `backend/tests/contract/test_admin_users_delete.py` (qa)
- [x] T021 [P] Contract test POST /api/admin/users/{id}/role in `backend/tests/contract/test_admin_users_role_post.py` (qa)
- [x] T022 [P] Integration test: Registration → Email verification → Login → Profile update in `backend/tests/integration/test_user_flow.py` (qa)
- [x] T023 [P] Integration test: Login with 2FA (success + rate limit on failures) in `backend/tests/integration/test_2fa_flow.py` (qa)
- [x] T024 [P] Integration test: RBAC role change and access checks in `backend/tests/integration/test_rbac.py` (qa)
- [x] T025 [P] Integration test: Account deletion schedule and cancellation window in `backend/tests/integration/test_account_deletion.py` (qa)
- [x] T026 [P] Frontend E2E: auth and profile flows in `frontend/tests/e2e/auth.spec.ts` (qa)

## Phase 3.3: Core Implementation (Backend)
- [x] T027 [P] Create DB session and config in `backend/src/db/session.py` (db)
- [x] T028 [P] Create models: `User`, `Role`, `UserRole`, `AuditLog` in `backend/src/models/{user.py,role.py,audit_log.py,user_role.py}` (db)
- [x] T029 [P] Create models: `EmailVerificationToken`, `PasswordResetToken`, `BackupCode` in `backend/src/models/tokens.py` (db)
- [x] T030 [P] Implement UserService in `backend/src/services/user_service.py` (backend)
- [x] T031 [P] Implement AuthService (password auth, JWT issue, session revoke) in `backend/src/services/auth_service.py` (backend)
- [x] T032 [P] Implement MFAService (TOTP, backup codes) in `backend/src/services/mfa_service.py` (backend)
- [x] T033 Implement RBACService policy checks in `backend/src/services/rbac_service.py` (backend)
- [x] T034 Implement AuditLogService append-only writes in `backend/src/services/audit_log_service.py` (backend)
- [x] T035 Implement rate limiting middleware (5 failed/15m/IP) in `backend/src/middleware/rate_limit.py` (backend)
- [x] T036 Implement security headers middleware (CSP/HSTS/X-Frame-Options/nosniff/Referrer-Policy) in `backend/src/middleware/security_headers.py` (backend)
- [x] T037 Implement auth endpoints in `backend/src/api/auth.py` (register, login, refresh, 2fa enable/verify) (backend)
- [ ] T038 Implement profile endpoints in `backend/src/api/profile.py` (GET/PUT) (backend)
- [ ] T039 Implement admin user endpoints in `backend/src/api/admin.py` (GET/PUT/DELETE, POST role) (backend)
- [ ] T040 Enforce last-admin rule in admin endpoints (cannot delete/demote last Admin) in `backend/src/api/admin.py` (backend)
- [ ] T041 Implement account deletion scheduling and cancellation window logic in `backend/src/services/user_service.py` (backend)
- [ ] T042 Add logging for auth success/failure, authorization failures, admin actions, sensitive access in `backend/src/services/*` (backend)

## Phase 3.4: Core Implementation (Frontend)
- [ ] T043 [P] Implement Register page and form with validation at `frontend/src/pages/register.tsx` (frontend)
- [ ] T044 [P] Implement Login page and form at `frontend/src/pages/login.tsx` (frontend)
- [ ] T045 [P] Implement Profile page with view/edit at `frontend/src/pages/profile.tsx` (frontend)
- [ ] T046 Implement Admin Users page (list/edit/delete, role change) at `frontend/src/pages/admin/users.tsx` (frontend)
- [ ] T047 Implement 2FA enrollment and verification UI at `frontend/src/components/auth/TwoFactor.tsx` (frontend)
- [ ] T048 Add accessibility, error/loading/empty states across forms (WCAG 2.1 AA) in relevant components (frontend)

## Phase 3.5: Integration (Security, DB, Middleware)
- [ ] T049 Wire DB models to services and ensure indexes; prevent N+1 via joins in `backend/src/services/*.py` (db)
- [ ] T050 Apply security headers and CORS in app factory in `backend/src/main.py` (backend)
- [ ] T051 Add JWT cookie config (HttpOnly, Secure, SameSite=Strict) and token TTLs in `backend/src/services/auth_service.py` (backend)
- [ ] T052 Add email verification sender integration (provider abstraction) in `backend/src/services/notification_service.py` (backend)
- [ ] T053 Add backups purge policy and deletion job stub (documentation/code comment) in `backend/src/services/user_service.py` (backend)

## Phase 3.6: Polish (Performance, Docs, Unit tests)
- [ ] T054 [P] Unit tests for validation rules in `backend/tests/unit/test_validation.py` (qa)
- [ ] T055 [P] Unit tests for services (auth, mfa, rbac) in `backend/tests/unit/test_services.py` (qa)
- [ ] T056 [P] LCP/FCP/TTI & Lighthouse checks script in `frontend/tests/perf/lighthouse.test.ts` (qa)
- [ ] T057 [P] Bundle budget enforcement (<200KB gz) in `frontend/` build config and CI (devops)
- [ ] T058 [P] DB index verification tests (<50ms lookups) in `backend/tests/perf/test_db_perf.py` (qa)
- [ ] T059 Update API docs at `specs/001-user-management/contracts/README.md` with response examples (docs)
- [ ] T060 Update quickstart with latest flows at `specs/001-user-management/quickstart.md` (docs)

## Dependencies
- Setup (T001–T010) before tests and implementation
- Contract/Integration tests (T011–T026) MUST be in place and failing before T027+
- Models (T028–T029) before services (T030–T034)
- Services before endpoints (T037–T041)
- RBAC and admin rules before exposing admin UI (T040 before T046)
- Integration/security tasks (T049–T053) before polish (T054–T060)

## Parallel Example
```
# Launch contract and integration tests in parallel once setup is complete:
T011, T012, T013, T014, T015, T016, T017, T018, T019, T020, T021
T022, T023, T024, T025, T026
```

## Validation Checklist
- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] Tests precede implementation for each concern
- [ ] [P] tasks touch different files with no dependencies
- [ ] Each task includes exact file path and owner area
- [ ] Security and privacy tasks present (headers, rate limits, deletion, export)
- [ ] Performance targets addressed (indexes, budgets)
