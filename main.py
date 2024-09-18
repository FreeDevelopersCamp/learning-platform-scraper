import requests
from bs4 import BeautifulSoup

# URL of the webpage containing the SVG
url = 'https://roadmap.sh/frontend?r=frontend-beginner'

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the SVG element
    svg = soup.find_all('svg')

    if svg:
        # Extract the SVG content as a string
        svg_content = str(svg)

        # Output or save the SVG content
        print(svg_content)
        # You can save it to a file if needed
        with open('roadmap.svg', 'w') as file:
            file.write(svg_content)
    else:
        print('No SVG found on the page.')
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
