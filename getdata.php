<?php
$servername = "localhost";
$username = "datalog";
$password = "diViqIgan1G3";
$dbname = "datalogger";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$query = "SELECT * FROM `datalogger`.`temperature` WHERE TIMESTAMP > date_sub(now(), INTERVAL 24 hour)";
$data = $conn->query($query);

//loop through the returned data
$cputemp = array();
foreach ($data as $row) {
  $cputemp[] = $row;
}

$data->close();
$conn->close();

print json_encode($cputemp);
?>

