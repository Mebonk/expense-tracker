from pydantic import BaseModel

import sqlite3

from fastapi import FastAPI

app = FastAPI()

conn = sqlite3.connect("expenses.db")

cursor = conn.cursor()

class Expense(BaseModel):
    text: str
    amount: float

cursor.execute ('''
CREATE TABLE IF NOT EXISTS expenses (
    text TEXT,
    amount REAL
)''')

conn.commit()

@app.get("/") #  @app.get("/") means: "when someone visits the lobby, run root()"
def root():
    return {"Hello": "World"}

@app.post("/expenses")
def create_expense(expense: Expense):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO expenses VALUES (?, ?)",
    (expense.text, expense.amount)
    )
               
    conn.commit()
    return {"message": "Expense created!"}

@app.get("/expenses")
def get_expense():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    return cursor.fetchall()
    