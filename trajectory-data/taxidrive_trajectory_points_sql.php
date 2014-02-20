<?php 
/**
 *
 * @author     Janaka Seneviratne
 * @copyright  2014 Janaka Seneviratne
 */

$str = get_point_array();

echo $str;

function get_centre(){
	$dbc = connect_taxidata_db();
	$result = mysql_query("SELECT * FROM tdrive WHERE dir_id='".$_REQUEST['dir']."' AND taxi_id='".$_REQUEST['trajectory']."'");
	
	$geo_array = mysql_fetch_array($result);
	mysql_close($dbc);
	return $geo_array['latitude'].','.$geo_array['longitude'];
}


function get_point_array(){
	
	$dbc = connect_taxidata_db();
	$result = mysql_query("SELECT * FROM tdrive WHERE dir_id='".$_REQUEST['dir']."' AND taxi_id='".$_REQUEST['trajectory']."'");

	$point_array="";

	$count =0;
	$lat1=0;$lon1=0;
	$distance = 0;

	$index = 0;
	//$row = mysql_fetch_array($result);	
	//$point_array=$point_array.$row['latitude'] .','.$row['longitude'];
	while($row = mysql_fetch_array($result))
  	{
		$index = $index + 1;
		if($index == 8000){
			break;
		}
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

function connect_taxidata_db(){

	$db_name="taxidata";
	$log_file = '/home4/taxidrive/taxidata.log';

	if($dbc = mysql_connect('localhost', 'taxi', '******<img src="tree.jpg" alt="" />')){
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
