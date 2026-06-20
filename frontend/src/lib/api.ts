const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

interface RequestOptions {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: unknown;
  token?: string | null;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (options.token) headers["Authorization"] = `Bearer ${options.token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method: options.method ?? "GET",
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (!res.ok) {
    let detail = `Request failed with status ${res.status}`;
    try {
      const data = await res.json();
      if (typeof data?.detail === "string") detail = data.detail;
      else if (Array.isArray(data?.detail)) {
        detail = data.detail.map((d: { msg?: string }) => d.msg).join("; ");
      }
    } catch {
      // response body wasn't JSON — keep the generic message
    }
    throw new ApiError(detail, res.status);
  }

  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export const api = {
  register: (email: string, full_name: string, password: string) =>
    request<{ access_token: string }>("/api/v1/auth/register", {
      method: "POST",
      body: { email, full_name, password },
    }),

  login: (email: string, password: string) =>
    request<{ access_token: string }>("/api/v1/auth/login", {
      method: "POST",
      body: { email, password },
    }),

  me: (token: string) => request<import("./types").UserPublic>("/api/v1/auth/me", { token }),

  submitOnboarding: (token: string, payload: import("./types").OnboardingInput) =>
    request<import("./types").FootprintSnapshot>("/api/v1/onboarding", { method: "POST", body: payload, token }),

  getProfile: (token: string) => request<import("./types").OnboardingInput>("/api/v1/onboarding/profile", { token }),

  getDashboard: (token: string) => request<import("./types").DashboardResponse>("/api/v1/dashboard", { token }),

  getInsights: (token: string) => request<import("./types").InsightsResponse>("/api/v1/insights", { token }),

  getActions: (token: string) => request<import("./types").ActionCardResponse[]>("/api/v1/actions", { token }),

  completeAction: (token: string, action_id: string) =>
    request<{ status: string }>("/api/v1/actions/complete", { method: "POST", body: { action_id }, token }),

  getProgress: (token: string) => request<import("./types").ProgressResponse>("/api/v1/progress", { token }),

  /** POST is idempotent — safe to call every time the user visits.
   *  Returns the existing record if already checked in today, or creates a new one. */
  dailyCheckin: (token: string) =>
    request<import("./types").FootprintSnapshot>("/api/v1/checkin", { method: "POST", token }),

  /** Returns the existing today's check-in (200) or undefined (204 → null). */
  getTodaysCheckin: (token: string) =>
    request<import("./types").FootprintSnapshot | undefined>("/api/v1/checkin", { token }),
};
