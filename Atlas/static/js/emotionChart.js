document.addEventListener("DOMContentLoaded", function () {
  if (!emotionData || emotionData.length === 0) return;

  const ctx = document.getElementById("emotionChart").getContext("2d");

  const labels = emotionData.map(item => item.date);
  const scores = emotionData.map(item => item.score);

  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Emotional Score",
        data: scores,
        borderColor: "#6A5ACD",
        backgroundColor: "rgba(106, 90, 205, 0.2)",
        fill: true,
        tension: 0.3,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Emotional Resonance Over Time",
          font: {
            size: 18
          }
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const sentiment = emotionData[context.dataIndex].sentiment;
              return `Score: ${context.raw} (${sentiment})`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 1
        }
      }
    }
  });
});
