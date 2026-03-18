import Link from "next/link";
import { getAllNBAStats, type LeaderEntry } from "@/lib/api";
import StatCategory from "@/components/StatCategory";

export const dynamic = "force-dynamic";

const CATEGORY_LABELS: Record<string, string> = {
  points: "Points",
  rebounds: "Rebounds",
  assists: "Assists",
  blocks: "Blocks",
  steals: "Steals",
  turnovers: "Turnovers",
  three_pointers: "Three Pointers Made",
  free_throws: "Free Throws Made",
  fantasy: "Fantasy Points",
};

const ROWS = [
  ["points", "rebounds", "assists"],
  ["blocks", "steals", "turnovers"],
  ["three_pointers", "free_throws", "fantasy"],
];

export default async function NBAPage() {
  let data;
  try {
    data = await getAllNBAStats();
  } catch {
    return (
      <div className="min-h-screen bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-8 py-10">
          <Link href="/" className="text-sm text-gray-400 hover:text-gray-600 mb-6 inline-block">
            ← All Sports
          </Link>
          <p className="text-gray-500 text-sm">Unable to load stats right now. Try again later.</p>
        </div>
      </div>
    );
  }

  const { categories, date, days_back } = data;
  const dateLabel = days_back === 1 ? "Yesterday's Leaders" : `Leaders — ${date}`;

  const firstCategory = Object.values(categories)[0];
  const hasData = firstCategory?.leaders?.length > 0;

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-8 py-10">
        <Link href="/" className="text-sm text-gray-400 hover:text-gray-600 mb-6 inline-block">
          ← All Sports
        </Link>

        <h1 className="text-lg font-bold text-gray-900 mb-1">{dateLabel}</h1>
        <p className="text-sm text-gray-500 mb-8">{date}</p>

        {!hasData ? (
          <p className="text-gray-500 text-sm">No games found in the last 4 days.</p>
        ) : (
          <div className="space-y-8">
            {ROWS.map((row, i) => (
              <div key={i}>
                {i > 0 && <hr className="border-gray-200 mb-8" />}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-10">
                  {row.map((cat) => (
                    <StatCategory
                      key={cat}
                      title={CATEGORY_LABELS[cat]}
                      players={categories[cat]?.leaders ?? []}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
