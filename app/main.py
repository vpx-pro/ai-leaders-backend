from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return sqlite3.connect("leaders.db")

@app.on_event("startup")
def startup():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leader_quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        title TEXT,
        quote TEXT,
        image TEXT,
        source TEXT,
        word_count INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

@app.get("/api/leaders")
def get_leaders():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT name, title, quote, image, source FROM leader_quotes
                 ORDER BY timestamp DESC LIMIT 10""")
    rows = c.fetchall()
    conn.close()
    return [
        {"name": r[0], "title": r[1], "quote": r[2], "image": r[3], "source": r[4]}
        for r in rows
    ]
