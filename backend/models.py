"""Pydantic response models and SQLAlchemy ORM models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, relationship


# ── SQLAlchemy ORM ────────────────────────────────────────────────────────────


class Base(DeclarativeBase):
    pass


class Sport(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)

    leagues = relationship("League", back_populates="sport")


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    season = Column(String(20))

    sport = relationship("Sport", back_populates="leagues")
    teams = relationship("Team", back_populates="league")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    name = Column(String(100), nullable=False)
    abbreviation = Column(String(10))
    logo = Column(Text)

    league = relationship("League", back_populates="teams")
    players = relationship("Player", back_populates="team")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    name = Column(String(100), nullable=False)
    position = Column(String(20))

    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStat", back_populates="player")


class PlayerStat(Base):
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    season = Column(String(20))
    category = Column(String(50), nullable=False)
    stats = Column(JSONB, nullable=False, default=dict)
    rank = Column(Integer)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    player = relationship("Player", back_populates="stats")


# ── Pydantic response schemas ────────────────────────────────────────────────


class SportOut(BaseModel):
    slug: str
    name: str

    model_config = {"from_attributes": True}


class LeagueOut(BaseModel):
    slug: str
    name: str
    season: str | None = None

    model_config = {"from_attributes": True}


class LeaderEntry(BaseModel):
    rank: int
    player: str
    team: str
    team_logo: str | None = None
    stats: dict[str, Any]


class CategoryLeaders(BaseModel):
    league: str
    season: str
    category: str
    updated_at: str
    leaders: list[LeaderEntry]
