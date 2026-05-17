# -*- coding: utf-8 -*-
"""Update sitemap.xml with all blog articles."""
import sys
sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from articles_data import ARTICLES, SITE_URL
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(r"C:\Users\3300v\Projects\ma-ss.ru\public_html")
start = date(2026, 3, 1)

urls = [f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>2026-05-17</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{SITE_URL}/blog/</loc>
    <lastmod>2026-05-17</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""]

for idx, art in enumerate(ARTICLES):
    d = (start + timedelta(days=idx * 3)).isoformat()
    urls.append(f"""  <url>
    <loc>{SITE_URL}/blog/{art['slug']}.html</loc>
    <lastmod>{d}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
xml += "\n".join(urls)
xml += "\n</urlset>\n"

(ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
print(f"Sitemap updated: {len(ARTICLES)+2} URLs")
