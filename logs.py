import win32evtlog
import sqlite3
import json

# Function to create the database and logs table
def create_db():
    try:
        conn = sqlite3.connect('logs.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (EventID int, TimeGenerated text, EventType text, 
                      LogSource text, SourceName text, StringInserts text)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

class SIEMLogCollector:
    def __init__(self):
        self.log_sources = []

    def add_log_source(self, log_source):
        self.log_sources.append(log_source)

    def collect_logs(self, log_count=10):
        all_logs = []

        for log_source in self.log_sources:
            logs = []
            try:
                # Connect to the Event Log
                hand = win32evtlog.OpenEventLog(None, log_source)

                # Read the last specified number of entries from the log
                flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
                total = win32evtlog.GetNumberOfEventLogRecords(hand)

                events = win32evtlog.ReadEventLog(hand, flags, 0)

                for idx, event in enumerate(events):
                    if idx >= log_count:
                        break

                    log_entry = {
                        "EventID": event.EventID,
                        "TimeGenerated": event.TimeGenerated.Format(),
                        "EventType": event.EventType,
                        "LogSource": log_source,  # Add the log source name
                        "SourceName": event.SourceName,
                        "StringInserts": event.StringInserts,
                    }
                    logs.append(log_entry)

                win32evtlog.CloseEventLog(hand)
            except Exception as e:
                print(f"Error collecting logs from {log_source}: {e}")
            
            all_logs.extend(logs)

        return all_logs

def store_logs(logs):
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    for log in logs:
        # Convert StringInserts list to string if not None
        string_inserts = ','.join(log['StringInserts']) if log['StringInserts'] else ''
        c.execute('INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)', 
                  (log['EventID'], log['TimeGenerated'], log['EventType'], 
                   log['LogSource'], log['SourceName'], string_inserts))
    conn.commit()
    conn.close()

def collect_and_append_powershell_logs():
    powershell_logs = []

    try:
        hand = win32evtlog.OpenEventLog(None, "Windows PowerShell")
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        for event in events:
            log_entry = {
                "EventID": event.EventID,
                "TimeGenerated": event.TimeGenerated.Format(),
                "EventType": event.EventType,
                "LogSource": "Windows PowerShell",
                "SourceName": event.SourceName,
                "StringInserts": event.StringInserts,
            }
            powershell_logs.append(log_entry)

        win32evtlog.CloseEventLog(hand)
    except Exception as e:
        print(f"Error collecting PowerShell logs: {e}")

    return powershell_logs

def main():
    create_db()  # Initialize the database
    log_collector = SIEMLogCollector()

    # Add log sources
    log_collector.add_log_source("System")
    log_collector.add_log_source("Application")
    log_collector.add_log_source("Perimeter Device Logs")
    log_collector.add_log_source("Windows Event Logs")
    log_collector.add_log_source("Endpoint Logs")
    log_collector.add_log_source("Proxy Logs")
    log_collector.add_log_source("IoT Logs")
    # Add other important log sources as needed...

    # Collect logs
    logs = log_collector.collect_logs(log_count=10)

    # Collect and append PowerShell logs
    powershell_logs = collect_and_append_powershell_logs()
    logs.extend(powershell_logs)

    # Store logs in a single file
    store_logs(logs)

if __name__ == "__main__":
    main()
