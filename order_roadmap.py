from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Correct path to ChromeDriver
driver_path = r'chromedriver-win64\chromedriver.exe'  # Use raw string or double backslashes

# Set up ChromeOptions
service = Service(driver_path)
options = webdriver.ChromeOptions()

# Initialize the ChromeDriver with Service and Options
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the ChatGPT webpage (replace with the actual URL if needed)
    driver.get('https://chat.openai.com/')  # Change this to the actual ChatGPT URL

    # Wait for the page to load fully
    time.sleep(10)  # Allow more time for the page to fully load

    # Debugging: Print page source to inspect elements
    print(driver.page_source)  # Optional: Uncomment to see the page source in the console

    # Find the chat input box using JavaScript execution if direct interaction fails
    input_box = driver.execute_script('return document.querySelector("textarea");')
    
    # Use JavaScript to set the input value and send a message
    driver.execute_script('arguments[0].value = arguments[1];', input_box, 'What is the capital of France?')
    
    # Trigger an 'input' event to simulate typing
    driver.execute_script('arguments[0].dispatchEvent(new Event("input", { bubbles: true }));', input_box)
    
    # Submit the input
    input_box.send_keys(Keys.RETURN)

    # Wait for the response to load
    time.sleep(10)

    # Extract the response (you might need to adjust the selector based on the page structure)
    messages = driver.find_elements(By.CSS_SELECTOR, 'div.message')  # Adjust selector to target chat messages
    response = messages[-1].text  # Assuming the last message is the response
    print('ChatGPT Response:', response)

finally:
    # Close the browser
    driver.quit()
