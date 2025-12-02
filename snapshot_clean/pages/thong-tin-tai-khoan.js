import { requireAuth } from '../js/utils.js';
import { getUserSession, getProfile } from '../js/auth.js';

document.addEventListener('DOMContentLoaded', async () => {
  const ok = await requireAuth('../login.html');
  if (!ok) return;

  const session = getUserSession();
  const profile = session ? getProfile(session.mst) : null;

  const mstEl = document.getElementById('account-mst');
  const nameEl = document.getElementById('account-fullname');
  const addressEl = document.getElementById('account-address');
  const officeEl = document.getElementById('account-tax-office');
  const phoneEl = document.getElementById('account-phone');
  const emailEl = document.getElementById('account-email');

  if (mstEl && session?.mst) mstEl.textContent = session.mst;
  if (nameEl && profile?.fullName) nameEl.textContent = profile.fullName.toLowerCase();
  if (addressEl && profile?.address) addressEl.textContent = profile.address;
  if (phoneEl && profile?.phone) phoneEl.textContent = profile.phone;
  if (emailEl && profile?.email) emailEl.textContent = profile.email;

  // Tên CQT quản lý hiện chưa có trong dữ liệu -> giữ placeholder
});
