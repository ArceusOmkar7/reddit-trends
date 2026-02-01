import { describe, expect, it } from "vitest";
import { formatLocalDateTime, formatLocalTime } from "@/lib/format";

const isIsoLike = (value: string) => /\d{4}-\d{2}-\d{2}T/.test(value);

describe("format helpers", () => {
  it("formats hour-bucket timestamps into local time", () => {
    const formatted = formatLocalTime("2026-02-01T07");
    expect(isIsoLike(formatted)).toBe(false);
    expect(formatted.length).toBeGreaterThan(0);
  });

  it("formats ISO timestamps into localized date time", () => {
    const formatted = formatLocalDateTime("2026-02-01T07:15:00Z");
    expect(isIsoLike(formatted)).toBe(false);
    expect(formatted.length).toBeGreaterThan(0);
  });

  it("returns original value for invalid dates", () => {
    expect(formatLocalTime("not-a-date")).toBe("not-a-date");
    expect(formatLocalDateTime("nope")).toBe("nope");
  });
});
