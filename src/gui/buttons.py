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
