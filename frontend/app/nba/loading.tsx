export default function Loading() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10">
        <div className="h-4 w-20 bg-gray-100 rounded mb-6 animate-pulse" />
        <div className="h-5 w-48 bg-gray-100 rounded mb-1 animate-pulse" />
        <div className="h-4 w-24 bg-gray-100 rounded mb-8 animate-pulse" />

        {[0, 1, 2].map((row) => (
          <div key={row}>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-10 mb-8">
              {[0, 1, 2].map((col) => (
                <div key={col} className="space-y-2">
                  <div className="h-3 w-24 bg-gray-100 rounded animate-pulse mb-3" />
                  {[0, 1, 2, 3, 4].map((p) => (
                    <div key={p} className="flex justify-between">
                      <div className="h-4 w-40 bg-gray-100 rounded animate-pulse" />
                      <div className="h-4 w-6 bg-gray-100 rounded animate-pulse" />
                    </div>
                  ))}
                </div>
              ))}
            </div>
            {row < 2 && <hr className="border-gray-200 mb-8" />}
          </div>
        ))}
      </div>
    </div>
  );
}
