// ── Central API helper ────────────────────────────────────────────
const BASE_URL = 'http://localhost:5000/api';

function getToken()  { return localStorage.getItem('slam_token'); }
function getUserId() { return localStorage.getItem('slam_user_id'); }
function getUserName(){ return localStorage.getItem('slam_user_name'); }

async function apiCall(endpoint, method = 'GET', body = null) {
  const headers = { 'Content-Type': 'application/json' };
  const token   = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const opts = { method, headers };
  if (body) opts.body = JSON.stringify(body);

  const res  = await fetch(`${BASE_URL}${endpoint}`, opts);
  const data = await res.json();

  if (!res.ok) throw new Error(data.error || 'Request failed');
  return data;
}

// ── Auth ──────────────────────────────────────────────────────────
async function apiRegister(name, email, password, careerGoal, interests) {
  return apiCall('/register', 'POST', { name, email, password, career_goal: careerGoal, interests });
}

async function apiLogin(email, password) {
  return apiCall('/login', 'POST', { email, password });
}

// ── Skills ────────────────────────────────────────────────────────
async function apiSaveSkills(skills, careerGoal) {
  return apiCall('/skills', 'POST', { user_id: getUserId(), skills, career_goal: careerGoal });
}

async function apiGetSkills() {
  return apiCall(`/skills/${getUserId()}`);
}

// ── Recommend ─────────────────────────────────────────────────────
async function apiRecommend() {
  return apiCall('/recommend', 'POST', { user_id: getUserId() });
}

// ── Progress ──────────────────────────────────────────────────────
async function apiGetProgress() {
  return apiCall(`/progress/${getUserId()}`);
}

async function apiUpdateProgress(courseId, status, pct = 0) {
  return apiCall('/progress/update', 'PUT', {
    user_id: getUserId(), course_id: courseId, status, completion_pct: pct
  });
}

// ── Dashboard ─────────────────────────────────────────────────────
async function apiDashboard() {
  return apiCall(`/dashboard/${getUserId()}`);
}

// ── Session helpers ───────────────────────────────────────────────
function saveSession(token, user) {
  localStorage.setItem('slam_token',     token);
  localStorage.setItem('slam_user_id',   user.id);
  localStorage.setItem('slam_user_name', user.name);
  localStorage.setItem('slam_user',      JSON.stringify(user));
}

function clearSession() {
  ['slam_token','slam_user_id','slam_user_name','slam_user'].forEach(k => localStorage.removeItem(k));
}

function requireAuth() {
  if (!getToken() || !getUserId()) {
    window.location.href = 'index.html';
    return false;
  }
  return true;
}

function showNavUser() {
  const el = document.getElementById('nav-user');
  if (el) el.textContent = getUserName() || 'User';
}

function logout() {
  clearSession();
  window.location.href = 'index.html';
}