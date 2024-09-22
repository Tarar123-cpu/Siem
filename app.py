from flask import Flask, render_template, jsonify
import json
import sqlite3
from logs import SIEMLogCollector, store_logs, collect_and_append_powershell_logs
import os.path

app = Flask(__name__)

def load_logs_from_database():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM logs')
    logs = [{'EventID': row[0], 'TimeGenerated': row[1], 'EventType': row[2],
             'LogSource': row[3], 'SourceName': row[4], 'StringInserts': row[5].split(',')}
            for row in c.fetchall()]
    conn.close()
    return logs

def generate_chart_data(logs):
    event_counts = {}  # Counts of each event type by month
    error_counts = {}  # Counts of errors by month
    warning_counts = {}  # Counts of warnings by month

    for log in logs:
        month = log["TimeGenerated"].split("-")[1]  # Assuming format YYYY-MM
        event_type = log["EventType"]

        if month not in event_counts:
            event_counts[month] = {}
        if event_type not in event_counts[month]:
            event_counts[month][event_type] = 0
        event_counts[month][event_type] += 1

        if event_type == "Error":
            if month not in error_counts:
                error_counts[month] = 0
            error_counts[month] += 1
        elif event_type == "Warning":
            if month not in warning_counts:
                warning_counts[month] = 0
            warning_counts[month] += 1

    labels = sorted(event_counts.keys())
    dataset = []
    # Prepare datasets for each type
    for event_type in ["Error", "Warning", "Event"]:  # Add more types if needed
        dataset.append({
            "label": f"{event_type} Counts",
            "data": [event_counts[month].get(event_type, 0) for month in labels],
            "backgroundColor": f"rgba({255 if event_type == 'Error' else 54 if event_type == 'Warning' else 75}, {99 if event_type == 'Error' else 162 if event_type == 'Warning' else 192}, {132 if event_type == 'Error' else 235 if event_type == 'Warning' else 192}, 0.2)",
            "borderColor": f"rgba({255 if event_type == 'Error' else 54 if event_type == 'Warning' else 75}, {99 if event_type == 'Error' else 162 if event_type == 'Warning' else 192}, {132 if event_type == 'Error' else 235 if event_type == 'Warning' else 192}, 1)",
            "borderWidth": 1
        })

    return {"labels": labels, "datasets": dataset}

@app.route('/')
def index():
    logs = load_logs_from_database()
    return render_template('index.html', logs=logs, len = len(logs))

@app.route('/charts')
def charts():
    logs = load_logs_from_database()
    chart_data = generate_chart_data(logs)
    return render_template('charts.html', chart_data=chart_data)

@app.route('/collect_logs')
def collect_logs_endpoint():
    # Collect logs
    log_collector = SIEMLogCollector()
    logs = log_collector.collect_logs()
    store_logs(logs)
    return "Logs collected and stored successfully!"

if __name__ == '__main__':
    app.run(debug=True)
