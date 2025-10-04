# Audit Logging Implementation

## Overview
Comprehensive audit logging is implemented throughout the application using `AuditLogService`. All security-sensitive operations are logged to the `audit_logs` table (append-only).

## Logging Coverage

### Authentication Events
- ✅ **Login Success**: `log_login_success()` - Called in `/api/login`
- ✅ **Login Failure**: `log_login_failure()` - Called in `/api/login` on invalid credentials
- ✅ **User Registration**: `log_user_created()` - Called in `/api/register`
- ✅ **Email Verification**: `log_email_verified()` - Available for email verification flow

### Authorization Events
- ✅ **Access Denied**: `log_access_denied()` - Available for RBAC failures
- ✅ **Role Changes**: `log_role_changed()` - Called in `/api/admin/users/{id}/role`

### User Management
- ✅ **User Created**: `log_user_created()` - Registration
- ✅ **User Updated**: `log_user_updated()` - Profile updates
- ✅ **User Deleted**: `log_user_deleted()` - Deletion scheduling

### Security Events
- ✅ **2FA Enabled**: `log_2fa_enabled()` - Called in `/api/2fa/enable`
- ✅ **2FA Disabled**: `log_2fa_disabled()` - Available for 2FA disable
- ✅ **Password Changed**: `log_password_changed()` - Available for password reset

### Admin Actions
- ✅ **Admin Actions**: `log_admin_action()` - Generic admin action logging
  - User updates
  - Deletion scheduling
  - Deletion cancellation
  - Role changes

## Audit Log Structure

```python
{
    "id": UUID,
    "actor_id": UUID | None,  # User performing action (None for system)
    "action": str,            # e.g., "USER_CREATED", "LOGIN_SUCCESS"
    "target_type": str,       # e.g., "user", "role", "security"
    "target_id": UUID,        # ID of affected entity
    "metadata": dict,         # Additional context (no raw PII)
    "timestamp": datetime     # UTC timestamp
}
```

## Constitution Compliance

✅ **Constitution VI**: Audit logging strategy
- All data access logged
- All modifications logged
- Actor tracking (user or system)
- Append-only (immutable)
- No raw PII in metadata

✅ **Spec Requirements**:
- Authentication events logged
- Authorization failures logged
- Admin actions logged
- Sensitive access logged

## Usage Examples

### In API Endpoints
```python
# Log successful login
await AuditLogService.log_login_success(db, user.id)

# Log failed login
await AuditLogService.log_login_failure(db, email)

# Log admin action
await AuditLogService.log_admin_action(
    db, admin_id, "UPDATE_USER", user.id, {"fields": ["full_name"]}
)
```

### In Services
```python
# Log role change
await AuditLogService.log_role_changed(
    db, user.id, admin_id, old_roles, new_roles
)
```

## Future Enhancements

- [ ] Add log retention policy
- [ ] Add log export functionality (GDPR)
- [ ] Add log search/filter API
- [ ] Add real-time log monitoring
- [ ] Add anomaly detection on logs
