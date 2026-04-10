<?php
header("Content-Type: application/json");

// DB connection
$conn = new mysqli("localhost", "root", "", "serenity");

if ($conn->connect_error) {
    die(json_encode([
        "success" => false,
        "message" => "Database connection failed"
    ]));
}

// Get latest reading
$sql = "SELECT * FROM readings ORDER BY id DESC LIMIT 1";
$result = $conn->query($sql);

if ($result && $row = $result->fetch_assoc()) {
    echo json_encode([
        "success" => true,
        "data" => $row
    ]);
} else {
    echo json_encode([
        "success" => false,
        "message" => "No data found"
    ]);
}

$conn->close();
?>
