// Firebase Configuration
// Note: Replace these with your actual Firebase config values
// You can get these from Firebase Console > Project Settings > General > Your apps

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase (if using Firebase SDK)
// For now, we'll use a simple localStorage-based auth
// Uncomment below if you want to use Firebase Auth SDK:
/*
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { app, auth };
*/

// For HTML version, we'll use localStorage-based auth (simpler)
// This matches the data-store.ts logic from the Next.js version

