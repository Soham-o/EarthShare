"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { UserPublic } from "@/lib/types";

const TOKEN_KEY = "earthshare_token";

interface AuthContextValue {
  token: string | null;
  user: UserPublic | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, fullName: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<UserPublic | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadUser = useCallback(async (t: string) => {
    try {
      const u = await api.me(t);
      setUser(u);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        window.localStorage.removeItem(TOKEN_KEY);
        setToken(null);
        setUser(null);
      }
    }
  }, []);

  useEffect(() => {
    const stored = window.localStorage.getItem(TOKEN_KEY);
    if (stored) {
      setToken(stored);
      loadUser(stored).finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, [loadUser]);

  const login = useCallback(
    async (email: string, password: string) => {
      const { access_token } = await api.login(email, password);
      window.localStorage.setItem(TOKEN_KEY, access_token);
      setToken(access_token);
      await loadUser(access_token);
    },
    [loadUser]
  );

  const register = useCallback(
    async (email: string, fullName: string, password: string) => {
      const { access_token } = await api.register(email, fullName, password);
      window.localStorage.setItem(TOKEN_KEY, access_token);
      setToken(access_token);
      await loadUser(access_token);
    },
    [loadUser]
  );

  const logout = useCallback(() => {
    window.localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  }, []);

  const refreshUser = useCallback(async () => {
    if (token) await loadUser(token);
  }, [token, loadUser]);

  return (
    <AuthContext.Provider value={{ token, user, isLoading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
