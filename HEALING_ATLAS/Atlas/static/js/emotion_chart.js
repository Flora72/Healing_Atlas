document.addEventListener('DOMContentLoaded', async function () {
  const response = await fetch('/test_chart/');
  const json = await response.json();

  const moodEntries = json.mood_data;
  const journalEntries = json.journal_data;

  const moodLabels = moodEntries.map(entry => entry.date);
  const moodScores = moodEntries.map(entry => entry.score);

  const journalLabels = journalEntries.map(entry => entry.date);
  const journalScores = journalEntries.map(entry => entry.score);

  const moodCtx = document.getElementById('moodChart').getContext('2d');
  const journalCtx = document.getElementById('journalChart').getContext('2d');

  const moodConfig = {
    type: 'line',
    data: {
      labels: moodLabels,
      datasets: [{
        label: 'Mood Score',
        data: moodScores,
        backgroundColor: 'rgba(33, 150, 243, 0.2)',
        borderColor: 'rgba(33, 150, 243, 1)',
        borderWidth: 2,
        pointRadius: 5,
        pointBackgroundColor: '#2196f3',
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Mood Tracker Over Time',
          font: { size: 18 },
          color: '#4a2c2a'
        }
      },
      scales: {
        x: { ticks: { color: '#4a2c2a' }, title: { display: true, text: 'Date', color: '#4a2c2a' } },
        y: { min: 0, max: 1, ticks: { color: '#4a2c2a' }, title: { display: true, text: 'Score', color: '#4a2c2a' } }
      }
    }
  };

  const journalConfig = {
    type: 'line',
    data: {
      labels: journalLabels,
      datasets: [{
        label: 'Journal Sentiment Score',
        data: journalScores,
        backgroundColor: 'rgba(156, 39, 176, 0.2)',
        borderColor: 'rgba(156, 39, 176, 1)',
        borderWidth: 2,
        pointRadius: 5,
        pointBackgroundColor: '#9c27b0',
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Journal Reflections Over Time',
          font: { size: 18 },
          color: '#4a2c2a'
        }
      },
      scales: {
        x: { ticks: { color: '#4a2c2a' }, title: { display: true, text: 'Date', color: '#4a2c2a' } },
        y: { min: 0, max: 1, ticks: { color: '#4a2c2a' }, title: { display: true, text: 'Score', color: '#4a2c2a' } }
      }
    }
  };

  new Chart(moodCtx, moodConfig);
  new Chart(journalCtx, journalConfig);
});
