# Import required libraries
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def scrape_data(url):
    try:
        # Make an HTTP request to get the content of the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if there's an error

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        scraped_data = []

        # Extract data from the current page
        # Find all hyperlinks on the page
        links = soup.find_all('a', href=True)

        # Recursively scrape data from child pages
        for link in links:
            child_url = link['href']
            if not child_url.startswith('http'):  # Handle relative URLs
                child_url = url + child_url

            scraped_data += scrape_data(child_url)

        return scraped_data

    except Exception as e:
        print("Error:", e)
        return []

@app.route('/scrape', methods=['POST'])
def scrape_api():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL not provided.'}), 400

    scraped_data = scrape_data(url)
    return jsonify({'data': scraped_data}), 200

@app.route('/search', methods=['POST'])
def search_api():
    data = request.json
    search_text = data.get('search_text')
    if not search_text:
        return jsonify({'error': 'Search text not provided.'}), 400

    results = []
    # Loop through the scraped data and check for the search_text
    return jsonify({'results': results}), 200

if __name__ == '__main__':
    app.run()
