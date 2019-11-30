console.log('JS is running')

var data1 = ['12', '19', '3', '5', '2', '3', '15', '10', '3', '7', '0', '5'];
var data2 = ['8', '12', '3', '0', '2', '1', '10', '8', '3', '6', '0', '4'];

function numberWrong(i) {
       return (data1[i] - data2[i])
}
    

var canvas = document.getElementById('myChart');
var data = {
  labels: ['Minor 2nd', 'Major 2nd', 'Minor 3rd', 'Major 3rd', 'Perfect 4th', 'Tritone', 'Perfect 5th', 'Minor 6th', 'Major 6th', 'Minor 7th', 'Major 7th', 'Octave'],
  datasets: [{   
    data: data1,
    backgroundColor: 'rgba(255, 99, 132, 0.4)',
    // tooltips: {
    //     callback: {
    //         label: function(tooltipItem, data1,data2) {
    //             var label = data.datasets[tooltipItem.datasetIndex].label
    //             label = data1[i] - data2[i];
    //             return label;
    // }},
    datalabels: {
      display: false,
    },
  }, {
    data: data2,   
    datalabels: {
      display: true},
    backgroundColor: 'rgba(0, 255, 125, 1)',
  },  
  ]
};
var option = {
  legend: {
    display: true,
  },
  tooltips: {
    //   enabled:false,
    callback: {
        label: function(tooltipItem,data1,data2) {
            var label = data.datasets[tooltipItem.datasetIndex].label || '';
            // label = (data1[i] - data2[i]);
            label = boo;
            return label;
}}},
//   tooltips: {
//     enabled: true,
//   },
  scales: {
    yAxes: [{
      scaleFontSize: 40,
      scaleLabel: {
        display: true,
      },
      ticks: {
        max: 10,
        min: 0,
        stepSize: 2,
        beginAtZero: true,
        callback: function(value) {
          return value + " "
        }
      },
    }],
    xAxes: [{
      id: "bar-x-axis1",
      stacked: true,
      barThickness: 30,     
    }, {
      id: "bar-x-axis2",
      stacked: true,
      display: false,      
      barThickness: 10,
    }, ],
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

// var data1 = ['12', '19', '3', '5', '2', '3', '15', '10', '3', '7', '0', '5'];
// var data2 = ['8', '12', '3', '0', '2', '1', '10', '8', '3', '6', '0', '4'];

// var ctx = document.getElementById('myChart');
// ctx.height = 500;
// var myChart = new Chart(ctx, {
//     type: 'bar',
//     data: {
//         labels: ['Minor 2nd', 'Major 2nd', 'Minor 3rd', 'Major 3rd', 'Perfect 4th', 'Tritone', 'Perfect 5th', 'Minor 6th', 'Major 6th', 'Minor 7th', 'Major 7th', 'Octave'],
//         datasets: [{
//             label: '# of attempts',
//             data: data1,
//             backgroundColor: 'rgba(255, 99, 132, 0.6)',
//             borderColor: 'rgba(255, 99, 132, 1)',
//             borderWidth: 1
//         }]
//     },
//     options: {
//         responsive: true,
//         maintainAspectRatio: false,
//         scales: {
//             xAxes: [{
//                 ticks: {
//                     fontSize: 25,
//                 }
//             }],
//             yAxes: [{
//                 ticks: {
//                     fontSize: 20,
//                     beginAtZero: true
//                 }
//             }]
//         },
//     }
// });