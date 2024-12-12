import tkinter as tk
from tkinter import messagebox
import math
import sqlite3

# Database setup
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

# Utility Functions
def calculate_selling_price(cost):
    return math.ceil(cost * 1.5 / 100.0) * 100

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

# Main Application
class MealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система расчета стоимости блюд")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        create_db()
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for buttons on the left
        left_frame = tk.Frame(self.root)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Create buttons on the left side
        tk.Button(left_frame, text="Добавить блюдо", command=self.add_meal_window).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Добавить ингредиенты", command=self.add_ingredient_window).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Список блюд", command=self.view_meals).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Список ингредиентов", command=self.view_ingredients).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Удалить блюдо", command=self.delete_meal_window).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Удалить ингредиенты", command=self.delete_ingredient_window).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Очистить ингредиенты", command=self.clear_ingredients).pack(fill='x', pady=5)

        # Create a frame for displaying meal list on the right
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def view_meals(self):
        # Clear any existing content in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Create a label for the meal list
        meal_list_label = tk.Label(self.right_frame, text="Список блюд", font=("Arial", 16, "bold"))
        meal_list_label.pack(pady=10)

        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM meals")
        meals = cursor.fetchall()

        for i, meal in enumerate(meals):
            meal_id, name = meal
            cost = calculate_meal_cost(meal_id)
            selling_price = calculate_selling_price(cost)

            meal_label = tk.Label(self.right_frame, text=f"ID: {meal_id} | {name} | Себестоимость: {cost:.2f} | Цена продажи: {selling_price}")
            meal_label.pack(pady=5)

        conn.close()
    
    def view_ingredients(self):
        # Clear any existing content in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Create a label for the ingredient list
        ingredient_list_label = tk.Label(self.right_frame, text="Список ингредиентов", font=("Arial", 16, "bold"))
        ingredient_list_label.pack(pady=10)

        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, cost FROM ingredients")
        ingredients = cursor.fetchall()

        for i, ingredient in enumerate(ingredients):
            ingredient_id, name, cost = ingredient
            ingredient_label = tk.Label(self.right_frame, text=f"ID: {ingredient_id} | {name} | Себестоимость: {cost:.2f}")
        ingredient_label.pack(pady=5)

        conn.close()


    def add_meal_window(self):
        window = tk.Toplevel(self.root)
        window.title("Добавить блюдо")

        tk.Label(window, text="Название блюда:").grid(row=0, column=0)
        name_entry = tk.Entry(window)
        name_entry.grid(row=0, column=1)

        tk.Label(window, text="Выберите ингредиенты:").grid(row=1, column=0, columnspan=2)

        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM ingredients")
        ingredients = cursor.fetchall()
        conn.close()

        ingredient_vars = []
        for i, (ing_id, ing_name) in enumerate(ingredients):
            var = tk.DoubleVar()
            tk.Label(window, text=ing_name).grid(row=2 + i, column=0)
            tk.Entry(window, textvariable=var).grid(row=2 + i, column=1)
            ingredient_vars.append((ing_id, var))

        def save_meal():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название блюда.")
                return

            conn = sqlite3.connect("meal_cost.db")
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM meals WHERE name = ?", (name,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Ошибка", "Блюдо с таким названием уже существует.")
                conn.close()
                return

            cursor.execute("INSERT INTO meals (name) VALUES (?)", (name,))
            meal_id = cursor.lastrowid

            for ing_id, var in ingredient_vars:
                try:
                    quantity = float(var.get())
                    if quantity > 0:
                        cursor.execute("INSERT INTO meal_ingredients (meal_id, ingredient_id, quantity) VALUES (?, ?, ?)", (meal_id, ing_id, quantity))
                except ValueError:
                    pass

            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Блюдо добавлено!")
            window.destroy()

        tk.Button(window, text="Сохранить", command=save_meal).grid(row=2 + len(ingredients), columnspan=2)

    def add_ingredient_window(self):
        window = tk.Toplevel(self.root)
        window.title("Добавить ингредиенты")

        tk.Label(window, text="Название ингредиента:").grid(row=0, column=0)
        tk.Label(window, text="Себестоимость:").grid(row=1, column=0)

        name_entry = tk.Entry(window)
        cost_entry = tk.Entry(window)

        name_entry.grid(row=0, column=1)
        cost_entry.grid(row=1, column=1)

        def save_ingredient():
            name = name_entry.get().strip()
            try:
                cost = float(cost_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", "Себестоимость должна быть числом.")
                return

            if name and cost > 0:
                conn = sqlite3.connect("meal_cost.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ingredients (name, cost) VALUES (?, ?)", (name, cost))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Ингредиент добавлен!")
                window.destroy()
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля корректно.")

        tk.Button(window, text="Сохранить", command=save_ingredient).grid(row=2, columnspan=2)

    def delete_meal_window(self):
        window = tk.Toplevel(self.root)
        window.title("Удалить блюдо")

        tk.Label(window, text="Выберите блюдо:").grid(row=0, column=0)

        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM meals")
        meals = cursor.fetchall()
        conn.close()

        meal_var = tk.StringVar()
        for i, meal in enumerate(meals):
            meal_id, name = meal
            tk.Radiobutton(window, text=f"ID: {meal_id} | {name}", variable=meal_var, value=meal_id).grid(row=i + 1, column=0)

        def delete_meal():
            meal_id = meal_var.get()
            if meal_id:
                conn = sqlite3.connect("meal_cost.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM meals WHERE id=?", (meal_id,))
                cursor.execute("DELETE FROM meal_ingredients WHERE meal_id=?", (meal_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Блюдо удалено!")
                window.destroy()

        tk.Button(window, text="Удалить", command=delete_meal).grid(row=len(meals) + 1, column=0)

    def delete_ingredient_window(self):
        window = tk.Toplevel(self.root)
        window.title("Удалить ингредиенты")

        tk.Label(window, text="Выберите ингредиент:").grid(row=0, column=0)

        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM ingredients")
        ingredients = cursor.fetchall()
        conn.close()

        ingredient_var = tk.StringVar()
        for i, ingredient in enumerate(ingredients):
            ing_id, name = ingredient
            tk.Radiobutton(window, text=f"ID: {ing_id} | {name}", variable=ingredient_var, value=ing_id).grid(row=i + 1, column=0)

        def delete_ingredient():
            ingredient_id = ingredient_var.get()
            if ingredient_id:
                conn = sqlite3.connect("meal_cost.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM ingredients WHERE id=?", (ingredient_id,))
                cursor.execute("DELETE FROM meal_ingredients WHERE ingredient_id=?", (ingredient_id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Ингредиент удален!")
                window.destroy()

        tk.Button(window, text="Удалить", command=delete_ingredient).grid(row=len(ingredients) + 1, column=0)

    def clear_ingredients(self):
        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ingredients")
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Все ингредиенты удалены!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MealApp(root)
    root.mainloop()
