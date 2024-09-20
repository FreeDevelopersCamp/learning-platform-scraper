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
driver.get('https://coral.cohere.com/?_gl=1*17rolzu*_gcl_au*MTA0MTQ5ODEzNC4xNzI2ODQwNzA3*_ga*MTk1ODIwOTMwNy4xNzI2ODQwNzA5*_ga_CRGS116RZS*MTcyNjg0MDcwNy4xLjEuMTcyNjg0MTU5Ny41OS4wLjA.')

emailBtn = driver.find_element(By.CSS_SELECTOR, "#__next > div > div.relative.mx-auto.flex.h-full.min-h-screen.w-full.max-w-page.flex-col.overflow-y-auto > div.my-auto.w-full.px-6.pb-6.md\:mx-auto.md\:w-fit.md\:px-0.md\:py-4 > div > div > div.mt-10.flex.w-full.flex-col.items-center.gap-1.sm\:h-10.sm\:flex-row > button:nth-child(1)")
emailBtn.click()

emailInput = driver.find_element(By.CSS_SELECTOR, "#identifierId")
emailInput.click()
emailInput.send_keys("s12010060@stu.najah.edu" + Keys.ENTER)
time.sleep(5)
passwordInput = driver.find_element("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")
time.sleep(5)
passwordInput.click()
passwordInput.send_keys("BisBis@@158963")
time.sleep(5)
# Wait for the input text area to be available
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#composer"))
)

# Find the input element using the correct CSS selector
input_element = driver.find_element(By.CSS_SELECTOR, "#composer")

# Clear any existing text (if any)
input_element.clear()

# Type the message and press Enter
input_element.send_keys("What is the capital of France?" + Keys.ENTER)

# Allow time for the response to be processed and appear
time.sleep(5)

# Wait for the response message to appear in the chat area
response_selector = "#message-row-2b5e905b-474c-4256-91c0-1af43194fa12 > div > div > div.flex.w-full.min-w-0.max-w-message.flex-1.flex-col.items-center.gap-x-1.md\:flex-row > div.w-full > div > div > div > p"
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, response_selector))
)

# Find the response element and extract the text
response_element = driver.find_element(By.CSS_SELECTOR, response_selector)
response_text = response_element.text
print(f"GPT-4 response: {response_text}")

# Wait a bit for the response to be fully generated
time.sleep(5)

# Quit the driver (close the browser)
driver.quit()
