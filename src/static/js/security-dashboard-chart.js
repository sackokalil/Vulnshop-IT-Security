var chartLabels = window.securityChartLabels || [];
var chartValues = window.securityChartValues || [];

if (chartLabels.length === 0) {
  chartLabels = ["No Events"];
  chartValues = [0];
}

var chartColors = [
  "rgba(255, 99, 132, 0.7)",
  "rgba(54, 162, 235, 0.7)",
  "rgba(255, 206, 86, 0.7)",
  "rgba(75, 192, 192, 0.7)",
  "rgba(153, 102, 255, 0.7)",
  "rgba(28, 200, 138, 0.7)",
  "rgba(231, 74, 59, 0.7)",
  "rgba(246, 194, 62, 0.7)"
];

var pieColors = [
  "#e74a3b",
  "#f6c23e",
  "#1cc88a",
  "#36b9cc",
  "#858796",
  "#4e73df",
  "#fd7e14",
  "#6f42c1"
];

var ctx = document.getElementById("myAreaChart");

var securityChart = new Chart(ctx, {
  type: "bar",

  data: {
    labels: chartLabels,

    datasets: [{
      label: "Exploit Attempts",
      data: chartValues,
      backgroundColor: chartColors,
      borderWidth: 1
    }]
  },

  options: {
    legend: {
      display: true
    },

    responsive: true,

    maintainAspectRatio: false,

    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
          precision: 0
        }
      }]
    }
  }
});

var pieCtx = document.getElementById("myPieChart");

var vulnerabilityPieChart = new Chart(pieCtx, {
  type: "doughnut",

  data: {
    labels: chartLabels,

    datasets: [{
      data: chartValues,
      backgroundColor: pieColors,
      hoverBackgroundColor: pieColors,
      hoverBorderColor: "rgba(234, 236, 244, 1)"
    }]
  },

  options: {
    maintainAspectRatio: false,

    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: "#dddfeb",
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,

      callbacks: {
        label: function(tooltipItem, data) {
          var dataset = data.datasets[tooltipItem.datasetIndex];
          var currentValue = dataset.data[tooltipItem.index];
          var label = data.labels[tooltipItem.index];

          return label + ": " + currentValue + " events";
        }
      }
    },

    legend: {
      display: false
    },

    cutoutPercentage: 70
  }
});



var legendContainer = document.getElementById("pieChartLegend");

if (legendContainer) {
  legendContainer.innerHTML = "";

  for (var i = 0; i < chartLabels.length; i++) {
    legendContainer.innerHTML += `
      <span class="mr-2">
        <i class="fas fa-circle" style="color: ${pieColors[i % pieColors.length]}"></i>
        ${chartLabels[i]}
      </span>
    `;
  }
}