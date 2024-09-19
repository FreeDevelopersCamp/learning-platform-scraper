from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up ChromeDriver service and options
service = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions()

# Initialize the driver
driver = webdriver.Chrome(service=service)

# Open ChatGPT
driver.get('https://chat.openai.com/')

# Wait for the input text area to be available
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#prompt-textarea"))
)

# Find the input element using the correct CSS selector
input_element = driver.find_element(By.CSS_SELECTOR, "#prompt-textarea")

# Clear any existing text (if any)
input_element.clear()

# Type the message and press Enter
input_element.send_keys("What is the capital of France?" + Keys.ENTER)

# Wait for the message to appear in the chat area
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "whitespace-pre-wrap"))
)

# # Optionally wait for GPT's response to appear (asynchronously)
# WebDriverWait(driver, 30).until(
#     EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'result')]"))
# )

# Wait a bit for the response to be fully generated
time.sleep(5)

# Quit the driver (close the browser)
driver.quit()
