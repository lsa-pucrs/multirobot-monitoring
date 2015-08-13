<?php

require_once("db.php");
if (strlen($_GET["hostname"]) < 2) {
	die("Invalid hostname. VM was not added on Nagios.");
}


// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$ip = $_GET["ip"];
$hostname = $_GET["hostname"];
$date = date('Y-m-d');
$time = date('H:i:s');

	// Remove old instances
	$sql = "DELETE from vms WHERE hostname = '$hostname'";

	if ($conn->query($sql) === TRUE) {
		echo "Old instances removed: IP: $ip Hostname: $hostname";
	} else {
		echo "Error: " . $sql . "<br>" . $conn->error;
	}

	// Created a new one
	$sql = "INSERT INTO vms (hostname, ip, date, time) VALUES ('$hostname', '$ip', '$date', '$time')";

	if ($conn->query($sql) === TRUE) {
		echo "VM added: IP: $ip Hostname: $hostname";
	} else {
		echo "Error: " . $sql . "<br>" . $conn->error;
	}


$conn->close();

/////////////////////////////////////////////////////
// Write nagios file
$myfile = fopen("template.cfg", "r") or die("Unable to open file!");
$template = fread($myfile,filesize("template.cfg"));
fclose($myfile);

//echo $template;

$template = str_replace("[hostname]", $hostname, $template);
$template = str_replace("[ip]", $ip, $template);

//echo $template;

$file_cfg = "./cfg/" . $hostname . ".cfg";
//echo $file_cfg;
$myfile = fopen($file_cfg, "w") or die("Unable to open file!");
fwrite($myfile, $template);
fclose($myfile);

?>