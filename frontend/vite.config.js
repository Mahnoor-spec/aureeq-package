import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    host: '0.0.0.0', // Force IPv4 and IPv6
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8002',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ''),
      }
    }
  }
})
