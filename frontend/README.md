# Frontend — User Management UI

Next.js TypeScript frontend for secure user management.

## Structure
- `src/components/` — Reusable UI components (auth, forms, etc.)
- `src/pages/` — Next.js pages (login, register, profile, admin)
- `src/services/` — API client and utilities
- `tests/e2e/` — End-to-end tests (Playwright)
- `tests/perf/` — Performance tests (Lighthouse, bundle size)

## Tech Stack
- Next.js (TypeScript)
- Tailwind CSS
- shadcn/ui components
- Jest + Playwright for testing

## Setup

### Quick Start
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run production server
npm start

# Code quality (zero-error policy)
npm run lint              # Lint with max-warnings 0
npm run lint:fix          # Auto-fix linting issues
npm run format            # Format code with Prettier
npm run format:check      # Check formatting
npm run type-check        # TypeScript type checking
npm run validate          # Run all checks (type + lint + format)
