// Home Page JavaScript

import { getUserSession, getProfile, logoutUser } from './js/auth.js';
import { navigateTo, registerServiceWorker } from './js/utils.js';
import { isAuthenticated } from './js/auth.js';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Register PWA service worker
  registerServiceWorker();

  // Check authentication
  if (!isAuthenticated()) {
    navigateTo('login.html');
    return;
  }

  // Load user data
  loadUserData();

  // Setup sidebar
  setupSidebar();

  // Setup header
  setupHeader();
});

// Load user data
function loadUserData() {
  const session = getUserSession();
  if (!session) {
    navigateTo('login.html');
    return;
  }

  const profile = getProfile(session.mst);
  const displayName = profile?.fullName || session.name || session.mst;
  const displayMst = session.mst;

  // Update profile card
  const profileName = document.getElementById('profile-name');
  const profileMst = document.getElementById('profile-mst');
  if (profileName) profileName.textContent = displayName;
  if (profileMst) profileMst.textContent = `MST: ${displayMst}`;

  // Update sidebar
  const sidebarName = document.getElementById('sidebar-name');
  const sidebarMst = document.getElementById('sidebar-mst');
  if (sidebarName) sidebarName.textContent = displayName;
  if (sidebarMst) sidebarMst.textContent = `MST: ${displayMst}`;

  // Populate sidebar menu
  populateSidebarMenu();
}

// Setup sidebar
function setupSidebar() {
  const sidebar = document.getElementById('sidebar');
  const sidebarOverlay = document.getElementById('sidebar-overlay');
  const sidebarClose = document.getElementById('sidebar-close');
  const headerMenu = document.getElementById('header-menu');
  const sidebarLogout = document.getElementById('sidebar-logout');

  // Open sidebar
  if (headerMenu) {
    headerMenu.addEventListener('click', () => {
      if (sidebar) {
        sidebar.setAttribute('aria-hidden', 'false');
        sidebar.setAttribute('aria-expanded', 'true');
        if (headerMenu) headerMenu.setAttribute('aria-expanded', 'true');
        if (sidebarOverlay) sidebarOverlay.classList.add('active');
      }
    });
  }

  // Close sidebar
  const closeSidebar = () => {
    if (sidebar) {
      sidebar.setAttribute('aria-hidden', 'true');
      sidebar.setAttribute('aria-expanded', 'false');
      if (headerMenu) headerMenu.setAttribute('aria-expanded', 'false');
      if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    }
  };

  if (sidebarClose) {
    sidebarClose.addEventListener('click', closeSidebar);
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener('click', closeSidebar);
  }

  // Logout
  if (sidebarLogout) {
    sidebarLogout.addEventListener('click', () => {
      logoutUser();
      navigateTo('login.html');
    });
  }
}

// Populate sidebar menu
function populateSidebarMenu() {
  const sidebarMenu = document.getElementById('sidebar-menu');
  if (!sidebarMenu) return;

  const menuItems = [
    { icon: 'assets/trangchu.webp', label: 'Trang chủ', href: 'home.html' },
    { icon: 'assets/index1.webp', label: 'Hoá đơn điện tử', href: 'pages/hoa-don-dien-tu.html' },
    { icon: 'assets/index2.webp', label: 'Khai thuế', href: 'pages/khai-thue.html' },
    { icon: 'assets/index3.webp', label: 'Đăng ký thuế', href: 'pages/dang-ky-thue.html' },
    { icon: 'assets/index4.webp', label: 'Hỗ trợ quyết toán thuế TNCN', href: 'pages/ho-tro-quyet-toan.html' },
    { icon: 'assets/index5.webp', label: 'Nhóm chức năng nộp thuế', href: 'pages/nhom-chuc-nang-nop-thue.html' },
    { icon: 'assets/index6.webp', label: 'Tra cứu nghĩa vụ thuế', href: 'pages/tra-cuu-nghia-vu-thue.html' },
    { icon: 'assets/index7.webp', label: 'Tra cứu thông báo', href: 'pages/thong-bao.html' },
    { icon: 'assets/index8.webp', label: 'Tiện ích', href: 'pages/tien-ich.html' },
    { icon: 'assets/index9.webp', label: 'Hỗ trợ', href: 'pages/ho-tro.html' },
    { icon: 'assets/index10.webp', label: 'Thiết lập cá nhân', href: 'pages/thiet-lap-ca-nhan.html' },
  ];

  sidebarMenu.innerHTML = menuItems.map(item => `
    <a href="${item.href}" class="sidebar-menu-item">
      <img src="${item.icon}" alt="" class="sidebar-menu-item-icon" width="24" height="24">
      <span>${item.label}</span>
    </a>
  `).join('');
}

// Setup header
function setupHeader() {
  const headerLogo = document.getElementById('header-logo');
  if (headerLogo) {
    headerLogo.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}

