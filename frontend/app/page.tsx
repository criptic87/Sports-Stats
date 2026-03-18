import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 flex flex-col items-center justify-center">
      <div className="text-center px-4">
        <h1 className="text-6xl font-black text-white mb-3 tracking-tight">
          Top Performers
        </h1>
        <p className="text-gray-400 text-lg mb-14">
          Daily leaders across your favourite sports
        </p>

        <div className="flex flex-col gap-4 items-center">
          <Link
            href="/nba"
            className="w-64 bg-[#C9082A] hover:bg-[#a5071f] text-white font-bold text-base px-8 py-4 rounded-lg transition-colors uppercase tracking-widest"
          >
            NBA
          </Link>

          <button
            disabled
            className="w-64 bg-gray-800 text-gray-600 font-bold text-base px-8 py-4 rounded-lg uppercase tracking-widest cursor-not-allowed"
          >
            NFL — Soon
          </button>

          <button
            disabled
            className="w-64 bg-gray-800 text-gray-600 font-bold text-base px-8 py-4 rounded-lg uppercase tracking-widest cursor-not-allowed"
          >
            Football — Soon
          </button>
        </div>
      </div>
    </main>
  );
}
