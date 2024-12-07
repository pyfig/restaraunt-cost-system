import tkinter as tk
from tkinter import ttk

class Button(ttk.Button):
    """Base button class extending ttk.Button with common functionality"""
    def __init__(self, parent, text="", command=None, **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.configure(padding=5)

class PrimaryButton(Button):
    """Primary action button with emphasized styling"""
    def __init__(self, parent, text="", command=None, **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.configure(style='Primary.TButton')

class SecondaryButton(Button):
    """Secondary action button with standard styling"""
    def __init__(self, parent, text="", command=None, **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.configure(style='Secondary.TButton')

class IconButton(Button):
    """Button with an icon and optional text"""
    def __init__(self, parent, icon=None, text="", command=None, **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        if icon:
            self.configure(image=icon, compound='left')

class ToggleButton(ttk.Checkbutton):
    """Button that toggles between two states"""
    def __init__(self, parent, text="", command=None, **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.configure(style='Toggle.TCheckbutton')


def main() -> tk.Tk:
    """Run the main loop of the application.

    Returns:
        The top-level Tk window.
    """
    app_window = tk.Tk()
    app_window.geometry('800x600')
    app_window.title("Restaurant Cost System")
    
    # Example usage of your custom buttons
    primary_button = PrimaryButton(app_window, text="Primary Action", command=lambda: print("Primary Clicked!"))
    secondary_button = SecondaryButton(app_window, text="Secondary Action", command=lambda: print("Secondary Clicked!"))
    toggle_button = ToggleButton(app_window, text="Toggle Me", command=lambda: print("Toggled!"))
    
    primary_button.pack(pady=10)
    secondary_button.pack(pady=10)
    toggle_button.pack(pady=10)
    
    app_window.mainloop()

    return app_window

if __name__ == "__main__":
    main()