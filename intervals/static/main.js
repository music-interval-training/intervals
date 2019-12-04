var data1 = ['4', '1', '1', '5', '2', '6', '1', '1', '3', '5', '0', '4'];
var data2 = ['0', '5', '0', '0', '2', '3', '4', '2', '3', '2', '1', '3'];

function numberWrong(i) {
  return (data1[i] - data2[i])
}


var canvas = document.getElementById('myChart');
canvas.height = 250;
var data = {
  labels: ['Minor 2nd', 'Major 2nd', 'Minor 3rd', 'Major 3rd', 'Perfect 4th', 'Tritone', 'Perfect 5th', 'Minor 6th', 'Major 6th', 'Minor 7th', 'Major 7th', 'Octave'],
  datasets: [
    {
      label: 'Correct',
      data: data1,
      backgroundColor: 'rgba(89, 171, 227, 1)',
    },
    {
      label: 'Incorrect',
      data: data2,
      backgroundColor: 'rgba(248, 148, 6, 1)',
    },
  ]
}
var option = {
  legend: {
    display: true,
  },
  scales: {
    yAxes: [{
      stacked: true,
      scaleFontSize: 40,
      scaleLabel: {
        display: true,
      },
      ticks: {
        max: 10,
        min: 0,
        beginAtZero: true,
        callback: function (value) {
          return value + " "
        }
      },
    }],
    xAxes: [{
      id: "bar-x-axis1",
      stacked: true,
      // barThickness: 20,
    }, {
      id: "bar-x-axis2",
      stacked: true,
      display: false,
      // barThickness: 20,
    },],
  },
  plugins: {
    datalabels: {
      anchor: 'end',
      align: 'top'
    }
  }
};

var myBarChart = Chart.Bar(canvas, {
  data: data,
  options: option
});
