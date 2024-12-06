import json
from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

# Vercel Function for the index route
def handler(request):
    scraped_data = None
    if request.method == 'POST':
        url = request.form['url']
        scraped_data = scrape_website(url)
    return json.dumps({"data": scraped_data})

# Function to scrape website
def scrape_website(url):
    data = {
        'html': None,
        'css_links': [],
        'js_links': [],
        'error': None
    }
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get all HTML content
        data['html'] = soup.prettify()

        # Get all CSS links
        for link in soup.find_all('link', rel='stylesheet'):
            data['css_links'].append(urljoin(url, link['href']))

        # Get all JS links
        for script in soup.find_all('script', src=True):
            data['js_links'].append(urljoin(url, script['src']))

    except Exception as e:
        data['error'] = str(e)

    return data

# Function to download files
def download(request, file_type):
    url = request.args.get('url')
    if not url:
        return "No URL provided.", 400

    if file_type == 'html':
        content = scrape_website(url)['html']
        if content is None:
            return "Error scraping the HTML content.", 400
        filename = 'scraped_data.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    elif file_type == 'css':
        css_links = scrape_website(url)['css_links']
        if not css_links:
            return "Error scraping the CSS links.", 400
        filename = 'scraped_styles.css'
        with open(filename, 'w', encoding='utf-8') as f:
            for link in css_links:
                f.write(link + '\n')
    elif file_type == 'js':
        js_links = scrape_website(url)['js_links']
        if not js_links:
            return "Error scraping the JS links.", 400
        filename = 'scraped_scripts.js'
        with open(filename, 'w', encoding='utf-8') as f:
            for link in js_links:
                f.write(link + '\n')
    else:
        return "Invalid file type.", 400

    return send_file(filename, as_attachment=True)
