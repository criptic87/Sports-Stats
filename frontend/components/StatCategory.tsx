import { LeaderEntry } from "@/lib/api";

interface Props {
  title: string;
  players: LeaderEntry[];
}

export default function StatCategory({ title, players }: Props) {
  if (players.length === 0) {
    return (
      <div>
        <h3 className="text-xs font-bold uppercase tracking-wider text-gray-900 mb-3">
          {title}
        </h3>
        <p className="text-xs text-gray-400">No data</p>
      </div>
    );
  }

  return (
    <div className="min-w-0">
      <h3 className="text-xs font-bold uppercase tracking-wider text-gray-900 mb-3">
        {title}
      </h3>

      <div className="space-y-[6px]">
        {players.map((player) => {
          const isTop = player.rank === 1;
          const statValue = Object.values(player.stats)[0] ?? 0;
          const displayValue = Number.isInteger(statValue)
            ? String(statValue)
            : statValue.toFixed(1);

          return (
            <div
              key={`${player.player}-${player.team}`}
              className="flex items-baseline justify-between gap-2"
            >
              <div className="flex items-baseline gap-1 min-w-0">
                <span className="text-sm text-gray-400 shrink-0 w-4 text-right">
                  {player.rank}.
                </span>
                <span
                  className={`text-sm leading-snug truncate ${
                    isTop ? "font-bold text-gray-900" : "text-gray-800"
                  }`}
                  title={player.player}
                >
                  {player.player}
                </span>
                <span className="text-[11px] text-gray-400 shrink-0 uppercase">
                  {player.team}
                </span>
              </div>

              <span
                className={`text-sm tabular-nums shrink-0 ${
                  isTop ? "font-bold text-gray-900" : "text-gray-800"
                }`}
              >
                {displayValue}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
