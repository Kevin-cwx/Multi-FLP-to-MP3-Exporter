from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

driver_path = '/path/to/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--new-tab")
driver = webdriver.Chrome(driver_path, options=chrome_options)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

url = "https://audiomack.com/upload/songs"
driver.get(url)

# Find the button by class name
button = driver.find_element_by_class_name('UploadForm-module__button--3rbYU')

# Click the button
button.click()


