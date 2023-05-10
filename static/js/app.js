function myFunction() {
	document.getElementById("my-form").addEventListener("submit", function(event) {
  event.preventDefault();
  var formData = new FormData(event.target);
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/process-data");
  xhr.onload = function() {
    document.getElementById("output").textContent = "The modified info is: " + xhr.responseText;
  };
  xhr.send(formData);
});
}
