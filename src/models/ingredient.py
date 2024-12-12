import sqlite3

def get_all_ingredients():
    conn = sqlite3.connect("meal_cost.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ingredients")
    ingredients = cursor.fetchall()
    conn.close()
    return ingredients

def add_ingredient(name, cost):
    conn = sqlite3.connect("meal_cost.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ingredients (name, cost) VALUES (?, ?)", (name, cost))
    conn.commit()
    conn.close()