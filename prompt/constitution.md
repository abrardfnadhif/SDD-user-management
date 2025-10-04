create a secure, simple user management app with the following key features:

- **User Registration**: Collects full name, email, password, role, and date of birth (optional).
- **Login & Authentication**: Uses JWT for authentication with secure cookie management (HttpOnly, Secure, SameSite). Includes rate limiting for login attempts and protection against brute force attacks.
- **User Profiles**: Users can view and update their own profile. Admins can view, update, or delete user profiles, and reset passwords.
- **Role Management**: Admins can assign roles to users (Admin, User). Roles defines permissions for access and actions within the application.
- **Password Storage**: Passwords are securely hashed with bcrypt, and salts are used for extra security.
- **Two-Factor Authentication (2FA)**: Optional two-factor authentication with TOTP apps like Google Authenticator. Provide backup codes for users to access their accounts in case they lose access to their TOTP app.
- **Account Deletion**: Users can deactivate or delete their accounts. Data should be securely erased or anonymized after deletion.
- **Security Measures**: Implement HTTPS for secure communication, HSTS, CSP headers, and protection against XSS and CSRF attacks.
- **Compliance**: The app should support GDPR/CCPA compliance, allowing users to download their data and delete their accounts. Provide a privacy policy and terms of service.
- **User Interface**: Simple and responsive design with accessible forms for login, registration, and profile management. Mobile-first design is a priority.
- **Security Protocols**: Focus on mitigating common security like SQL injection, cross-site scripting (XSS), cross-site request forgery (CSRF), and brute force attacks. implement logging and monitoring for security events. Conduct regular security audits and penetration testing.

Use the most secure methods available for each functionality and ensure that codebase quality is high by adhering to best practices and standards.
