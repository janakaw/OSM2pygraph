<?php //index.php
/* This is the home page for this site. It uses templates to create the layout. */
//define('TITLE', 'Welcome !');
include('templates/header.html');
?>
<?php
$search_root='/home4/taxidrive/';
$log_file = '/home4/taxidrive/taxidata.log';

read_all($search_root, $log_file);

print '<p>Over</p>';


function insert_file($path_id,$file_id, $dir_id, $dbc,$log_file){

	$insert_query="LOAD DATA LOCAL INFILE '".$path_id."'
			
			INTO TABLE tdrive

   			FIELDS TERMINATED BY ','
        
			LINES TERMINATED BY '\r\n'

			(taxi_id, date_time, longitude, latitude)

			SET dir_id = '".$dir_id."';";
	
	if(mysql_query($insert_query,$dbc)){

		return "TRUE";
						
	}else{
		print('<p>'.$path_id.'</p>');
		print('<p style="color: red;">not inserted!!!'.mysql_error().'</p>');
		print('<p>Insert error: taxi_id:'.$file_id.' dir:'.$dir_id.'</p>');
		return "FALSE";						
	}

}

function read_all($search_root,$log_file){

	if(!file_exists($log_file)){
		print '<p>file error</p>';
		return;	
	}	

	$dbc=connect_taxidata_db($log_file);
	print '<p>connected</p>';

	set_time_limit(36000);
	file_put_contents($log_file, 'start:'.PHP_EOL, FILE_APPEND);

	ini_set('auto_detect_line_endings',1);
	$contents_root=scandir($search_root);
	foreach ($contents_root as $dir_id) {
		$dir_path = $search_root.$dir_id.'/';
		print '<p>'.$dir_path.'</p>';

		if(is_dir($dir_path) AND substr($item_root,0,1) !='.' ){
			$contents_next=scandir($dir_path);
			$i=0;
			foreach ($contents_next as $file_id) {
				$file_path = $dir_path.$file_id; 	
				
				if( (is_file($file_path)) AND (substr($file_id,0,1) !='.') ){
					
					$ret = insert_file($file_path, $file_id, $dir_id, $dbc,$log_file);

					if($ret == "FALSE"){
						file_put_contents($log_file, 'Error: taxi:'.$file_id.' dir:'.$dir_id.PHP_EOL, FILE_APPEND);
						print '<p>Error taxi: '.$taxi_id.' dir: '.$dir_id.'</p>';
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


function connect_taxidata_db($log_file){

	$db_name="taxidata";

	if($dbc = mysql_connect('localhost', 'janakawc_taxi', '*******')){
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
