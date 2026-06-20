"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LayoutDashboard, Leaf, LogOut, Sparkles, Store, TrendingUp } from "lucide-react";
import { useAuth } from "@/lib/auth-context";
import clsx from "clsx";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/insights", label: "Insights", icon: Sparkles },
  { href: "/marketplace", label: "Marketplace", icon: Store },
  { href: "/progress", label: "Progress", icon: TrendingUp },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-40 border-b border-glass-border bg-obsidian/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
          <Link href="/dashboard" className="flex items-center gap-2 font-display text-base font-semibold text-mist">
            <Leaf className="h-5 w-5 text-signal" aria-hidden="true" />
            EarthShare
          </Link>

          <nav aria-label="Primary" className="flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const active = pathname === item.href;
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  aria-current={active ? "page" : undefined}
                  className={clsx(
                    "flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                    active ? "bg-signal/15 text-signal" : "text-mist-dim hover:bg-white/5 hover:text-mist"
                  )}
                >
                  <Icon className="h-4 w-4" aria-hidden="true" />
                  <span className="hidden sm:inline">{item.label}</span>
                </Link>
              );
            })}
          </nav>

          <div className="flex items-center gap-3">
            {user && <span className="hidden text-sm text-mist-dim md:inline">{user.full_name}</span>}
            <button
              onClick={() => {
                logout();
                router.push("/login");
              }}
              aria-label="Log out"
              className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-mist-dim hover:bg-white/5 hover:text-mist"
            >
              <LogOut className="h-4 w-4" aria-hidden="true" />
              <span className="hidden sm:inline">Log out</span>
            </button>
          </div>
        </div>
      </header>

      <main id="main-content" className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
        {children}
      </main>
    </div>
  );
}
