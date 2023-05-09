// Collect information
function showValue() {
    // Get the value of the input & select element from front end "insurance_estimator.html"
    var client_age = document.getElementById("age").value;
    var children_no = document.getElementById("children").value
    var bmi = document.getElementById("bmi").value
    var gender = document.getElementById("gender").value
    var smoker = document.getElementById("smoker").value
    var medical_history = document.getElementById("medical_history").value
    var family_medical_history = document.getElementById("family_medical_history").value
    var exercise_frequency = document.getElementById("exercise_frequency").value
    var occupation = document.getElementById("occupation").value
    var coverage_level = document.getElementById("coverage_level").value

    var client_data = {
        "age": client_age,
        "gender": gender,
        "bmi": bmi,
        "children": children_no,
        'smoker': smoker,
        'medical_history': medical_history,
        'family_medical_history': family_medical_history,
        'exercise_frequency': exercise_frequency,
        'occupation': occupation,
        'coverage_level': coverage_level
    } 

    var client_data_json = JSON.stringify(client_data);

    // alert(client_data_json)

    // Display the value in an alert box
    // alert("You are" + client_age + "with" + children_no + "kid" + bmi + gender + smoker + medical_history + family_medical_history + exercise_frequency + occupation + coverage_level) ;
    
    fetch("http://127.0.0.1:5000/estimator", { // send POST request to Flask server
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
          },
        body: client_data_json
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Response from server:', data);
      })
      .catch(error => {
        console.error('Error while fetching data:', error);
      });
}

  


  


  
