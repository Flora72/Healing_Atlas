fetch('/emotion-data/')
  .then(response => response.json())
  .then(data => {
    const emotionData = data.emotion_data;  // ✅ Accessing the correct key

    const moodColors = {
      hopeful: '#f7b7a3',
      positive: '#a3f7bf',
      anxious: '#f7d6a3',
      tired: '#d1d1d1',
      grateful: '#f7a3e0',
      calm: '#a3d1f7'
    };

    const ctx = document.getElementById('emotionChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: emotionData.map(d => d.date),
        datasets: [{
          label: 'Sentiment Score',
          data: emotionData.map(d => d.score),
          borderColor: '#d16ba5',
          backgroundColor: 'rgba(209,107,165,0.2)',
          fill: true,
          tension: 0.4,
          pointRadius: 6,
          pointHoverRadius: 8,
          pointBackgroundColor: emotionData.map(d => moodColors[d.sentiment] || '#d16ba5')
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
                const index = context.dataIndex;
                const sentiment = emotionData[index].sentiment;
                const note = emotionData[index].note || '';
                return `Score: ${context.formattedValue} (${sentiment})\n${note}`;
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
