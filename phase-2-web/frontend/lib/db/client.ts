import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

/**
 * Database Client for Better Auth
 * Connects to PostgreSQL using Drizzle ORM
 */

// Get the database URL from environment
const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl) {
  throw new Error("DATABASE_URL environment variable is not set");
}

// Create PostgreSQL connection with proper configuration for Neon
const client = postgres(databaseUrl, {
  ssl: "require",
  max: 10, // Limit connection pool size for serverless
});

// Initialize Drizzle ORM with the schema
export const db = drizzle(client, { schema });
