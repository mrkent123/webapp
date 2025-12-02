// Khai Thuế Page JavaScript

import { requireAuth } from '../js/utils.js';

document.addEventListener('DOMContentLoaded', async () => {
  await requireAuth('../login.html');
});

