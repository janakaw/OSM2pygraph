<?php 
ob_start();
session_start();
if($_SESSION['loggedintaxi']!='yes')
	header('Location: logintaxi.php');

print( '<!DOCTYPE html>
<html>
  <head>
    <!-- POPUP -->
    <link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
  <script src="//code.jquery.com/jquery-1.9.1.js"></script>
  <script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
  <script>
    var $j = jQuery.noConflict();
    </script>
    <style type="text/css">
    .no-close .ui-dialog-titlebar-close {
  display: none;
}
    </style>
    <!--/POPUP-->
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
    var range_left = 0;
      var range_right = 0;
      var in_data = "";
            
      
	function initialize() {
	
	//-----------------------
	
	
	$j( "#dialog" ).dialog({ autoOpen: false });
	
		$j( "#dialog" ).dialog({
  dialogClass: "no-close",
  buttons: [
    {
      text: "Submit",
      click: function() {
        $j("#dialog" ).dialog( "close" );
      }
    }
  ]
});
	
	$j( "#dialog" ).on( "custom_dialogclose", function( event, ui ) {on_user_traj_next();} );
	$j( "#dialog" ).dialog({
   close : function( event, ui ) {range_left = document.getElementById("left").value; 
  range_right = document.getElementById("right").value; 
  $j( "#dialog").trigger( "custom_dialogclose", [ "Custom", "Event" ] );
 } });
	//--------------------------
		var myLatLng; ');

if($_REQUEST['dir']!="")
	print_centre();

print('var mapOptions = {
          zoom: 10,
          center: myLatLng,
          mapTypeId: google.maps.MapTypeId.TERRAIN
        };

        var map = new google.maps.Map(document.getElementById(\'map_canvas\'), mapOptions);

        var flightPlanCoordinates = [');

if($_REQUEST['dir']!="")
	print_point_array();

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
		var date_id = document.getElementById("uls").value;
		//var url="taxidrive_trajectory_list_sql.php?user=" + escape(date_id);
		
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
		var url_jquery = "taxidrive_trajectory_list_sql.php";
		document.body.style.cursor  = \'wait\'; 
		$j.post(url_jquery,{dir: escape(date_id)},
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
		var dir_id = document.getElementById("uls").value;
		var trajectory_id = document.getElementById("tls").value;
		
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
		var url_jquery = "taxidrive_trajectory_points_sql.php";
		document.body.style.cursor  = \'wait\'; 
		$j.post(url_jquery,{dir: escape(dir_id), trajectory: escape(trajectory_id)},
		 function(data){
		 	on_user_traj(data);
		})

		
	      }
	      
	      
	      //-----------------
	      
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
			
			$j( "#dialog" ).dialog({ modal: true });

			
			var right_point_count_sub_field_id = document.getElementById(\'right\');
			right_point_count_sub_field_id.value = len.toString();
			var left_point_count_sub_field_id = document.getElementById(\'left\');
			left_point_count_sub_field_id.value = "0";
			in_data = data;
				
			 $j(function() {
    $j( "#dialog" ).dialog("open");
  });
			
			
			
		}
	      
	      //------------------------

	
		function on_user_traj_next(){

			data = in_data;
			
			left = range_left;
			right = range_right;

			
			document.body.style.cursor  = \'default\'; 

			var points_and_dis = data.split(" ");
			var total_distance = points_and_dis[0];
			var pointArray = points_and_dis[1].split(":");
			var start_str = pointArray[0];
			var start_pt = start_str.split(",");
			
			var x; 
			var len = pointArray.length;
			var mid = Math.round(len/2);
			
			//------------------------------
			
			
			//---------------------------------
			var distance_div_id = document.getElementById(\'dis\');
	
			var distance_field_id = document.getElementById(\'dis_val\');
			if(distance_field_id != null){
				distance_div_id.removeChild(distance_field_id);
			}
			var distance_field_id = document.createElement(\'label\');
			distance_field_id.setAttribute(\'id\',\'dis_val\');
			var str1 = "distance:";
			
			
			var mypt_ct = 0;
			//---------------------------------
			var flightPlanCoordinates = [];
			for(x in pointArray){
				
			        if (parseInt(x,10)> parseInt(left,10) && parseInt(x,10)<parseInt(right,10)){
			        				        mypt_ct += 1;
			        
				var coord = pointArray[x].split(",");
				var point = new google.maps.LatLng((parseFloat(coord[0])+0.0013).toString(), (parseFloat(coord[1])+0.0061).toString());
				flightPlanCoordinates.push(point); }
			}
			
			var mid_str=pointArray[mid];
			var mid_pt = mid_str.split(",");
		        var myLatLng = new google.maps.LatLng((parseFloat(mid_pt[0])+0.0013).toString(), (parseFloat(mid_pt[1])+0.0061).toString());
	        	var mapOptions = {
	          		zoom: 10,
			        center: myLatLng,
				mapTypeId: google.maps.MapTypeId.ROADMAP
	        	};
	        	
	        	distance_field_id.innerHTML = str1.concat(total_distance.toString()).concat(": points:").concat(mypt_ct.toString());
	
			distance_div_id.appendChild(distance_field_id);
	
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
	<form action="taxidata_draw_trajectory.php" method="GET" bgcolor="blue"><table border="0" bgcolor="#FFEE00">
        <tr><td><div style="color:#FFEE00">..........</div></td><td><div id="ul">');

print_dir_list();

print('</div></td><td><div id="tl"></div></td><td><div id="dis"><label id="dis_val">Pick a user...</label></div></td><td><div id="speeds"></div></td><td><div id="distance"></div></td><td><div id="time"></div></td></tr></table></form>
<div id="dialog" title="Enter Range" >
<form>
  <label id="pt_count">
  <p>Range</p>
  <input type="text" id="left" />
  <input type="text" id="right" />
  </form>
</div>
<div id="map_canvas" style="width:100%; height:100%"></div>
  </body>
</html>');


function print_dir_list(){

	$dbc = connect_taxidata_db();

	$result = mysql_query("SELECT DISTINCT(dir_id) FROM tdrive");

	print '<select name="date" id="uls" onchange="user_traj_list()">';

	print '<option name="date" value=" ">select date</option>'; 

	while($row = mysql_fetch_array($result))
  	{	
		print '<option name="user" value="'.$row[0].'">'.$row[0].'</option>'; 
  	}
	print '</select>';

	close_connection($dbc);

}

function print_point_array(){

	$result = get_array();
	
	
	while($row = mysql_fetch_array($result))
  	{
		print('new google.maps.LatLng('.$row['latitude'] .','.$row['longitude'].'),');		
  	}
	
	

}


function print_centre(){

	$result = get_array();
	$geo_array = mysql_fetch_array($result);
	print('myLatLng= new google.maps.LatLng('.$geo_array['latitude'].','.$geo_array['longitude'].');');
}

function get_array(){

	$dbc = connect_taxidata_db();

	$result = mysql_query("SELECT * FROM tdrive WHERE dir_id='".$_REQUEST['dir']."' AND taxi_id='".$_REQUEST['trajectory']."'");
	close_connection($dbc);
	return $result;

}


function connect_taxidata_db(){

	$db_name="janakawc_taxidata";
	$log_file = '/home4/janakawc/taxidrive/taxidata.log';

	if($dbc = mysql_connect('localhost', 'janakawc_taxi', 'jaN@@201209')){
		file_put_contents($log_file, 'Connected.'.PHP_EOL, FILE_APPEND); 
	} else {
		file_put_contents($log_file, 'Not connected.'.PHP_EOL, FILE_APPEND);
		print '<p>Error not connected'.mysql_error().'</p>';
	}

	if($dbc){
		if(mysql_select_db($db_name,$dbc)){
			file_put_contents($log_file, 'Selected the db'.PHP_EOL, FILE_APPEND);
		} else {
			file_put_contents($log_file, 'Not selected the db'.PHP_EOL, FILE_APPEND);
			print '<p>Error not selected</p>';
		}
	}
	return $dbc;
}

function close_connection($dbc){
	$log_file = '/home4/janakawc/taxidrive/taxidata.log';
	if(mysql_close($dbc)){
		file_put_contents($log_file, 'DB closed'.PHP_EOL, FILE_APPEND);
	}
}

ob_end_flush();
?>