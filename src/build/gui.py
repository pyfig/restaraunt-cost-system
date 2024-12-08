from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Toplevel


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")


def relative_to_assets(path: str) -> Path:
    """Возвращает путь к файлу assets относительно assets/frame0"""
    return ASSETS_PATH / Path(path)

def main_windows_template(title: str):
    """Создает новое окно"""
    new_window = Toplevel(window)
    new_window.geometry("800x600")
    new_window.configure(bg="#FFFFFF")
    new_window.title(title)
    return new_window

def create_button(image_path: str, command, x: float, y: float, width: float, height: float):
    """Создает кнопку"""
    global canvas
    button_image = PhotoImage(file=relative_to_assets(image_path))
    button = Button(
        image=button_image,
        borderwidth=0,
        highlightthickness=0,
        command=command,
        relief="flat"
    )
    button.image = button_image  # Keep a reference to avoid garbage collection
    button.place(x=x, y=y, width=width, height=height)
    return button


def main_window_menu():
    """Главное окно"""
    global window, canvas
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

    buttons_config = [
        ("button_1.png", lambda: main_windows_template("Add dishes"), 144.0, 222.0),
        ("button_2.png", lambda: main_windows_template("Ingredients"), 409.0, 261.0),
        ("button_3.png", lambda: main_windows_template("Dishes"), 144.0, 315.0),
        ("button_4.png", lambda: main_windows_template("Edit ingredients"), 409.0, 354.0)
    ]
    for image, command, x, y in buttons_config:
        create_button(image, command, x, y, 247.0, 78.0)

    canvas.create_text(
        131.0,
        47.0,
        anchor="nw",
        text=" ",
        fill="#000000",
        font=("Inter", 56 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    main_window_menu()
