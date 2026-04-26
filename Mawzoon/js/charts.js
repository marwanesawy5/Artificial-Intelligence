/* ==========================================
   js/charts.js
   FinAI Charts using Chart.js
========================================== */

document.addEventListener("DOMContentLoaded", () => {

  Chart.defaults.color = "#9F9F9F";
  Chart.defaults.font.family = "Manrope";
  Chart.defaults.borderColor = "rgba(255,255,255,0.06)";

  /* ==========================================
     Wealth Growth Chart (Dashboard)
  ========================================== */
  const wealthCanvas = document.getElementById("wealthChart");

  if (wealthCanvas) {
    new Chart(wealthCanvas, {
      type: "line",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [
          {
            label: "Net Worth",
            data: [42000, 48000, 52000, 61000, 73000, 84200],
            borderColor: "#FCE849",
            backgroundColor: "rgba(252,232,73,0.15)",
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: "#FCE849"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: "#21212E",
            titleColor: "#FFFFFF",
            bodyColor: "#FFFFFF",
            borderColor: "#FCE849",
            borderWidth: 1
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => "$" + value.toLocaleString()
            }
          }
        }
      }
    });
  }

  /* ==========================================
     Portfolio Allocation Doughnut
  ========================================== */
  const portfolioCanvas = document.getElementById("portfolioChart");

  if (portfolioCanvas) {
    new Chart(portfolioCanvas, {
      type: "doughnut",
      data: {
        labels: ["Stocks", "Gold", "Crypto", "Cash"],
        datasets: [
          {
            data: [45, 20, 15, 20],
            backgroundColor: [
              "#FCE849",
              "#FFFFFF",
              "#9F9F9F",
              "#3B3C4A"
            ],
            borderWidth: 0,
            hoverOffset: 8
          }
        ]
      },
      options: {
        cutout: "72%",
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              padding: 18
            }
          }
        }
      }
    });
  }

  /* ==========================================
     Gold Price Chart (Markets Page)
  ========================================== */
  const goldCanvas = document.getElementById("goldChart");

  if (goldCanvas) {
    new Chart(goldCanvas, {
      type: "bar",
      data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        datasets: [
          {
            label: "Gold",
            data: [2320, 2338, 2315, 2350, 2368, 2379, 2388],
            backgroundColor: "#FCE849",
            borderRadius: 10,
            borderSkipped: false
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: "#21212E",
            borderColor: "#FCE849",
            borderWidth: 1
          }
        },
        scales: {
          y: {
            ticks: {
              callback: value => "$" + value
            }
          }
        }
      }
    });
  }

  /* ==========================================
     Sparkline Mini Charts (Optional Future)
  ========================================== */
  const sparkCanvases = document.querySelectorAll(".spark-chart");

  sparkCanvases.forEach(canvas => {
    new Chart(canvas, {
      type: "line",
      data: {
        labels: ["1", "2", "3", "4", "5"],
        datasets: [
          {
            data: [5, 8, 6, 10, 12],
            borderColor: "#FCE849",
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.4
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        },
        scales: {
          x: { display: false },
          y: { display: false }
        }
      }
    });
  });

});