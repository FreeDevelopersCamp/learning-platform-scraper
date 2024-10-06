from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scroll_and_click(g_element, driver):
    while True:
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView();", g_element)
        time.sleep(0.5)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(g_element)
            )
            g_element.click()
            break
        except Exception:
            driver.execute_script("window.scrollBy(0, 100);")

def scrape_roadmap():
    driver = webdriver.Chrome()
    url = 'https://roadmap.sh/backend?r=backend-beginner'

    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'g[data-title][data-type="topic"], g[data-title][data-type="subtopic"]'))
        )
        
        g_elements = driver.find_elements(By.CSS_SELECTOR, 'g[data-title][data-type="topic"], g[data-title][data-type="subtopic"]')
        
        all_scraped_data = []
        topics_dict = {}
        subtopics_temp = []  # Temporary list for subtopics

        for g_element in g_elements:
            topic_title = g_element.get_attribute('data-title')
            topic_id = g_element.get_attribute('data-node-id')
            parent_id = g_element.get_attribute('parent-node-id') 
            
            print(f"Processing: {topic_title}")

            scroll_and_click(g_element, driver)

            # Wait after clicking to ensure content has time to load
            time.sleep(3)  # Adding more delay

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'flex-1'))
            )

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Debugging: Print the first 500 characters of the page source to inspect it
            print(page_source[:500])

            detail_div = soup.find('div', class_='flex-1')

            if not detail_div:
                print(f"Detail div not found for {topic_title}. Full page source might be dynamic or missing.")

            if detail_div:
                print(f"detail_div found for: {topic_title}")
                
                h1_title = detail_div.find('h1').get_text(strip=True) if detail_div.find('h1') else None
                explanation = detail_div.find('p').get_text(strip=True) if detail_div.find('p') else None
                resources = []

                for p in detail_div.find_all('p'):
                    span = p.find('span')
                    if span:
                        ul = p.find_next_sibling('ul')
                        if ul:
                            for li in ul.find_all('li'):
                                genre_span = li.find('span')
                                resource_genre = genre_span.get_text(strip=True) if genre_span else ""
                                a_tag = li.find('a')  # Find the <a> tag inside the <li>
                                
                                if a_tag:
                                    resource_link_text = a_tag.get_text(strip=True)
                                    resource_link_href = a_tag['href']
                                    resource_detail = f"{resource_genre} {resource_link_text} ({resource_link_href})"
                                    resources.append(resource_detail)

                if g_element.get_attribute('data-type') == 'topic':
                    topics_dict[topic_id] = {
                        "topic": topic_title,
                        "title": h1_title,
                        "explanation": explanation,
                        "resources": resources,
                        "subtopics": [],
                        "data_node_id": topic_id,
                        "parent_node_id": None
                    }
                elif g_element.get_attribute('data-type') == 'subtopic':
                    subtopics_temp.append({
                        "title": topic_title,
                        "explanation": explanation,
                        "resources": resources,
                        "data_node_id": topic_id,
                        "parent_node_id": parent_id
                    })

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#close-topic'))
            )
            close_topic = driver.find_element(By.CSS_SELECTOR, '#close-topic')
            close_topic.click()

            time.sleep(1)

        # After scraping, assign subtopics to their parent topics
        for subtopic in subtopics_temp:
            parent_id = subtopic['parent_node_id']
            if parent_id in topics_dict:
                topics_dict[parent_id]['subtopics'].append(subtopic)
            else:
                print(f"Warning: Parent topic with ID {parent_id} not found for subtopic {subtopic['title']}")

        all_scraped_data = list(topics_dict.values())
        
        print(all_scraped_data)

        # Print and save the data
        with open('roadmap_details.txt', 'w', encoding='utf-8') as file:
            for data in all_scraped_data:
                file.write(f"Topic: {data['topic']} (ID: {data['data_node_id']})\n")
                file.write(f"Title: {data['title']}\n")
                file.write(f"Explanation: {data['explanation']}\n")
                file.write(f"Resources:\n")
                for resource in data['resources']:
                    file.write(f"  {resource}\n")

                for subtopic in data['subtopics']:
                    file.write(f"  Subtopic: {subtopic['title']} (ID: {subtopic['data_node_id']}, Parent ID: {subtopic['parent_node_id']})\n")
                    file.write(f"  Explanation: {subtopic['explanation']}\n")
                    file.write(f"  Resources:\n")
                    for resource in subtopic['resources']:
                        file.write(f"    {resource}\n")

                file.write(f"{'-'*40}\n")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_roadmap()

