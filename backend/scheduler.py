"""APScheduler — refresh cached stats every 6 hours."""

from __future__ import annotations

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from cache import cache
from services.espn import fetch_nba_leaders

log = logging.getLogger("scheduler")

scheduler = AsyncIOScheduler()


async def refresh_nba() -> None:
    """Fetch fresh NBA leaders and update the cache."""
    log.info("Refreshing NBA leaders …")
    try:
        data = await fetch_nba_leaders()
        cache.set("nba_leaders", data, ttl=6 * 3600)
        log.info("NBA leaders refreshed — date=%s", data.get("date"))
    except Exception:
        log.exception("Failed to refresh NBA leaders")


def start() -> None:
    scheduler.add_job(
        refresh_nba,
        "interval",
        hours=6,
        id="refresh_nba",
        replace_existing=True,
    )
    scheduler.start()
    log.info("Scheduler started — NBA refresh every 6 h")


def stop() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
        log.info("Scheduler stopped")
