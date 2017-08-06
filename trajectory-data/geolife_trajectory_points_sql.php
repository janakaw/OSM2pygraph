<?php 
/**
 *
 * @author     Janaka Seneviratne
 * @copyright  2014 Janaka Seneviratne
 */

//$ret_string = get_centre();

$str = get_point_array();

echo $str;

function get_centre(){
	$dbc = connect_geolife_db();
	$result = mysql_query("SELECT * FROM geolife WHERE user_id='".$_REQUEST['user']."' AND file_id='".$_REQUEST['trajectory']."'");
	
	$geo_array = mysql_fetch_array($result);
	mysql_close($dbc);
	return $geo_array['latitude'].','.$geo_array['longitude'];
}


function get_point_array(){
	
	$dbc = connect_geolife_db();
	$result = mysql_query("SELECT * FROM geolife WHERE user_id='".$_REQUEST['user']."' AND file_id='".$_REQUEST['trajectory']."'");

	$point_array="";

	$count =0;
	$lat1=0;$lon1=0;
	$distance = 0;
	
	while($row = mysql_fetch_array($result))
  	{
		if($point_array!=""){
			$point_array = $point_array.":";
		}
  		$point_array=$point_array.$row['latitude'] .','.$row['longitude'];

		if($count==0){
			$lat1 = $row['latitude'];
			$lon1 = $row['longitude'];
		} else {
			$distance = $distance + get_distance($lat1, $lon1,$row['latitude'],$row['longitude']);
			$lat1 = $row['latitude'];
			$lon1 = $row['longitude'];

		}
		$count=$count+1;

  	}
  	//separated by space
	$point_array = $distance."KM:total_points:".$count." ".$point_array;
	mysql_close($dbc);
	return $point_array;

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

?>
