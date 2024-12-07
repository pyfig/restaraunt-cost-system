import tkinter as tk
from tkinter import ttk
from gui import buttons


def main() -> tk.Tk:
    """Run the main loop of the application.

    Returns:
        The top-level Tk window.
    """
    app_window = tk.Tk()
    app_window.geometry('800x600')
    app_window.title("Restaurant Cost System")

    # Create and pack a PrimaryButton
    primary_button = PrimaryButton(app_window, text="Primary Action", command=lambda: print("Primary Button Clicked"))
    primary_button.pack(pady=10)

    # Create and pack a SecondaryButton
    secondary_button = SecondaryButton(app_window, text="Secondary Action", command=lambda: print("Secondary Button Clicked"))
    secondary_button.pack(pady=10)

    # Create and pack an IconButton with text
    icon_button = IconButton(app_window, text="Icon Button", command=lambda: print("Icon Button Clicked"))
    icon_button.pack(pady=10)

    # Create and pack a ToggleButton
    toggle_button = ToggleButton(app_window, text="Toggle", command=lambda: print("Toggle Button Clicked"))
    toggle_button.pack(pady=10)

    app_window.mainloop()

    return app_window

if __name__ == "__main__":
    main()

