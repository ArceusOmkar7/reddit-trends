import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import TopBar from "@/components/layout/TopBar";
import { RefreshProvider, useRefreshContext } from "@/components/layout/RefreshContext";
import React, { useEffect } from "react";

vi.mock("next/navigation", () => ({
  usePathname: () => "/subreddits/technology"
}));

function Wrapper({ children }: { children: React.ReactNode }) {
  return <RefreshProvider>{children}</RefreshProvider>;
}

function SetLastRefreshed({ value }: { value: string }) {
  const { setLastRefreshed } = useRefreshContext();
  useEffect(() => {
    setLastRefreshed(value);
  }, [setLastRefreshed, value]);
  return null;
}

describe("TopBar", () => {
  it("shows route context and last refreshed", () => {
    render(
      <Wrapper>
        <SetLastRefreshed value="Feb 1, 2026, 7:00 AM" />
        <TopBar />
      </Wrapper>
    );

    expect(screen.getByText(/Subreddit: r\/technology/i)).toBeInTheDocument();
    expect(screen.getByText(/Feb 1, 2026/i)).toBeInTheDocument();
  });
});
