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

# Run linter
npm run lint
```

### One-line Dev Setup
See root `Makefile` for automated setup with backend and database.

### Adding shadcn/ui Components
```bash
npx shadcn@latest add button
npx shadcn@latest add form
npx shadcn@latest add input
# etc.
```

## Development
Open [http://localhost:3000](http://localhost:3000) to view the app.
