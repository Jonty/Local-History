<!DOCTYPE html>  
<html>  
  <head>
    <title>Local History</title>
    <style type="text/css">
        body {
            font-family: Helvetica, Bitstream Vera Sans, sans-serif;
            color: #000000;
        }
        .content {
            text-align: left;
            margin-left: 20%;
            margin-top: 8%;
        }
        .heading {
            font-size: 3em;
            font-weight: bold;
        }
        .item {
            margin-left: 3%;
        }
        .mainlink {
            font-size: 2em;
        }
        .subitem {
            font-size: 1.2em;
        }
        .status {
            color: gray;
            font-size: 1em;
            margin-left: 1%;
        }
        A:link {
            text-decoration: none;
            color: #008000;
        }
        A:visited {
            text-decoration: none;
            color: #008000;
        }
        A:active {
            text-decoration: none;
            color: #008000;
        }
        A:hover {
            text-decoration: underline;
            color: #008000;
        }
    </style>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>  
    <script>  
        jQuery(window).ready(function(){  
            $('#status').html("Locating you...");
            navigator.geolocation.getCurrentPosition(handle_geolocation_query, handle_errors);
        });  
  
        function handle_geolocation_query(position){  

            $.ajax({
                url: 'lookupServerProxy.php?lat=' + position.coords.latitude + '&lon=' + position.coords.longitude,
                dataType: 'json',
                success: function(data) {
                    if (data.length == 0) {
                        $('#status').html("No things near you!");
                    } else {
                        $('#status').html(data.length + " things near you.");
                        process_response(data);
                    }
                }
            });

            $('.footer').css('display', '');
        }

        function handle_errors(error)  
        {  
            switch(error.code)  
            {  
                case error.PERMISSION_DENIED: 
                    alert("You need to allow geolocation permission");  
                    break;  
  
                case error.POSITION_UNAVAILABLE:
                    alert("Could not detect current position");  
                    break;  
  
                case error.TIMEOUT: 
                    alert("Retrieving position timed out");  
                    break;  
  
                default:
                    alert("Unknown error");  
                    break;  
            }  
        }

        function process_response(data)
        {
            $.each(
                data,
                function (key, site) {
                    var clone = $('.template-node').clone();
                    clone.css('display', '');
                    clone.removeClass('template-node');
                    clone.find('.mainlink').text(site.name);
                    clone.find('.period').text(site.period.join(', '));
                    clone.find('.description').text(site.description);
                    clone.find('.article').text(site.article);
                    clone.find('.location').text(site.location);
                    clone.find('.location').attr(
                        "href",
                        "http://maps.google.co.uk/maps?q=" + site.latitude + "," + site.longitude   
                    );
                    $('#result').append(clone);
                }
            );
        }

    </script>  
  </head>  
  <body>
    <span class='heading'>Local History</span>
    <div id='status' class='status'></div>

    <div id='result'>
    </div>
  
    <div class="template-node" style="display:none;">
        <span class="mainlink"></span>
        <div style="margin-left: 2%">
            <div><strong>Period:</strong> <span class="period"></span></div>
            <div><strong>Article:</strong> <span class="article"></span></div>
            <div><strong>Description:</strong> <span class="description"></span></div>
            <div><strong>Location:</strong> <a href="" class="location"></a></div>
            <hr>
        </div>
    </div>

    <div style="display:none;" class="footer">
        <small><a href="http://github.com/jonty">code</a> by <a href="http://jonty.co.uk">jonty</a></small>
    </div>

  </body>  
</html> 
