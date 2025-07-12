import sqlite3

DB_NAME = "cbtc_logs.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    log_level TEXT,
    log_message TEXT,
    fault_type TEXT
)
""")

conn.commit()
conn.close()

print("✅ logs table created successfully in cbtc_logs.db")
