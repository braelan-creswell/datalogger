<?php
header('Content-Type: application/json');
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
  $cputemp[] = $row; //send row data to array
}

$data->close(); //free query memory
$conn->close(); //disconnect from MySQL

print json_encode($cputemp); //return data as a json file.
?>

