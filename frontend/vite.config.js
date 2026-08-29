import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools()
  ],

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },

  server: {
    proxy: {
      '/login': 'http://localhost:5001',
      '/signup': 'http://localhost:5001',
      '/admin': 'http://localhost:5001',
      '/auth': 'http://localhost:5001',
      '/user': 'http://localhost:5001'
    }
  }
})