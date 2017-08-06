<?php 
/**
 *
 * @author     Janaka Seneviratne
 * @copyright  2014 Janaka Seneviratne
 */
define('TITLE', 'Login to view geolife trajectories');
include('templates/header.html');

print '<h2>Login Form</h2>';

if($_SERVER['REQUEST_METHOD'] == 'POST'){
	
	if( (!empty($_POST['user_name'])) && (!empty($_POST['password'])) ){
		
		if( (strtolower($_POST['user_name']) == 'janakaw') && 
			($_POST['password'] == 'test') ){
				session_start();
				$_SESSION['user_name']=$_POST['user_name'];
				$_SESSION['iloggedin'] = 'yes';				
				ob_end_clean();
				header('Location: geolife_draw_trajectory.php');
				exit();
				
			} else { // check for correct email and password - else
				
				print '<br /> Go back and try again.</p>';
				
			} // check for correct email and password - end of if else
		
	} else { // check for empty email and password - else
		
		print '<p>Please make sure you enter both a user name and a password <br />
		Go back and try again.</p>';
		
	}// check for empty email and password - end of if else

} else {// check for POST method - else /
	//Display the form.
	
	print '<form action="logingeo.php" method="post">
	<p>user name: <input type="text" name="user_name" size="20" /></p>
	<p>Password:  <input type="password" name="password" size="20" /></p>
	<p><input type="submit" name="submit" value="Log In!" /></p>
	</form>';
	
}// check for POST method - done

include('templates/footer.html');

?>
