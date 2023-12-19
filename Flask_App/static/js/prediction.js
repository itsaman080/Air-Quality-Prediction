$("#predict").click(function(){
	debugger;
  var date=document.getElementById('date').value;
  
  var time=document.getElementById('time').value;
  $.ajax({
    type: "GET",
    url: "/pred",
    contentType: "application/json;charset=UTF-8",
    data: {
        "date": date,
        "time": time
    },
    dataType: "json",
    success: function(response) {
        var result = response.data;

        // Assuming 'resultDiv' is the ID of the div where you want to display the data
        var resultDiv = $('#resultDiv');

        // Clear previous content in the div
        resultDiv.empty();

        // Process the received data and display it in the 'resultDiv'
        var formattedData = "Received Data: " + JSON.stringify(result);
         resultDiv.text(formattedData);
    },
    error: function(error) {
        alert('Failed to fetch data');
    }
});
	
});