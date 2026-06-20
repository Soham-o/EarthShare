import type { Metadata, Viewport } from "next";
import "@fontsource/space-grotesk/500.css";
import "@fontsource/space-grotesk/600.css";
import "@fontsource/space-grotesk/700.css";
import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import "@fontsource/jetbrains-mono/500.css";
import "@fontsource/jetbrains-mono/600.css";
import "./globals.css";
import { AuthProvider } from "@/lib/auth-context";

export const metadata: Metadata = {
  title: "EarthShare — Own a share of the planet",
  description:
    "Track, understand, and reduce your carbon footprint. EarthShare turns daily actions into a personal stake in a healthier planet.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  // Explicitly NOT capping maximumScale or disabling user-scalable — doing
  // so breaks pinch-zoom / text scaling for low-vision users.
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">
        <a
          href="#main-content"
          className="sr-only-focusable fixed top-2 left-2 z-50 rounded bg-signal px-4 py-2 font-semibold text-obsidian"
        >
          Skip to main content
        </a>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
