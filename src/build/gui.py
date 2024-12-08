from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Toplevel, Entry

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")

def relative_to_assets(path: str) -> Path:
    """Возвращает путь к файлу assets относительно assets/frame0"""
    return ASSETS_PATH / Path(path)

def create_button(canvas, image_path: str, command, x: float, y: float, width: float, height: float):
    """Создает кнопку с изображением"""
    button_image = PhotoImage(file=relative_to_assets(image_path))
    button = Button(
        canvas,
        image=button_image,
        borderwidth=0,
        highlightthickness=0,
        command=command,
        relief="flat"
    )
    button.image = button_image  # Храним ссылку на изображение, чтобы не было сборки мусора
    button.place(x=x, y=y, width=width, height=height)

def main_window_menu():
    """Главное окно приложения"""
    window = Tk()
    window.title("Restaraunt Cost System v1.0")
    window.geometry("800x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Конфигурация кнопок
    buttons_config = [
        ("button_1.png", add_dishes_window, 144.0, 222.0),
        ("button_2.png", ingredients_window, 409.0, 261.0),
        ("button_3.png", dishes_window, 144.0, 315.0),
        ("button_4.png", edit_ingredients_window, 409.0, 354.0)
    ]

    for image, command, x, y in buttons_config:
        create_button(canvas, image, command, x, y, 247.0, 78.0)

    canvas.create_text(
        131.0,
        47.0,
        anchor="nw",
        text="Restaraunt Cost System",
        fill="#000000",
        font=("Inter", 24)
    )

    window.resizable(False, False)
    window.mainloop()

# Отдельные функции для кнопок
def add_dishes_window():
    """Окно добавления блюд"""
    create_window_with_entry("Add Dishes", "Enter dish name:")
    
def ingredients_window():
    """Окно ингредиентов"""
    create_window_with_entry("Ingredients", "Enter ingredient name:")

def dishes_window():
    """Окно блюд"""
    create_window_with_entry("Dishes", "Enter dish details:")

def edit_ingredients_window():
    """Окно редактирования ингредиентов"""
    create_window_with_entry("Edit Ingredients", "Edit ingredient details:")

# Общая функция для создания окон с текстовыми полями
def create_window_with_entry(title: str, label_text: str):
    """Создает окно с текстовым полем"""
    window = Toplevel()
    window.title(title)
    window.geometry("800x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    canvas.create_text(
        131.0,
        47.0,
        anchor="nw",
        text=title,
        fill="#000000",
        font=("Inter", 24)
    )

    canvas.create_text(
        131.0,
        150.0,
        anchor="nw",
        text=label_text,
        fill="#000000",
        font=("Inter", 16)
    )

    entry_1 = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0,
        font=("Inter", 14)
    )
    entry_1.place(
        x=233.0,
        y=190.0,
        width=300.0,
        height=30.0
    )

if __name__ == "__main__":
    main_window_menu()
