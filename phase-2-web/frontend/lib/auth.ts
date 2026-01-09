import { createAuthClient } from "better-auth/react";

/**
 * Better Auth Client (Frontend)
 * Use this on the frontend to interact with Better Auth API
 * Points to the local Next.js API route, NOT the Python backend
 */
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  fetchOptions: {
    credentials: "include" // Include cookies for session management
  }
});

/**
 * Get current session data
 * Returns user info and session data from Better Auth
 */
export async function getSession() {
  try {
    const session = await authClient.getSession();
    return session;
  } catch (error) {
    console.error("Failed to get session:", error);
    return null;
  }
}
