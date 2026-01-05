import sqlite3

conn = sqlite3.connect("expenses.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

c.execute("PRAGMA table_info(expenses)")
columns = [info[1] for info in c.fetchall()]
if "user_id" not in columns:
    c.execute("ALTER TABLE expenses ADD COLUMN user_id INTEGER")

conn.commit()
conn.close()

print("Database setup complete!")

