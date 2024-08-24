import pyautogui
import os
import time
from PIL import ImageGrab
import pygetwindow as gw

# Define the path to the project and the screenshot location
project_path = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\TTYNB.flp"
screenshot_path = os.path.join(
    os.path.expanduser("~"), "Desktop", "screenshot.png")

# Open the project
os.startfile(project_path)

# Allow some time for the project to open
time.sleep(7)

# Find the FL Studio window
fl_studio_window = None
for window in gw.getWindowsWithTitle('FL Studio'):
    if 'FL Studio' in window.title:
        fl_studio_window = window
        break

# Ensure FL Studio window is found
if fl_studio_window:
    # Activate the FL Studio window
    fl_studio_window.activate()

    # Allow some time for the window to be activated
    time.sleep(2)

    # Maximize the FL Studio window
    pyautogui.hotkey('win', 'up')

    # Allow a moment for the maximize action to complete
    time.sleep(2)

    # Press F5 (ensure FL Studio is the active window)
    pyautogui.press('f5')
    pyautogui.hotkey('alt', 'f8')


    # Allow some time for any actions triggered by F5 to complete
    time.sleep(5)

    # Take a screenshot
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)

    #Revert back to user's preference, dont have a way to check if user has project picker open
    pyautogui.hotkey('alt', 'f8')
    print(f"Screenshot saved to {screenshot_path}")
    fl_studio_window.close()
else:
    print("FL Studio window not found")
