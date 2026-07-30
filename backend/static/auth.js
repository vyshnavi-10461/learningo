// auth.js
// All auth logic is already inside api.js (saveSession, clearSession, requireAuth, logout).
// This file is kept for any additional auth utilities you want to add later.

// ── Password strength checker (optional UI helper) ────────────────
function checkPasswordStrength(password) {
  let score = 0;
  if (password.length >= 8)              score++;
  if (/[A-Z]/.test(password))           score++;
  if (/[0-9]/.test(password))           score++;
  if (/[^A-Za-z0-9]/.test(password))   score++;
  return ['', 'Weak', 'Fair', 'Good', 'Strong'][score] || 'Weak';
}

// ── Format career goal for display ───────────────────────────────
function formatCareerGoal(goal) {
  if (!goal) return '–';
  return goal.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}