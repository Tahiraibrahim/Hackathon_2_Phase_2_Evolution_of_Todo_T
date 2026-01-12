import axios from "axios";
import { authClient } from "@/lib/auth"; 

// ✅ FIX: Agar URL ke aakhir mein '/' ho to usay hata do taake double slash na aye
const getBaseUrl = () => {
  const url = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
  return url.endsWith("/") ? url.slice(0, -1) : url;
};

const API_BASE_URL = getBaseUrl();

/**
 * Axios instance configured for the Task Management API
 */
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // ✅ CRITICAL: Cookies bhejne ke liye zaroori hai
});

export type Priority = "High" | "Medium" | "Low";

export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  priority: Priority;
  category: string | null;
  due_date: string | null;
  is_recurring: boolean;
  user_id: number;
}

/**
 * ✅ Request Interceptor: JWT Token Better Auth se le kar lagayega
 */
api.interceptors.request.use(
  async (config) => {
    // 1. Better Auth se Session nikalo
    const session = await authClient.getSession();
    
    // 2. Token extract karo
    const token = (session?.data?.session as any)?.token || (session?.data as any)?.token;

    // 3. Agar token mil gaya to Header mai laga do
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor to handle 401 errors
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        console.error("⚠️ 401 Unauthorized: Token rejected by backend");
        // Optional: Redirect logic here if needed
      }
    }
    return Promise.reject(error);
  }
);

/**
 * API client methods
 */
export const taskApi = {
  getTasks: async (params?: { search?: string; priority?: Priority }): Promise<Task[]> => {
    const response = await api.get<Task[]>("/api/todos", { params });
    return response.data;
  },

  createTask: async (data: {
    title: string;
    description?: string;
    priority?: Priority;
    category?: string;
    due_date?: string;
    is_recurring?: boolean;
  }): Promise<Task> => {
    const response = await api.post<Task>("/api/todos", data);
    return response.data;
  },

  updateTask: async (
    id: number,
    data: Partial<Task>
  ): Promise<Task> => {
    const response = await api.put<Task>(`/api/todos/${id}`, data);
    return response.data;
  },

  deleteTask: async (id: number): Promise<void> => {
    await api.delete(`/api/todos/${id}`);
  },
};