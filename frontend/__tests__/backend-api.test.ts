import { describe, expect, it, vi, afterEach } from "vitest";
import { fetchDashboardData } from "@/lib/api/backend";

const mockResponse = (data: unknown) =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve(data)
  }) as Promise<Response>;

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("backend API formatting", () => {
  it("localizes lastUpdated and time series labels", async () => {
    const payload = {
      lastUpdated: "2026-02-01T07:00:00Z",
      kpis: [],
      sentimentTrend: [{ time: "2026-02-01T07", value: 0.2 }],
      volumeTrend: [{ time: "2026-02-01T07", value: 12 }],
      trendingTopics: [],
      activeSubreddits: [],
      activeEvents: []
    };

    vi.stubGlobal("fetch", vi.fn(() => mockResponse(payload)));

    const data = await fetchDashboardData();

    expect(data.lastUpdated).not.toMatch(/T\d{2}/);
    expect(data.sentimentTrend[0].time).not.toMatch(/T\d{2}$/);
    expect(data.volumeTrend[0].time).not.toMatch(/T\d{2}$/);
  });
});
