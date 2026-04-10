<?php
header("Content-Type: application/json");

$conn = new mysqli("localhost", "root", "", "serenity");

if ($conn->connect_error) {
    die(json_encode(["success" => false]));
}

// GET current state
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $result = $conn->query("SELECT alert_enabled FROM control_settings WHERE id = 1");
    $row = $result->fetch_assoc();

    echo json_encode([
        "success" => true,
        "alert_enabled" => (int)$row['alert_enabled']
    ]);
}

// UPDATE state
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $alert_enabled = $_POST['alert_enabled'];

    $stmt = $conn->prepare("UPDATE control_settings SET alert_enabled=? WHERE id=1");
    $stmt->bind_param("i", $alert_enabled);
    $stmt->execute();

    echo json_encode(["success" => true]);
}

$conn->close();
?>