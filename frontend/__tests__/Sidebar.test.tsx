import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import Sidebar from "@/components/layout/Sidebar";

vi.mock("next/navigation", () => ({
  usePathname: () => "/sentiment"
}));

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  )
}));

describe("Sidebar", () => {
  it("renders nav items and marks active route", () => {
    render(<Sidebar />);
    expect(screen.getByText("Sentiment")).toBeInTheDocument();
    expect(screen.getByText("Dashboard")).toBeInTheDocument();
  });
});
