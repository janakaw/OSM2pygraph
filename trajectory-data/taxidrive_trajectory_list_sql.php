<?php 
/**
 *
 * @author     Janaka Seneviratne
 * @copyright  2014 Janaka Seneviratne
 */
echo get_trajectories_list();

function get_trajectories_list(){

	$dbc = connect_taxidata_db();

	$result = mysql_query("SELECT DISTINCT(taxi_id) FROM tdrive WHERE dir_id='".$_REQUEST['dir']."'");

	$trajectory_list="";

	while($row = mysql_fetch_array($result))
  	{	if($trajectory_list!="")
			$trajectory_list=$trajectory_list.",";	
		$trajectory_list=$trajectory_list.$row[0];
  	}

	close_connection($dbc);
	return $trajectory_list;

}



function connect_taxidata_db(){

	$db_name="taxidata";
	$log_file = '/home4/taxidrive/taxidata.log';

	if($dbc = mysql_connect('localhost', 'taxi', '*******')){
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
?>
