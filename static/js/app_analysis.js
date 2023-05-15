const url = "http://127.0.0.1:5000/analysis";

/* data route */
    
d3.json(url).then (function(response){

          console.log (response)

          // get prediction result based on clients' insurance cover option
          let ClientValue = Math.ceil(response[0].Client_option/52)
          console.log(ClientValue)

          // chart init
          let xValue = ['Basic', 'Standard', 'Premium'];
        
          let yValue = [Math.ceil(response[0].Basic/52), Math.ceil(response[0].Standard/52), Math.ceil(response[0].Premium/52)]
          console.log(yValue)

          let color_list = ['rgb(52, 83, 168)', 'rgb(52, 83, 168)', 'rgb(52, 83, 168)']
          var client_cover

          console.log(yValue,color_list)

          for (let i = 0; i< yValue.length; i++) {
            if (yValue[i] == ClientValue) {
              color_list[i] = 'rgb(52, 168, 53)';
              client_cover = xValue[i]
              console.log(client_cover)
            }
          }

          document.getElementById("Predict").innerHTML = '<p>By selecting the <b>'+ client_cover + '</b> Option,<br>' +
                                                        'the estimated cost for this choice will be <br>' +
                                                        '<b>USA$' + ClientValue + '</b> per week.</p>';

          // Create a trace for the bar chart
          let trace = {
            x: xValue,
            y: yValue,
            type: 'bar',
            marker: {
              color: color_list // Set the color of the bars
            },
            text: yValue.map(String), // Convert yValue array to string and assign as text for each bar
            textposition: 'auto' // Position the text on top of each bar
          };
          
          // Create a layout for the chart
          let layout = {
            title: 'Predicted Insurance Costs',
            titlefont: {
              size: 20,
              color: 'rgb(107, 107, 107)'
            },
            xaxis: {
              title: 'Insurance Plan',
              titlefont: {
                size: 20,
                color: 'rgb(107, 107, 107)'
              },
              tickfont: {
                size: 20,
                color: 'rgb(107, 107, 107)'
              }
            },
            yaxis: {
              title: 'Insurance Cost',
              titlefont: {
                size: 20,
                color: 'rgb(107, 107, 107)'
              },
              tickfont: {
                size: 20,
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