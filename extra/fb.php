<?php
if(isset($_GET['access_token'])) {

  // more validate here
  $access_token = $_GET['access_token'];
  if (!preg_match("/^[A-Za-z0-9]+$/", $access_token)) {
    echo 'error';
    exit;
  }
  
  $client_id = '440490789296919';
  $client_secret = 'ENTER_YOUR_KEY_HERE';
  $ex_url = 'https://graph.facebook.com/oauth/access_token?client_id=' . $client_id . '&client_secret=' . $client_secret . '&grant_type=fb_exchange_token&fb_exchange_token=%s';
  

  $response = @file_get_contents(sprintf($ex_url, $access_token));
  parse_str($response, $out);
  
  if(isset($out['expires'])) {
    $out['expires_in'] = $out['expires'];
  }  
  
  echo json_encode($out);
  
  exit;
}
?>

<!DOCTYPE html PUBLIC 
  "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

    <head>
      <title>My Facebook Login Page</title>
      <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    </head>
    <script>
    

    
$(document).ready(function() {

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

      $.ajax({
        dataType: 'jsonp',
        jsonp: 'jsonp_callback',
        url: form_url,
        data: form_data,
        success: function (data) {
          setMsg(data.msg);
        }
      }).fail(function() { setMsg('error'); });    
      

    }
    
    function longlife() {
      $.getJSON('/fb.php', form.serialize(), function(data) {
        FillForm(data)
        submittobox()
      });
    }
    
    function setMsg(msg) {
      form.find('#result').html(msg);
    }
      
    function FillForm(items) {
      $.each(items, function(key, value) { 
        form.find('#' + key).val(value);
      });    
    }


    var form = $('#box_form');
    FillForm(getParameters())

    submittobox()
    
    form.submit(function(event) {
      event.preventDefault() 
    });
    
    $("#fb_longlife").click(function(event) {
      event.preventDefault() 
      setMsg('requesting...')
      longlife();
    });    

});      
    </script>
    <body>

<form action="<?php print $_GET['local']; ?>" method="post" id='box_form'>

    <div>
      <p>Submit to box on: <?php print $_GET['local']; ?></p>
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
      <input type="submit" id="fb_longlife" value="Request Longlive" />
    </div>
    
    <p>Your box returned: <b><span id="result"></span></b></p>
    
</form>

    </body>
 </html>
 