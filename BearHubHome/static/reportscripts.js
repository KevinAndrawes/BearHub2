// Get the data from the Django view and pass it to the JavaScript file
var users = "{{ users|safe }}";
var users9 = "{{ users9|safe }}";
var users10 = "{{ users10|safe }}";
var users11 = "{{ users11|safe }}";
var users12 = "{{ users12|safe }}";

// Create an array of labels for the chart
var labels = ["9th Grade", "10th Grade", "11th Grade", "12th Grade"];

// Create an array of data for the chart
var data = [users9.length, users10.length, users11.length, users12.length];

// Create a function to generate the chart
function generateChart() {
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Points per Grade',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

// Call the function to generate the chart
generateChart();