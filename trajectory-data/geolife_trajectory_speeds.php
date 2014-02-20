<?php 
/**
 *
 * @author     Janaka Seneviratne
 * @copyright  2014 Janaka Seneviratne
 */
session_start();
$lat_array=array();
$lon_array=array();
$time_array=array();

//get_point_arrays($lat_array, $lon_array, $time_array);

//echo get_speed_array($lat_array, $lon_array, $time_array);

//function get_point_arrays($lat_array,$lon_array,$time_array){
	
	$dbc = connect_geolife_db();
	$result = mysql_query("SELECT * FROM geolife WHERE user_id='".$_REQUEST['user']."' AND file_id='".$_REQUEST['trajectory']."'");
	
	while($row = mysql_fetch_array($result))
  	{
		array_push($lat_array, $row['latitude']);
		array_push($lon_array, $row['longitude']);
		array_push($time_array, $row['time_in_days']);
  	}
	
	mysql_close($dbc);
//}

//function get_speed_array($lat_array,$lon_array,$time_array){
	$prev_lat=$lat_array[0];
	$prev_lon=$lon_array[0];
	$prev_time=$time_array[0];

	$speed_array = array();

	$total_distance=0;
	$total_time = 0;

	for($i=1; $i<count($time_array);$i++){
		
		$distance = get_distance($prev_lat, $prev_lon, $lat_array[$i], $lon_array[$i]);
		$total_distance=$total_distance+$distance;

		$time_delta = $time_array[$i] - $prev_time;
		$total_time = $total_time + $time_delta;

		$speed_array[$i-1]=get_speed($distance,$time_delta);
		$prev_lat=$lat_array[$i];
		$prev_lon=$lon_array[$i];
		$prev_time=$time_array[$i];
	}

	$speeds=$_REQUEST['user'].",".$_REQUEST['trajectory'].",".(string)$total_distance.",".(string)($total_time*24);

	for($i=0; $i<count($speed_array);$i++){
		if($speeds!="")
			$speeds=$speeds.",";
		$speeds	= $speeds.(string)$speed_array[$i];	
		
	}

	//$_SESSION['tt']=$total_time;
	//$_SESSION['td']=$total_distance;

	echo $speeds;
//}

function get_distance($lat1,$lon1,$lat2,$lon2){
	$RADIUS = 6371;

	$D2R = pi()/180;

	$lat1_rad = $lat1*$D2R;
	$lat2_rad = $lat2*$D2R;
	$lon1_rad = $lon1*$D2R;
	$lon2_rad = $lon2*$D2R;

	$a = pow(sin(($lat1_rad-$lat2_rad)/2),2) + cos($lat1_rad)*cos($lat2_rad)*pow(sin(($lon1_rad-$lon2_rad)/2),2);

	$distance = abs(2*$RADIUS*atan2(sqrt($a), sqrt(1-$a)));
	return $distance;
}

function get_speed($distance, $time_delta){
	return round($distance/($time_delta*24),0); //km/h
}

function connect_geolife_db(){

	$db_name="geolife";

	if($dbc = mysql_connect('geolife.db.9149993.hostedresource.com', 'geolife', '*****')){
	
	} else {
	
	}

	if($dbc){
		if(mysql_select_db($db_name,$dbc)){
	
		} else {
	
		}
	}
	return $dbc;
}

?>
