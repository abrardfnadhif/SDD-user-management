# Data Model — User Management

## Entities

### User
- id: UUID
- email: string (unique, lowercased)
- full_name: string (1..200)
- dob: date (optional)
- password_hash: string (bcrypt)
- two_factor_enabled: boolean (default: false)
- created_at: datetime (UTC)
- updated_at: datetime (UTC)

Constraints:
- email unique index
- password policy enforced at application level (see Constitution V)

### Role
- id: UUID
- name: enum {Admin, User} (extensible)

Constraints:
- name unique index

### UserRole (association)
- user_id: UUID (FK -> User.id)
- role_id: UUID (FK -> Role.id)

Primary Key: (user_id, role_id)

### AuditLog
- id: UUID
- actor_id: UUID (FK -> User.id, nullable for system)
- action: string (e.g., USER_CREATED, ROLE_CHANGED)
- target_type: string (e.g., user, role)
- target_id: UUID
- timestamp: datetime (UTC)
- metadata: JSON (no raw PII values)

Behavior:
- Append-only; immutable once written

### EmailVerificationToken
- id: UUID
- user_id: UUID (FK -> User.id)
- token_hash: string (one-way hashed)
- expires_at: datetime (UTC) — 24h after issue
- created_at: datetime (UTC)

### PasswordResetToken
- id: UUID
- user_id: UUID (FK -> User.id)
- token_hash: string (one-way hashed)
- expires_at: datetime (UTC)
- created_at: datetime (UTC)

### BackupCode
- id: UUID
- user_id: UUID (FK -> User.id)
- code_hash: string (one-way hashed)
- used_at: datetime (UTC, nullable)

## Relationships
- User 1..* UserRole *..1 Role
- User 1..* AuditLog (as actor)
- User 1..* EmailVerificationToken
- User 1..* PasswordResetToken
- User 1..* BackupCode

## Indexes
- users(email)
- user_roles(user_id, role_id)
- audit_logs(target_type, target_id, timestamp)
- email_verification_tokens(user_id, expires_at)
- password_reset_tokens(user_id, expires_at)
- backup_codes(user_id, used_at)
