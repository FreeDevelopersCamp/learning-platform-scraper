from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_roadmap():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed

    # URL of the webpage containing the SVG
    url = 'https://roadmap.sh/frontend?r=frontend-beginner'

    # Open the webpage
    driver.get(url)

    try:
        # Waiting for the first occurrence of an element with 'data-title' attribute
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'g[data-title]'))
        )

        # Find all `g` elements with 'data-title' attribute
        g_elements = driver.find_elements(By.CSS_SELECTOR, 'g[data-title]')
        
        # Create an empty list to store all the scraped data
        all_scraped_data = []

        # Loop through each `g` element
        for g_element in g_elements:
            # Get the topic title (data-title attribute)
            topic_title = g_element.get_attribute('data-title')

            # Find the `rect` element inside the `g` tag and click it to open the detailed view
            rect_element = g_element.find_element(By.TAG_NAME, 'rect')
            rect_element.click()

            # Wait for the detailed information (class 'flex-1') to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'flex-1'))
            )

            # Get the page source after the div with class 'flex-1' has loaded
            page_source = driver.page_source

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find the div containing the detailed information
            detail_div = soup.find('div', class_='flex-1')

            if detail_div:
                # Extract the text from the detailed information div
                detailed_info = detail_div.get_text(separator='\n').strip()

                # Add the scraped data to the list
                all_scraped_data.append({
                    "topic": topic_title,
                    "details": detailed_info
                })

            # Sleep for a second before continuing to the next element (to avoid overwhelming the page)
            time.sleep(1)

        # Save all the scraped data to a file
        with open('roadmap_details.txt', 'w', encoding='utf-8') as file:
            for data in all_scraped_data:
                file.write(f"Topic: {data['topic']}\nDetails:\n{data['details']}\n{'-'*40}\n")

    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    scrape_roadmap()
