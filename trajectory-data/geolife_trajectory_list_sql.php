<?php //index.php
/* This is the home page for this site. It uses templates to create the layout. */

echo get_trajectories_list();

function get_trajectories_list(){

	$dbc = connect_geolife_db();

	$result = mysql_query("SELECT DISTINCT(file_id) FROM geolife WHERE user_id='".$_REQUEST['user']."'");

	$trajectory_list="";

	while($row = mysql_fetch_array($result))
  	{	if($trajectory_list!="")
			$trajectory_list=$trajectory_list.",";	
		$trajectory_list=$trajectory_list.$row[0];
  	}

	close_connection($dbc);
	return $trajectory_list;

}



function connect_geolife_db(){

	$db_name="geolife";

	if($dbc = mysql_connect('localhost', 'geolife', '********')){
	
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
?>
