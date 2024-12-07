from sys import version_info

from gui.buttons import make_test_buttons


if version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


def main() -> None:
    """Run the main loop of the application."""
    app_window = tk.Tk()
    app_window.geometry('800x600')
    app_window.title("Restaurant Cost System")
    make_test_buttons(app_window)
    app_window.mainloop()


if __name__ == "__main__":
    main()

