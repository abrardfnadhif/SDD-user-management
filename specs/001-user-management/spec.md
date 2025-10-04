# Feature Specification: User Management

**Feature Branch**: `[001-user-management]`  
**Created**: 2025-10-04  
**Status**: Draft  
**Input**: User description: "Specify a complete, testable Feature Specification for the User Management application, aligned with the Constitution. In-scope: registration, login, profiles, RBAC, 2FA, account deletion, security headers, logging/monitoring."

---

## User Scenarios & Testing (mandatory)

### Primary User Story
As an Anonymous User, I want to register an account so that I can log in and manage my profile securely. After registration, I log in (with 2FA if enabled) and update my profile information.

### Acceptance Scenarios
1. Given a unique email and valid inputs, When I submit registration, Then my account is created and I receive a verification email; I MUST verify email via magic link (expires in 24 hours) before first login.
2. Given an existing account, When I log in with correct credentials, Then I am authenticated and receive a session (secure cookies) within policy timeouts.
3. Given 2FA is enabled, When I provide correct TOTP after password, Then I am authenticated; When I provide incorrect TOTP 5 times, Then I am temporarily blocked per rate limits.
4. Given I am authenticated, When I update my profile with valid data, Then the profile is saved and an audit entry is recorded.
5. Given I am an Admin, When I change a user's role, Then the role is updated and history recorded; access reflects RBAC immediately.
6. Given I request account deletion, When I confirm and re-authenticate, Then the account is scheduled for deletion and data anonymization per policy with confirmation shown.
7. Given any response, When I inspect headers, Then CSP, HSTS, X-Frame-Options, X-Content-Type-Options, and Referrer-Policy are present.
8. Given suspicious auth failures occur, When thresholds are exceeded, Then alerts are generated and relevant security logs are retained.

### Edge Cases
- Duplicate email during registration → friendly error without leaking account existence beyond necessary messaging.
- Weak password / policy violations → specific guidance.
- Expired/invalid JWT or refresh token → re-authentication required.
- Time drift for TOTP → ±30s drift window (one 30-second time-step).
- Orphaned admin prevention → disallow deleting/demoting the last active Admin; require at least one Admin at all times.
- Legal hold → account deletion requests are blocked during legal hold; account may be deactivated; deletion resumes after hold is lifted.
---

## Requirements (mandatory)

### Functional Requirements
- **FR-001 Registration**: System MUST allow users to register with full name, email, password, role, and optional DOB; validate email format; enforce password policy from Constitution V; handle duplicate emails.
- **FR-002 Consent**: System MUST present privacy policy and terms; account creation MUST require explicit consent.
- **FR-003 Login**: System MUST authenticate using password and manage sessions using JWT with secure cookies (HttpOnly, Secure, SameSite=Strict); access token ≤15 minutes, refresh ≤7 days.
- **FR-004 Rate Limiting**: System MUST rate limit login attempts to 5 failed attempts per 15 minutes per IP and temporarily lock further attempts.
- **FR-005 RBAC**: System MUST enforce role-based access (Admin, User) on all protected actions at API and UI layers.
- **FR-006 Profiles**: Authenticated users MUST view/update their own profile fields; admins MAY view/update/delete users and reset passwords; all changes MUST be audited.
- **FR-007 2FA**: System MUST support TOTP-based 2FA with 10 backup codes; 2FA is mandatory for Admins and optional for Users.
- **FR-008 Account Deletion**: System MUST support account deletion/deactivation with re-authentication; deletion is scheduled to occur within 30 days with a 14-day cancellation window; data MUST be anonymized/erased per policy; backups purged within 90 days; user MAY export data prior to deletion.
- **FR-009 Security Headers**: System MUST include CSP (strict), HSTS(1y, includeSubDomains), X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy: strict-origin-when-cross-origin on all responses.
- **FR-010 Logging & Monitoring**: System MUST log auth success/failure, authorization failures, admin actions, and sensitive data access; exclude secrets/PII; retain ≥90 days; alert on suspicious patterns.
- **FR-011 Data Export**: System MUST allow users to download their data in machine-readable format (JSON/CSV) upon request (GDPR portability).
- **FR-012 Email Verification**: System MUST require email verification via magic link sent to the registered email; link expires in 24 hours; login is blocked until verified; resends rate-limited (max 3/hour, 10/day); verification attempts logged.
- **FR-013 Email Change**: System MUST require re-authentication and verification of the new email via 24-hour magic link; change completes only after verification; notify old email of the change; revoke all active sessions upon successful change.

#### Assumptions & Defaults (resolved)
- Email verification required before first login; 24-hour magic link; resend limits as specified.
- Email change requires re-auth + new email verification; notify old email; revoke sessions on change.
- At least one Admin account MUST always exist; last Admin cannot be deleted/demoted.
- Deletion has a 14-day cancellation window; legal hold blocks deletion and permits deactivation only; backups purge in 90 days.
- Data residency: no specific regional constraint assumed; data stored in the primary deployment region; revisit if regulatory requirements emerge.

### Key Entities (include if data involved)
- **User**: id, full_name, email, role, dob(optional), two_factor_enabled, created_at, updated_at
- **Role**: name, permissions
- **AuthSession/Tokens**: access_token, refresh_token, exp
- **MFASecret/BackupCodes**: secret_metadata, codes_remaining
- **AuditLog**: actor_id, action, target_type, target_id, timestamp, metadata (no PII values)

---

## Review & Acceptance Checklist

Note: All prior clarification items have been resolved via the Assumptions & Defaults section; no [NEEDS CLARIFICATION] markers remain.

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] User scenarios defined
- [ ] Requirements generated
- [ ] Review checklist passed
