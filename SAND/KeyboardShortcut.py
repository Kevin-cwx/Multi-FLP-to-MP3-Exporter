# Keyboard module in Python
import keyboard
import time
import pyautogui
 
# press ctrl+shift+z to print "Hotkey Detected"
#time.sleep(3)
keyboard.send("ctrl+shift+R")
keyboard.release("ctrl+shift+R")



#keyboard.add_hotkey('ctrl+O', print, args =('Hotkey', 'Detected'))
pyautogui.write("C:\Users\Kfoen\Documents\Docs KF\FLPOutputMp3")
keyboard.add_hotkey('enter', print, args =('Hotkey', 'Detected'))

