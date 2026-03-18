"""FastAPI entry-point for Top Performers backend."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import scheduler
from routers import leagues, sports, stats

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s  %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: warm cache + start scheduler
    await scheduler.refresh_nba()
    scheduler.start()
    yield
    # Shutdown
    scheduler.stop()


app = FastAPI(
    title="Top Performers API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow the Next.js frontend (dev + production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(sports.router)
app.include_router(leagues.router)
app.include_router(stats.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
