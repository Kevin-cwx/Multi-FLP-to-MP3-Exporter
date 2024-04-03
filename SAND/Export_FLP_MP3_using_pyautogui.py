import pyautogui
import time
from AppOpener import open

#open("fl studio") 


# projectPath= "C:/freak.flp"
def export_song():
    # Adjust these values according to your screen resolution
    file_button_position = (10,10)
    export_button_position = (100, 100)
    export_menu_position = (200, 200)
    export_wav_position = (300, 300)
    export_ok_position = (400, 400)

    # Click the export button
    time.sleep(2)
    pyautogui.click(*file_button_position)
    pyautogui.click(*export_button_position)

    # Add a delay to ensure the export menu appears
    time.sleep(1)

    # Click the export menu
    pyautogui.click(*export_menu_position)

    # Add a delay to ensure the export options appear
    time.sleep(1)

    # Click the WAV option
    pyautogui.click(*export_wav_position)

    # Add a delay to ensure the export options close
    time.sleep(1)

    # Click the OK button
    pyautogui.click(*export_ok_position)
export_song()
