<?php 
/**
 *
 * @author     Janaka Seneviratne
 * @copyright  2014 Janaka Seneviratne
 */
print( '<!DOCTYPE html>
<html>
  <head>
	<h2>GeoLife</h2>
	<script language="javascript" type="text/javascript">	
	</script>
  </head>
  <body onload="initialize()">
    <div id=1><form action="geolife_draw_trajectory.php"><input type="text" name="user" value="'.$_REQUEST['user'].'" /><input type="submit" value="Draw Trajectory" />');

print('<table border="0">
   <tr><td><div style="color:#FFFFFF">aaaaaaaaaaa</div></td><td>');

print_trajectories_list();

print('</td></tr>');

print ('</table></form></div>');	
 
//print_debug(); 

print('</body>
</html>');


function print_debug(){
		print ('<p><textarea cols="50" rows="4" name="debug">'.$_REQUEST['user']."\r\n"."SELECT DISTINCT(file_id) FROM geolife WHERE user_id='".$_REQUEST['user']."'".'</textarea></p>');
}

function print_trajectories_list(){

	$dbc = connect_geolife_db();

	$result = mysql_query("SELECT DISTINCT(file_id) FROM geolife WHERE user_id='".$_REQUEST['user']."'");

	$count = 0;
	print('<select name="trajectory">');
	while($row = mysql_fetch_array($result))
  	{	
		$count++;
		//if($count%20==0)
		//	print('</td><td>');	
		print '<option name="trajectory" value="'.$row[0].'" >'.$row[0].'</option><br/>';
  	}
	print("</select>");
	close_connection($dbc);

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
