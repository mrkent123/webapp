import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';
import basicSsl from '@vitejs/plugin-basic-ssl';

export default defineConfig({
  plugins: [
    basicSsl(), // Enable HTTPS
    VitePWA({
      strategies: 'generateSW',
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,webp,webmanifest}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'google-fonts-cache',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 365 // <== 1 year
              },
              cacheableResponse: {
                statuses: [0, 200]
              }
            }
          }
        ]
      },
      manifest: {
        name: 'eTax Mobile',
        short_name: 'eTax Mobile',
        description: 'Tra cứu thuế điện tử - Cổng thông tin thuế điện tử',
        theme_color: '#C60000',
        background_color: '#ffffff',
        display: 'fullscreen',
        orientation: 'portrait',
        scope: '/',
        start_url: '/login.html',
        icons: [
          {
            src: 'assets/logo-192.webp',
            sizes: '192x192',
            type: 'image/webp',
            purpose: 'any'
          },
          {
            src: 'assets/logo.webp',
            sizes: '512x512',
            type: 'image/webp',
            purpose: 'any'
          }
        ]
      }
    })
  ],
  server: {
    port: 5173,
    host: true, // Allow external connections (LAN access)
    https: true // Enable HTTPS
  },
  build: {
    outDir: 'dist'
  }
});