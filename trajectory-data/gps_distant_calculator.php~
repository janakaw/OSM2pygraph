<?php 

print( '<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
      html { height: 100% }
      body { height: 100%; margin: 0; padding: 0 }
      #map_canvas { height: 100% }
    </style>
    <script type="text/javascript"
      src="http://maps.googleapis.com/maps/api/js?key=AIzaSyD29y39LDdNheGcYB5vMEMq2xGS19z8dEI&sensor=false">
    </script>
    <script type="text/javascript">

	function calc_distance(){

		var RADIUS = 6371;
		var D2R = Math.PI/180;

		var result_div_id = document.getElementById(\'result\');

		var result_label_id = document.getElementById(\'res\');

		if(result_label_id != null){
			result_div_id.removeChild(result_label_id);
		}

		result_label_id = document.createElement(\'label\');
		result_label_id.setAttribute(\'id\',\'res\');

		var lat1 = document.getElementById(\'latitude1\').value;
		var lon1 = document.getElementById(\'longitude1\').value;
		var lat2 = document.getElementById(\'latitude2\').value;
		var lon2 = document.getElementById(\'longitude2\').value;

		var pattn = new RegExp("[^0-9.]");

		if(pattn.test(lat1) || pattn.test(lon1) || pattn.test(lat2) || pattn.test(lon2)){

			result_label_id.innerHTML = \'Invalid input.\';
			result_div_id.appendChild(result_label_id);
		
		} else {
		

		var lat1_rad = parseFloat(lat1)*D2R;
		var lat2_rad = parseFloat(lat2)*D2R;
		var lon1_rad = parseFloat(lon1)*D2R;
		var lon2_rad = parseFloat(lon2)*D2R;

		if(!(90 > parseFloat(lat1) && parseFloat(lat1)> -90 && 90 > parseFloat(lat2) && parseFloat(lat2)> -90 &&
			180 > parseFloat(lon1) && parseFloat(lon1)> -180 && 180 > parseFloat(lon2) && parseFloat(lon2)> -180)){
			
			result_label_id.innerHTML = \'Invalid input.\';
			result_div_id.appendChild(result_label_id);			
			return;
		}


		var a = Math.pow(Math.sin((lat1_rad-lat2_rad)/2),2) + Math.cos(lat1_rad)*Math.cos(lat2_rad)*Math.pow(Math.sin((lon1_rad-lon2_rad)/2),2);

		var distance = Math.abs(2*RADIUS*Math.atan2(Math.sqrt(a), Math.sqrt(1-a)));
				
		str1 = "Distance from point1 (".concat(lat1).concat(",").concat(lon1).concat(") to point2 (").concat(lat2).concat(",").concat(lon2).concat("): ").concat(distance.toString()).concat(\' KM\');
		
		result_label_id.innerHTML = str1;

		document.getElementById(\'latitude1\').value = \'\';
		document.getElementById(\'longitude1\').value = \'\';
		document.getElementById(\'latitude2\').value = \'\';
		document.getElementById(\'longitude2\').value = \'\';
		
		if(distance.toString()!=\'NaN\'){
			result_div_id.appendChild(result_label_id);
		} else {
			result_label_id.innerHTML = \'No input\';
			result_div_id.appendChild(result_label_id);
		}
	    }
	}
    </script>
  </head>
  <body bgcolor="#FFEE00">
	<h3>GPS distanace calculator</h3>
	<p>Only support signed degrees format (DDD.dddd) for the moment. <br/>Latitude range -90 to 90 degrees <br/> Longitude range -180 to 180 degrees</p>
	<table border="0" bgcolor="#FFEE00">
        <tr><td>Point 1</td><td>Latitude</td><td><input type="text" name="latitude1" id="latitude1"/></td><td>deg</td><td>Longitude</td><td><input type="text" name="longitude1" id="longitude1"/></td><td>deg  </td></tr>
	<tr><td>Point 2</td><td>Latitude</td><td><input type="text" name="latitude2" id="latitude2"/></td><td>deg  </td><td>Longitude</td><td><input type="text" name="longitude2" id="longitude2"/></td><td>deg</td></tr>
	<tr><td colspan="1"><input type="submit" value="get distance" onclick="calc_distance()" /></td></tr></table>
	<br/><div id="result"></div></tr> 
	
  </body>
</html>');

?>
