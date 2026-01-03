import sqlite3

conn = sqlite3.connect("schedule.db")
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        date TEXT,
        content TEXT
    )
    """)
    conn.commit()

def add_schedule(date, content):
    cur.execute("INSERT INTO schedule VALUES (?, ?)", (date, content))
    conn.commit()

def get_schedule(date):
    cur.execute("SELECT content FROM schedule WHERE date=?", (date,))
    return cur.fetchall()

def delete_schedule(date, content):
    cur.execute(
        "DELETE FROM schedule WHERE date=? AND content=?",
        (date, content)
    )
    conn.commit()

def update_schedule(date, old, new):
    cur.execute(
        "UPDATE schedule SET content=? WHERE date=? AND content=?",
        (new, date, old)
    )
    conn.commit()
