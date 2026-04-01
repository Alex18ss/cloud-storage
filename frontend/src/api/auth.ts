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

export type LoginResponse = {
  message: string;
  user_id: number;
  email: string;
  username: string;
};

export type RegisterResponse = AuthUser & {
  is_active: boolean;
  created_at: string;
};

export const authApi = {
  login: (data: LoginRequest) =>
    api.post<LoginResponse>("/auth/login", data),

  register: (data: RegisterRequest) =>
    api.post<RegisterResponse>("/auth/register", data),
};
