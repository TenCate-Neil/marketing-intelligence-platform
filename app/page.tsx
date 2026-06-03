import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[#003087]">
      <div className="text-center space-y-6">
        <h1 className="text-4xl font-bold text-white tracking-tight">
          TenCate Marketing Intelligence
        </h1>
        <p className="text-blue-200 text-lg max-w-md">
          AI-powered content generation and brand analytics for TenCate Grass.
        </p>
        <Link
          href="/dashboard"
          className="inline-block bg-[#E87722] text-white px-8 py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors"
        >
          Go to Dashboard
        </Link>
      </div>
    </main>
  );
}
