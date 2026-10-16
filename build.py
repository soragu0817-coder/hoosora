#!/usr/bin/env python3
"""구소라 한의사 사이트 빌더.

content/ 폴더의 각 .html 조각 맨 위에 JSON 머리말(<!--meta ... -->)을 두고,
이 스크립트가 공통 헤더·푸터·구조화 데이터를 붙여 docs/ 폴더에 완성본을 만듭니다.
GitHub Pages는 docs/ 폴더를 그대로 공개하면 됩니다.

사용:  python3 build.py
"""
import json, re, shutil, html
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "content"
OUT = ROOT / "docs"
ASSETS = ROOT / "assets"

# ── 사이트 공통 정보 (바뀌면 여기만 고치세요) ─────────────────────────
SITE = {
    # 도메인을 정하면 여기에 넣으세요. 예: "https://drsora.kr"
    # 비워 두면 canonical·sitemap 주소가 빠집니다.
    "base_url": "https://hoosora.kr",
    "site_name": "구소라 한의사의 피부·체형 이야기",
    "doctor": "구소라",
    "role": "후한의원 천안점 대표원장",
    "clinic": "후한의원 천안점",
    "address": "충남 천안시 동남구 만남로 52 문타워 3층",
    "address_short": "천안 동남구 신부동 · 천안터미널 도보 5~6분",
    "phone": "041-622-7073",
    "hours_weekday": "10:30 – 20:30",
    "hours_lunch": "13:30 – 14:30",
    "hours_weekend": "10:00 – 16:00",
    "reserve": "https://ca.hooclinic.co.kr/clinicPriceSide/reservation.php",
    "consult": "https://ca.hooclinic.co.kr/contact/online.php",
    "kakao": "https://pf.kakao.com/_eNnPj",
    "homepage": "https://ca.hooclinic.co.kr/",
    "events": "https://ca.hooclinic.co.kr/clinicPrice/eventList.php",
    # 검색엔진 소유확인 코드
    "naver_verify": "39f11d82fd0fb40640284da155b9c19200d7998a",
    "google_verify": "V4takhUUKI0iLC34rKnYgHMLg0czGFQ8cedgzhoE9HU",
    # 있으면 채우세요 (비우면 링크가 숨겨집니다)
    "naver_place": "",
    "blog": "",
    "instagram": "",
}

NAV = [
    ("질환 정보", "/#diseases"),
    ("칼럼", "/column/"),
    ("원장 소개", "/doctor/"),
    ("오시는 길", "/clinic/"),
]


def rel(depth: int, href: str) -> str:
    """사이트 내부 절대경로(/x/)를 상대경로로 바꿔 어떤 호스팅에서도 동작하게."""
    if not href.startswith("/"):
        return href
    prefix = "../" * depth if depth else "./"
    target = href.lstrip("/")
    if target.startswith("#"):
        return prefix + "index.html" + target if depth else target
    if target == "":
        return prefix + "index.html"
    if target.endswith("/"):
        target += "index.html"
    elif "#" in target:
        p, h = target.split("#", 1)
        if p.endswith("/"):
            p += "index.html"
        target = p + "#" + h
    return prefix + target


def header(depth):
    links = "".join(f'<a href="{rel(depth, h)}">{t}</a>' for t, h in NAV)
    return f'''<header class="top">
  <div class="wrap top-in">
    <a class="brand" href="{rel(depth, '/')}">
      <span class="brand-mark" aria-hidden="true">소</span>
      <span><strong>{SITE["doctor"]} 한의사</strong><small>{SITE["role"]}</small></span>
    </a>
    <nav class="nav">{links}</nav>
    <a class="btn btn-sm" href="{SITE["reserve"]}" target="_blank" rel="noopener">진료 예약</a>
  </div>
</header>'''


