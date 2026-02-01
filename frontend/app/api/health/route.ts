import { NextResponse } from "next/server";

const baseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

export async function GET() {
  try {
    const response = await fetch(`${baseUrl}/health`, { cache: "no-store" });
    const payload = (await response.json()) as { status?: string };
    return NextResponse.json({
      status: response.ok ? "ok" : "degraded",
      backend: payload.status ?? (response.ok ? "ok" : "degraded")
    });
  } catch (error) {
    return NextResponse.json(
      { status: "degraded", backend: "unreachable" },
      { status: 503 }
    );
  }
}
