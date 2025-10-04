Create a detailed plan for building the user management app using the following tech stack:

- **Frontend**: Next.js with TypeScript (React framework), Tailwind CSS, and Shadcn UI.
- **Backend**: FastAPI (Python framework)
- **Database**: PostgreSQL
- **Docker**: For containerizing PostgreSQL database and local development environment
- **Architecture Goals**:
  - Use **SOLID** principles
  - Use **Five Lines of Code** principles
  - Maintain separation of concerns
  - Use **Audit Trails** to track critical user actions

## Plan Command Instructions (SDD)

Generate `specs/001-user-management/plan.md` using `.specify/templates/plan-template.md`, based on the feature spec at `specs/001-user-management/spec.md` and the Constitution at `.specify/memory/constitution.md` (v1.1.0). Follow the template section order and fill concrete details (no placeholders left).

### Inputs
- Feature Spec: `specs/001-user-management/spec.md`
- Constitution: `.specify/memory/constitution.md`
- Template: `.specify/templates/plan-template.md`

### Fill These Sections Precisely
- **Summary**: One paragraph extracting the main requirement and approach from the spec.
- **Technical Context**:
  - Language/Version: Frontend TypeScript (Next.js), Backend Python 3.11 (FastAPI)
  - Primary Dependencies: Next.js, Tailwind CSS, shadcn/ui; FastAPI, pydantic; JWT libs
  - Storage: PostgreSQL 15
  - Testing: Frontend Jest + Playwright; Backend pytest + httpx
  - Target Platform: Web (frontend and backend)
  - Project Type: web
  - Performance Goals: from Constitution IV (p50/p95 latencies, FCP/TTI, Lighthouse ≥90)
  - Constraints: from Constitution IV (bundle <200KB gz, no N+1, indexed queries)
  - Scale/Scope: simple user management, 1,000 concurrent users

- **Constitution Check**: Fill all checklists from plan-template for Principles I–VI:
  - Code Quality (I), TDD (II), UX (III), Performance (IV), Security (V), Privacy & Compliance (VI)
  - If any violation, record in Complexity Tracking; otherwise this gate should pass.

- **Project Structure** (use Web application layout; replace options with concrete tree):
```
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

specs/001-user-management/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
```

- **Phase 0: Outline & Research**: List unknowns and decisions to research (email verification flow, email change policy, data residency if any). Output `research.md`.

- **Phase 1: Design & Contracts**:
  - Extract entities from the spec into `data-model.md`
  - Generate API contracts (registration, login, refresh, profile, admin users, roles) and save to `/contracts/`
  - Create failing contract tests for each endpoint
  - Extract test scenarios into `quickstart.md`
  - If available, run `.specify/scripts/bash/update-agent-context.sh windsurf` as per template guidance

- **Phase 2: Task Planning Approach**: Describe how /tasks will generate TDD-first tasks (do not create tasks).

- **Complexity Tracking**: If any Constitution Check items cannot be satisfied, justify here.

- **Progress Tracking**: Initialize all checkboxes per template; mark “Initial Constitution Check: PASS” only if no violations.

### Performance Targets (from Constitution IV)
- API: p50<100ms reads, p95<200ms reads, p95<500ms writes
- Frontend: FCP<1.5s, TTI<3.5s, Lighthouse ≥90
- DB: no N+1; indexed queries; simple lookups <50ms
- Bundle: initial JS <200KB gzipped; route-based code splitting

### Security & Privacy (Principles V & VI)
- JWT with secure cookies (HttpOnly, Secure, SameSite=Strict); access ≤15m, refresh ≤7d; rate limit 5/15m/IP
- RBAC enforced server and UI; bcrypt ≥12; password history(5); CSRF, XSS protections; TLS 1.3; CSP/HSTS headers
- 2FA TOTP with 10 backup codes; admin required
- GDPR/CCPA: data export, deletion with 14-day cancellation, backups purge ≤90 days; audit logs; no third-party sharing without consent

### Acceptance Criteria for this Plan
- Uses `.specify/templates/plan-template.md` with no leftover placeholders or option labels
- Constitution Check fully populated for I–VI
- Concrete project structure tree present (no “Option” text)
- Phase outputs and gating accurately described
- Performance/Security/Privacy targets explicitly listed

### **1. Project Setup & Initialization**

