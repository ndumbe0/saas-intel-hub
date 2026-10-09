import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig(() => {
  return {
    plugins: [react(), tailwindcss()],
    server: {
      port: 5174,
      proxy: {
        '/api': 'http://localhost:8004',
      }
    },
    base: './'
  };
});
