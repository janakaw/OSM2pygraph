<?php 
/**
 *
 * @author     Janaka Seneviratne
 * @copyright  2014 Janaka Seneviratne
 */
include('templates/header.html');
?>
<?php

print '<div><ul>';
print '<li><a href="http://www.janakaw.com/programming/gps_distant_calculator.php">GPS distant calculator</a></li>';
print '</ul></div>';

$search_path='programming';
print '<p>For the time being some samples from Google Map API3. Watch out this space for more stuff...</p>';
print '<div><ul>';
$contents = scandir($search_path);

foreach ($contents as $item){
	$parts = explode(".",$item);
	if(substr($item,0,1) !='.' && is_file($search_path.'/'.$item)){
		print '<li><a href="http://www.janakaw.com/programming/'.$item.'">'.$parts[0].'</a></li>';
	}
}

/*print '</ul></div>';

print '<p>Some themes...</p>';
$csssearch_path='programming/css';
print '<div><ul>';
$contents = scandir($csssearch_path);

foreach ($contents as $item){
	if(substr($item,0,1) !='.' && is_dir($csssearch_path.'/'.$item)){
		print '<li><a href="http://www.janakaw.com/programming/css/'.$item.'/index.html">'.$item.'</a></li>';
	}
}

print '</ul></div>';*/

?>
<?php 
/*This is the footer */
include('templates/footer.html');
?>
