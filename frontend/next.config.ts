import type { NextConfig } from "next";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// Extract the API host for CSP connect-src
function apiHost(url: string): string {
  try {
    return new URL(url).origin;
  } catch {
    return url;
  }
}

const cspDirectives: Record<string, string[]> = {
  "default-src": ["'self'"],
  "script-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
  "style-src":   ["'self'", "'unsafe-inline'"],  // Tailwind/CSS-in-JS
  "img-src":     ["'self'", "data:", "blob:"],
  "font-src":    ["'self'", "data:"],
  "connect-src": ["'self'", apiHost(API_URL)],
  "frame-src":   ["'none'"],
  "object-src":  ["'none'"],
  "base-uri":    ["'self'"],
  "form-action": ["'self'"],
};

const csp = Object.entries(cspDirectives)
  .map(([key, values]) => `${key} ${values.join(" ")}`)
  .join("; ");

const securityHeaders = [
  { key: "Content-Security-Policy",        value: csp },
  { key: "X-Content-Type-Options",         value: "nosniff" },
  { key: "X-Frame-Options",                value: "DENY" },
  { key: "Referrer-Policy",                value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy",             value: "geolocation=(), microphone=(), camera=()" },
];

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        // Apply to all routes
        source: "/(.*)",
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;
