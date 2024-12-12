import tkinter as tk
from tkinter import messagebox
from db.database import create_db
from models.meal import get_all_meals, add_meal_window
from models.ingredient import get_all_ingredients, add_ingredient
from utils.calculations import calculate_selling_price, calculate_meal_cost

class MealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система расчета стоимости блюд")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        create_db()
        self.create_widgets()

    def create_widgets(self):
        left_frame = tk.Frame(self.root)
        left_frame.pack(anchor="w", side="left", padx=10, pady=10)

        tk.Button(left_frame, text="Добавить блюдо", command=self.add_meal_window).pack(fill='both', pady=5)
        tk.Button(left_frame, text="Добавить ингредиенты", command=self.add_ingredient_window).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Список блюд", command=self.view_meals).pack(fill='x', pady=5)
        tk.Button(left_frame, text="Список ингредиентов", command=self.view_ingredients).pack(fill='x', pady=5)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def view_meals(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.right_frame, text="Список Блюд", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        meals = get_all_meals()
        for meal in meals:
            meal_id, meal_name = meal
            meal_price = calculate_selling_price(calculate_meal_cost(meal_id))

            meal_frame = tk.Frame(self.right_frame)
            meal_frame.pack(fill='x', pady=5)

            tk.Label(meal_frame, text=f"ID: {meal_id}, Блюдо: {meal_name}, Цена: {meal_price}").pack(side="left")

    def view_ingredients(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.right_frame, text="Список Ингредиентов", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        ingredients = get_all_ingredients()
        for ing in ingredients:
            ing_id, ing_name, ing_cost = ing

            ingredient_frame = tk.Frame(self.right_frame)
            ingredient_frame.pack(fill='x', pady=5)

            tk.Label(ingredient_frame, text=f"ID: {ing_id}, Ингредиент: {ing_name}, Стоимость: {ing_cost}").pack(side="left")
