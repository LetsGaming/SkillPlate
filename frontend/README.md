# SkillPlate — Frontend

Vue 3 + Ionic app for generating and browsing AI-powered cooking courses via the SkillPlate Flask backend.

## Prerequisites

- Node.js ≥ 18
- pnpm (or npm)
- SkillPlate backend running on `http://localhost:5000`

## Install & run

```bash
pnpm install
pnpm dev
```

Open `http://localhost:5173` in your browser.

## Default credentials (backend mock)

Username: `LetsGamingDE` · Password: `password123`

## Environment variables

Copy `.env.example` to `.env.local` and adjust if the backend runs on a different host/port:

```
VITE_API_BASE_URL=http://localhost
VITE_API_PORT=5000
VITE_API_BASE_PATH=/api
```
