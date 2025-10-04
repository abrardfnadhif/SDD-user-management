# User Management Application

Secure user management system with authentication, RBAC, 2FA, and GDPR/CCPA compliance.

## Architecture

- **Backend**: FastAPI (Python 3.11) - `/backend`
- **Frontend**: Next.js (TypeScript) - `/frontend`
- **Database**: PostgreSQL 15 (Dockerized)
- **Specs**: Design documents - `/specs/001-user-management`

## Quick Start

```bash
# One-line setup (requires Docker)
make dev

# Or manual setup:
# 1. Start database
docker-compose up -d postgres

# 2. Setup backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.sample .env  # Edit with your values

# 3. Setup frontend
cd frontend
npm install
cp env.example .env.local  # Edit with your values
npm run dev
```

## Environment Variables

### Backend (`backend/.env`)
Copy `backend/.env.sample` and configure:

**Required Secrets** (⚠️ NEVER commit these):
- `JWT_SECRET_KEY`: Minimum 32 characters, cryptographically random
- `DATABASE_URL`: PostgreSQL connection string
- Email provider credentials (SMTP/SendGrid/SES/Postmark)

**Security Configuration**:
- `BCRYPT_ROUNDS`: 12 (minimum, per Constitution V)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: 15
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS`: 7
- `RATE_LIMIT_LOGIN_ATTEMPTS`: 5 per 15 minutes

**Privacy & Compliance**:
- `DELETION_GRACE_PERIOD_DAYS`: 14 (GDPR right to cancel)
- `DELETION_COMPLETE_DAYS`: 30 (complete within 30 days)
- `BACKUP_RETENTION_DAYS`: 90 (purge backups)

### Frontend (`frontend/.env.local`)
Copy `frontend/env.example` and configure:

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_APP_ENV`: development|staging|production

## Security Notes

⚠️ **CRITICAL**: Never commit `.env` or `.env.local` files to version control.

### Generating Secrets

```bash
# Generate JWT secret (backend)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or using openssl
openssl rand -base64 32
```

### Required Permissions

- Database user needs: CREATE, SELECT, INSERT, UPDATE, DELETE on all tables
- Email service needs: Send transactional emails
- Redis (optional): Read/write for distributed rate limiting

## Development

See individual README files:
- Backend: `/backend/README.md`
- Frontend: `/frontend/README.md`

## Constitution Compliance

This project follows Constitution v1.1.0 principles:
- **Code Quality (I)**: Type safety, linting, ≤50 lines per function
- **TDD (II)**: Tests first, ≥80% coverage, 100% on critical paths
- **UX (III)**: Responsive, WCAG 2.1 AA, consistent components
- **Performance (IV)**: API p95<200ms, Lighthouse≥90, bundle<200KB
- **Security (V)**: JWT, RBAC, bcrypt≥12, 2FA, CSP/HSTS, rate limiting
- **Privacy (VI)**: GDPR/CCPA, data export, deletion, audit logs

## License

[Your License Here]
