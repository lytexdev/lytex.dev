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
    metadata = load_metadata()
    article = next((item for item in metadata if item["filepath"] == subpath), None)
    
    if not article:
        return abort(404)
    
    md_path = os.path.join(ARTICLES_PATH, f"{subpath}.md")
    if not os.path.exists(md_path):
        return abort(404)

    with open(md_path, 'r') as f:
        content = f.read()
        html_content = markdown(content, extras=['fenced-code-blocks'])
    
    return render_template('article.html', title=article['title'], content=html_content)


if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=8999)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
