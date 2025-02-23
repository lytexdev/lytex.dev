from flask import Flask, jsonify, render_template, send_from_directory, abort, url_for
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
    article_index = next((index for index, item in enumerate(metadata) if item["filepath"] == subpath), None)
    
    if article_index is None:
        return abort(404)

    article = metadata[article_index]
    md_path = os.path.join(ARTICLES_PATH, f"{subpath}.md")
    
    if not os.path.exists(md_path):
        return abort(404)

    with open(md_path, 'r') as f:
        content = f.read()
        html_content = markdown(content, extras=['fenced-code-blocks'])
        
    authors = article.get('authors', 'lytex')

    prev_article = metadata[article_index - 1] if article_index > 0 else None
    next_article = metadata[article_index + 1] if article_index < len(metadata) - 1 else None
    
    return render_template(
        'article.html',
        title=article['title'],
        content=html_content,
        created_at=article['created_at'],
        authors=authors,
        prev_article=prev_article,
        next_article=next_article
    )

if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
