# Quickstart — Validation Scenarios

This guide validates the end-to-end user journeys using acceptance scenarios from the specification.

## Prerequisites
- Environment running (frontend + backend + PostgreSQL)
- Seed roles: Admin, User
- Test user email inbox accessible for verification links

## Scenario A: Registration → Email Verification → Login → Profile Update
1. Navigate to /register
2. Fill full name, email (unique), strong password, role=User; accept privacy/terms
3. Submit
4. Check mailbox; open verification link within 24 hours
5. Navigate to /login; enter email/password
6. Expect authenticated session (secure cookies set)
7. Go to /profile; update full name and DOB; save
8. Expect success message and audit log entry created

## Scenario B: Login with 2FA Enabled
1. As Admin, enable 2FA for your account; store backup codes
2. Logout; go to /login; enter email/password
3. Enter valid TOTP; expect login success
4. Enter invalid TOTP 5 times; expect temporary block due to rate limit

## Scenario C: RBAC Role Change
1. Login as Admin; go to /admin/users
2. Change a user's role from User → Admin
3. Expect success message, role history recorded; verify access changes immediately

## Scenario D: Account Deletion
1. Logged in as User, request account deletion and re-authenticate
2. Confirm deletion; expect scheduled deletion within 30 days and 14-day cancellation window displayed
3. Export data before deletion; confirm backups purge policy ≤90 days documented

## Scenario E: Security Headers
1. Inspect any response headers
2. Verify presence of CSP (strict), HSTS (1y includeSubDomains), X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy: strict-origin-when-cross-origin

## Scenario F: Logging & Monitoring
1. Trigger successful login, failed login, forbidden admin action as non-admin
2. Verify logs recorded without secrets/PII; alerts for suspicious patterns
