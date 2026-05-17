# -*- coding: utf-8 -*-
"""Generate 30 blog articles for ma-ss.ru + download images from Pexels."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import os, json, time, urllib.request, urllib.parse
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).parent))
from articles_data import ARTICLES, SITE_NAME, SITE_URL, AUTHOR, PHONE, PHONE_HREF, METRIKA_ID

ROOT    = Path(r"C:\Users\3300v\Projects\ma-ss.ru\public_html")
BLOG    = ROOT / "blog"
IMG     = BLOG / "img"
BLOG.mkdir(exist_ok=True)
IMG.mkdir(exist_ok=True)

PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "")
UA = "Mozilla/5.0 (compatible; MaSS-Blog/1.0)"

# Curated free Pexels images for massage topics
FALLBACK = {
    "massage": "https://images.pexels.com/photos/3865676/pexels-photo-3865676.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "spa":     "https://images.pexels.com/photos/3997998/pexels-photo-3997998.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "back":    "https://images.pexels.com/photos/5793953/pexels-photo-5793953.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "relax":   "https://images.pexels.com/photos/6560369/pexels-photo-6560369.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "neck":    "https://images.pexels.com/photos/3768914/pexels-photo-3768914.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "sport":   "https://images.pexels.com/photos/4162487/pexels-photo-4162487.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "leg":     "https://images.pexels.com/photos/3865547/pexels-photo-3865547.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "head":    "https://images.pexels.com/photos/3997985/pexels-photo-3997985.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "baby":    "https://images.pexels.com/photos/35537/child-children-girl-happy.jpg?auto=compress&cs=tinysrgb&w=1200",
    "elderly": "https://images.pexels.com/photos/339620/pexels-photo-339620.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "wellness":"https://images.pexels.com/photos/3768611/pexels-photo-3768611.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "default": "https://images.pexels.com/photos/3865676/pexels-photo-3865676.jpeg?auto=compress&cs=tinysrgb&w=1200",
}

def pick_fallback(query):
    q = query.lower()
    for k in FALLBACK:
        if k in q:
            return FALLBACK[k]
    return FALLBACK["default"]

def pexels_url(query, page=1):
    if not PEXELS_KEY:
        return None
    q = urllib.parse.quote(query)
    url = f"https://api.pexels.com/v1/search?query={q}&per_page=1&page={page}"
    req = urllib.request.Request(url, headers={"Authorization": PEXELS_KEY, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            photos = data.get("photos", [])
            if photos:
                return photos[0]["src"]["large"]
    except Exception as e:
        print(f"  Pexels error: {e}")
    return None

def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"  Download error: {e}")
        return False


def render_article(art, idx, pub_date):
    slug   = art["slug"]
    img_rel = f"img/{slug}.jpg"
    img_url = f"{SITE_URL}/blog/{img_rel}"
    can_url = f"{SITE_URL}/blog/{slug}.html"

    sections_html = ""
    for h, body in art["sections"]:
        sections_html += f"""
        <h2>{h}</h2>
        <p>{body}</p>"""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{art['title']} | {SITE_NAME}</title>
    <meta name="description" content="{art['desc']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{can_url}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{art['title']}">
    <meta property="og:description" content="{art['desc']}">
    <meta property="og:url" content="{can_url}">
    <meta property="og:image" content="{img_url}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:locale" content="ru_RU">
    <link rel="icon" href="/favicon.ico">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "{art['title']}",
        "description": "{art['desc']}",
        "datePublished": "{pub_date}",
        "dateModified": "{pub_date}",
        "author": {{"@type": "Person", "name": "{AUTHOR}"}},
        "publisher": {{
            "@type": "LocalBusiness",
            "name": "{SITE_NAME}",
            "url": "{SITE_URL}"
        }},
        "image": "{img_url}",
        "mainEntityOfPage": "{can_url}"
    }}
    </script>
    <!-- Yandex.Metrika -->
    <script type="text/javascript">
    (function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
    m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
    ym({METRIKA_ID},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true}});
    </script>
    <noscript><img src="https://mc.yandex.ru/watch/{METRIKA_ID}" style="position:absolute;left:-9999px" alt=""></noscript>
    <style>
        *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
        body{{font-family:'Inter',system-ui,sans-serif;color:#1d1d1f;background:#fbfbfd;line-height:1.7;-webkit-font-smoothing:antialiased}}
        a{{color:#2d6a4f;text-decoration:none}}
        a:hover{{text-decoration:underline}}
        /* NAV */
        .nav{{position:sticky;top:0;z-index:100;background:rgba(251,251,253,.88);backdrop-filter:blur(16px);border-bottom:1px solid #e5e5e5;padding:0 24px}}
        .nav__inner{{max-width:800px;margin:0 auto;height:52px;display:flex;align-items:center;justify-content:space-between}}
        .nav__logo{{font-weight:700;font-size:1rem;color:#1d1d1f}}
        .nav__cta{{background:#2d6a4f;color:#fff;padding:8px 20px;border-radius:980px;font-size:.85rem;font-weight:500}}
        .nav__cta:hover{{background:#40916c;text-decoration:none}}
        /* ARTICLE */
        .article{{max-width:800px;margin:0 auto;padding:48px 24px 80px}}
        .breadcrumb{{font-size:.8rem;color:#6e6e73;margin-bottom:24px}}
        .breadcrumb a{{color:#6e6e73}}
        .meta{{display:flex;gap:16px;align-items:center;margin-bottom:24px;flex-wrap:wrap}}
        .meta__city{{background:#d8f3dc;color:#2d6a4f;padding:4px 12px;border-radius:980px;font-size:.8rem;font-weight:600}}
        .meta__time{{color:#6e6e73;font-size:.85rem}}
        .meta__date{{color:#6e6e73;font-size:.85rem}}
        h1{{font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;letter-spacing:-.02em;line-height:1.2;margin-bottom:24px;color:#1d1d1f}}
        .lead{{font-size:1.15rem;color:#3d3d3f;margin-bottom:32px;line-height:1.65;border-left:3px solid #2d6a4f;padding-left:16px}}
        .hero-img{{width:100%;border-radius:16px;margin-bottom:40px;aspect-ratio:16/9;object-fit:cover}}
        h2{{font-size:1.3rem;font-weight:700;margin:40px 0 12px;color:#1d1d1f}}
        p{{color:#3d3d3f;margin-bottom:16px}}
        .conclusion{{background:#d8f3dc;border-radius:16px;padding:24px 28px;margin:40px 0}}
        .conclusion p{{color:#1d4a2e;margin:0;font-weight:500}}
        /* CTA */
        .cta-box{{background:linear-gradient(135deg,#1b4332,#2d6a4f);border-radius:20px;padding:40px 32px;text-align:center;margin:48px 0}}
        .cta-box h3{{color:#fff;font-size:1.4rem;margin-bottom:12px}}
        .cta-box p{{color:rgba(255,255,255,.8);margin-bottom:24px}}
        .cta-box__btns{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
        .btn-white{{background:#fff;color:#1d4a2e;padding:14px 28px;border-radius:980px;font-weight:600;font-size:.95rem}}
        .btn-white:hover{{background:#f0faf5;text-decoration:none}}
        .btn-wa{{background:#25D366;color:#fff;padding:14px 28px;border-radius:980px;font-weight:600;font-size:.95rem}}
        .btn-wa:hover{{background:#1ebe5d;text-decoration:none}}
        /* FOOTER */
        .footer{{background:#1d1d1f;color:rgba(255,255,255,.5);padding:32px 24px;text-align:center;font-size:.85rem}}
        .footer a{{color:rgba(255,255,255,.6)}}
        @media(max-width:600px){{
            .article{{padding:32px 16px 60px}}
            .cta-box{{padding:28px 20px}}
        }}
    </style>
</head>
<body>
<nav class="nav">
    <div class="nav__inner">
        <a href="{SITE_URL}" class="nav__logo">Людмила — Массаж</a>
        <a href="{SITE_URL}/#contact" class="nav__cta">Записаться</a>
    </div>
</nav>

<article class="article">
    <div class="breadcrumb">
        <a href="{SITE_URL}">Главная</a> &rsaquo;
        <a href="{SITE_URL}/blog/">Блог</a> &rsaquo;
        {art['h1']}
    </div>

    <div class="meta">
        <span class="meta__city">{art['city']}</span>
        <span class="meta__time">⏱ {art['read_time']}</span>
        <span class="meta__date">{pub_date}</span>
    </div>

    <h1>{art['h1']}</h1>

    <p class="lead">{art['lead']}</p>

    <img class="hero-img" src="{img_rel}" alt="{art['h1']}" width="800" height="450" loading="lazy">
    {sections_html}

    <div class="conclusion">
        <p>{art['conclusion']}</p>
    </div>

    <div class="cta-box">
        <h3>Записаться на массаж</h3>
        <p>Принимаю в собственном кабинете в Павловском Посаде.<br>Клиентов из Электростали и Ногинска жду с удовольствием.</p>
        <div class="cta-box__btns">
            <a href="tel:{PHONE_HREF}" class="btn-white">📞 {PHONE}</a>
            <a href="https://wa.me/{PHONE_HREF}" class="btn-wa">WhatsApp</a>
        </div>
    </div>
</article>

<footer class="footer">
    <p>{SITE_NAME} &nbsp;|&nbsp; <a href="{SITE_URL}">{SITE_URL}</a> &nbsp;|&nbsp; {PHONE}</p>
</footer>
</body>
</html>"""


