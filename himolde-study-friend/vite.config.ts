import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true, // Optional: if you want to use global APIs like `test`, `expect`
    setupFiles: './src/setupTests.ts', // Optional: for global test setup
  },
})
