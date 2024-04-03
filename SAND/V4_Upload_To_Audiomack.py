from selenium import webdriver
import webbrowser
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

UserEmail =""
UserPW =""
def GetUserCredentials():
    UserEmail = input("Enter email:\n")
    UserPW = input("Enter PW:\n")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
keyboard = Controller()

#GetUserCredentials()

#Keyboard press and release
def PressEnterKey():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

#Opens browser
driver = webdriver.Chrome('drivers/chromedriver.exe', chrome_options=chrome_options)
driver.implicitly_wait(10)
driver.get("https://audiomack.com/upload/songs")

# Types email
driver.find_element(By.NAME, "email").click()
keyboard.type(r"kfoendoe1@gmail.com")
#keyboard.type(UserEmail)
PressEnterKey()

# Types Password
driver.find_element(By.ID, "password").click()
keyboard.type(r"Accolade721")
#keyboard.type(UserPW)
PressEnterKey()

# Click "browse to your file"
driver.find_element(By.CLASS_NAME, "UploadForm-module__buttonWrap--2b8Sh").click()
time.sleep(1)

# Type Local song path
keyboard.type(r"C:\Users\Kfoen\Music\DropHere\buffalo city.mp3")
PressEnterKey()


# Make dynamic, Build, wait untill element appears
# Select song tag "dj mix"
time.sleep(6)

#driver.find_elements(By.ID, "dropdown-genre-24305627").click()
driver.find_element("xpath", "//*[contains(text(), 'Choose a genre')]").click()
keyboard.type(r"dj")
PressEnterKey()

# Click next on page upload
driver.find_element("xpath", "//*[contains(text(), 'Next Step')]").click()
time.sleep(1)
driver.find_element("xpath", "//*[contains(text(), 'Next Step')]").click()
driver.find_element(By.CLASS_NAME, "LabeledInput-module__label--1zG4T").click()
time.sleep(2)
driver.find_element(By.CLASS_NAME, "SongUploadDrawer-module__nextButton--2W5Ks button button--pill button--med").click()

#driver.find_element(By.XPATH, "//button[@type='submit']").click()