def contact_block():
    S = SITE
    return f'''<section class="contact" id="contact">
  <div class="wrap">
    <p class="eyebrow">CONTACT</p>
    <h2>진료 안내</h2>
    <div class="contact-grid">
      <div class="card"><span class="num">01</span><h3>주소</h3>
        <p>{S["address"]}</p><p class="muted">{S["address_short"]}</p></div>
      <div class="card"><span class="num">02</span><h3>진료시간</h3>
        <dl class="hours"><dt>평일</dt><dd>{S["hours_weekday"]}</dd>
        <dt>점심시간</dt><dd>{S["hours_lunch"]}</dd>
        <dt>주말</dt><dd>{S["hours_weekend"]} <span class="muted">(점심시간 없음)</span></dd></dl>
        <p class="muted small">휴진일은 예약 전 전화로 확인해 주세요.</p></div>
      <div class="card"><span class="num">03</span><h3>주차</h3>
        <p>건물 기계식 주차장 이용 가능</p>
        <p class="muted">RV·SUV는 들어가기 어려워요. 신부동 제5공영주차장 이용 시 주차권을 드립니다.</p></div>
      <div class="card"><span class="num">04</span><h3>예약·문의</h3>
        <p><a href="tel:{S["phone"]}">{S["phone"]}</a></p>
        <p class="muted">온라인 예약, 카카오톡 상담도 가능합니다.</p></div>
    </div>
    <div class="cta-row">
      <a class="btn" href="{S["reserve"]}" target="_blank" rel="noopener">온라인 예약</a>
      <a class="btn btn-ghost" href="tel:{S["phone"]}">전화 {S["phone"]}</a>
      <a class="btn btn-ghost" href="{S["kakao"]}" target="_blank" rel="noopener">카카오톡 상담</a>
    </div>
  </div>
</section>'''


def footer(depth):
    S = SITE
    extra = [("네이버 플레이스", S["naver_place"]), ("블로그", S["blog"]), ("인스타그램", S["instagram"])]
    extra_links = "".join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in extra if u)
    return f'''<footer class="foot">
  <div class="wrap foot-in">
    <div>
      <p class="foot-title">{S["site_name"]}</p>
      <p class="foot-tag">이름부터 정확히 구분하고, <strong>다시 생기는 이유까지 함께.</strong></p>
      <p class="muted">{S["role"]} {S["doctor"]}</p>
    </div>
    <div>
      <p class="foot-h">병원 정보</p>
      <p>{S["address"]}<br>평일 {S["hours_weekday"]} (점심 {S["hours_lunch"]}) · 주말 {S["hours_weekend"]}<br>
      <a href="tel:{S["phone"]}">{S["phone"]}</a> · <a href="{S["homepage"]}" target="_blank" rel="noopener">후한의원 천안점 홈페이지</a></p>
    </div>
    <div class="foot-links">
      <p class="foot-h">바로가기</p>
      <a href="{S["reserve"]}" target="_blank" rel="noopener">온라인 예약</a>
      <a href="{S["kakao"]}" target="_blank" rel="noopener">카카오톡 상담</a>
      <a href="{S["events"]}" target="_blank" rel="noopener">시술 안내·이벤트</a>
      {extra_links}
    </div>
  </div>
  <div class="wrap foot-note">
    <a href="{rel(depth, '/policy/')}">콘텐츠 작성 원칙</a> · 이 사이트의 글은 일반적인 건강 정보이며 진료를 대신하지 않습니다. 효과와 경과는 개인의 상태에 따라 다를 수 있습니다.
  </div>
</footer>
<a class="sticky-cta" href="{S["reserve"]}" target="_blank" rel="noopener">진료 예약하기 →</a>'''


def clinic_ld():
    S = SITE
    d = {
        "@context": "https://schema.org",
        "@type": "MedicalClinic",
        "name": S["clinic"],
        "telephone": S["phone"],
        "url": S["homepage"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "동남구 만남로 52 문타워 3층",
            "addressLocality": "천안시",
            "addressRegion": "충청남도",
            "addressCountry": "KR",
        },
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
             "opens": "10:30", "closes": "20:30"},
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Saturday", "Sunday"], "opens": "10:00", "closes": "16:00"},
        ],
        "medicalSpecialty": "Dermatology",
        "employee": {"@type": "Physician", "name": S["doctor"], "jobTitle": S["role"]},
    }
    return d


