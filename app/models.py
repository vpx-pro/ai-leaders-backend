import sqlite3

def insert_quote(name, title, quote, image, source):
    word_count = len(quote.split())
    conn = sqlite3.connect("leaders.db")
    c = conn.cursor()
    c.execute("""INSERT INTO leader_quotes
        (name, title, quote, image, source, word_count)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (name, title, quote, image, source, word_count)
    )
    conn.commit()
    conn.close()
