
/**
 * Diese Datei Repräsentier unser Security chart und pie in der seite Dashboard(index)
 * hier ist der Chart mit statischen Daten erstellt
 * Später werden wir diesen Daten aus der Datenbank abrufen.
 */

var ctx = document.getElementById("myAreaChart");

var securityChart = new Chart(ctx, {

  type: 'bar',

  data: {

    labels: [
      "Login Attempts",
      "SQL Injection",
      "XSS",
      "IDOR",
      "File Downloads"
    ],

    datasets: [{

      label: "Exploit Attempts",

      data: [35, 18, 12, 9, 6],

      backgroundColor: [
        "rgba(255, 99, 132, 0.7)",
        "rgba(54, 162, 235, 0.7)",
        "rgba(255, 206, 86, 0.7)",
        "rgba(75, 192, 192, 0.7)",
        "rgba(153, 102, 255, 0.7)"
      ],

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
          beginAtZero: true
        }
      }]
    }
  }
});



// Pie Chart

var pieCtx = document.getElementById("myPieChart");

var vulnerabilityPieChart = new Chart(pieCtx, {

    type: 'doughnut',

    data: {

        labels: [
            "SQL Injection",
            "XSS",
            "Broken Access Control",
            "Path Traversal",
            "Broken Authentication"
        ],

        datasets: [{

            data: [35, 25, 20, 10, 10],

            backgroundColor: [
                "#e74a3b",
                "#f6c23e",
                "#1cc88a",
                "#36b9cc",
                "#858796"
            ],

            hoverBackgroundColor: [
                "#c0392b",
                "#dda20a",
                "#17a673",
                "#2c9faf",
                "#6c757d"
            ],

            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },

    options: {

        maintainAspectRatio: false,

        tooltips: {

            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
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

                    return label + ": " + currentValue + "%";
                }
            }
        },

        legend: {
            display: false
        },

        cutoutPercentage: 70,
    },
});