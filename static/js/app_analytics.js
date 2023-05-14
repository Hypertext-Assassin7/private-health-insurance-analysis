
const url = "http://127.0.0.1:5000/analytics";

/* data route */
    
d3.json(url).then (function(response_reg){
        
          let values = []
          let labels = []
          console.log (response_reg)
          for (let i = 0; i <= response_reg.length-1; i++){
            values.push(response_reg[i].reg_number)
            labels.push(response_reg[i].regions)
          }

          console.log(labels)

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
            title: 'regions_breakdown',
            annotations: [
              {
                font: {
                  size: 20
                },
                showarrow: false,
                text: 'regions',
                x: 0.5,
                y: 0.5
              }
            ],
            height: 500,
            width: 500,
            showlegend: true,
            grid: {rows: 1, columns: 1}
          };
          
          Plotly.newPlot('regions', data, layout);
          
});

// });