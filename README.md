# Serenity - IoT Environmental Monitoring System

Serenity is a Raspberry Pi and Sense HAT based IoT project that monitors indoor environmental comfort and provides local and remote feedback.

Link to Dashboard: http://<ip_Address>/serenity-api/index.html

## Features
- Temperature and humidity monitoring
- Local comfort classification
- Sense HAT LED matrix status display
- PHP + MySQL data storage
- AllThingsTalk MQTT integration
- Remote alert toggle through web dashboard

## Technologies
- Python
- Raspberry Pi
- Sense HAT
- PHP
- MySQL
- JavaScript
- AllThingsTalk Maker

## Main Files
## Main Files
- `serenity_dual_send.py` - main application script handling sensor data collection, processing, LED matrix display, API communication, MQTT integration, and remote actuation
- `add_reading.php` - API endpoint for storing sensor data in the MySQL database
- `latest_reading.php` - API endpoint for retrieving the most recent sensor reading
- `control.php` - API endpoint for handling remote alert toggle (actuation)
- `index.html` - web dashboard for displaying live data and controlling the system

## Notes
- Designed as a proof-of-concept IoT system
- Runs on Raspberry Pi OS
- Uses a custom dashboard and cloud dashboard
