// charts.js
// Reusable Chart.js helpers used across dashboard.html and progress.html

/**
 * Create or update a doughnut chart.
 * @param {string} canvasId   - id of the <canvas> element
 * @param {object} instance   - existing Chart instance (pass null on first call)
 * @param {number[]} values   - [done, inProgress, notStarted]
 * @returns Chart instance
 */
function buildDoughnutChart(canvasId, instance, values) {
  if (instance) instance.destroy();

  return new Chart(document.getElementById(canvasId), {
    type: 'doughnut',
    data: {
      labels: ['Completed', 'In Progress', 'Not Started'],
      datasets: [{
        data: values,
        backgroundColor: ['#10b981', '#f59e0b', '#e2e8f0'],
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { font: { size: 12 }, padding: 12 }
        }
      }
    }
  });
}

/**
 * Create a horizontal bar chart showing skill proficiency.
 * @param {string} canvasId
 * @param {object} instance
 * @param {object[]} skills  - [{skill_name, proficiency}]
 * @returns Chart instance
 */
function buildSkillsBar(canvasId, instance, skills) {
  if (instance) instance.destroy();

  return new Chart(document.getElementById(canvasId), {
    type: 'bar',
    data: {
      labels: skills.map(s => s.skill_name),
      datasets: [{
        label: 'Proficiency',
        data: skills.map(s => s.proficiency),
        backgroundColor: 'rgba(79,70,229,0.2)',
        borderColor: '#4f46e5',
        borderWidth: 1.5,
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      scales: {
        x: { min: 0, max: 5, ticks: { stepSize: 1 } }
      },
      plugins: { legend: { display: false } }
    }
  });
}