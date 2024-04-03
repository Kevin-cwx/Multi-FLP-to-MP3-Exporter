import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import messagebox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select




driver_path = '/path/to/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

url = "https://audiomack.com/join?redirectTo=%2Fupload%2Fsongs"
driver.get(url)


# Fill input fields
email_input = driver.find_element(By.NAME, 'email')
email_input.clear()
email_input.send_keys('amorpicniccuracao@gmail.com')

username_input = driver.find_element(By.ID, 'username')
username_input.clear()
username_input.send_keys('GreenAvocado452')

password_input = driver.find_element(By.ID, 'password')
password_input.clear()
password_input.send_keys('GreenAvocado452@#$')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#Prompt user to fill out captcha
root = tk.Tk()
root.geometry("+400+0")
root.withdraw()  # Hide the main window
    
messagebox.showinfo("Captcha Prompt", "Please fill out the 'I'm not a robot' captcha. and click Sign up")


"""
Second page
Assumes user filled out captcha and clicked submit
"""

time.sleep(14)

# Find the birthday input field by its ID
birthday_input = driver.find_element(By.ID, 'birthday')

# Clear the input field in case it contains any pre-filled value
birthday_input.clear()

# Type the birthday into the input field
birthday_input.send_keys('05/19/1972')

# Find the gender select field by its name
gender_select = Select(driver.find_element(By.NAME, 'gender'))

# Select the value "Male" from the gender select field
gender_select.select_by_value('Male')

submit_button = driver.find_element(By.CLASS_NAME, 'button.button--pill.button--padded.auth__submit.auth-submit-button.u-spacing-top-20')
submit_button.click()

# Add a delay to keep the browser open for a few seconds
time.sleep(60)