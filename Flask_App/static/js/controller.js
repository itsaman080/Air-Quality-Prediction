$("#btn_createaccount").click(function(){
  //alert("You clicked me");
  debugger;
  var nm=document.getElementById('name').value;
  var em=document.getElementById('email').value;
  var ph=document.getElementById('phone').value;
  var gen=document.getElementById('gender').value;
  var pswd=document.getElementById('pswd').value;
  var addr=document.getElementById('addr').value;
  
  var nmpattern=/^[A-Za-z ]+$/;
  var phpattern=/^(6|7|8|9){1}[0-9]{9}$/;
  
  if(!nmpattern.test(nm))
  {
	  alert("Invalid name");
	  return false;
  }  
  if(!phpattern.test(ph))
  {
	  alert("Invalid Phone #");
	  return false;
  }
  
  if(gen=="Select Gender")
  {
	  alert("Please select gender");
	  return false;
  }
	

	$.ajax({
		type:"GET",
		url:"/regdata",
		contentType:"application/json;charset=UTF-8",
		data:{
			"uname":nm,
			"email":em,
			"phone":ph,
			"gender":gen,
			"pswd":pswd,
			"addr":addr
		},
		dataType:"json",
		success: function(result){
			alert('Data Saved Successfully');
			window.location="register";
		},
		failure: function(result){
			alert('Data Saving Failed');
		}
		
  });	
  
  
	  
  
});



$("#btn_accessaccount").click(function(){
  //alert("You clicked me");
  debugger;
  var em=document.getElementById('email').value;
  var pswd=document.getElementById('pswd').value;
 
	$.ajax({
		type:"GET",
		url:"/logdata",
		contentType:"application/json;charset=UTF-8",
		data:{
			"email":em,
			"pswd":pswd
		},
		dataType:"json",
		success: function(result){
			if(result=="Success")
			{
				alert('Logged in Successfully');
				window.location="dashboard";
			}
			else{
				alert('Credentials not found');
				window.location="register";
			}
				
		},
		failure: function(result){
			alert('Data Saving Failed');
		}
		
  });	
  
  
	  
  
});

$("#btn_cleardata").click(function(){
	var form_data = new FormData($('#upload-file')[0]);
	debugger;
	 $.ajax({
            type: 'POST',
            url: '/cleardataset',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				alert('Dataset has been cleared');
            },
        });
        });

$("#btn_loaddata").click(function(){
	var form_data = new FormData($('#upload-file')[0]);
	debugger;
	 $.ajax({
            type: 'POST',
            url: '/savedataset',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
				alert('Dataset has been loaded');
            },
        });
});