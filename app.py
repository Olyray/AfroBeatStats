#!/usr/bin/python3
from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/afrobeatstats/', strict_slashes=False)
def index():
    # Load the contents of file_storage.json
    with open('file_storage.json', 'r') as file:
        artists = json.load(file)

    # Render the modified template with the loaded data
    return render_template('topartists.html', artists=artists)

@app.route('/afrobeatstats/about', strict_slashes=False)
def about():
    return render_template('about.html')

@app.route('/afrobeatstats/contact', strict_slashes=False)
def contact():
    return render_template('contact.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)
