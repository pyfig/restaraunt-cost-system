import sqlite3

def calculate_selling_price(cost):
    return round(cost * 1.5)

def calculate_meal_cost(meal_id):
    conn = sqlite3.connect("meal_cost.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT SUM(i.cost * mi.quantity)
    FROM ingredients i
    JOIN meal_ingredients mi ON i.id = mi.ingredient_id
    WHERE mi.meal_id = ?
    """, (meal_id,))
    total_cost = cursor.fetchone()[0] or 0
    conn.close()
    return total_cost