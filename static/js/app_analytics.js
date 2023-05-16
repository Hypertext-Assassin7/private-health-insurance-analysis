
const url_1 = "http://127.0.0.1:5000/analytics";

/* get data from url analytics and run two pie chart for region & exercise frequency breakdown */
    
d3.json(url_1).then (function(response_reg){
    
    console.log(response_reg)

    /* set up various for x, y values for pie and bar charts to demostrate breakdown of "region","exercise", "smoker", "occupation" */    
    let labels = response_reg[0].regions
    let values = response_reg[1].count

    let labels_exe = response_reg[2].exercise
    let values_exe = response_reg[3].exe_count

    let xValue1 = [response_reg[4].smoker[0], response_reg[4].smoker[1]]
    let xValue2 = [response_reg[4].smoker[2], response_reg[4].smoker[3]]

    let yValue1 = [response_reg[5].smoker_count[0], response_reg[5].smoker_count[1]]
    let yValue2 = [response_reg[5].smoker_count[2], response_reg[5].smoker_count[3]]

    let x_occ1 = [response_reg[6].occupation[0], response_reg[6].occupation[1],response_reg[6].occupation[2], response_reg[6].occupation[3]]
    let x_occ2 = [response_reg[6].occupation[4], response_reg[6].occupation[5],response_reg[6].occupation[6], response_reg[6].occupation[7]]
    let y_occ1 = [response_reg[7].occupation_count[0], response_reg[7].occupation_count[1],response_reg[7].occupation_count[2], response_reg[7].occupation_count[3]]
    let y_occ2 = [response_reg[7].occupation_count[4], response_reg[7].occupation_count[5],response_reg[7].occupation_count[6], response_reg[7].occupation_count[7]]

    let y_med1 = [response_reg[9].medical_count[0], response_reg[9].medical_count[1],response_reg[9].medical_count[2], response_reg[9].medical_count[3]]
    let y_med2 = [response_reg[11].family_medical_count[0], response_reg[11].family_medical_count[1],response_reg[11].family_medical_count[2], response_reg[11].family_medical_count[3]]

    console.log('medical', y_med1, y_med2)
          
    piechart("regions",values,labels)
    piechart("exercise",values_exe,labels_exe)
    barchart("smoker", xValue1,yValue1,xValue2,yValue2)
    barchart("occupation", x_occ1,y_occ1,x_occ2,y_occ2)

    /* stacked bar chart function */
  const ctx = document.getElementById('medical');
  new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Diabetes', 'Heart disease', 'High blood pressure', 'None'],
        datasets: [
          {
            label: 'Medical History',
            data: y_med1,
          },
          {
            label: 'Family Medical History',
            data: y_med2,
          },
        ],
      },
      options: {
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
          },
        },
      },
    });
})

/* donut pie chart function */
function piechart(html_id, values,labels) {
    var data = [{
        values: values,
        labels: labels,
        domain: {column: 0},
        name: labels,
        hoverinfo: 'label+percent+name',
        hole: 0.5,
        type: 'pie'
    }]

    var layout = {
        title: html_id + ' breakdown',
        annotations: [
      {
        font: {
          size: 20
        },
        showarrow: false,
        text: html_id,
        x: 0.5,
        y: 0.5
      }
    ],
    height: 600,
    width: 600,
    showlegend: true,
    grid: {rows: 1, columns: 1}
    };
    Plotly.newPlot(html_id, data, layout)}

/* grouped bar chart function*/
function barchart(html_id, x1, y1, x2, y2) {
  var trace1 = {
    x: x1,
    y: y1,
    name: 'female',
    type: 'bar'
  };
  
  var trace2 = {
    x: x2,
    y: y2,
    name: 'male',
    type: 'bar'
  };
  
  var data = [trace1, trace2];
  
  var layout = {
    barmode: 'group',
    title: html_id + ' breakdown',
    height: 500,
    width: 600,
  };
  
  Plotly.newPlot(html_id, data, layout)}