# Top Performers

Daily top performers across major sports — starting with NBA.

A full-stack app that fetches real-time box scores from ESPN's public API, ranks players across 9 statistical categories, and presents them in a clean, responsive leaderboard.

![Tech Stack](https://img.shields.io/badge/Next.js-15-black?logo=next.js)
![Tech Stack](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![Tech Stack](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)
![Tech Stack](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)
![Tech Stack](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?logo=tailwindcss)
![Tech Stack](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Running the App](#running-the-app)
- [Docker](#docker)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [How It Works](#how-it-works)
- [NBA Stat Categories](#nba-stat-categories)
- [Fantasy Scoring](#fantasy-scoring)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)

---

## Features

- **Zero API Keys Required** — ESPN's public API needs no authentication
- **9 NBA Stat Categories** — Points, rebounds, assists, blocks, steals, turnovers, 3PT, FT, and DraftKings fantasy points
- **Auto-Refreshing Data** — APScheduler proactively fetches fresh data every 6 hours
- **In-Memory Cache** — 1-hour TTL cache (Redis-ready for production)
- **Server-Side Rendering** — Next.js Server Components with ISR (hourly revalidation)
- **Proper Tie Handling** — Players with the same stat value get the same rank
- **Mobile-Responsive** — 1-column on mobile, 3-column grid on desktop
- **Interactive API Docs** — Swagger UI auto-generated at `/docs`
- **One-Command Startup** — `npm run dev` starts both backend and frontend

---

## Tech Stack

| Layer         | Technology                          | Purpose                            |
| ------------- | ----------------------------------- | ---------------------------------- |
| **Frontend**  | Next.js 15 (App Router) + React 18  | Server-rendered UI with ISR        |
| **Styling**   | Tailwind CSS 3.4                    | Utility-first responsive design    |
| **Backend**   | FastAPI (Python, async)             | REST API with auto OpenAPI docs    |
| **Data**      | ESPN Public API                     | Real-time NBA box scores           |
| **Cache**     | In-memory TTL (Redis-ready)         | 1-hour default TTL                 |
| **Scheduler** | APScheduler (AsyncIO)               | Background data refresh every 6h   |
| **ORM**       | SQLAlchemy 2.0 (async)              | Database-ready models (Phase 2)    |

---

## Project Structure

```
Top-performers/
├── backend/
│   ├── main.py                 # FastAPI app entry point (CORS, lifespan, routes)
│   ├── models.py               # SQLAlchemy ORM models + Pydantic response schemas
│   ├── cache.py                # In-memory TTL cache (swap for Redis later)
│   ├── scheduler.py            # APScheduler — refreshes NBA data every 6 hours
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variable template
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── sports.py           # GET /api/sports
│   │   ├── leagues.py          # GET /api/leagues/{sport}
│   │   └── stats.py            # GET /api/stats/{league}/{category}
│   └── services/
│       ├── __init__.py
│       └── espn.py             # ESPN API client + box score parser
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx          # Root layout with metadata
│   │   ├── page.tsx            # Home page — sport selection
│   │   ├── globals.css         # Tailwind base styles
│   │   └── nba/
│   │       ├── page.tsx        # NBA leaderboard (Server Component, ISR)
│   │       └── loading.tsx     # Skeleton loading state
│   ├── components/
│   │   └── StatCategory.tsx    # Reusable top-5 player list card
│   ├── lib/
│   │   └── api.ts              # Typed API client (fetch wrapper)
│   ├── .env.local              # Frontend env vars
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── next.config.ts
│
├── package.json                # Root — runs both servers via concurrently
└── README.md
```

---

## Prerequisites

| Tool        | Version | Check with          |
| ----------- | ------- | ------------------- |
| **Node.js** | 18+     | `node --version`    |
| **npm**     | 9+      | `npm --version`     |
| **Python**  | 3.10+   | `python --version`  |
| **pip**     | 22+     | `pip --version`     |
| **Docker**  | 24+     | `docker --version`  |

> **Docker only?** If you just want to run the app via Docker, you only need Docker Desktop installed. Skip the Node/Python/pip requirements.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd top-performers
```

### 2. Backend Setup

```bash
cd backend

# Create a Python virtual environment
python -m venv venv

# Activate it
# Windows (CMD):
venv\Scripts\activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Copy and edit env vars
copy .env.example .env       # Windows
cp .env.example .env         # macOS/Linux
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

The frontend environment is pre-configured in `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 4. Root Setup (one-command startup)

From the project root:

```bash
npm install     # installs concurrently (first time only)
```

---

## Running the App

### Option A: One Command (Recommended)

From the **project root**:

```bash
npm run dev
```

This starts **both** servers simultaneously using `concurrently`. You'll see color-coded output:
- **[API]** (yellow) — FastAPI backend on port 8000
- **[WEB]** (cyan) — Next.js frontend on port 3000

### Option B: Two Separate Terminals

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

### Option C: Background the Backend

```bash
# Start backend in background, then frontend
cd backend && uvicorn main:app --reload --port 8000 &
cd frontend && npm run dev
```

Then open **http://localhost:3000** in your browser.

### What Happens on Startup

1. FastAPI starts and warms the cache by fetching latest NBA data from ESPN
2. APScheduler starts — automatically refreshes data every 6 hours
3. The API is live at `http://localhost:8000` (docs at `/docs`)
4. Next.js dev server starts with hot module reloading on port 3000

---

## Docker

The easiest way to run (or share) the app. **No Node.js or Python needed** — just Docker.

### Quick Start

```bash
docker compose up --build
```

That's it. Open **http://localhost:3000**.

- Backend: `http://localhost:8000` (API docs at `/docs`)
- Frontend: `http://localhost:3000`

### What Docker Does

| Container        | Image Base       | Port | Description                      |
| ---------------- | ---------------- | ---- | -------------------------------- |
| `tp-backend`     | `python:3.12-slim` | 8000 | FastAPI + uvicorn + APScheduler |
| `tp-frontend`    | `node:20-alpine`   | 3000 | Next.js standalone production build |

The frontend waits for the backend to pass its healthcheck before starting.

### Common Docker Commands

```bash
# Build and start both containers
docker compose up --build

# Run in the background (detached)
docker compose up --build -d

# View logs
docker compose logs -f            # both services
docker compose logs -f backend    # backend only
docker compose logs -f frontend   # frontend only

# Stop everything
docker compose down

# Rebuild from scratch (no cache)
docker compose build --no-cache
docker compose up
```

### Sharing the Image

```bash
# Option 1: Push to Docker Hub
docker compose build
docker tag tp-backend your-dockerhub-user/top-performers-api:latest
docker tag tp-frontend your-dockerhub-user/top-performers-web:latest
docker push your-dockerhub-user/top-performers-api:latest
docker push your-dockerhub-user/top-performers-web:latest

# Option 2: Export as .tar files (share without a registry)
docker save tp-backend  | gzip > top-performers-api.tar.gz
docker save tp-frontend | gzip > top-performers-web.tar.gz

# The recipient loads them:
docker load < top-performers-api.tar.gz
docker load < top-performers-web.tar.gz
docker compose up
```

---

## Available Scripts

### Root Level

| Command                | Description                              |
| ---------------------- | ---------------------------------------- |
| `npm run dev`          | Start both backend and frontend          |
| `npm run dev:backend`  | Start only the backend                   |
| `npm run dev:frontend` | Start only the frontend                  |
| `npm run install:all`  | Install frontend npm dependencies        |

### Backend

| Command                                     | Description                  |
| ------------------------------------------- | ---------------------------- |
| `python main.py`                            | Start with auto-reload       |
| `uvicorn main:app --reload --port 8000`     | Start via uvicorn directly   |

### Frontend

| Command          | Description                     |
| ---------------- | ------------------------------- |
| `npm run dev`    | Start dev server (port 3000)    |
| `npm run build`  | Production build                |
| `npm run start`  | Start production server         |

---

## Environment Variables

### Backend (`backend/.env`)

| Variable       | Required | Default    | Description                              |
| -------------- | -------- | ---------- | ---------------------------------------- |
| `HOST`         | No       | `0.0.0.0`  | Server bind address                      |
| `PORT`         | No       | `8000`     | Server port                              |
| `DATABASE_URL` | No       | —          | PostgreSQL connection string (Phase 2)   |
| `REDIS_URL`    | No       | —          | Redis URL — falls back to in-memory cache|

### Frontend (`frontend/.env.local`)

| Variable              | Required | Default                     | Description          |
| --------------------- | -------- | --------------------------- | -------------------- |
| `NEXT_PUBLIC_API_URL` | Yes      | `http://localhost:8000/api` | Backend API base URL |

---

## API Reference

Base URL: `http://localhost:8000/api`

### Interactive Docs

| URL                             | Description  |
| ------------------------------- | ------------ |
| `http://localhost:8000/docs`    | Swagger UI   |
| `http://localhost:8000/redoc`   | ReDoc        |

### Endpoints

#### Health Check

```
GET /api/health
```
```json
{ "status": "ok" }
```

#### List Sports

```
GET /api/sports
```
```json
[
  { "slug": "basketball", "name": "Basketball" },
  { "slug": "football", "name": "American Football" },
  { "slug": "soccer", "name": "Football (Soccer)" }
]
```

#### List Leagues for a Sport

```
GET /api/leagues/{sport}
```
Example: `GET /api/leagues/basketball`
```json
[
  { "slug": "nba", "name": "NBA", "season": "2024-25" }
]
```

#### Get Leaders by Category

```
GET /api/stats/{league}/{category}
```
Example: `GET /api/stats/nba/points`
```json
{
  "league": "NBA",
  "season": "2024-25",
  "category": "points",
  "updated_at": "03/16/2026",
  "leaders": [
    {
      "rank": 1,
      "player": "Shai Gilgeous-Alexander",
      "team": "OKC",
      "team_logo": null,
      "stats": { "pts": 45 }
    },
    {
      "rank": 2,
      "player": "Luka Doncic",
      "team": "DAL",
      "team_logo": null,
      "stats": { "pts": 42 }
    }
  ]
}
```

#### Get All Categories (main endpoint used by frontend)

```
GET /api/stats/{league}
```
Example: `GET /api/stats/nba`
```json
{
  "league": "NBA",
  "season": "2024-25",
  "date": "03/16/2026",
  "days_back": 1,
  "categories": {
    "points": { "league": "NBA", "category": "points", "leaders": [...] },
    "rebounds": { ... },
    "assists": { ... },
    "blocks": { ... },
    "steals": { ... },
    "turnovers": { ... },
    "three_pointers": { ... },
    "free_throws": { ... },
    "fantasy": { ... }
  }
}
```

---

## How It Works

```
                        Every 6 hours
                    ┌──────────────────┐
                    │   APScheduler    │
                    └────────┬─────────┘
                             │ refresh_nba()
                             ▼
┌──────────┐  GET   ┌──────────────┐  fetch   ┌───────────┐
│  Next.js │ ────── │   FastAPI    │ ──────── │  ESPN API  │
│ Frontend │  /api  │   Backend    │  httpx   │ (public)   │
└──────────┘        └──────┬───────┘          └───────────┘
                           │
                    ┌──────┴───────┐
                    │  TTL Cache   │
                    │  (1 hour)    │
                    └──────────────┘
```

### Data Pipeline

1. **Scoreboard fetch** — Checks ESPN's scoreboard API for the last 4 days to find the most recent day with NBA games
2. **Box score fetch** — Fetches all game summaries (box scores) in parallel using `asyncio.gather()`
3. **Stat extraction** — Parses individual player stat lines from ESPN's JSON format
4. **Fantasy scoring** — Calculates DraftKings-style fantasy points with bonus detection
5. **Ranking** — Sorts players and returns top 5 per category, with correct tie handling
6. **Caching** — Results cached in-memory with 1-hour TTL; APScheduler refreshes every 6 hours

### Frontend Architecture

- The NBA page is a **React Server Component** — data is fetched on the server, not in the browser
- Next.js **ISR** (`revalidate = 3600`) regenerates the page at most once per hour
- A **skeleton loading state** (`loading.tsx`) provides a smooth loading experience

---

## NBA Stat Categories

| Category       | Slug             | Stat Key | Description             |
| -------------- | ---------------- | -------- | ----------------------- |
| Points         | `points`         | `pts`    | Total points scored     |
| Rebounds       | `rebounds`       | `reb`    | Total rebounds          |
| Assists        | `assists`        | `ast`    | Total assists           |
| Blocks         | `blocks`         | `blk`    | Total blocks            |
| Steals         | `steals`         | `stl`    | Total steals            |
| Turnovers      | `turnovers`      | `to`     | Total turnovers         |
| Three-Pointers | `three_pointers` | `3pt`    | Three-pointers made     |
| Free Throws    | `free_throws`    | `ft`     | Free throws made        |
| Fantasy Points | `fantasy`        | `fpts`   | DraftKings fantasy score|

---

## Fantasy Scoring

Fantasy points use **DraftKings-style** scoring:

| Stat            | Multiplier |
| --------------- | ---------- |
| Points          | x 1.0     |
| Rebounds        | x 1.25    |
| Assists         | x 1.5     |
| Steals          | x 2.0     |
| Blocks          | x 2.0     |
| Turnovers       | x -0.5    |
| Double-double   | + 1.5     |
| Triple-double   | + 3.0     |

A **double-double** is reaching 10+ in two of: points, rebounds, assists, steals, blocks.
A **triple-double** is reaching 10+ in three of those categories (awards both bonuses).

---

## Deployment

### Recommended Stack (Free Tier)

| Service      | Platform      | Free Tier                |
| ------------ | ------------- | ------------------------ |
| **Frontend** | Vercel        | Unlimited hobby projects |
| **Backend**  | Render        | 750 hours/month          |
| **Database** | Supabase      | 500 MB (Phase 2)        |
| **Cache**    | Upstash Redis | 10k requests/day         |

### Deploy Frontend to Vercel

1. Push your repo to GitHub
2. Import the project in [Vercel](https://vercel.com)
3. Set **Root Directory** to `frontend`
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://your-backend.onrender.com/api`

### Deploy Backend to Render

1. Create a new **Web Service** on [Render](https://render.com)
2. Set **Root Directory** to `backend`
3. **Build command:** `pip install -r requirements.txt`
4. **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add your Vercel domain to the CORS `allow_origins` list in `backend/main.py`

---

## Roadmap

### Phase 1 — MVP (current)

- [x] FastAPI backend with ESPN API integration
- [x] NBA leaderboards — 9 stat categories, top 5 per category
- [x] In-memory cache with 1-hour TTL
- [x] APScheduler for background data refresh (every 6h)
- [x] Next.js 15 frontend with Server Components + ISR
- [x] Skeleton loading states
- [x] `concurrently` script to run both servers in one terminal
- [ ] Supabase database integration
- [ ] Deploy to Vercel + Render

### Phase 2 — Multi-Sport

- [ ] NFL stats via ESPN API
- [ ] European football via football-data.org
- [ ] Sport/league navigation in the UI
- [ ] Category filter tabs

### Phase 3 — Polish

- [ ] Upstash Redis for distributed caching
- [ ] Team logos and player headshots
- [ ] Playwright fallback scraper for edge cases
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Rate limiting and error monitoring

---

## Troubleshooting

### Backend won't start — `ModuleNotFoundError`

Make sure your virtual environment is activated:

```bash
cd backend
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
```

### Frontend can't reach the backend — `fetch failed`

1. Confirm the backend is running on port 8000: visit `http://localhost:8000/api/health`
2. Check `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
3. **Restart** the frontend dev server after changing `.env` files

### "No games found in the last 4 days"

This means there were no NBA games recently (All-Star break, off-season, etc.). The app will automatically show data once games resume.

### Port already in use

```bash
# Windows — find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS / Linux
lsof -ti:8000 | xargs kill -9
```

### CORS errors in browser console

Add your frontend URL to the `allow_origins` list in `backend/main.py`:

```python
allow_origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://your-domain.vercel.app",  # add your deployed URL
],
```

### `concurrently` not found

Run `npm install` from the project root (not from `frontend/`):

```bash
cd top-performers    # project root
npm install
npm run dev
```

---

## License

This project is for personal/educational use. ESPN data is fetched from their public, undocumented API.
