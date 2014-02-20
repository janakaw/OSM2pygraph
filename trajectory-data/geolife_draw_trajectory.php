<?php 
/**
 *
 * @author     Janaka Seneviratne
 * @copyright  2014 Janaka Seneviratne
 * @version    CVS: $Id:$
 */
ob_start();
session_start();
if($_SESSION['iloggedin']!='yes')
	header('Location: logingeo.php');

print( '<!DOCTYPE html>
<html>
  <head>
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
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
	function initialize() {
		var myLatLng; ');

if($_REQUEST['user']!="")
	print_centre($geo_array,$result);

print('var mapOptions = {
          zoom: 12,
          center: myLatLng,
          mapTypeId: google.maps.MapTypeId.TERRAIN
        };

        var map = new google.maps.Map(document.getElementById(\'map_canvas\'), mapOptions);

        var flightPlanCoordinates = [');

if($_REQUEST['user']!="")
	print_point_array($result,$geo_array);

	print ('];
		var flightPath = new google.maps.Polyline({
		  path: flightPlanCoordinates,
		  strokeColor: \'#FF0000\',
		  strokeOpacity: 1.0,
		  strokeWeight: 2
		});

		flightPath.setMap(map);
	      }


		var request=new XMLHttpRequest();
	      	var count=0;
		var center_str="";
		var point_array="";
	
	     function user_traj_list(){
		count=0;
		var user_id = document.getElementById("uls").value;
		var url="geolife_trajectory_list_sql.php?user=" + escape(user_id);
		
		//--------------------
		var distance_div_id = document.getElementById(\'dis\');

		var distance_field_id = document.getElementById(\'dis_val\');
		if(distance_field_id != null){
			distance_div_id.removeChild(distance_field_id);
		}
		var distance_field_id = document.createElement(\'label\');
		distance_field_id.setAttribute(\'id\',\'dis_val\');
		var str1 = "Please wait while the trajectory list is updated...";
		distance_field_id.innerHTML = str1;

		distance_div_id.appendChild(distance_field_id);
				
		//--------JQuery post-------------
		var url_jquery = "geolife_trajectory_list_sql.php";
		document.body.style.cursor  = \'wait\'; 
		$.post(url_jquery,{user: escape(user_id)},
		 function(data){
		 	on_traj_list(data);
		})

	
	      }

	     function on_traj_list(data){
		
		document.body.style.cursor  = \'default\';
		var trajectory_list = data.split(",");
		var trajectory_list_div_id = document.getElementById(\'tl\');

		var trajectory_list_id = document.getElementById(\'tls\');
		if(trajectory_list_id != null){
			trajectory_list_div_id.removeChild(trajectory_list_id);
		}
		var trajectory_list_id = document.createElement(\'select\');
		trajectory_list_id.setAttribute(\'id\',\'tls\');
		trajectory_list_id.name = \'trajectory\';
		var x;

			var ini_trajectory_id = document.createElement(\'option\');
			ini_trajectory_id.name = \'trajectory\';
			ini_trajectory_id.value = \' \';
			ini_trajectory_id.text = \'select trajectory\';			
			trajectory_list_id.appendChild(ini_trajectory_id);
		

		for(x in trajectory_list){
			var next_trajectory_id = document.createElement(\'option\');
			next_trajectory_id.name = \'trajectory\';
			next_trajectory_id.value = trajectory_list[x];
			next_trajectory_id.text = trajectory_list[x];			
			trajectory_list_id.appendChild(next_trajectory_id);
		}
		trajectory_list_id.onchange = user_traj;
		trajectory_list_div_id.appendChild(trajectory_list_id);

		//--------------------
		var distance_div_id = document.getElementById(\'dis\');

		var distance_field_id = document.getElementById(\'dis_val\');
		if(distance_field_id != null){
			distance_div_id.removeChild(distance_field_id);
		}
		var distance_field_id = document.createElement(\'label\');
		distance_field_id.setAttribute(\'id\',\'dis_val\');
		var str1 = "Pick a trajectory...";
		distance_field_id.innerHTML = str1;

		distance_div_id.appendChild(distance_field_id);
		//--------------------

	     }

	     function user_traj(){
		count=0;
		var user_id = document.getElementById("uls").value;
		var trajectory_id = document.getElementById("tls").value;
		var url="geolife_trajectory_points_sql.php?user=" + escape(user_id) + "&trajectory=" + escape(trajectory_id);
		
		//--------------------
		var distance_div_id = document.getElementById(\'dis\');

		var distance_field_id = document.getElementById(\'dis_val\');
		if(distance_field_id != null){
			distance_div_id.removeChild(distance_field_id);
		}
		var distance_field_id = document.createElement(\'label\');
		distance_field_id.setAttribute(\'id\',\'dis_val\');
		var str1 = "Please wait...(if hourglass stops try a different trajectory)";
		distance_field_id.innerHTML = str1;

		distance_div_id.appendChild(distance_field_id);
						
		//--------JQuery post-------------
		var url_jquery = "geolife_trajectory_points_sql.php";
		document.body.style.cursor  = \'wait\'; 
		$.post(url_jquery,{user: escape(user_id), trajectory: escape(trajectory_id)},
		 function(data){
		 	on_user_traj(data);
		})

		
	      }

	
		function on_user_traj(data){
		
			document.body.style.cursor  = \'default\'; 
			
			var points_and_dis = data.split(" ");
			var total_distance = points_and_dis[0];
			var pointArray = points_and_dis[1].split(":");
			var start_str = pointArray[0];
			var start_pt = start_str.split(",");
			
			var x; 
			var len = pointArray.length;
			var mid = Math.round(len/2);
	
	
			//---------------------------------
			var distance_div_id = document.getElementById(\'dis\');
	
			var distance_field_id = document.getElementById(\'dis_val\');
			if(distance_field_id != null){
				distance_div_id.removeChild(distance_field_id);
			}
			var distance_field_id = document.createElement(\'label\');
			distance_field_id.setAttribute(\'id\',\'dis_val\');
			var str1 = "distance:";
			distance_field_id.innerHTML = str1.concat(total_distance.toString()).concat(": points:").concat(pointArray.length.toString());
	
			distance_div_id.appendChild(distance_field_id);
			//---------------------------------
			var flightPlanCoordinates = [];
			for(x in pointArray){
				var coord = pointArray[x].split(",");
				var point = new google.maps.LatLng((parseFloat(coord[0])+0.0013).toString(), (parseFloat(coord[1])+0.0061).toString());
				flightPlanCoordinates.push(point);
			}
			
			var mid_str=pointArray[mid];
			var mid_pt = mid_str.split(",");
		        var myLatLng = new google.maps.LatLng((parseFloat(mid_pt[0])+0.0013).toString(), (parseFloat(mid_pt[1])+0.0061).toString());
	        	var mapOptions = {
	          		zoom: 15,
			        center: myLatLng,
				mapTypeId: google.maps.MapTypeId.ROADMAP
	        	};
	
	        	var map = new google.maps.Map(document.getElementById(\'map_canvas\'), mapOptions);
	        	
	        	
	        		var c=0
	        		var pinColor = "FF8866";
	        		 var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
	        new google.maps.Size(11, 24),
	        new google.maps.Point(0,0),
	        new google.maps.Point(5, 24));
	        
		        	for (y in flightPlanCoordinates){
		        	//change marker color every 20
		        		if(y%40==0){
		        		pinColor = "FF8866"; //green
		        			
	    pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
	        new google.maps.Size(21, 34),
	        new google.maps.Point(0,0),
	        new google.maps.Point(10, 34));
		        		
		        		
		        		} else if(y%20==0){
		        			pinColor = "2266FF"; //blue
		        			
	   pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
	        new google.maps.Size(21, 34),
	        new google.maps.Point(0,0),
	        new google.maps.Point(10, 34));
		        		
		        		}
		        		//if(y%2) continue; //draw only each 5th point 
		  			var marker = new google.maps.Marker({
		      				position: flightPlanCoordinates[y],
		      				map: map,
		      				title: y.toString() + ":" +pointArray[y],
		      				icon: pinImage
		  				});
				}  
				
				//var flightPath = new google.maps.Polyline({
	          		//	path: flightPlanCoordinates,
	 		 	//       strokeColor: \'#FF0000\',
			 	//       strokeOpacity: 1.0,
	          		//	strokeWeight: 2
	        		//	});
	
	        		//	flightPath.setMap(map);      		
	        		
			
	}

    </script>
  </head>
  <body onload="initialize()" bgcolor="#FFEE00">
	<form action="geolife_draw_trajectory.php" method="GET" bgcolor="blue"><table border="0" bgcolor="#FFEE00">
        <tr><td><div style="color:#FFEE00">..........</div></td><td><div id="ul">');

print_user_list();

print('</div></td><td><div id="tl"></div></td><td><div id="dis"><label id="dis_val">Pick a user...</label></div></td><td><div id="speeds"></div></td><td><div id="distance"></div></td><td><div id="time"></div></td></tr></table></form>
<div id="map_canvas" style="width:100%; height:100%"></div>
  </body>
</html>');


function print_user_list(){

	$dbc = connect_geolife_db();

	$result = mysql_query("SELECT DISTINCT(user_id) FROM geolife");

	print '<select name="user" id="uls" onchange="user_traj_list()">';

	print '<option name="user" value=" ">select user</option>'; 

	while($row = mysql_fetch_array($result))
  	{	
		print '<option name="user" value="'.$row[0].'">'.$row[0].'</option>'; 
  	}
	print '</select>';

	close_connection($dbc);

	return $user_list;

}

function print_point_array(){

	$result = get_array();
	
	
	while($row = mysql_fetch_array($result))
  	{
		print('new google.maps.LatLng('.$row['latitude'] .','.$row['longitude'].'),');		
  	}
	
	

}


function print_centre($geo_array){

	$result = get_array();
	$geo_array = mysql_fetch_array($result);
	print('myLatLng= new google.maps.LatLng('.$geo_array['latitude'].','.$geo_array['longitude'].');');
}

function get_array(){

	$dbc = connect_geolife_db();

	$result = mysql_query("SELECT * FROM geolife WHERE user_id='".$_REQUEST['user']."' AND file_id='".$_REQUEST['trajectory']."'");
	close_connection($dbc);
	return $result;

}


function connect_geolife_db(){

	$db_name="janakawc_geolife";

	if($dbc = mysql_connect('localhost', 'janakawc_geolife', 'jaN@@201209')){
	
	} else {
	
	}

	if($dbc){
		if(mysql_select_db($db_name,$dbc)){
	
		} else {
	
		}
	}
	return $dbc;
}

function close_connection($dbc){
	if(mysql_close($dbc)){
	
	}
}
ob_end_flush();
?>
