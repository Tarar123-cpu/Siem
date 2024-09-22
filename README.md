## SIEM Solution - Python Flask

## Project Overview

This project is a Security Information and Event Management (SIEM) solution built using Python Flask. It is designed to monitor and analyze security logs, detect threats, and provide real-time insights into security incidents. The solution offers a dashboard displaying critical information about connected agents and their activities.

## Features

1. Dashboard Overview: Displays key metrics and information about the connected agents.
2. Agent Management: Ability to monitor and manage agent activities in real time.
3. Log Monitoring: Continuous tracking of logs for security events and alerts.
4. Alert System: Detects malicious activities and provides alerts.
5. Graphical Representation: Data is visualized through graphs and charts for easier analysis.
6. User Authentication: Secure login and signup system for managing users.

## Installation and Setup

Prerequisites
Ensure you have the following installed:

Python 3.x
Flask
Virtual Environment (optional but recommended)

## Project Structure

Siem/
│
├── app/                    # Contains the Flask application files
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # HTML templates
│   ├── views.py             # View routes for the application
│   └── models.py            # Database models
│
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── run.py                   # Entry point to start the application

## Usage
Login/Signup: Users can sign in or create an account to access the dashboard.
Dashboard: View real-time data of connected agents, malicious alerts, and logs.
Agents: View the list of agents connected and their current status.
Logs: Check the security logs and filter them based on certain criteria.
Alerts: See the generated alerts for potential security incidents.

## Technologies Used
Python Flask: Backend framework for building the web application.
HTML/CSS/JavaScript: Frontend for the user interface.
SQLite: Database used for storing logs and user information.
Chart.js/D3.js: For creating dynamic graphs and charts.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
