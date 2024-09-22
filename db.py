import sqlite3

def create_db():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (EventID int, TimeGenerated text, EventType text, 
                  LogSource text, SourceName text, StringInserts text)''')
    conn.commit()
    conn.close()
