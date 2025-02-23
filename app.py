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

@app.route('/sitemap.xml')
def sitemap():
    metadata = load_metadata()
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
    
    sitemap_xml += f'''
    <url>
        <loc>{url_for('index', _external=True)}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>'''

    for article in metadata:
        article_url = url_for('show_article', subpath=article["filepath"], _external=True)
        lastmod = article.get("created_at", datetime.now().strftime('%Y-%m-%d'))
        sitemap_xml += f'''
    <url>
        <loc>{article_url}</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>'''

    sitemap_xml += "\n</urlset>"
    return Response(sitemap_xml, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    robots_txt = f'''User-agent: *

Allow: /

Sitemap: {url_for('sitemap', _external=True)}
'''
    return Response(robots_txt, mimetype='text/plain')

if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
