import tkinter as tk
from views.main_window import MealApp

if __name__ == "__main__":
    root = tk.Tk()
    app = MealApp(root)
    root.mainloop()