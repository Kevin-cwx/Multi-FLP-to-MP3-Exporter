import os
import time
from pywinauto import application
import pygetwindow as gw
import pyautogui
from PIL import ImageGrab

# Define the path to the project and the screenshot location
project_path = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\BT WIN.flp"
screenshot_path = os.path.join(
    os.path.expanduser("~"), "Desktop", "screenshot.png")

# Open the project
os.startfile(project_path)

# Function to check if FL Studio is the active window


def is_fl_studio_active():
    active_window = gw.getActiveWindow()
    return active_window and 'FL Studio' in active_window.title


# Wait until FL Studio is the active window
while not is_fl_studio_active():
    time.sleep(0.5)

# Connect to FL Studio window using pywinauto
app = application.Application().connect(title_re=".*FL Studio.*")
fl_studio_window = app.top_window()

# Maximize the FL Studio window
fl_studio_window.maximize()

# Wait until FL Studio is maximized and ready by searching for specific text elements


def is_fl_studio_ready(window):
    window_text = window.window_text()
    return "File" in window_text and "Edit" in window_text and "Add" in window_text


# Retry loop for readiness check
retries = 5
for _ in range(retries):
    if is_fl_studio_ready(fl_studio_window):
        break
    time.sleep(6)
else:
    raise Exception("FL Studio did not become ready in time")

# Press F5
pyautogui.press('f5')

# Wait until any actions triggered by F5 are complete by searching for specific text elements


def is_f5_action_complete(window):
    window_text = window.window_text()
    return "Playlist" in window_text


# Retry loop for F5 action completion check
for _ in range(retries):
    if is_f5_action_complete(fl_studio_window):
        break
    time.sleep(2)
else:
    raise Exception("F5 action did not complete in time")

# Take a screenshot
screenshot = ImageGrab.grab()
screenshot.save(screenshot_path)

print(f"Screenshot saved to {screenshot_path}")
