# build_db.py (Corrected Version)
import sqlite3
import csv

DB_NAME = 'game.db'
CSV_NAME = 'scenarios.csv'

def create_database():
    """Reads the CSV and creates/populates the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS scenarios")

    cursor.execute("""
    CREATE TABLE scenarios (
        scenario_id INTEGER PRIMARY KEY,
        market_type TEXT,
        pair TEXT,
        image_filename TEXT,
        ta_text TEXT,
        fa_text TEXT,
        correct_answer TEXT,
        win_amount INTEGER,
        loss_amount INTEGER,
        win_feedback TEXT,
        loss_feedback TEXT,
        time_limit_seconds INTEGER
    )
    """)

    with open(CSV_NAME, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
            INSERT INTO scenarios VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                # Convert the following values from text to numbers (integers)
                int(row['scenario_id']), 
                row['market_type'], 
                row['pair'],
                row['image_filename'], 
                row['ta_text'], 
                row['fa_text'],
                row['correct_answer'], 
                int(row['win_amount']), 
                int(row['loss_amount']),
                row['win_feedback'], 
                row['loss_feedback'], 
                int(row['time_limit_seconds'])
            ))

    conn.commit()
    conn.close()
    print(f"✅ Database '{DB_NAME}' created successfully from '{CSV_NAME}'!")

if __name__ == "__main__":
    create_database()