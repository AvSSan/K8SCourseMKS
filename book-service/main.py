from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str

DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            return conn
        except Exception as e:
            print(f"Waiting for DB... Error: {e}")
            retries -= 1
            time.sleep(2)
    return None

@app.get("/")
def read_root():
    return {"Service": "Book Service (Python)", "Status": "Running"}

@app.get("/books")
def get_books():
    conn = get_db_connection()
    if not conn: raise HTTPException(status_code=500, detail="DB connection failed")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM books;")
    items = cur.fetchall()
    conn.close()
    return items

@app.post("/books")
def add_book(book: Book):
    conn = get_db_connection()
    if not conn: raise HTTPException(status_code=500, detail="DB connection failed")
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author) VALUES (%s, %s) RETURNING id;", (book.title, book.author))
    new_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return {"id": new_id, **book.dict()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)