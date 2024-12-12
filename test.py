
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
        left_frame.pack(anchor="w",side="left", padx=10, pady=10)

        # Create buttons on the left side
        tk.Button(left_frame, text="Добавить блюдо", command=self.add_meal_window).pack(fill='both', pady=5)
        tk.Button(left_frame, text="Добавить ингредиенты", command=self.add_ingredient_window).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Список блюд", command=self.view_meals).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Список ингредиентов", command=self.view_ingredients).pack(fill='x', pady=5)

        # Create a frame for displaying meal list on the right
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    def view_meals(self):
        # Очищаем правую панель перед выводом нового списка
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Добавляем заголовок
        title_label = tk.Label(self.right_frame, text="Список Блюд", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM meals")
        meals = cursor.fetchall()

        # Создаем список с блюдами и кнопками удаления
        for meal in meals:
            meal_id = meal[0]
            meal_name = meal[1]
            meal_price = calculate_selling_price(calculate_meal_cost(meal_id))  # Calculate selling price

            meal_frame = tk.Frame(self.right_frame)
            meal_frame.pack(fill='x', pady=5)

            tk.Label(meal_frame, text=f"ID: {meal_id}, Блюдо: {meal_name}, Цена: {meal_price}").pack(side="left")

            # Кнопка для удаления блюда
            delete_button = tk.Button(meal_frame, text="Удалить", command=lambda meal_id=meal_id: self.delete_meal(meal_id))
            delete_button.pack(side="right", padx=5)

        conn.close()

    def view_ingredients(self):
        # Очищаем правую панель перед выводом нового списка
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Добавляем заголовок
        title_label = tk.Label(self.right_frame, text="Список Ингредиентов", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM ingredients")
        ingredients = cursor.fetchall()

        # Создаем список с ингредиентами и кнопками удаления
        for ingredient in ingredients:
            ing_id = ingredient[0]
            ing_name = ingredient[1]
            ing_cost = ingredient[2]

            ingredient_frame = tk.Frame(self.right_frame)
            ingredient_frame.pack(fill='x', pady=5)

            tk.Label(ingredient_frame, text=f"ID: {ing_id}, Ингредиент: {ing_name}, Стоимость: {ing_cost}").pack(side="left")

            # Кнопка для удаления ингредиента
            delete_button = tk.Button(ingredient_frame, text="Удалить", command=lambda ing_id=ing_id: self.delete_ingredient(ing_id))
            delete_button.pack(side="right", padx=5)

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
        ingredient_quantity_vars = []
        for i, (ing_id, ing_name) in enumerate(ingredients):
            var = tk.IntVar()
            quantity_var = tk.IntVar(value=1)  # Default quantity is 1
            # Чекбокс для выбора ингредиента
            tk.Checkbutton(window, text=ing_name, variable=var).grid(row=2 + i, column=0, sticky="w")
            # Поле для ввода количества
            tk.Label(window, text="Количество:").grid(row=2 + i, column=1)
            tk.Entry(window, textvariable=quantity_var).grid(row=2 + i, column=2)

            ingredient_vars.append((ing_id, var))
            ingredient_quantity_vars.append(quantity_var)

        # Кнопка "Сохранить"
        def save_meal():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Ошибка", "Введите название блюда.")
                return

            # Проверяем, выбраны ли хотя бы один ингредиент
            selected_ingredients = [(ing_id, var.get(), quantity_var.get()) for (ing_id, var), quantity_var in zip(ingredient_vars, ingredient_quantity_vars) if var.get() > 0]

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

            # Добавляем выбранные ингредиенты с количеством
            for ing_id, is_selected, quantity in selected_ingredients:
                if is_selected and quantity > 0:
                    cursor.execute("INSERT INTO meal_ingredients (meal_id, ingredient_id, quantity) VALUES (?, ?, ?)", (meal_id, ing_id, quantity))

            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Блюдо добавлено!")
            window.destroy()
            self.view_meals()  # Обновляем список после добавления блюда

        tk.Button(window, text="Сохранить", command=save_meal).grid(row=2 + len(ingredients), columnspan=3)

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
                cost = float(cost_entry.get())  # Allow decimal cost
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
                self.view_ingredients()  # Обновляем список после добавления ингредиента
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля корректно.")

        tk.Button(window, text="Сохранить", command=save_ingredient).grid(row=2, columnspan=2)

    def delete_meal(self, meal_id):
        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()

        # Удаляем запись из таблицы meal_ingredients
        cursor.execute("DELETE FROM meal_ingredients WHERE meal_id = ?", (meal_id,))
        # Удаляем саму запись из таблицы meals
        cursor.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Блюдо удалено!")
        self.view_meals()

    def delete_ingredient(self, ing_id):
        conn = sqlite3.connect("meal_cost.db")
        cursor = conn.cursor()

        # Удаляем запись из таблицы meal_ingredients
        cursor.execute("DELETE FROM meal_ingredients WHERE ingredient_id = ?", (ing_id,))
        # Удаляем саму запись из таблицы ingredients
        cursor.execute("DELETE FROM ingredients WHERE id = ?", (ing_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Ингредиент удален!")
        self.view_ingredients()

if __name__ == "__main__":
    root = tk.Tk()
    app = MealApp(root)
    root.mainloop()

