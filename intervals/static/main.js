
var ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
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







// var data1 = ['7.8', '5', '', '', '7.7', '7.8', '8.1', '7.8'];
// var data2 = ['8', '8', '', '', '8', '8', '8', '8'];

// var data3 = ['6', '7.76', '', '', '7.04', '7.6', '6.96', ''];
// var data4 = ['8', '8', '', '', '8', '8', '8', ''];

// function calculateFirst(i) {
//    return (data1[i] / data2[i] * 100)
// }

// function calculateSecond(i) {
//    return (data3[i] / data4[i] * 100)
// }


// var canvas = document.getElementById('myChart');
// var data = {
//   labels: ['1','2','3','4','5','6','7','8'],
//   datasets: [{   
//     data: data1,
//     backgroundColor: ['#c3cd46', '#e31c24', '#FFFFFF', '#FFFFFF', '#c3cd46', '#267533', '#267533', '#267533'],
//     datalabels: {
//       display: false,
//     },
//   }, {
//     data: data2,   
//     datalabels: {
//       display: true,
//       formatter: function(context, chart_obj) {
//       	 return isNaN(calculateFirst(chart_obj.dataIndex)) ? '' : calculateFirst(chart_obj.dataIndex)+ '%';
//       },
//     },
//     backgroundColor: ['rgba(61, 146, 125, 1)', 'rgba(61, 146, 125, 1)', 'rgba(61, 146, 125, 1)', 'rgba(61, 146, 125, 1)', 'rgba(61, 146, 125, 1)', 'rgba(61, 146, 125, 1)', 'rgba(61, 146, 125, 1)', 'rgba(61, 146, 125, 1)'],
//   }, {   
//     data: data3,
//     backgroundColor: ['#c3cd46', '#e31c24', '#FFFFFF', '#FFFFFF', '#c3cd46', '#267533', '#267533', '#267533'],
//     datalabels: {
//       display: false,
//     },
//   },
//   {
//     data: data4,   
//     datalabels: {
//       display: true,
//       formatter: function(context, chart_obj) {
//       	 return isNaN(calculateSecond(chart_obj.dataIndex)) ? '' : calculateSecond(chart_obj.dataIndex)+ '%';
//       },
//     },
//     backgroundColor: ['rgba(111, 175, 158, 1)', 'rgba(111, 175, 158, 1)', 'rgba(111, 175, 158, 1)', 'rgba(111, 175, 158, 1)', 'rgba(111, 175, 158, 1)', 'rgba(111, 175, 158, 1)', 'rgba(111, 175, 158, 1)', 'rgba(111, 175, 158, 1)'],
//   },  
//   ]
// };
// var option = {
//   legend: {
//     display: false,
//   },
//   tooltips: {
//     enabled: false,
//   },
//   scales: {
//     yAxes: [{
//       scaleFontSize: 40,
//       scaleLabel: {
//         display: true,
//       },
//       ticks: {
//         max: 10,
//         min: 0,
//         stepSize: 2,
//         beginAtZero: true,
//         callback: function(value) {
//           return value + " h"
//         }
//       },
//     }],
//     xAxes: [{
//       id: "bar-x-axis1",
//       stacked: true,
//       barThickness: 30,     
//     }, {
//       id: "bar-x-axis2",
//       stacked: true,
//       display: false,      
//       barThickness: 10,
//     }, {
//       id: "bar-x-axis3",
//       stacked: true,    
//       barThickness: 30,
//       display: false
//     }, {
//       id: "bar-x-axis4",
//       stacked: true,    
//       display: false,
//       barThickness: 10,
//     }, ],
//   },
//   plugins: {
//     datalabels: {
//       anchor: 'end',
//       align: 'top'   
//     }
//   }
// };

// var myBarChart = Chart.Bar(canvas, {
//   data: data,
//   options: option
// });
