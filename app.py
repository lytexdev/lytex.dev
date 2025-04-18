from flask import Flask, render_template, Response, abort, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from collections import defaultdict, OrderedDict
from markdown import markdown
import markdown.extensions.codehilite
import markdown.extensions.fenced_code
import markdown.extensions.tables
import markdown.extensions.toc
import markdown.extensions.admonition
from pygments.formatters import HtmlFormatter
from datetime import datetime
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

ARTICLES_PATH = './articles'
METADATA_PATH = './data/articles.json'

def load_metadata():
    with open(METADATA_PATH, 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    metadata = load_metadata()

    latest_articles = sorted(metadata, key=lambda x: x["created_at"], reverse=True)[:3]
    categorized_articles = defaultdict(lambda: defaultdict(list))
    
    for article in metadata:
        filepath_parts = article["filepath"].split("/")
        
        if len(filepath_parts) == 1:
            categorized_articles["Andere"]["_root"].append(article)
        elif len(filepath_parts) == 2:
            category = filepath_parts[0]
            categorized_articles[category]["_root"].append(article)
        else:
            category = filepath_parts[0]
            subcategory = filepath_parts[1]
            categorized_articles[category][subcategory].append(article)
    
    ordered_categories = OrderedDict()
    
    if "Privacy-Security" in categorized_articles:
        ordered_categories["Privacy-Security"] = categorized_articles.pop("Privacy-Security")

    for category in sorted(categorized_articles.keys()):
        ordered_categories[category] = categorized_articles[category]

    return render_template('index.html', 
                           articles=latest_articles, 
                           categories=ordered_categories)

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

        html_content = markdown.markdown(content, extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables', 
            'markdown.extensions.toc',
            'markdown.extensions.admonition',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists'
        ])
        
    authors = article.get('authors', 'lytexdev')

    prev_article = metadata[article_index - 1] if article_index > 0 else None
    next_article = metadata[article_index + 1] if article_index < len(metadata) - 1 else None

    breadcrumbs = []
    filepath_parts = article["filepath"].split("/")

    breadcrumbs.append({"name": "Home", "url": url_for('index')})

    if len(filepath_parts) > 1:
        category = filepath_parts[0]
        breadcrumbs.append({"name": category, "url": url_for('show_category', category=category)})

        if len(filepath_parts) > 2:
            subcategory = filepath_parts[1]
            breadcrumbs.append({
                "name": subcategory, 
                "url": url_for('show_subcategory', category=category, subcategory=subcategory)
            })

    breadcrumbs.append({"name": article["title"], "url": None})
    
    pygments_css = HtmlFormatter(style='monokai').get_style_defs('.codehilite')
    
    return render_template(
        'article.html',
        title=article['title'],
        content=html_content,
        created_at=article['created_at'],
        authors=authors,
        prev_article=prev_article,
        next_article=next_article,
        pygments_css=pygments_css,
        breadcrumbs=breadcrumbs
    )

@app.route('/category/<category>')
def show_category(category):
    metadata = load_metadata()
    category_articles = [article for article in metadata if article["filepath"].split('/')[0] == category]
    
    if not category_articles:
        return abort(404)
    
    category_articles = sorted(category_articles, key=lambda x: x["created_at"], reverse=True)
    
    subcategories = defaultdict(list)
    root_articles = []
    
    for article in category_articles:
        path_parts = article["filepath"].split('/')
        
        if len(path_parts) == 2:
            root_articles.append(article)
        else:
            subcategory = path_parts[1]
            subcategories[subcategory].append(article)

    ordered_subcategories = OrderedDict()
    for subcategory in sorted(subcategories.keys()):
        ordered_subcategories[subcategory] = sorted(subcategories[subcategory], 
                                                   key=lambda x: x["created_at"], 
                                                   reverse=True)
    
    return render_template('category.html',
                          category=category,
                          root_articles=root_articles,
                          subcategories=ordered_subcategories)

@app.route('/category/<category>/<subcategory>')
def show_subcategory(category, subcategory):
    metadata = load_metadata()
    
    subcategory_articles = [
        article for article in metadata 
        if article["filepath"].split('/')[0] == category 
        and len(article["filepath"].split('/')) > 2
        and article["filepath"].split('/')[1] == subcategory
    ]
    
    if not subcategory_articles:
        return abort(404)
    
    subcategory_articles = sorted(subcategory_articles, key=lambda x: x["created_at"], reverse=True)
    
    return render_template('subcategory.html',
                          category=category,
                          subcategory=subcategory,
                          articles=subcategory_articles)

@app.route('/sitemap.xml')
@limiter.limit("20 per minute")
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

    categories = set()
    subcategories = defaultdict(set)
    
    for article in metadata:
        parts = article["filepath"].split("/")
        if len(parts) > 0:
            category = parts[0]
            categories.add(category)
            
            if len(parts) > 1:
                subcategory = parts[1]
                subcategories[category].add(subcategory)
    
    for category in categories:
        sitemap_xml += f'''
    <url>
        <loc>{url_for('show_category', category=category, _external=True)}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>'''

    for category, subs in subcategories.items():
        for subcategory in subs:
            sitemap_xml += f'''
    <url>
        <loc>{url_for('show_subcategory', category=category, subcategory=subcategory, _external=True)}</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
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
@limiter.limit("20 per minute")
def robots():
    robots_txt = f'''User-agent: *

Allow: /

Sitemap: {url_for('sitemap', _external=True)}
'''
    return Response(robots_txt, mimetype='text/plain')

@app.errorhandler(404)
@limiter.limit("20 per minute")
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
@limiter.limit("20 per minute")
def page_internal_server(error):
    return render_template('500.html'), 500

@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = ("geolocation=(), microphone=(), camera=(), payment=(), usb=()")
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
