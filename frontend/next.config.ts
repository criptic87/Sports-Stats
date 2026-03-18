import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone", // Required for Docker — produces a self-contained build
  async rewrites() {
    // Proxy /api/* requests to the backend.
    // In Docker: "backend:8000" resolves via Docker DNS.
    // Locally: falls back to localhost:8000.
    const backendUrl =
      process.env.BACKEND_URL ?? "http://localhost:8000";
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
