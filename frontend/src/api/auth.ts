import api from "./axios";

export type LoginRequest = {
  email: string;
  password: string;
};

export type RegisterRequest = {
  username: string;
  email: string;
  password: string;
};

export type AuthUser = {
  id: number;
  username: string;
  email: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: string;
  user: AuthUser;
};

export type RegisterResponse = AuthResponse;

export const authApi = {
  login: (data: LoginRequest) => api.post<AuthResponse>("/auth/login", data),
  register: (data: RegisterRequest) =>
    api.post<RegisterResponse>("/auth/register", data),
  me: () => api.get<AuthUser>("/auth/me"),
};
