import sqlite3

def create_db():
    conn = sqlite3.connect("meal_cost.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cost REAL NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meal_ingredients (
        meal_id INTEGER NOT NULL,
        ingredient_id INTEGER NOT NULL,
        quantity REAL NOT NULL,
        FOREIGN KEY (meal_id) REFERENCES meals (id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
    )
    """)
    conn.commit()
    conn.close()
