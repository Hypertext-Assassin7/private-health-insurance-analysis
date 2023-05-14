
const url_1 = "http://127.0.0.1:5000/analytics";

/* data route */
    
d3.json(url_1).then (function(response_reg){
    
    console.log(response_reg)
        
    let labels = response_reg[0].regions
    let values = response_reg[1].count
    let labels_exe = response_reg[2].exercise
    let values_exe = response_reg[3].exe_count

    console.log(values, labels)
          
    piechart("regions",values,labels)
    piechart("exercise",values_exe,labels_exe)
});

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
  
  console.log(data.values)

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
    height: 500,
    width: 500,
    showlegend: true,
    grid: {rows: 1, columns: 1}
  };
  
  Plotly.newPlot(html_id, data, layout);}