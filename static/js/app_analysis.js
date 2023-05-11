const url = "http://127.0.0.1:5000/analysis";

/* data route */
    
d3.json(url).then (function(response){

          console.log (response)

          // get prediction result based on clients' insurance cover option
          let ClientValue = [response[0].Client_option]

          document.getElementById("Predict").innerHTML = 'Your estimate insurance price is ' + ClientValue + ' per year.';

          // chart init
          let xValue = ['Basic', 'Standard', 'Premium'];
        
          let yValue = [response[0].Basic, response[0].Standard, response[0].Premium]
          console.log(yValue)
          
          // Create a trace for the bar chart
          let trace = {
            x: xValue,
            y: yValue,
            type: 'bar',
            marker: {
              color: 'rgb(52, 168, 83)' // Set the color of the bars
            }
          };
          
          // Create a layout for the chart
          let layout = {
            title: 'Predicted Insurance Costs',
            xaxis: {
              title: 'Insurance Plan',
              tickfont: {
                size: 14,
                color: 'rgb(107, 107, 107)'
              }
            },
            yaxis: {
              title: 'Insurance Cost',
              titlefont: {
                size: 16,
                color: 'rgb(107, 107, 107)'
              },
              tickfont: {
                size: 14,
                color: 'rgb(107, 107, 107)'
              }
            },
            margin: {
              b: 100 // Set the bottom margin to make room for the x-axis labels
            }
          };
          
          // Put the trace and layout into an array
          let data = [trace];
          
          // Create the chart
          Plotly.newPlot('chart', data, layout)
        })          