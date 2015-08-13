<?php

require_once("db.php");
if (strlen($_GET["hostname"]) < 2) {
	die("Invalid hostname.");
}


// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$ip = $_GET["ip"];
$hostname = $_GET["hostname"];
$cpu = $_GET["cpu"];
$memory = $_GET["memory"];
$bandwidth = $_GET["bandwidth"];
$date = date('Y-m-d');
$time = date('H:i:s');

	// Created a new one
	$sql = "INSERT INTO statuses (date, time, hostname, ip, cpu, memory, bandwidth) VALUES ('$date', '$time', '$hostname', '$ip', '$cpu', '$memory', '$bandwidth')";

	if ($conn->query($sql) === TRUE) {
		echo "Status added. SQL $sql";
	} else {
		echo "Error: " . $sql . "<br>" . $conn->error;
	}


$conn->close();

?>