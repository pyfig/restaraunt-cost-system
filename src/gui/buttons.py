import tkinter as tk
def make_test_buttons():
    """Create test buttons."""
    # Create a frame to group the test buttons.
    test_frame = tk.Frame(main.app_window)
    test_frame.pack()

    # Create a test button that prints "Hello, World!" to the console.
    test_button = tk.Button(test_frame,
                            text="Test",
                            command=lambda: print("Hello, World!"))
    test_button.pack()