def faq_ld(body):
    """본문의 <details class="faq"><summary>Q</summary><div>A</div></details> 를 FAQPage로."""
    items = re.findall(r'<details class="faq">\s*<summary>(.*?)</summary>\s*<div>(.*?)</div>\s*</details>', body, re.S)
    if not items:
        return None
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": strip(q),
             "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items
        ],
    }


def page_ld(meta, url):
    if meta.get("type") != "article":
        return None
    d = {
        "@context": "https://schema.org",
        "@type": "MedicalWebPage",
        "headline": meta["h1"],
        "description": meta["description"],
        "inLanguage": "ko-KR",
        "dateModified": meta.get("updated") or meta.get("date", ""),
        "datePublished": meta.get("date") or meta.get("updated", ""),
        "author": {"@type": "Physician", "name": SITE["doctor"], "jobTitle": SITE["role"]},
        "reviewedBy": {"@type": "Physician", "name": SITE["doctor"]},
        "about": {"@type": "MedicalCondition", "name": meta.get("condition", meta["h1"])},
    }
    if url:
        d["url"] = url
    return d


def reviewer_box(meta, depth):
    if meta.get("type") != "article":
        return ""
    return f'''<aside class="reviewer">
  <img class="reviewer-photo" src="{rel(depth, '/assets/doctor-face.webp')}" width="200" height="200" alt="구소라 한의사">
  <div>
    <p class="muted small">감수 한의사</p>
    <p><a href="{rel(depth, '/doctor/')}"><strong>{SITE["doctor"]}</strong></a> · {SITE["role"]}</p>
    <p class="reviewer-note">{meta.get("note", "")}</p>
    <p class="muted small">{"작성" if meta.get("kind") == "column" else "최종 수정"} {meta.get("updated") or meta.get("date", "")}</p>
  </div>
</aside>'''


def breadcrumb(meta, depth):
    if meta["path"] == "":
        return ""
    return f'<nav class="crumb wrap"><a href="{rel(depth, "/")}">홈</a> › {meta.get("crumb", meta["h1"])}</nav>'


def render(meta, body):
    depth = meta["path"].count("/")
    url = (SITE["base_url"].rstrip("/") + "/" + meta["path"]) if SITE["base_url"] else ""
    lds = [x for x in (clinic_ld() if meta["path"] == "" else None, page_ld(meta, url), faq_ld(body)) if x]
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    canonical = f'<link rel="canonical" href="{url}">' if url else ""
    og_url = f'<meta property="og:url" content="{url}">' if url else ""
    # 본문 안의 /경로 링크를 상대경로로
    body = re.sub(r'(href|src)="(/[^"]*)"', lambda m: f'{m.group(1)}="{rel(depth, m.group(2))}"', body)
    css = rel(depth, "/assets/style.css")
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta["title"]}</title>
<meta name="description" content="{meta["description"]}">
<meta name="author" content="{SITE["doctor"]}">
<meta name="robots" content="index, follow, max-image-preview:large">
{f'<meta name="naver-site-verification" content="{SITE["naver_verify"]}">' if SITE["naver_verify"] else ""}
{f'<meta name="google-site-verification" content="{SITE["google_verify"]}">' if SITE["google_verify"] else ""}
{canonical}
<meta property="og:type" content="{'article' if meta.get('type') == 'article' else 'website'}">
<meta property="og:title" content="{meta["title"]}">
<meta property="og:description" content="{meta["description"]}">
<meta property="og:site_name" content="{SITE["site_name"]}">
<meta property="og:locale" content="ko_KR">
{og_url}
{f'<meta property="og:image" content="{SITE["base_url"].rstrip("/")}/assets/doctor.webp">' if SITE["base_url"] else ""}
<meta name="theme-color" content="#f6f1ea">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
{ld_html}
</head>
<body>
{header(depth)}
{breadcrumb(meta, depth)}
<main>
{body}
{reviewer_box(meta, depth) if meta.get("type") == "article" else ""}
</main>
{contact_block() if meta.get("contact", True) else ""}
{footer(depth)}
<script src="{rel(depth, '/assets/check.js')}" defer></script>
</body>
</html>
'''


def load(f):
    text = f.read_text(encoding="utf-8")
    m = re.match(r"<!--meta\s*(\{.*?\})\s*-->\s*", text, re.S)
    return json.loads(m.group(1)), text[m.end():]


def column_card(c):
    return (f'<a class="col-card" href="/{c["path"]}"><span class="col-date">{c["date"]}</span>'
            f'<strong>{c["h1"]}</strong><span class="col-sum">{c["description"]}</span></a>')


def column_list_page(cols):
    cards = "".join(column_card(c) for c in cols) or '<p class="muted">곧 첫 칼럼이 올라옵니다.</p>'
    meta = {
        "path": "column/", "crumb": "칼럼",
        "title": "칼럼 | 구소라 한의사의 피부·체형 이야기",
        "h1": "진료실에서 자주 받는 질문, 칼럼",
        "description": "천안 후한의원 구소라 한의사가 진료실에서 자주 받는 여드름, 여드름 자국, 편평사마귀, 다이어트 한약, 안면비대칭 질문을 칼럼으로 정리합니다.",
    }
    body = f'''<article class="article">
  <p class="eyebrow">COLUMN</p>
  <h1>{meta["h1"]}</h1>
  <p class="lead">진료실에서 실제로 자주 받는 질문 하나를 골라, 짧고 정확하게 답합니다.</p>
  <div class="col-list">{cards}</div>
