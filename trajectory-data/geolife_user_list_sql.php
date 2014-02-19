<?php //index.php
/* This is the home page for this site. It uses templates to create the layout. */

echo print_user_list();

function print_user_list(){

	$dbc = connect_geolife_db();

	$result = mysql_query("SELECT DISTINCT(user_id) FROM geolife");

	$user_list="";	

	while($row = mysql_fetch_array($result))
  	{	if($user_list!="")
			$user_list=$user_list.",";
		$user_list=$user_list.$row[0];
  	}

	close_connection($dbc);

	return $user_list;
}



function connect_geolife_db(){

	$db_name="geolife";

	if($dbc = mysql_connect('localhost', 'geolife', '*******')){
	
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
