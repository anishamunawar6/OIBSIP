import sqlite3
from datetime import datetime


# Database connection
def create_database():
    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


# BMI record save karna
def save_record(name, weight, height, bmi, category):
    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO bmi_history 
        (name, weight, height, bmi, category, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, 
    (name, weight, height, bmi, category, date))

    conn.commit()
    conn.close()


# History dekhna
def get_records():
    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bmi_history")

    records = cursor.fetchall()

    conn.close()

    return records

def get_bmi_data():

    conn = sqlite3.connect("bmi_records.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT date, bmi FROM bmi_history"
    )

    data = cursor.fetchall()

    conn.close()

    return data