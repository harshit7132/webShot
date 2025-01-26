from flask import Flask, render_template, request, send_file, redirect, url_for
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

# Firebase Initialization
cred = credentials.Certificate('secret/firebase_settings.json') 
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/', methods=['GET', 'POST'])
def index():
    scraped_data = None
    if request.method == 'POST':
        url = request.form['url']
        scraped_data = scrape_website(url)      

        # Ensure that scraped_data['html'] exists before passing it to the template
        if not scraped_data or 'html' not in scraped_data:
            scraped_data = {'html': ''}  # Fallback to empty HTML if there's an issue

    return render_template('index.html', data=scraped_data)

@app.route('/history')
def history():
    # history = fetch_history()
    return render_template('history.html')
    # return render_template('history.html', history=history)

@app.route('/signIn')
def login():
    return render_template('signIn.html')

@app.route('/signUp')
def register():
    return render_template('signUp.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/jarvis')
def jarvis():
    return render_template('jarvis_screen.html')

def scrape_website(url):
    data = {
        'html': None,
        'css_links': [],
        'js_links': [],
        'error': None
    }
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        data['html'] = soup.prettify()

        for link in soup.find_all('link', rel='stylesheet'):
            data['css_links'].append(urljoin(url, link['href']))

        for script in soup.find_all('script', src=True):
            data['js_links'].append(urljoin(url, script['src']))

    except Exception as e:
        data['error'] = str(e)
    return data

@app.route('/download/<file_type>', methods=['GET'])
def download(file_type):
    url = request.args.get('url')
    if not url:
        return "No URL provided.", 400

    filename = None
    content = None

    if file_type == 'html':
        content = scrape_website(url)['html']
        if content:
            filename = 'scraped_data.html'
    elif file_type == 'css':
        links = scrape_website(url)['css_links']
        if links:
            filename = 'scraped_styles.css'
            content = '\n'.join(links)
    elif file_type == 'js':
        links = scrape_website(url)['js_links']
        if links:
            filename = 'scraped_scripts.js'
            content = '\n'.join(links)

    if not content:
        return f"Error scraping the {file_type} content.", 400

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    return send_file(filename, as_attachment=True)

@app.route('/delete/<doc_id>', methods=['POST'])
def delete_data(doc_id):
    db.collection('scraped_data').document(doc_id).delete()
    return redirect(url_for('history'))

def store_scraped_data(url, scraped_data):
    data = {
        'url': url,
        'html': scraped_data['html'],
        'css_links': scraped_data['css_links'],
        'js_links': scraped_data['js_links'],
        'error': scraped_data['error'],
        'timestamp': datetime.utcnow()
    }
    db.collection('scraped_data').add(data)

def fetch_history():
    docs = db.collection('scraped_data').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
    history = []
    for doc in docs:
        item = doc.to_dict()
        item['id'] = doc.id
        history.append(item)
    return history

if __name__ == '__main__':
    app.run(debug=True)
