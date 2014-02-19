<?php //login.php
define('TITLE', 'Login to view geolife trajectories');
include('templates/header.html');
?>
<?php

print '<h3>Trajectories on the map</h3>';
print '<div><ul>';
print '<li><a href="http://www.janakaw.com/geolife_draw_trajectory.php">Geolife</a></li>';
print '</ul></div>';
print '<p>Click on the above link to view geolife trajectories on Google Maps. It works fine on Mozilla Firefox, Checking some issues found on other browsers..</p>';
print '<p>The geolife data set is provided by <a href="http://research.microsoft.com/en-us/downloads/b16d359d-d164-469e-9fd4-daa38f2b2e13/">Microsoft Research</a> under the terms of its <a href="http://research.microsoft.com/en-us/downloads/b16d359d-d164-469e-9fd4-daa38f2b2e13/MSR-LA%20GPS%20Trajectories.txt">license</a>.';
?>
<?php
include('templates/footer.html');
?>
