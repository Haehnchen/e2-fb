<!DOCTYPE html PUBLIC 
  "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

    <head>
      <title>My Facebook Login Page</title>
      <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    </head>
    <script>
    
function getParameters() {
  var searchString = window.location.hash.substring(1)
  var params = searchString.split("&")
  var hash = {}

  for (var i = 0; i < params.length; i++) {
    var val = params[i].split("=");
    hash[unescape(val[0])] = unescape(val[1]);
  }
  return hash;
}

  function submittobox() {
    form_data = form.serialize();
    form_url = form.attr('action')
    //console.log(url);
    //$.post(url, function(data) {
     // $('.result').html(data);
    //})
    
    $.ajax({
      dataType: 'jsonp',
      jsonp: 'jsonp_callback',
      url: form_url,
      data: form_data,
      success: function (data) {
        //obj.html(data.text);
        form.find('#result').html(data.msg);
      }
    }).fail(function() { form.find('#result').html('error'); });    
    

  }
    
    
$(document).ready(function() {
    //alert(document.getElementById('test').contentWindow.location.href);
    //console.log();
    form = $('#box_form');
    parms = getParameters();
    $.each(parms, function(key, value) { 
      form.find('#' + key).val(value);
    });   

    submittobox()
    
    form.submit(function(event) {
      event.preventDefault() 
      submittobox()
    });
  


    
});      
    </script>
    <body>

<form action="<?php print $_GET['local']; ?>" method="post" id='box_form'>

    <div>
      <p>Submit box on on: <?php print $_GET['local']; ?></p>
    </div>

    <div>
         <label for="access_token">access_token:</label>
         <input type="text" name="access_token" id="access_token" value="" tabindex="1" />
    </div>
    <div>
         <label for="expires_in">expires_in:</label>
         <input type="text" name="expires_in" id="expires_in" value="" tabindex="1" />
    </div>
	    <input type="submit" value="Resubmit to box" />
    </div>
    
    <p>Your box returned: <b><span id="result"></span></b></p>
    
</form>

    </body>
 </html>
 