</article>'''
    return meta, body


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ASSETS, OUT / "assets")
    items = [load(f) for f in sorted(SRC.glob("*.html"))]
    cols = [load(f) for f in sorted((SRC / "column").glob("*.html"))] if (SRC / "column").exists() else []
    cols.sort(key=lambda x: x[0]["date"], reverse=True)
    col_metas = [c[0] for c in cols]
    items += cols
    items.append(column_list_page(col_metas))
    pages = []
    for meta, body in items:
        if "<!--LATEST_COLUMNS-->" in body:
            latest = "".join(column_card(c) for c in col_metas[:3])
            body = body.replace("<!--LATEST_COLUMNS-->", f'<div class="col-list">{latest}</div>' if latest else "")
        if meta.get("type") == "article" and meta.get("kind") != "column":
            rel_cols = [c for c in col_metas if meta["path"] in c.get("topics", [])][:5]
            if rel_cols:
                lis = "".join(f'<li><a href="/{c["path"]}">{c["h1"]}</a></li>' for c in rel_cols)
                body += f'\n<div class="article"><h2>관련 칼럼</h2><ul>{lis}</ul></div>'
        if meta.get("kind") == "column":
            rel_dis = [m for m, _ in items if m.get("type") == "article" and m.get("kind") != "column" and m["path"] in meta.get("topics", [])]
            if rel_dis:
                lis = "".join(f'<li><a href="/{m["path"]}">{m["h1"]}</a></li>' for m, _ in [(x, None) for x in rel_dis])
                body += f'\n<div class="article"><h2>더 자세한 질환 정보</h2><ul>{lis}</ul></div>'
        dest = OUT / meta["path"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(meta, body), encoding="utf-8")
        pages.append(meta)
        print("built", dest.relative_to(ROOT))
    (OUT / ".nojekyll").write_text("")
    # GitHub Pages 맞춤 도메인
    if SITE["base_url"]:
        (OUT / "CNAME").write_text(SITE["base_url"].split("//", 1)[1].rstrip("/") + "\n")
    base = SITE["base_url"].rstrip("/")
    robots = "User-agent: *\nAllow: /\n"
    if base:
        urls = "".join(
            f"<url><loc>{base}/{p['path']}</loc>{'<lastmod>'+(p.get('updated') or p.get('date'))+'</lastmod>' if (p.get('updated') or p.get('date')) else ''}</url>"
            for p in pages)
        (OUT / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
            encoding="utf-8")
        robots += f"Sitemap: {base}/sitemap.xml\n"
    (OUT / "robots.txt").write_text(robots)


if __name__ == "__main__":
    main()
