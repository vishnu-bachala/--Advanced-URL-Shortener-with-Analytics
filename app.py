from flask import Flask, request, redirect, render_template_string
import random
import string
import json
from datetime import datetime

app = Flask(__name__)

# Dictionary to store shortened URLs and their click counts
urls = {}

def generate_short_code():
    """Generate a random 6-character alphanumeric code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

@app.route('/')
def index():
    return render_template_string('''
        <form action="/shorten" method="post">
            <input type="text" name="url" placeholder="Enter URL">
            <button type="submit">Shorten</button>
        </form>
    ''')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_code = generate_short_code()
    urls[short_code] = {'url': original_url, 'clicks': 0, 'created_at': datetime.now().isoformat()}
    return f'Shortened URL: {request.host_url}{short_code}'

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code in urls:
        urls[short_code]['clicks'] += 1
        return redirect(urls[short_code]['url'])
    else:
        return 'URL not found', 404

@app.route('/analytics/<short_code>')
def get_analytics(short_code):
    if short_code in urls:
        return json.dumps(urls[short_code])
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
