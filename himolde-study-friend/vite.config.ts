import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path"; // Import 'path' module

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"), // Configure alias for TypeScript paths
    },
  },
  test: {
    environment: "jsdom",
    globals: true, // Optional: if you want to use global APIs like `test`, `expect`
    setupFiles: "./src/setupTests.ts", // Optional: for global test setup
  },
});
