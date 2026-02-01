import { render, screen, act } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { useAsyncData } from "@/lib/hooks/useAsyncData";

function TestComponent({ fetcher }: { fetcher: () => Promise<{ value: string }> }) {
  const { data, loading, error } = useAsyncData(fetcher, [], 1000);
  return (
    <div>
      <span>{loading ? "loading" : "idle"}</span>
      <span>{data?.value ?? "no-data"}</span>
      <span>{error ?? "no-error"}</span>
    </div>
  );
}

describe("useAsyncData", () => {
  it("loads data and updates state", async () => {
    const fetcher = vi.fn().mockResolvedValue({ value: "ok" });
    render(<TestComponent fetcher={fetcher} />);

    expect(screen.getByText("loading")).toBeInTheDocument();

    await act(async () => {
      await Promise.resolve();
    });

    expect(screen.getByText("idle")).toBeInTheDocument();
    expect(screen.getByText("ok")).toBeInTheDocument();
  });

  it("sets error when fetch fails", async () => {
    const fetcher = vi.fn().mockRejectedValue(new Error("boom"));
    render(<TestComponent fetcher={fetcher} />);

    await act(async () => {
      await Promise.resolve();
    });

    expect(screen.getByText("boom")).toBeInTheDocument();
  });

  it("refreshes on interval", async () => {
    vi.useFakeTimers();
    const fetcher = vi.fn().mockResolvedValue({ value: "ok" });
    render(<TestComponent fetcher={fetcher} />);

    await act(async () => {
      await Promise.resolve();
    });

    await act(async () => {
      vi.advanceTimersByTime(1000);
      await Promise.resolve();
    });

    expect(fetcher).toHaveBeenCalledTimes(2);
    vi.useRealTimers();
  });
});
