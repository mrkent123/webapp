// Utility functions

// Debounce helper
export function debounce(fn, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Get safe area insets
export function getSafeAreaInsets() {
  if (typeof window === "undefined") {
    return { top: 0, bottom: 0, left: 0, right: 0 };
  }

  const style = getComputedStyle(document.documentElement);
  return {
    top: parseInt(style.getPropertyValue("env(safe-area-inset-top)") || "0", 10),
    bottom: parseInt(style.getPropertyValue("env(safe-area-inset-bottom)") || "0", 10),
    left: parseInt(style.getPropertyValue("env(safe-area-inset-left)") || "0", 10),
    right: parseInt(style.getPropertyValue("env(safe-area-inset-right)") || "0", 10),
  };
}

// Check if iOS
export function isIOS() {
  if (typeof window === "undefined") return false;
  return /iPad|iPhone|iPod/.test(navigator.userAgent);
}

// Check if PWA standalone mode
export function isStandalone() {
  if (typeof window === "undefined") return false;
  return (
    window.navigator.standalone ||
    window.matchMedia("(display-mode: standalone)").matches
  );
}

// Set viewport height dynamically (fix iOS viewport issues)
export function setViewportHeight() {
  if (typeof window === "undefined") return;

  const setHeight = () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty("--vh", `${vh}px`);
  };

  setHeight();
  window.addEventListener("resize", setHeight);
  window.addEventListener("orientationchange", setHeight);
}

// Format MST (add spaces)
export function formatMST(mst) {
  if (!mst) return "";
  return mst.replace(/(\d{3})(\d{3})(\d{3})(\d+)/, "$1 $2 $3 $4");
}

// Validate MST format
export function validateMST(mst) {
  if (!mst) return false;
  const cleaned = mst.replace(/\s/g, "");
  return /^\d{10,13}$/.test(cleaned);
}

// Show error message
export function showError(element, message) {
  if (!element) return;
  element.textContent = message;
  element.style.display = "block";
}

// Hide error message
export function hideError(element) {
  if (!element) return;
  element.textContent = "";
  element.style.display = "none";
}

// Navigate to page
export function navigateTo(url) {
  if (typeof window !== "undefined") {
    window.location.href = url;
  }
}

// Redirect if not authenticated (async version)
export async function requireAuth(redirectTo = "login.html") {
  const { isAuthenticated } = await import('./auth.js');
  if (!isAuthenticated()) {
    navigateTo(redirectTo);
    return false;
  }
  return true;
}

// Register service worker for PWA
export async function registerServiceWorker() {
  if (typeof window === "undefined") return;

  if ("serviceWorker" in navigator) {
    try {
      await navigator.serviceWorker.register("./service-worker.js");
      // Optional: log for debugging, will be ignored by users
      console.log("Service worker registered");
    } catch (error) {
      console.warn("Service worker registration failed", error);
    }
  }
}


