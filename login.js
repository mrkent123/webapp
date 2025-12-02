// Login Page JavaScript - HMR Test Change

import { loginUserByMst, getUserSession } from './js/auth.js';
import {
  navigateTo,
  showError,
  hideError,
  setViewportHeight,
  getSafeAreaInsets,
  registerServiceWorker,
} from './js/utils.js';

// Export functions for use in script tag (if not using modules)
if (typeof window !== 'undefined') {
  window.loginUserByMst = loginUserByMst;
  window.getUserSession = getUserSession;
  window.navigateTo = navigateTo;
  window.showError = showError;
  window.hideError = hideError;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Register PWA service worker
  registerServiceWorker();

  // Set viewport height
  setViewportHeight();

  // Check if already logged in
  const session = getUserSession();
  if (session) {
    navigateTo('home.html');
    return;
  }

  // Setup form
  setupLoginForm();
  setupPasswordToggle();
  setupViewportHeight();
  setupBadgeClose();
});

// Setup login form
function setupLoginForm() {
  const form = document.getElementById('login-form');
  const mstInput = document.getElementById('mst-input');
  const passwordInput = document.getElementById('password-input');
  const mstError = document.getElementById('mst-error');
  const errorMessage = document.getElementById('error-message');
  const loginButton = document.getElementById('login-button');

  // Clear errors on input
  mstInput.addEventListener('input', () => {
    hideError(mstError);
    hideError(errorMessage);
  });

  passwordInput.addEventListener('input', () => {
    hideError(errorMessage);
  });

  // Handle form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const mst = mstInput.value.trim();
    const password = passwordInput.value.trim();

    // Clear previous errors
    hideError(mstError);
    hideError(errorMessage);

    // Validate
    if (!mst) {
      showError(mstError, 'Vui lòng nhập tài khoản');
      return;
    }

    if (!password) {
      showError(errorMessage, 'Vui lòng nhập mật khẩu');
      return;
    }

    // Disable button
    loginButton.disabled = true;
    loginButton.textContent = 'Đang đăng nhập...';

    try {
      const result = await loginUserByMst(mst, password);
      
      if (result) {
        // Success - redirect to home
        navigateTo('home.html');
      } else {
        // Failed
        showError(errorMessage, 'Sai MST hoặc mật khẩu');
        loginButton.disabled = false;
        loginButton.textContent = 'Đăng nhập';
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Đăng nhập thất bại';
      showError(errorMessage, message);
      loginButton.disabled = false;
      loginButton.textContent = 'Đăng nhập';
    }
  });
}

// Setup password toggle
function setupPasswordToggle() {
  const passwordInput = document.getElementById('password-input');
  const passwordToggle = document.getElementById('password-toggle');
  const eyeIcon = passwordToggle.querySelector('.eye-icon');
  let isEyeOpen = true;

  passwordToggle.addEventListener('click', () => {
    const isPassword = passwordInput.type === 'password';
    passwordInput.type = isPassword ? 'text' : 'password';
    
    // Toggle eye icon
    if (isEyeOpen) {
      eyeIcon.src = 'assets/icon-eye-closed.svg';
      passwordToggle.setAttribute('aria-label', 'Hiện mật khẩu');
    } else {
      eyeIcon.src = 'assets/icon-eye.svg';
      passwordToggle.setAttribute('aria-label', 'Ẩn mật khẩu');
    }
    
    isEyeOpen = !isEyeOpen;
  });
}

// Setup badge close
function setupBadgeClose() {
  const badgeClose = document.querySelector('.badge-close');
  const builtWithBadge = document.querySelector('.built-with-badge');
  
  if (badgeClose && builtWithBadge) {
    badgeClose.addEventListener('click', () => {
      builtWithBadge.style.display = 'none';
    });
  }
}

// Setup viewport height (fix iOS issues)
function setupViewportHeight() {
  const wrapper = document.getElementById('login-wrapper');
  const bottomNav = document.getElementById('bottom-nav');

  const updateHeight = () => {
    if (wrapper) {
      const height = window.innerHeight;
      wrapper.style.height = `${height}px`;
    }

    // Handle bottom nav safe area
    if (bottomNav) {
      const safeArea = getSafeAreaInsets();
      if (safeArea.bottom > 0) {
        bottomNav.style.bottom = `-${safeArea.bottom}px`;
      } else {
        bottomNav.style.bottom = '0px';
      }
    }
  };

  updateHeight();
  window.addEventListener('resize', updateHeight);
  window.addEventListener('orientationchange', updateHeight);
}

