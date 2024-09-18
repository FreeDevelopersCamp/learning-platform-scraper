from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_roadmap():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed

    # URL of the webpage containing the SVG
    url = 'https://roadmap.sh/frontend?r=frontend-beginner'

    # Open the webpage
    driver.get(url)

    # Wait until at least one tspan element is present
    try:
        # Waiting for the first occurrence of a tspan element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'tspan'))
        )
        
        # Get the page source after the tspan elements are loaded
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the tspan elements directly
        tspan_elements = soup.find_all('tspan')

        # Extract and store the text content
        roadmap_text = ""
        for tspan in tspan_elements:
            roadmap_text += tspan.get_text() + "\n"
        
        # Save the roadmap text to a file
        with open('roadmap_data.txt', 'w') as file:
            file.write(roadmap_text)
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == "__main__":
    scrape_roadmap()
