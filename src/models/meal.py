from db.database import create_db
import sqlite3

def get_all_meals():
    conn = sqlite3.connect("meal_cost.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meals")
    meals = cursor.fetchall()
    conn.close()
    return meals

def add_meal(name, ingredients):
    conn = sqlite3.connect("meal_cost.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO meals (name) VALUES (?)", (name,))
    meal_id = cursor.lastrowid
    for ing_id, quantity in ingredients:
        cursor.execute("INSERT INTO meal_ingredients (meal_id, ingredient_id, quantity) VALUES (?, ?, ?)", (meal_id, ing_id, quantity))
    conn.commit()
    conn.close()
