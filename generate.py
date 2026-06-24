#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""寶寶副食食材庫 — 靜態頁面生成器。
讀取 data/foods.json，產生：每個食材頁、index.html、sitemap.xml、llms.txt。
上線前把下方 DOMAIN 改成正式網域即可。"""

import json
import os
import datetime

DOMAIN = "https://ianian22493.github.io/babyfood-db"
GA_ID = "G-ET2EWNN5ZC"  # Google Analytics 4 Measurement ID（留空字串則不輸出追蹤碼）
ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()

GA_SNIPPET = ("""<!-- Google Analytics (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '%s');
</script>""" % (GA_ID, GA_ID)) if GA_ID else ""

GSC_VERIFY = "DQIJMBwacydAwS3gSjbX_gf5CCTtkHqw6pbvA8HQOC0"  # Google Search Console 驗證碼（留空則不輸出）
GSC_META = ('<meta name="google-site-verification" content="%s">' % GSC_VERIFY) if GSC_VERIFY else ""

BRAND_MARK = ('<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true">'
    '<rect width="32" height="32" rx="8" fill="#3f8a62"/>'
    '<path d="M16 7c-3.2 0-5.6 2.3-5.6 5.4 0 2.1 1.2 3.7 2.9 5.2.9.8 1.4 1.4 1.4 2.6v3.1a1.3 1.3 0 0 0 2.6 0v-3.1c0-1.2.5-1.8 1.4-2.6 1.7-1.5 2.9-3.1 2.9-5.2C21.6 9.3 19.2 7 16 7z" fill="#eafff3"/>'
    '<circle cx="16" cy="12.4" r="2.2" fill="#3f8a62"/></svg>')


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def header(asset_prefix, show_back):
    nav = ('<nav><a href="%sindex.html">← 回食材庫</a></nav>' % asset_prefix) if show_back else ""
    return ('<header class="site-header"><div class="wrap">\n  ' + BRAND_MARK +
            '\n  <div class="brand-text"><b>寶寶副食食材庫</b>'
            '<span>Baby First Foods · 依據 WHO 等公開衛教指引整理</span></div>\n  '
            + nav + '\n</div></header>')


FOOTER = ('<footer><div class="wrap">\n'
          '  <span>© 2026 寶寶副食食材庫</span>\n'
          '  <span>資料整理自 WHO 與台灣兒科醫學會等公開衛教指引</span>\n'
          '</div></footer>')


def render_food(food, sources_map):
    slug = food["slug"]
    name = food["name_zh"]
    title = "寶寶幾個月可以吃%s？" % name
    page_title = "%s｜寶寶副食食材庫" % title
    url = "%s/foods/%s.html" % (DOMAIN, slug)
    desc = food["answer"][:90]

    facts_html = "\n".join(
        '    <div class="fact"><div class="k">%s</div><div class="v">%s</div></div>' % (esc(k), esc(v))
        for k, v in food["facts"])

    safety_html = ""
    if food.get("safety_note"):
        safety_html = ('  <div class="warn-box"><div class="t">⚠ %s</div><p>%s</p></div>\n'
                       % (esc(food.get("safety_title", "重要提醒")), esc(food["safety_note"])))

    prep_html = "\n".join('      <li>%s</li>' % esc(p) for p in food["prep"])

    faq_html = "\n".join(
        '    <div class="faq-item"><p class="q">%s</p><p class="a">%s</p></div>' % (esc(q), esc(a))
        for q, a in food["faq"])

    sources = sources_map[food.get("sources_key", "default_sources")]

    medpage = {
        "@context": "https://schema.org", "@type": "MedicalWebPage",
        "name": title, "url": url, "inLanguage": "zh-Hant-TW", "dateModified": TODAY,
        "about": {"@type": "Thing", "name": name + "副食品"},
        "audience": {"@type": "ParentAudience", "audienceType": "嬰幼兒照顧者"},
        "publisher": {"@type": "Organization", "name": "寶寶副食食材庫"},
        "citation": ["世界衛生組織（WHO）嬰幼兒補充性餵食指引",
                     "美國兒科醫學會（AAP）嬰幼兒餵食建議",
                     "台灣兒科醫學會副食品建議"]}
    faqpage = {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q,
                               "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in food["faq"]]}
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "食材庫", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": food["category"]},
            {"@type": "ListItem", "position": 3, "name": name}
        ]}

    html = """<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{gsc}
{ga}
<title>{page_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="zh_TW">
<meta property="og:site_name" content="寶寶副食食材庫">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="stylesheet" href="../assets/style.css">
<script type="application/ld+json">
{medpage}
</script>
<script type="application/ld+json">
{faqpage}
</script>
<script type="application/ld+json">
{breadcrumb}
</script>
</head>
<body>

{header}

<main><div class="wrap">
  <div class="crumb">食材庫 › {category} › {name}</div>
  <h1>{title}</h1>
  <div class="byline"><span class="badge">依據 WHO 指引整理</span><span>資料更新 {today}</span></div>

  <div class="answer">
    <h2>一句話結論</h2>
    <p>{answer}</p>
  </div>

{safety}  <div class="facts">
{facts}
  </div>

  <section>
    <h2>{prep_heading}</h2>
    <ol class="prep-list">
{prep}
    </ol>
  </section>

  <section>
    <h2>營養重點</h2>
    <p>{nutrition}</p>
  </section>

  <section>
    <h2>常見問題</h2>
{faq}
  </section>

  <p class="sources">{sources}</p>
</div></main>

{footer}
</body>
</html>
""".format(
        gsc=GSC_META, ga=GA_SNIPPET, page_title=esc(page_title), desc=esc(desc), url=url, title=esc(title),
        og_image=DOMAIN + "/assets/og-image.svg",
        medpage=json.dumps(medpage, ensure_ascii=False, indent=2),
        faqpage=json.dumps(faqpage, ensure_ascii=False, indent=2),
        breadcrumb=json.dumps(breadcrumb, ensure_ascii=False, indent=2),
        header=header("../", True), category=esc(food["category"]), name=esc(name),
        today=TODAY, answer=esc(food["answer"]), safety=safety_html, facts=facts_html,
        prep_heading=esc(food["prep_heading"]), prep=prep_html,
        nutrition=esc(food["nutrition"]), faq=faq_html, sources=esc(sources), footer=FOOTER)

    out = os.path.join(ROOT, "foods", slug + ".html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out


def render_index(foods):
    cards = []
    for fd in foods:
        cards.append(
            '    <a class="food-card" href="foods/%s.html" data-name="%s %s">'
            '<div class="emoji">%s</div><div class="name">%s</div>'
            '<div class="meta">%s</div><div class="tag-%s">%s</div></a>'
            % (fd["slug"], esc(fd["name_zh"]), esc(fd["name_en"]).lower(), fd["emoji"],
               esc(fd["name_zh"]), esc(fd["card_meta"]), fd["card_tag_class"], esc(fd["card_tag"])))
    grid = "\n".join(cards)

    website = {"@context": "https://schema.org", "@type": "WebSite",
               "name": "寶寶副食食材庫", "url": DOMAIN + "/",
               "description": "嬰幼兒副食品食材資料庫，提供每種食材的建議月齡、過敏風險與處理方式。",
               "inLanguage": "zh-Hant-TW"}

    html = """<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{gsc}
{ga}
<title>寶寶副食食材庫｜每種食材幾個月可以吃、過敏風險與處理方式</title>
<meta name="description" content="嬰幼兒副食品食材資料庫。每種食材一頁，提供建議月齡、過敏風險、建議質地與處理方式，整理自 WHO 與台灣兒科醫學會等公開衛教指引。">
<link rel="canonical" href="{domain}/">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="website">
<meta property="og:title" content="寶寶副食食材庫">
<meta property="og:description" content="每種副食品食材幾個月可以吃、過敏風險與處理方式，整理自 WHO 等公開衛教指引。">
<meta property="og:url" content="{domain}/">
<meta property="og:locale" content="zh_TW">
<meta property="og:site_name" content="寶寶副食食材庫">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="寶寶副食食材庫">
<meta name="twitter:description" content="每種副食品食材幾個月可以吃、過敏風險與處理方式，整理自 WHO 等公開衛教指引。">
<meta name="twitter:image" content="{og_image}">
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">
{website}
</script>
</head>
<body>

{header}

<main><div class="wrap">
  <div class="hero">
    <h1>每種副食品，幾個月可以吃？</h1>
    <p>一種食材一頁：建議月齡、過敏風險、建議質地與處理方式，一查就懂。內容整理自 WHO 與台灣兒科醫學會等公開衛教指引。</p>
  </div>

  <div class="search"><input id="q" type="search" placeholder="搜尋食材，例如：酪梨、雞蛋、蜂蜜…" aria-label="搜尋食材"></div>

  <div class="grid" id="grid">
{grid}
  </div>
</div></main>

{footer}

<script>
  const q = document.getElementById('q');
  const cards = [...document.querySelectorAll('.food-card')];
  q.addEventListener('input', () => {{
    const v = q.value.trim().toLowerCase();
    cards.forEach(c => {{ c.style.display = c.dataset.name.toLowerCase().includes(v) ? '' : 'none'; }});
  }});
</script>
</body>
</html>
""".format(gsc=GSC_META, ga=GA_SNIPPET, domain=DOMAIN, website=json.dumps(website, ensure_ascii=False, indent=2),
           og_image=DOMAIN + "/assets/og-image.svg",
           header=header("", False), grid=grid, footer=FOOTER)

    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out


def render_sitemap(foods):
    rows = ['  <url><loc>%s/</loc><lastmod>%s</lastmod><priority>1.0</priority></url>' % (DOMAIN, TODAY)]
    for fd in foods:
        rows.append('  <url><loc>%s/foods/%s.html</loc><lastmod>%s</lastmod><priority>0.8</priority></url>'
                    % (DOMAIN, fd["slug"], TODAY))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    out = os.path.join(ROOT, "sitemap.xml")
    with open(out, "w", encoding="utf-8") as f:
        f.write(xml)
    return out


def render_llms(foods):
    lines = ["# 寶寶副食食材庫 (Baby First Foods Database)", "",
             "> 一個專為「嬰幼兒副食品食材」整理的結構化資料庫。每種食材一頁，提供建議月齡、過敏風險、建議質地、處理方式與營養概要。內容整理自 WHO、AAP、台灣兒科醫學會等公開衛教指引。", "",
             "## 食材頁面"]
    for fd in foods:
        lines.append("- [%s %s](/foods/%s.html): %s" % (fd["name_zh"], fd["name_en"], fd["slug"], fd["card_meta"]))
    lines += ["", "## 使用說明",
              "- 所有月齡建議以「足月、發展正常的嬰兒」為前提，特殊狀況請依個別醫囑。",
              "- 本資料為衛教參考，不取代醫師臨床判斷。", ""]
    out = os.path.join(ROOT, "llms.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out


def main():
    with open(os.path.join(ROOT, "data", "foods.json"), encoding="utf-8") as f:
        data = json.load(f)
    foods = data["foods"]
    sources_map = {"default_sources": data["default_sources"], "allergen_sources": data["allergen_sources"]}
    os.makedirs(os.path.join(ROOT, "foods"), exist_ok=True)
    for fd in foods:
        render_food(fd, sources_map)
    render_index(foods)
    render_sitemap(foods)
    render_llms(foods)
    print("Generated %d food pages + index + sitemap + llms.txt" % len(foods))


if __name__ == "__main__":
    main()
