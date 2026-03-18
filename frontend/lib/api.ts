/**
 * Backend API client — replaces direct ESPN calls.
 */

// Server components need an absolute URL; browser can use relative "/api" (proxied by rewrites).
const isServer = typeof window === "undefined";
const API_BASE = isServer
  ? (process.env.BACKEND_URL ?? "http://localhost:8000") + "/api"
  : "/api";

export interface LeaderEntry {
  rank: number;
  player: string;
  team: string;
  team_logo?: string;
  stats: Record<string, number>;
}

export interface CategoryLeaders {
  league: string;
  season: string;
  category: string;
  updated_at: string;
  leaders: LeaderEntry[];
}

export interface NBAAllCategories {
  league: string;
  season: string;
  date: string;
  days_back: number;
  categories: Record<string, CategoryLeaders>;
}

export interface SportOut {
  slug: string;
  name: string;
}

export interface LeagueOut {
  slug: string;
  name: string;
  season: string | null;
}

async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { next: { revalidate: 3600 } });
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${path}`);
  }
  return res.json();
}

export function getSports() {
  return apiFetch<SportOut[]>("/sports");
}

export function getLeagues(sport: string) {
  return apiFetch<LeagueOut[]>(`/leagues/${sport}`);
}

export function getStats(league: string, category: string) {
  return apiFetch<CategoryLeaders>(`/stats/${league}/${category}`);
}

export function getAllNBAStats() {
  return apiFetch<NBAAllCategories>(`/stats/nba`);
}