def render_index(articles_meta):
    cards = ""
    for a in articles_meta:
        cards += f"""
        <a href="{a['slug']}.html" class="card">
            <img src="img/{a['slug']}.jpg" alt="{a['h1']}" loading="lazy">
            <div class="card__body">
                <span class="card__city">{a['city']}</span>
                <h2>{a['h1']}</h2>
                <p>{a['desc'][:120]}…</p>
                <span class="card__read">{a['read_time']}</span>
            </div>
        </a>"""

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Блог о массаже | {SITE_NAME}</title>
    <meta name="description" content="Статьи о массаже от профессионального массажиста Людмилы. Классический, антицеллюлитный, баночный массаж в Павловском Посаде, Электростали, Ногинске.">
    <link rel="canonical" href="{SITE_URL}/blog/">
    <link rel="icon" href="/favicon.ico">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Yandex.Metrika -->
    <script type="text/javascript">
    (function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
    m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");
    ym({METRIKA_ID},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true}});
    </script>
    <style>
        *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
        body{{font-family:'Inter',system-ui,sans-serif;background:#fbfbfd;color:#1d1d1f;-webkit-font-smoothing:antialiased}}
        a{{color:inherit;text-decoration:none}}
        .nav{{position:sticky;top:0;z-index:100;background:rgba(251,251,253,.88);backdrop-filter:blur(16px);border-bottom:1px solid #e5e5e5;padding:0 24px}}
        .nav__inner{{max-width:1120px;margin:0 auto;height:52px;display:flex;align-items:center;justify-content:space-between}}
        .nav__logo{{font-weight:700;color:#1d1d1f}}
        .nav__cta{{background:#2d6a4f;color:#fff;padding:8px 20px;border-radius:980px;font-size:.85rem;font-weight:500}}
        .header{{max-width:1120px;margin:0 auto;padding:64px 24px 40px;text-align:center}}
        .header h1{{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:700;letter-spacing:-.02em;margin-bottom:12px}}
        .header p{{color:#6e6e73;font-size:1.1rem}}
        .grid{{max-width:1120px;margin:0 auto;padding:0 24px 80px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
        .card{{background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 2px 16px rgba(0,0,0,.06);transition:transform .25s,box-shadow .25s;display:flex;flex-direction:column}}
        .card:hover{{transform:translateY(-4px);box-shadow:0 8px 32px rgba(0,0,0,.1)}}
        .card img{{width:100%;aspect-ratio:16/9;object-fit:cover}}
        .card__body{{padding:20px;flex:1;display:flex;flex-direction:column;gap:8px}}
        .card__city{{background:#d8f3dc;color:#2d6a4f;padding:3px 10px;border-radius:980px;font-size:.75rem;font-weight:600;width:fit-content}}
        .card h2{{font-size:1rem;font-weight:700;line-height:1.3}}
        .card p{{color:#6e6e73;font-size:.85rem;line-height:1.5;flex:1}}
        .card__read{{color:#6e6e73;font-size:.8rem}}
        .footer{{background:#1d1d1f;color:rgba(255,255,255,.5);padding:32px 24px;text-align:center;font-size:.85rem}}
        .footer a{{color:rgba(255,255,255,.6)}}
        @media(max-width:768px){{.grid{{grid-template-columns:1fr}}}}
        @media(max-width:1024px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
    </style>
</head>
<body>
<nav class="nav">
    <div class="nav__inner">
        <a href="{SITE_URL}" class="nav__logo">Людмила — Массаж</a>
        <a href="{SITE_URL}/#contact" class="nav__cta">Записаться</a>
    </div>
</nav>
<div class="header">
    <h1>Блог о массаже</h1>
    <p>Советы, разборы и ответы на частые вопросы от практикующего массажиста</p>
</div>
<div class="grid">{cards}
</div>
<footer class="footer">
    <p>{SITE_NAME} &nbsp;|&nbsp; <a href="{SITE_URL}">{SITE_URL}</a> &nbsp;|&nbsp; {PHONE}</p>
</footer>
</body>
</html>"""


def main():
    start_date = date(2026, 3, 1)
    for idx, art in enumerate(ARTICLES):
        pub_date = (start_date + timedelta(days=idx * 3)).isoformat()
        slug = art["slug"]
        print(f"[{idx+1:02d}/30] {slug}")

        # Image
        img_path = IMG / f"{slug}.jpg"
        if not img_path.exists():
            url = pexels_url(art["image_query"], idx + 1) or pick_fallback(art["image_query"])
            print(f"  img -> {url[:60]}...")
            if not download(url, img_path):
                # try fallback
                download(pick_fallback(art["image_query"]), img_path)
            time.sleep(0.3)

        # HTML
        html = render_article(art, idx, pub_date)
        out = BLOG / f"{slug}.html"
        out.write_text(html, encoding="utf-8")

    # Index page
    (BLOG / "index.html").write_text(render_index(ARTICLES), encoding="utf-8")
    print("\nДонe! Создано 30 статей + index.")


if __name__ == "__main__":
    main()
