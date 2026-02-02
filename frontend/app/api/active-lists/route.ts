import { NextResponse } from "next/server";

const baseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

export async function GET() {
  try {
    const [subreddits, events] = await Promise.all([
      fetch(`${baseUrl}/meta/subreddits`, { cache: "no-store" }),
      fetch(`${baseUrl}/meta/events`, { cache: "no-store" })
    ]);
    const subredditsPayload = await subreddits.json();
    const eventsPayload = await events.json();
    return NextResponse.json({
      subreddits: subredditsPayload,
      events: eventsPayload
    });
  } catch (error) {
    return NextResponse.json(
      { subreddits: [], events: [] },
      { status: 503 }
    );
  }
}
