"""
⬜ Add Auto open project
    Current version - Have FLP project open, toggle to FLP window
⬜ Make input parameter, FLP project
⬜ Add feature where function auto opens up project 
⬜ !ZIP doesnt actually have to be saved, only the wav or MP3 info needs to be saved. Thus delete ZIP after info is saved
⬜ Save MP3 and wav info to DT for project
⬜ Add error cather to replace if file has same name

Does not work, also need to find a better way to do this that is not GUI dependent
"""

import pyautogui
import time
import keyboard
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import subprocess
import os

Project_Name = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 20 - projects\K1\21 savage lemon.flp"
subprocess.call(Project_Name, shell=True)

output_zip_path = r"C:\Users\Kfoen\Desktop\project.zip"
print("Made it here")

time.sleep(5)
print("Waited 5 second")
#Simulate Shift + Ctrl + S key combination
keyboard.press("shift")
keyboard.press("ctrl")
keyboard.press("s")
keyboard.release("s")
keyboard.release("ctrl")
keyboard.release("shift")
time.sleep(1)

pyautogui.typewrite(output_zip_path)
pyautogui.press('tab')
pyautogui.hotkey('ctrl', 'z')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('tab')
pyautogui.press('enter')

print("Done")