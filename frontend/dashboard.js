// dashboard.js
// Reusable render helpers — called from dashboard.html's inline script.

/**
 * Render a list of course cards into a container element.
 * @param {HTMLElement} container
 * @param {object[]}    courses
 * @param {Function}    onStart  - callback(courseId)
 */
function renderCourseCards(container, courses, onStart) {
  if (!courses.length) {
    container.innerHTML = `<div class="empty-state">
      <div class="icon">📚</div>
      <p>No courses recommended yet. Add more skills to get suggestions.</p>
    </div>`;
    return;
  }

  container.innerHTML = courses.map(c => `
    <div class="course-card">
      <div>
        <div class="course-card-title">${c.title}</div>
        <div class="course-card-platform">📌 ${c.platform}</div>
      </div>
      <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
        <span class="badge badge-${c.level}">${c.level}</span>
        <span class="stars">${'★'.repeat(Math.round(c.rating))}${'☆'.repeat(5 - Math.round(c.rating))}</span>
        <span style="font-size:12px;color:var(--muted)">${c.rating}</span>
      </div>
      <div class="course-card-footer">
        <button class="btn btn-outline btn-sm" onclick="(${onStart.toString()})(${c.id})">
          📖 Start
        </button>
        <a href="${c.url}" target="_blank" class="btn btn-primary btn-sm">Open →</a>
      </div>
    </div>
  `).join('');
}

/**
 * Render skill gap badges into a container.
 * @param {HTMLElement} container
 * @param {string[]}    gaps
 */
function renderGapBadges(container, gaps) {
  if (!gaps.length) {
    container.innerHTML = `<div style="color:var(--success);font-weight:700;padding:12px 0">
      ✅ No gaps! You already have all required skills for your goal.</div>`;
    return;
  }
  container.innerHTML = `
    <div style="display:flex;flex-wrap:wrap;gap:8px">
      ${gaps.map(g => `<span class="badge badge-gap">❌ ${g}</span>`).join('')}
    </div>
    <p style="font-size:13px;color:var(--muted);margin-top:12px">
      Enrol in the recommended courses below to close these gaps.
    </p>`;
}

/**
 * Render an inline skills proficiency list.
 * @param {HTMLElement} container
 * @param {object[]}    skills
 */
function renderSkillsList(container, skills) {
  if (!skills.length) {
    container.innerHTML = `<div class="empty-state" style="padding:16px 0">
      <p>No skills added. <a href="skills.html">Add skills →</a></p></div>`;
    return;
  }
  container.innerHTML = skills.map(s => `
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--border)">
      <div style="flex:1;font-size:13px;font-weight:600;text-transform:capitalize">${s.skill_name}</div>
      <div style="width:80px">
        <div class="progress-bar-wrap">
          <div class="progress-bar-fill" style="width:${s.proficiency * 20}%"></div>
        </div>
      </div>
      <div style="font-size:12px;color:var(--muted);min-width:28px;text-align:right">${s.proficiency}/5</div>
    </div>
  `).join('');
}