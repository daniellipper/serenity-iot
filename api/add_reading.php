<?php
header("Content-Type: application/json");

$host = "localhost";
$dbname = "serenity";
$username = "root";
$password = ""; // default XAMPP password is usually blank

$conn = new mysqli($host, $username, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode([
        "success" => false,
        "message" => "Database connection failed: " . $conn->connect_error
    ]));
}

$raw_temp = $_POST['raw_temp'] ?? null;
$corrected_temp = $_POST['corrected_temp'] ?? null;
$humidity = $_POST['humidity'] ?? null;
$status = $_POST['status'] ?? null;

if ($raw_temp === null || $corrected_temp === null || $status === null) {
    echo json_encode([
        "success" => false,
        "message" => "Missing required fields"
    ]);
    exit;
}

$stmt = $conn->prepare("INSERT INTO readings (raw_temp, corrected_temp, humidity, status) VALUES (?, ?, ?, ?)");
$stmt->bind_param("ddds", $raw_temp, $corrected_temp, $humidity, $status);

if ($stmt->execute()) {
    echo json_encode([
        "success" => true,
        "message" => "Reading stored successfully"
    ]);
} else {
    echo json_encode([
        "success" => false,
        "message" => "Insert failed: " . $stmt->error
    ]);
}

$stmt->close();
$conn->close();
?>
