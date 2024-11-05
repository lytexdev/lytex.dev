from flask import Flask, jsonify, render_template, send_from_directory, abort
import os
import json
from markdown2 import markdown

app = Flask(__name__)

ARTICLES_PATH = './articles'
METADATA_PATH = './data/articles.json'

def load_metadata():
    with open(METADATA_PATH, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    metadata = load_metadata()
    return render_template('index.html', articles=metadata)

@app.route('/<path:subpath>')
def show_article(subpath):
    md_path = os.path.join(ARTICLES_PATH, f"{subpath}.md")
    if not os.path.exists(md_path):
        return abort(404)
    
    with open(md_path, 'r') as f:
        content = f.read()
        html_content = markdown(content)
    
    return render_template('article.html', content=html_content)


if __name__ == "__main__":
    app.run(debug=True)
