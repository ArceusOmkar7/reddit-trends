import { NextResponse } from "next/server";

const baseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const response = await fetch(`${baseUrl}/meta/ingestion`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      cache: "no-store"
    });
    const payload = await response.json();
    return NextResponse.json(payload, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      { enabled: false, intervalSeconds: 300, lastRun: null, nextRun: null },
      { status: 503 }
    );
  }
}
