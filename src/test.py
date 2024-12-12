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
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        create_db()
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Добавить блюдо", command=self.add_meal_window).pack(pady=10)
        tk.Button(self.root, text="Добавить ингредиенты", command=self.add_ingredient_window).pack(pady=10)
        tk.Button(self.root, text="Список блюд", command=self.view_meals).pack(pady=10)
        tk.Button(self.root, text="Список ингредиентов", command=self.view_ingredients).pack(pady=10)
        tk.Button(self.root, text="Удалить блюдо", command=self.delete_meal_window).pack(pady=10)
        tk.Button(self.root, text="Удалить ингредиенты", command=self.delete_ingredient_window).pack(pady=10)
        tk.Button(self.root, text="Очистить все данные", command=self.clear_all_data).pack(pady=10)

    def add_meal_window(self):
        window = tk.Toplevel(self.root)
        window.title("Добавить блюдо")
        window.geometry("600x400")

        tk.Label(window, text="Название блюда:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(window, text="Выберите ингредиенты:").grid(row=1, column=0, columnspan=2, pady=10)

        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM ingredients")
        ingredients = cursor.fetchall()
        conn.close()

        ingredient_vars = []
        quantity_vars = []
        for i, (ing_id, ing_name) in enumerate(ingredients):
            var = tk.IntVar()
            quantity_var = tk.DoubleVar()
            tk.Checkbutton(window, text=ing_name, variable=var).grid(row=2 + i, column=0, padx=10, sticky="w")
            tk.Entry(window, textvariable=quantity_var).grid(row=2 + i, column=1, padx=10)
            ingredient_vars.append((ing_id, var, quantity_var))

        def save_meal():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название блюда.")
                return

            selected_ingredients = [(ing_id, quantity_var.get()) for ing_id, var, quantity_var in ingredient_vars if var.get()]

            if not selected_ingredients:
                messagebox.showerror("Ошибка", "Выберите хотя бы один ингредиент.")
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

            for ing_id, quantity in selected_ingredients:
                if quantity > 0:
                    cursor.execute("INSERT INTO meal_ingredients (meal_id, ingredient_id, quantity) VALUES (?, ?, ?)", (meal_id, ing_id, quantity))

            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Блюдо добавлено!")
            window.destroy()

        tk.Button(window, text="Сохранить", command=save_meal).grid(row=2 + len(ingredients), columnspan=2, pady=10)

    def add_ingredient_window(self):
        window = tk.Toplevel(self.root)
        window.title("Добавить ингредиенты")
        window.geometry("400x200")

        tk.Label(window, text="Название ингредиента:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(window, text="Себестоимость:").grid(row=1, column=0, padx=10, pady=5)

        name_entry = tk.Entry(window)
        cost_entry = tk.Entry(window)

        name_entry.grid(row=0, column=1, padx=10, pady=5)
        cost_entry.grid(row=1, column=1, padx=10, pady=5)

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

        tk.Button(window, text="Сохранить", command=save_ingredient).grid(row=2, columnspan=2, pady=10)

    def clear_all_data(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить все данные из базы?"):
            conn = sqlite3.connect("meal_cost.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM meal_ingredients")
            cursor.execute("DELETE FROM meals")
            cursor.execute("DELETE FROM ingredients")
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Все данные удалены!")

    # Other methods remain unchanged...

if __name__ == "__main__":
    root = tk.Tk()
    app = MealApp(root)
    root.mainloop()
