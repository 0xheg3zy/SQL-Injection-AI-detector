import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

c.execute("INSERT INTO users VALUES (NULL, 'admin', 'admin123')")
c.execute("INSERT INTO users VALUES (NULL, 'user', 'user123')")

conn.commit()
conn.close()

