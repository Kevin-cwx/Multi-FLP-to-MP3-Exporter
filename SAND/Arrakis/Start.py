import tkinter as tk
from tkinter import filedialog
import subprocess

My_Font_Size = 16

def continue_button_click():
    # Add your continuation logic here
    print("Continue button clicked")
    subprocess.Popen(["python", "./Sand/Arrakis/Main_Logic.py"])

   
root = tk.Tk()
root.title("Start Screen")

# Get the screen width
screen_width = root.winfo_screenwidth()

# Set the default window size to be half the screen width
default_width = screen_width // 2
default_height = 400
root.geometry(f"{default_width}x{default_height}")

# Make the window non-resizable
root.resizable(False, False)

continue_button = tk.Button(
    root, text="Submit", command=continue_button_click, font=("Arial", My_Font_Size))
continue_button.pack(side=tk.BOTTOM, pady=(20, 10), padx=10, anchor="e")

root.mainloop()