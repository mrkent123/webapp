const fs = require('fs').promises;
const path = require('path');

async function buildPWA(outputDir) {
  try {
    // Create output directory if it doesn't exist
    await fs.mkdir(outputDir, { recursive: true });
    
    // Generate manifest.json
    const manifestContent = generateManifest();
    const manifestPath = path.join(outputDir, 'manifest.json');
    await fs.writeFile(manifestPath, manifestContent);
    
    // Generate service-worker.js
    const swContent = generateServiceWorker();
    const swPath = path.join(outputDir, 'service-worker.js');
    await fs.writeFile(swPath, swContent);
    
    // Create placeholder icons directory and sample icons
    const iconsDir = path.join(outputDir, 'icons');
    await fs.mkdir(iconsDir, { recursive: true });
    
    console.log(`PWA assets generated successfully in ${outputDir}`);
    return { 
      manifestPath, 
      swPath,
      iconsDir
    };
  } catch (error) {
    console.error('Error building PWA:', error);
    throw error;
  }
}

function generateManifest() {
  return JSON.stringify({
    "name": "Web Builder App",
    "short_name": "WB App",
    "description": "A web application built with the Web Builder",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#3b82f6",
    "orientation": "any",
    "icons": [
      {
        "src": "icons/icon-72x72.png",
        "sizes": "72x72",
        "type": "image/png"
      },
      {
        "src": "icons/icon-96x96.png",
        "sizes": "96x96",
        "type": "image/png"
      },
      {
        "src": "icons/icon-128x128.png",
        "sizes": "128x128",
        "type": "image/png"
      },
      {
        "src": "icons/icon-144x144.png",
        "sizes": "144x144",
        "type": "image/png"
      },
      {
        "src": "icons/icon-152x152.png",
        "sizes": "152x152",
        "type": "image/png"
      },
      {
        "src": "icons/icon-192x192.png",
        "sizes": "192x192",
        "type": "image/png"
      },
      {
        "src": "icons/icon-384x384.png",
        "sizes": "384x384",
        "type": "image/png"
      },
      {
        "src": "icons/icon-512x512.png",
        "sizes": "512x512",
        "type": "image/png"
      }
    ]
  }, null, 2);
}

function generateServiceWorker() {
  return `// Service Worker for Web Builder PWA
const CACHE_NAME = 'web-builder-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/styles.css',
  '/manifest.json'
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Return cached version if available, otherwise fetch from network
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});

self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
`;
}

module.exports = { buildPWA };