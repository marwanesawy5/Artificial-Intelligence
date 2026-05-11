document.addEventListener("DOMContentLoaded", async () => {
    Chart.defaults.color = "#9F9F9F";
    Chart.defaults.font.family = "Manrope";
    Chart.defaults.borderColor = "rgba(255,255,255,0.06)";

    try {
        // --- 1. FETCH LIVE DATA FROM FLASK ---
        const financeRes = await fetch('/api/finances');
        const finances = await financeRes.json();
        const historyRes = await fetch('/api/planner_history');
        let history = await historyRes.json();

        // --- 2. UPDATE THE 4 TOP CARDS ---
        if (!finances.error) {
            document.getElementById('user-savings').innerText = '$' + (finances.monthly_savings || 0).toLocaleString();
            document.getElementById('user-investments').innerText = '$' + (finances.investments || 0).toLocaleString();
            document.getElementById('user-emergency').innerText = '$' + (finances.emergency_fund || 0).toLocaleString();
            document.getElementById('user-expenses').innerText = '$' + (finances.expenses || 0).toLocaleString();
        }

        // --- 3. PREPARE HISTORY DATA FOR CHARTS ---
        let chartLabels = ["No Data"];
        let chartSurplus = [0];
        let latestExpenses = 0;
        let latestSurplus = 0;

        if (history && history.length > 0) {
            // The API sends newest first. We reverse it so the chart goes left-to-right (oldest to newest)
            history.reverse(); 
            
            // Extract dates and calculate surplus for the line chart
            chartLabels = history.map(plan => plan.date.split(" - ")[0]); // Just get the 'Jan 01' part
            chartSurplus = history.map(plan => plan.salary - plan.expenses);

            // Get the absolute newest plan for the doughnut chart
            const latestPlan = history[history.length - 1];
            latestExpenses = latestPlan.expenses;
            latestSurplus = latestPlan.salary - latestPlan.expenses;
        } else {
            // Fallback dummy data if they haven't generated a plan yet
            chartLabels = ["Create a plan first!"];
            chartSurplus = [0];
            latestExpenses = 50;
            latestSurplus = 50;
        }

        // --- 4. DRAW WEALTH GROWTH (LINE CHART) ---
        const wealthCanvas = document.getElementById("wealthChart");
        if (wealthCanvas) {
            new Chart(wealthCanvas, {
                type: "line",
                data: {
                    labels: chartLabels,
                    datasets: [{
                        label: "Monthly Surplus ($)",
                        data: chartSurplus,
                        borderColor: "#FCE849",
                        backgroundColor: "rgba(252,232,73,0.15)",
                        fill: true,
                        tension: 0.4,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: "#FCE849"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
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
                            ticks: { callback: value => "$" + value.toLocaleString() }
                        }
                    }
                }
            });
        }

        // --- 5. DRAW CURRENT BREAKDOWN (DOUGHNUT CHART) ---
        const portfolioCanvas = document.getElementById("portfolioChart");
        if (portfolioCanvas) {
            new Chart(portfolioCanvas, {
                type: "doughnut",
                data: {
                    labels: ["Expenses", "Surplus / Savings"],
                    datasets: [{
                        data: [latestExpenses, latestSurplus],
                        backgroundColor: [
                            "#3B3C4A", // Dark Grey for expenses
                            "#FCE849"  // Yellow for savings/surplus
                        ],
                        borderWidth: 0,
                        hoverOffset: 8
                    }]
                },
                options: {
                    cutout: "75%",
                    plugins: {
                        legend: {
                            position: "bottom",
                            labels: { padding: 20, color: "#FFFFFF" }
                        }
                    }
                }
            });
        }

    } catch (error) {
        console.error("Failed to load dashboard data:", error);
    }
});