<?php //index.php
/* This is the home page for this site. It uses templates to create the layout. */
define('TITLE', 'Welcome !');
include('templates/header.html');
?>
<?php
$search_root='taxidrive';
$log_file = 'taxidrive/geolife.log';

//read_all($search_root, $log_file);

print '<p>Over</p>'


function insert_file($user_id,$file_id,$file,$dbc,$log_file){

	$insert_query="LOAD DATA LOCAL INFILE '".'geolife/Geolife\ Trajectories\ 1.3/Data/'.$user_id.'/Trajectory/'.$file_id."'
			
			INTO TABLE geolife

   			FIELDS TERMINATED BY ','
        
			LINES TERMINATED BY '\r\n'
    
			IGNORE 6 LINES

			(latitude, longitude, junk, altitude, time_in_days, date, time)

			SET user_id = '".$user_id."',file_id='".$file_id."';";
	
	if(mysql_query($insert_query,$dbc)){

		return "TRUE";
						
	}else{
		print('<p style="color: red;">not inserted!!!'.mysql_error().'</p>');
		file_put_contents($log_file, 'Insert error: user:'.$item_root.' file:'.$item.PHP_EOL, FILE_APPEND);
		return "FALSE";						
	}

}

function read_all($search_root,$log_file){

	$dbc=connect_geolife_db($log_file);
	print '<p>connected</p>';

	set_time_limit(36000);
	file_put_contents($log_file, 'start:'.PHP_EOL, FILE_APPEND);

	ini_set('auto_detect_line_endings',1);
	$contents_root=scandir($search_root);
	foreach ($contents_root as $item_root) {

		if(is_dir($search_root.'/'.$item_root.'/Trajectory') && substr($item_root,0,2) != '00' && substr($item_root,0,1) == '0'){
			$contents_next=scandir($search_root.'/'.$item_root.'/Trajectory');
			$i=0;
			foreach ($contents_next as $item) {
				$file = $search_root.'/'.$item_root.'/Trajectory'.'/'.$item; 	
				
				if( (is_file($file)) AND (substr($item,0,1) !='.') ){
					
					$ret = insert_file($item_root,$item,$file,$dbc);
					if($ret=="FALSE"){
						file_put_contents($log_file, 'Error: user:'.$item_root.' file:'.$item.PHP_EOL, FILE_APPEND);
						print '<p>Error user: '.$item_root.' file: '.$item.'</p>';
						close_connection($dbc,$log_file);
						return;
					}	

				} 				
								
			}
		}
	}

	file_put_contents($log_file, 'End: '.date('l F j, Y : h i s : u ').PHP_EOL, FILE_APPEND);
	print '<p>finished</p>';
	close_connection($dbc, $log_file);
}


function connect_geolife_db($log_file){

	$db_name="janakawc_taxidata";

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

function close_connection($dbc,$log_file){
	if(mysql_close($dbc)){
		file_put_contents($log_file, 'DB closed'.PHP_EOL, FILE_APPEND);
	}
}

?>
<?php 
/*This is the footer */
include('templates/footer.html');
?>
