document.addEventListener("DOMContentLoaded", function () {
  if (!emotionData || emotionData.length === 0) return;

  const ctx = document.getElementById("emotionChart").getContext("2d");

  const labels = emotionData.map(item => item.date);
  const scores = emotionData.map(item => item.score);
  const sentiments = emotionData.map(item => item.sentiment);
  const colors = scores.map(score => {
    if (score > 0.6) return "#a3f7bf";
    if (score > 0.3) return "#fdfd96";
    return "#ffb3ba";
  });

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: "Emotional Motion Score",
        data: scores,
        backgroundColor: colors,
        borderColor: "#333",
        borderWidth: 2,
        fill: false,
        tension: 0.3
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true, max: 1 }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              return `Score: ${context.raw}, Mood: ${sentiments[context.dataIndex]}`;
            }
          }
        }
      }
    }
  });
});
