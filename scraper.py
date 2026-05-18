#!/usr/bin/env python3
"""GitHub Actions - 抓取 beeweb.top 今日更新"""
import urllib.request
import re
import json
from datetime import datetime

BEEWEB_URL = "https://www.beeweb.top/index.php?show_updated=1"
OUTPUT_FILE = "beeweb_today.json"

def fetch_html():
    req = urllib.request.Request(
        BEEWEB_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    resp = urllib.request.urlopen(req, timeout=30)
    return resp.read().decode("utf-8", errors="replace")

def parse_anime(html):
    cards = html.split('class="card-effect')
    results = []
    seen = set()
    for card in cards[1:]:
        m = re.search(r'<h3[^>]*>\s*(.*?)\s*</h3>', card, re.DOTALL)
        if not m:
            continue
        name = m.group(1).strip()
        if '<i class' in name or len(name) > 50:
            continue
        if name in seen:
            continue
        seen.add(name)

        item = {"name": name}

        qm = re.search(r'top-0 left-0[^"]*?>([^<]+)</span>', card)
        if qm:
            q = qm.group(1).strip()
            if any(k in q for k in ['4K', '1080', '720']):
                item['quality'] = q

        tm = re.search(r'top-0 right-0[^"]*?>([^<]+)</span>', card)
        if tm:
            t = tm.group(1).strip()
            if re.match(r'\d{1,2}:\d{2}', t):
                item['time'] = t.replace('更新', '')

        dm = re.search(r'fa-calendar-o[^>]*></i>\s*(.*?)\s*</span>', card, re.DOTALL)
        if dm:
            item['date'] = dm.group(1).strip()

        ls = re.search(r'text-gray-600 mb-2(.*?)</div>\s*<!-- 底部信息', card, re.DOTALL)
        if ls:
            for label, url in re.findall(r'([\w\u4e00-\u9fff]+)\s*<a\s+href="([^"]+)"', ls.group(1)):
                lb = label.strip()
                if 'quark' in lb.lower() or '夸克' in lb:
                    item.setdefault('quark', []).append(url)
                elif '百度' in lb or 'baidu' in lb.lower():
                    item.setdefault('baidu', []).append(url)
                elif 'uc' in lb.lower():
                    item.setdefault('uc', []).append(url)
                elif '115' in lb:
                    item.setdefault('115', []).append(url)

        results.append(item)
    return results

def main():
    html = fetch_html()
    items = parse_anime(html)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] beeweb: {len(items)} items scraped")

if __name__ == '__main__':
    main()
