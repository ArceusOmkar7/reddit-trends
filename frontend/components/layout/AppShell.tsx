"use client";

import Sidebar from "@/components/layout/Sidebar";
import TopBar from "@/components/layout/TopBar";
import { RefreshProvider } from "@/components/layout/RefreshContext";

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <RefreshProvider>
      <div className="flex min-h-screen bg-surface-offWhite">
        <Sidebar />
        <div className="flex flex-1 flex-col">
          <TopBar />
          <main className="flex-1 space-y-8 px-6 pb-10 pt-8 lg:px-10">
            {children}
          </main>
        </div>
      </div>
    </RefreshProvider>
  );
}
