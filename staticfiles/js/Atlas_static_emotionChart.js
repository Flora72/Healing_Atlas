document.addEventListener('DOMContentLoaded', function () {
  const rawData = document.getElementById('emotion-data').dataset.emotions;
  const emotionEntries = JSON.parse(rawData);

  const labels = emotionEntries.map(entry => entry.date);
  const scores = emotionEntries.map(entry => entry.score);

  const ctx = document.getElementById('emotionChart').getContext('2d');

  const emotionData = {
    labels: labels,
    datasets: [{
      label: 'Emotional Score',
      data: scores,
      backgroundColor: 'rgba(124, 77, 255, 0.2)',
      borderColor: 'rgba(124, 77, 255, 1)',
      borderWidth: 2,
      pointRadius: 5,
      pointBackgroundColor: '#7c4dff',
      tension: 0.3
    }]
  };

  const config = {
    type: 'line',
    data: emotionData,
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Emotional Landscape Over Time',
          font: {
            size: 18
          },
          color: '#4a2c2a'
        },
        legend: {
          labels: {
            color: '#4a2c2a'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: '#4a2c2a'
          },
          title: {
            display: true,
            text: 'Date',
            color: '#4a2c2a'
          }
        },
        y: {
          min: 0,
          max: 1,
          ticks: {
            color: '#4a2c2a'
          },
          title: {
            display: true,
            text: 'Emotion Score',
            color: '#4a2c2a'
          }
        }
      }
    }
  };

  new Chart(ctx, config);
});
