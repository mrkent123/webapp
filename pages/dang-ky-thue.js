import { requireAuth } from '../js/utils.js';

document.addEventListener('DOMContentLoaded', async () => {
  await requireAuth('../login.html');
  // Các nút hiện chỉ là UI, sau này có thể gắn navigateTo(...) nếu cần
});
