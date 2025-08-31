document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("emotionChart").getContext("2d");

  // Example data — replace with dynamic fetch or template injection
  const labels = ["Aug 25", "Aug 26", "Aug 27"];
  const scores = [0.85, 0.42, 0.12];
  const sentiments = ["positive", "neutral", "negative"];
  const colors = scores.map(score => {
    // positive 
    if (score > 0.6) return "#a3f7bf";
    // neutral       
    if (score > 0.3) return "#fdfd96";  
    // negative    
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
