import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  authApi,
  type AuthUser,
  type LoginRequest,
  type RegisterRequest,
} from "../api/auth";

interface User extends AuthUser {}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const clearSession = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }, []);

  const persistSession = useCallback((nextToken: string, nextUser: User) => {
    setToken(nextToken);
    setUser(nextUser);
    localStorage.setItem("token", nextToken);
    localStorage.setItem("user", JSON.stringify(nextUser));
  }, []);

  useEffect(() => {
    const restoreSession = async () => {
      const savedToken = localStorage.getItem("token");
      if (!savedToken) {
        setIsLoading(false);
        return;
      }

      setToken(savedToken);

      const savedUser = localStorage.getItem("user");
      if (savedUser) {
        setUser(JSON.parse(savedUser));
      }

      try {
        const response = await authApi.me();
        setUser(response.data);
        localStorage.setItem("user", JSON.stringify(response.data));
      } catch {
        clearSession();
      } finally {
        setIsLoading(false);
      }
    };

    void restoreSession();
  }, [clearSession]);

  const login = useCallback(
    async (data: LoginRequest) => {
      const response = await authApi.login(data);
      persistSession(response.data.access_token, response.data.user);
    },
    [persistSession]
  );

  const register = useCallback(
    async (data: RegisterRequest) => {
      const response = await authApi.register(data);
      persistSession(response.data.access_token, response.data.user);
    },
    [persistSession]
  );

  const logout = useCallback(() => {
    clearSession();
  }, [clearSession]);

  const ctx = useMemo(
    () => ({
      user,
      token,
      isAuthenticated: !!token,
      isLoading,
      login,
      register,
      logout,
    }),
    [user, token, isLoading, login, register, logout]
  );

  return <AuthContext.Provider value={ctx}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
