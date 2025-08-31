document.addEventListener("DOMContentLoaded", function () {
  const emotionData = window.emotionData;
  if (!emotionData || emotionData.length === 0) {
    console.warn("No emotional data to display.");
    return;
  }

  const moodColors = {
    hopeful: '#f7b7a3',
    positive: '#a3f7bf',
    anxious: '#f7d6a3',
    tired: '#d1d1d1',
    grateful: '#f7a3e0',
    calm: '#a3d1f7'
  };

  const labels = emotionData.map(entry => entry.date);
  const scores = emotionData.map(entry => entry.score);
  const pointColors = emotionData.map(entry => moodColors[entry.sentiment] || '#d16ba5');

  const ctx = document.getElementById('emotionChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Sentiment Score',
        data: scores,
        borderColor: '#d16ba5',
        backgroundColor: 'rgba(209,107,165,0.2)',
        fill: true,
        tension: 0.4,
        pointRadius: 6,
        pointHoverRadius: 8,
        pointBackgroundColor: pointColors
      }]
    },
    options: {
      responsive: true,
      animation: {
        duration: 1200,
        easing: 'easeOutQuart'
      },
      plugins: {
        title: {
          display: true,
          text: 'Emotional Landscape',
          font: {
            size: 18,
            weight: 'bold'
          },
          color: '#c04e90'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const entry = emotionData[context.dataIndex];
              return `Score: ${context.formattedValue} (${entry.sentiment})\n${entry.note || ''}`;
            }
          }
        },
        legend: {
          display: true,
          labels: {
            color: '#4a2c2a'
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Date',
            color: '#4a2c2a'
          },
          ticks: {
            color: '#4a2c2a'
          }
        },
        y: {
          beginAtZero: true,
          max: 1,
          title: {
            display: true,
            text: 'Sentiment Score',
            color: '#4a2c2a'
          },
          ticks: {
            color: '#4a2c2a'
          }
        }
      }
    }
  });
});
