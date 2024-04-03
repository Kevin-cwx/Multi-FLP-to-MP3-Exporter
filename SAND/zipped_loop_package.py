import time
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pynput
import keyboard

"""
#blocks all keys of keyboard
for i in range(150):
    keyboard.block_key(i)

mouse_listener = pynput.mouse.Listener(suppress=True)
mouse_listener.start()

"""

print("Mouse and Keyboard disabled, temporarily. Now why are you moving the mouse around so violently")

flp_path = r"C:\Users\Kfoen\Documents\Image-Line\FL{SPACE}Studio\Projects\FL{SPACE}20{SPACE}-{SPACE}projects\K2\2023\MWM.flp"
output_zip_path = r"C:\Users\Kfoen\Desktop\project.zip"


def export_zipped_loop_package(flp_path, output_zip_path):
    # Launch FL Studio
    app = Application().start(r"C:\Program Files\Image-Line\FL Studio 20\FL64.exe")

    # Wait for FL Studio to launch
    time.sleep(2)

    # Connect to the running FL Studio application
    fl_window = app.window(title_re="FL Studio.*")
    
    
    # Open the FLP project
    fl_window.set_focus()  # Ensure the FL Studio window has focus
    send_keys("^o")  # Press Ctrl + O to open the file dialog
    time.sleep(1)
    send_keys(flp_path)  # Type the path to the FLP project
    time.sleep(1)
    send_keys("{ENTER}")  # Press Enter to open the FLP project

   
    # Wait for the project to load
    time.sleep(5)

"""
    # Export the loop package
    fl_window.menu_select("File -> Export -> Zipped loop package...")
    app.ExportZippedLoopPackageDialog.FileNameEdit.set_edit_text(output_zip_path)
    app.ExportZippedLoopPackageDialog.ExportButton.click()

    # Wait for the export to finish
    time.sleep(5)

    # Close FL Studio
    fl_window.close()

    print("Zipped loop package exported successfully!")




# Export the zipped loop package

"""
"""

"""

export_zipped_loop_package(flp_path, output_zip_path)