- **Frontend (Next.js)**
  - Create Next.js TypeScript app; add Tailwind and shadcn/ui.
  - Configure ESLint/Prettier with zero-error policy; CI lint step.
  - Add base pages: `/login`, `/register`, `/profile`, `/admin/users`.
  - Establish global UX: responsive (320/768/1920), WCAG 2.1 AA, error/empty/loading states.
  - Set up API client with centralized error handling and typed responses.

- **Backend (FastAPI)**
  - Python 3.11; FastAPI with routers: `auth`, `users`, `roles`, `admin`.
  - Security middleware: CORS, security headers (CSP/HSTS via proxy or ASGI), CSRF strategy for state-changing forms if needed.
  - Rate limiting middleware (5 failed login attempts/15m/IP); logging config for auth/authorization events.
  - Testing scaffold: pytest + httpx; contract/integration tests to be generated in Phase 1.

- **Database (PostgreSQL)**
  - Provision PostgreSQL 15; create application DB/user; .env.sample with secrets (no hardcoding).
  - Apply schema (see Section 4) and seed roles (Admin, User).

- **Docker**
  - docker-compose for `postgres`, `backend`, optional `reverse-proxy`.
  - Healthchecks, named volumes, network; dev profile with hot-reload; production profile later.
  - Makefile or npm scripts to wrap common commands.

### **2. Development Milestones & Features**

- **Milestone 1: Setup & Architecture**
  - Repo initialized with frontend/backend folders, lint/format, pre-commit hooks.
  - Dockerized Postgres + service skeletons; basic CI (lint + tests).
  - Constitution Check I–VI: PASS (document any deviations in Complexity Tracking).

- **Milestone 2: User Registration & Profile Management**
  - Registration endpoint with email verification (24h magic link, resend limits).
  - Profile read/update with audit logging.
  - Frontend forms with validation and accessibility.
  - Contract, integration, and E2E tests first; then implementation to green.

- **Milestone 3: Role-Based Access Control (RBAC)**
  - Roles seeded (Admin, User); server-side RBAC checks on protected endpoints.
  - Admin UI for role management; enforce "at least one Admin" rule.
  - Tests for authorization happy/deny paths.

- **Milestone 4: Two-Factor Authentication (2FA)**
  - TOTP enrollment, verification, backup codes (10 single-use), admin required.
  - 2FA gating on login; recovery flows; audit entries.
  - Security tests; negative attempts rate-limited.

- **Milestone 5: Dockerization & CI/CD Pipeline**
  - Hardened images; multi-stage builds where applicable.
  - CI runs unit/integration/contract/E2E; coverage ≥80% (100% critical paths).
  - Basic CD (optional) with environment-specific configs.

### **3. Authentication Flow**

- **JWT Authentication**
  - Email verification required before first login.
  - Login: issue access (≤15m) and refresh (≤7d) in secure cookies (HttpOnly, Secure, SameSite=Strict).
  - Refresh rotation optional; on email change or password reset, revoke sessions.
  - 2FA (if enabled) after password, before issuing tokens.

- **Rate Limiting & Brute Force Protection**
  - 5 failed login attempts per 15 minutes per IP → temporary block.
  - Log and alert on suspicious patterns; never leak which factor failed.

### **4. Database Setup & Schema**

- **Database Schema**
  - `users(id, email unique, full_name, dob, password_hash, two_factor_enabled, created_at, updated_at)`
  - `roles(id, name unique)` and `user_roles(user_id, role_id, pk(user_id, role_id))` (flexible for future roles)
  - `audit_logs(id, actor_id, action, target_type, target_id, timestamp, metadata JSONB)` (append-only)
  - `email_verification_tokens(id, user_id, token_hash, expires_at, created_at)`
  - `password_reset_tokens(id, user_id, token_hash, expires_at, created_at)`
  - `backup_codes(id, user_id, code_hash, used_at)`
  - Indexes on `users.email`, foreign keys, and timestamps for auditing; ensure no N+1 via query design and indexes.

### **5. Developer Experience**

- **1 Line setup for local development**
  - Provide a single command to start dev environment (e.g., `make dev` or `npm run dev:all`) that:
    - boots docker-compose (Postgres, backend, proxy),
    - runs frontend and backend in watch mode,
    - applies DB migrations and seeds roles,
    - prints URLs and test credentials.
  - Include `.env.sample` and scripts to generate secrets; never commit real secrets.
