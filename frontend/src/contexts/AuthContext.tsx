import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
  useMemo,
} from "react";
import { authApi, type LoginRequest, type RegisterRequest } from "../api/auth";

interface User {
  id: number;
  username: string;
  email: string;
}

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

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (data: LoginRequest) => {
    const response = await authApi.login(data);
    const userData = {
      id: response.data.user_id,
      username: response.data.username,
      email: response.data.email,
    };
    const sessionToken = `temp-session-${response.data.user_id}`;
    setToken(sessionToken);
    setUser(userData);
    localStorage.setItem("token", sessionToken);
    localStorage.setItem("user", JSON.stringify(userData));
  }, []);

  const register = useCallback(async (data: RegisterRequest) => {
    const response = await authApi.register(data);
    const userData = {
      id: response.data.id,
      username: response.data.username,
      email: response.data.email,
    };
    const sessionToken = `temp-session-${response.data.id}`;
    setToken(sessionToken);
    setUser(userData);
    localStorage.setItem("token", sessionToken);
    localStorage.setItem("user", JSON.stringify(userData));
  }, []);

  const logout = useCallback(() => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }, []);

  const ctx = useMemo(() => ({
    user,
    token,
    isAuthenticated: !!token,
    isLoading,
    login,
    register,
    logout,
  }), [user, token, isLoading, login, register, logout])

  return (
    <AuthContext.Provider
      value={ctx}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
