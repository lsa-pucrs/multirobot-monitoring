<?php

require_once("db.php");
// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT DISTINCT hostname, ip FROM vms order by ip ASC";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo $row["ip"] . "\t" . $row["hostname"] . "\n";
    }
} else {
    echo "0 results";
}
$conn->close();
?>